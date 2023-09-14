import common::*;

module format_encoder #(
    parameter int WIDTH = 7,
    parameter int EN = 1,
    // Bits required for each field (+ sign bit)
    parameter int W_REG = $clog2(WIDTH) + 1,
    parameter int W_EXP = $clog2(WIDTH) + 1,
    parameter int W_MAN = WIDTH
) (
    input logic signed [W_REG-1:0] regime,
    input logic signed [W_EXP-1:0] exponent,
    input logic unsigned [W_MAN-1:0] mantissa,
    input logic n_r,
    output logic [WIDTH-1:0] q
);

    // step 1: combination and alignment
    // 1 bit is always implicit for the sign
    // hence for 2 extra bits for rounding we only need WIDTH
    logic [WIDTH:0] expanded_mantissa;
    logic unsigned [W_REG-1:0] abs_regime;
    assign abs_regime = (regime < 0) ? -regime : regime + 'b1;

    // this is a bit complex as it depends on the size of the posit and IR
    // in one step shift the mantissa to its correct position, and grow to the full size
    generate
        if (WIDTH >= W_MAN) begin : gen_expanded_mantissa_a
            // if the e_m is bigger than the mantissa IR, left align
            assign expanded_mantissa = {
                mantissa >> (abs_regime + EN[W_REG-1:0] + 1), {WIDTH + 1 - $bits(mantissa) {1'b0}}
            };
        end else begin : gen_expanded_mantissa_b
            logic [W_MAN-1:0] interim_em;
            assign interim_em = mantissa >> (abs_regime + EN[W_REG-1:0] + 1);
            assign expanded_mantissa[WIDTH:0] = interim_em[W_MAN:W_MAN-WIDTH];
        end
    endgenerate

    // extract the rounding pair
    logic [WIDTH-2:0] interim_posit;
    logic [1:0] rounding_pair;
    // assign interim_posit = expanded_mantissa[WIDTH:2];
    assign rounding_pair = expanded_mantissa[1:0];
    // TODO this rounding just adds 1 to the final posit if theres excess mantissa
    assign interim_posit = rounding_pair[1] ? expanded_mantissa[WIDTH:2] + 1'b1 : expanded_mantissa[WIDTH:2];

    // align the exponent
    logic [WIDTH-2:0] shifted_exponent;
    assign shifted_exponent = {{WIDTH-W_EXP-1{1'b0}},exponent}<<(WIDTH[W_EXP-1:0]-1-abs_regime-1-EN[W_EXP-1:0]);


    // generate the regime (set first abs_r ones)
    // if r < 0 we use abs_regime*"0", else abs_regime*"1" + r_nought

    // get the r_nought bit
    // TODO - MAY BE NEGATIVE
    logic [WIDTH-2:0] regime_rno;
    assign regime_rno = 1'b1 << (WIDTH[W_REG-1:0] - 2 - abs_regime);

    // get the regime bits
    logic [WIDTH-2:0] regime_rno_invert;
    /* verilator lint_off UNOPTFLAT */
    logic [WIDTH-2:0] regime_mask;
    assign regime_rno_invert = ~regime_rno;

    // there is atleast 1 regime bit
    // extend until the rnought bit
    generate
        assign regime_mask[WIDTH-2] = 1'b1;
        for (genvar i = WIDTH - 3; i >= 0; i--) begin
            assign regime_mask[i] = regime_mask[i+1] & (regime_rno_invert[i]);
        end
    endgenerate

    // combine all the fields
    // if r < 0 we use abs_regime*"0", else abs_regime*"1" + r_nought
    always_comb begin
        if (regime < 0) begin
            // r_no = 1
            posit_aligned = {1'b0, regime_rno | shifted_exponent | interim_posit};
        end else begin
            posit_aligned = {1'b0, regime_mask | shifted_exponent | interim_posit};
        end
    end

    logic [WIDTH-1:0] posit_aligned;
    logic [WIDTH-1:0] posit_rounded;

    // step 3: sign check
    // if (n_r) return a TC of the rounded posit
    logic [WIDTH-1:0] posit_signed;
    logic [WIDTH-1:0] posit_complement;
    two_comp #(WIDTH) output_sign (
        .a(posit_aligned),
        .q(posit_complement)
    );
    assign posit_signed = n_r ? posit_complement : posit_aligned;

    // export
    assign q = posit_signed;

endmodule

