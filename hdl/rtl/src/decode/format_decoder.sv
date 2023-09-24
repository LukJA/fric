// takes a posit bus and extracts the relevant
// regions as digital signed byte values
`include "common.svh"

import common::*;

// Comb
module format_decoder #(
    parameter int WIDTH = 7,
    parameter int EN = 1,
    // Bits required for each field (+ sign bit)
    parameter int W_REG = $clog2(WIDTH),
    parameter int W_EXP = $clog2(WIDTH),
    parameter int W_MAN = WIDTH
) (
    input logic [WIDTH-1:0] posit,
    output sign_t sign,
    output logic signed [W_REG-1:0] regime,
    output logic signed [W_EXP-1:0] exponent,
    output logic unsigned [W_MAN-1:0] mantissa
);

    parameter W_RED = WIDTH - 1; // reduced (no sign) for width
    parameter MSB = WIDTH - 2;

    logic [WIDTH-1:0] posit_comp;
    logic [W_RED-1:0] posit_reduced;

    // generate complements of the inputs
    two_comp #(WIDTH) m_input_comp (
        .a(posit),
        .q(posit_comp)
    );

    // Extract sign bit
    assign sign = (posit[WIDTH-1] == 0) ? POS : NEG;

    // Explicit select the positive form
    assign posit_reduced =
        (sign == POS) ? posit[W_RED-1:0] : posit_comp[W_RED-1:0];

    // Now the hard part - length decomposition
    // find the length of the regime region and convert it to a regime value
    logic [W_REG-1:0] leading_ones;
    logic [W_REG-1:0] leading_zeroes;
    logic [W_REG-1:0] regime_len;
    logic signed [W_REG-1:0] negative_regime;
    logic signed [W_REG-1:0] subbed_regime;

    logic clo_valid, clz_valid;

    count_lead_one #(
        .W_IN ($bits(posit_reduced))
    ) m_regime_clo (
        .vec(posit_reduced),
        .cnt(leading_ones),
        .valid(clo_valid)
    );
    count_lead_zero #(
        .W_IN ($bits(posit_reduced))
    ) m_regime_clz (
        .vec(posit_reduced),
        .cnt(leading_zeroes),
        .valid(clz_valid)
    );
    assign regime_len = (posit_reduced[MSB] == 1'b1) ? leading_ones : leading_zeroes;

    // Regime value conversion
    // generates a signed regime value
    two_comp #(W_REG) m_regime_comp (
        .a(regime_len),
        .q(negative_regime)
    );
    assign subbed_regime = regime_len - 1;
    assign regime  = (posit_reduced[MSB] == 1'b0) ? negative_regime : subbed_regime;

    // The remaining sections may or may not exist
    // The logic here is a bit dodgy
    // we are extracting region lengths, and then 'muxing' the outputs using them as indices
    // how about generating a mask, and then doing the realignment as a mux :)

    // Step 1: Create a regime region MSB mask

    wire [W_REG-1:0] leading_count =
        (posit_reduced[MSB] == 1'b0) ? leading_zeroes : leading_ones;

    wire [W_RED-1:0] mask = ~({W_RED {1'b1}} << leading_count);

    // Step 2: split the remainder mask into nought, exp, and fraction masks
    logic [W_RED-1:0] nought_mask;
    logic [W_RED-1:0] exp_mask;
    logic [W_RED-1:0] frac_mask;

    // Find nought mask: nought is the first 1 that appears in the anti-mask
    find_first_one #(W_RED) m_ffo_nought (
        .a(mask),
        .q(nought_mask)
    );

    // Find exp mask: exp is the next #EN ones:
    find_first_n_ones #(
        .W(W_RED),
        .N(EN)
    ) m_ffno_exponent (
        .a(mask & ~nought_mask),
        .q(exp_mask)
    );

    // finally the fraction is just the remaining mask
    assign frac_mask = mask & (~nought_mask) & (~exp_mask);

    // debug signals
    logic [W_RED-1:0] nought_masked;
    logic [W_RED-1:0] exp_masked;
    logic [W_RED-1:0] frac_masked;

    assign nought_masked = posit_reduced & nought_mask;
    assign frac_masked   = posit_reduced & frac_mask;
    assign exp_masked    = posit_reduced & exp_mask;

    // Both the fraction and the exponent require alignment
    // This is done with explicit generation of every version, and a muxing
    // selection of the correct desired position based on a MSB/LSB bit flag
    // This is possibly faster than a CLO/CLZ tree and a barrell shifter

    // the fraction is missing it's leading 1 that signifies the point location
    // and needs to be aligned to the MSB, as it is right-expanding

    // create an MSB+1 bit identifier
    logic [W_RED-1:0] frac_MSB_bit;
    // First bit is always the same
    assign frac_MSB_bit[WIDTH-2] = frac_mask[WIDTH-2];
    generate
        for (genvar k = WIDTH-3; k >= 0; k--) begin : gen_frac_MSB
            assign frac_MSB_bit[k] = (frac_mask[k] & ~frac_mask[k+1]);
        end
    endgenerate

    // Now generate all shifted versions of the frac region and select the right one
    logic [  WIDTH-2:0] frac_shifted_array[WIDTH-2:0];
    logic [2*WIDTH-2:0] extended_f;
    assign extended_f = {frac_mask & posit_reduced, {WIDTH{1'b0}}};
    generate
        for (genvar m = 0; m <= WIDTH - 2; m++) begin : gen_frac_shifted_array
            assign frac_shifted_array[m] = (frac_MSB_bit[m]==1'b1) ? extended_f[m+WIDTH:m+2] : 'b0;
        end
    endgenerate
    logic [WIDTH-2:0] frac_shifted;
    assign frac_shifted = frac_shifted_array.or();

    // The mantissa field can now be extracted
    generate
        if (W_MAN >= WIDTH) begin : gen_export_mantissa_large
            assign mantissa = {1'b1, frac_shifted, {(W_MAN-1-$bits(frac_shifted)){1'b0}}};
        end else begin : gen_export_mantissa_small
            assign mantissa = {1'b1, frac_shifted[$bits(mantissa)-2:0]};
        end
    endgenerate

    // The exponent needs to be correctly shifted to remove trailing zeroes but
    // can be right aligned as a valid whole number value
    // Hence repeat the above extraction semantics

    // create a LSB bit identifier
    logic [WIDTH-2:0] exp_LSB_bit;
    assign exp_LSB_bit[0] = exp_mask[0];
    generate
        for (genvar j = 1; j <= WIDTH - 2; j++) begin : gen_exponent_LSB
            assign exp_LSB_bit[j] = (exp_mask[j] & ~exp_mask[j-1]);
        end
    endgenerate

    // Now generate all shifted versions of the exp region and select the right one
    logic [2*WIDTH-2:0] extended_e;
    assign extended_e = {{WIDTH{1'b0}}, exp_mask & posit_reduced};
    logic [WIDTH-2:0] exp_shifted_array[WIDTH-2:0];
    generate
        for (genvar l = 0; l <= WIDTH - 2; l++) begin : gen_exponent_shifted_array
            assign exp_shifted_array[l] = (exp_LSB_bit[l] == 1'b1) ? extended_e[WIDTH-2+l:l] : 'b0;
        end
    endgenerate
    logic [WIDTH-2:0] exp_shifted;
    assign exp_shifted = exp_shifted_array.or();

    // The exponent field can now be extracted
    generate
        if (W_EXP >= $bits(exp_shifted)) begin : gen_exp_out_large
            assign exponent = {{(W_EXP-$bits(exp_shifted)){1'b0}}, exp_shifted};
        end else begin : gen_exp_out_small
            assign exponent = exp_shifted[W_EXP-1:0];
        end
    endgenerate

endmodule : format_decoder

