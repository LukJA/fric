// takes a posit bus and extracts the relevant
// regions as digital signed byte values 
import common::*;

// Comb
module format_encoder #(
	parameter WIDTH=7,
    parameter EN=1)(
	input logic signed [7:0] regime, exponent,
    input logic unsigned [7:0] mantissa,
    input logic n_r,
	output logic [WIDTH-1:0] q
    );

// step 1: combination and alignment
// 1 bit is always implicit for the sign
// hence for 2 extra bits for rounding we only need WIDTH
logic [WIDTH:0] expanded_mantissa;
logic unsigned [7:0] abs_regime;
assign abs_regime = (regime<0) ? -regime : regime+'b1 ;

// this is a bit complex as it depends on the size of the posit and IR
generate
    if (WIDTH >= 7) begin
        // if the e_m is bigger than the mantissa IR, left align
        assign expanded_mantissa = {mantissa>>(abs_regime+EN+1), {WIDTH-7{1'b0}}};
    end else begin
        logic [7:0] interim_em; 
        assign interim_em = mantissa>>(abs_regime+EN+1);
        assign expanded_mantissa[WIDTH:0] = interim_em[7:7-WIDTH];
    end
endgenerate

// extract the rounding pair 
logic [WIDTH-2:0] interim_posit;
logic [1:0] rounding_pair;
assign interim_posit = expanded_mantissa[WIDTH:2];
assign rounding_pair = expanded_mantissa[1:0];

// align the exponent
// TODO - MAY BE NEGATIVE
// TODO fix width inconsistency
logic [WIDTH-2:0] shifted_exponent;
logic [7:0] shifted_exponent_ir;
assign shifted_exponent_ir = exponent<<(WIDTH-2-abs_regime-1);
assign shifted_exponent = shifted_exponent_ir[WIDTH-2:0];

// generate the regime (set first abs_r ones)
// if r < 0 we use abs_regime*"0", else abs_regime*"1" + r_nought

// get the r_nought bit
// TODO - MAY BE NEGATIVE
logic [WIDTH-2:0] regime_rno;
assign regime_rno = 1'b1<<(WIDTH-2-abs_regime);

// get the regime bits
logic [WIDTH-2:0] regime_rno_invert;
/* verilator lint_off UNOPTFLAT */ 
logic [WIDTH-2:0] regime_mask;
assign regime_rno_invert = ~regime_rno;

// there is atleast 1 regime bit
// extend until the rnought bit
generate
    assign regime_mask[WIDTH-2] = 1'b1;
    for (genvar i = WIDTH-3; i >= 0; i--) begin
        assign regime_mask[i] = regime_mask[i+1] & (regime_rno_invert[i]);
    end
endgenerate

// combine all the fields
// if r < 0 we use abs_regime*"0", else abs_regime*"1" + r_nought
always_comb
begin
    if (regime<0) begin
        // r_no = 1
        posit_aligned = {1'b0 , regime_rno | shifted_exponent | interim_posit};
    end else begin
        posit_aligned = {1'b0, regime_mask | shifted_exponent | interim_posit};
    end
end

logic [WIDTH-1:0] posit_aligned;

// step 2: rounding 
logic [WIDTH-1:0] posit_rounded;
assign posit_rounded = posit_aligned;

// step 3: sign check
// if (n_r) return a TC of the rounded posit
logic [WIDTH-1:0] posit_signed;
logic [WIDTH-1:0] posit_complement;
two_comp #(WIDTH) output_sign (.a(posit_rounded), .q(posit_complement));
assign posit_signed = n_r ? posit_complement : posit_rounded;

// export
assign q = posit_signed;

endmodule

