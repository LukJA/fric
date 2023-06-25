import common::*;

module mantissa_adder #(
	parameter WIDTH=7,
    parameter EN=1)(
    input sign_t a_sign, b_sign,
    input logic signed [7:0] a_regime, a_exponent,
    input logic unsigned [7:0] a_mantissa,
    input logic signed [7:0] b_regime, b_exponent, 
    input logic unsigned [7:0] b_mantissa
    );

logic big_sign, small_sign;
logic signed [7:0] big_regime, big_exponent;
logic unsigned [7:0] big_mantissa;
logic signed [7:0] small_regime, small_exponent;
logic unsigned [7:0] small_mantissa;

comparator u_comp (.a_sign(a_sign), .b_sign(b_sign),
					.a_regime(a_regime), .a_exponent(a_exponent), .a_mantissa(a_mantissa),
					.b_regime(b_regime), .b_exponent(b_exponent), .b_mantissa(b_mantissa), 
					.big_sign(big_sign), .small_sign(small_sign),
					.big_regime(big_regime), .big_exponent(big_exponent), .big_mantissa(big_mantissa),
					.small_regime(small_regime), .small_exponent(small_exponent), .small_mantissa(small_mantissa));

// collect the interim values
logic signed [7:0] interim_regime, interim_exponent;
assign interim_regime = big_regime;
assign interim_exponent = big_exponent - 1;

// calulate the necessary addition offsets
logic signed [7:0] delta_regime, delta_exponent, shamt;
logic signed [7:0] small_mantissa_sh;
assign delta_regime = big_regime - small_regime;
assign delta_exponent = big_exponent - small_exponent;
assign shamt = (delta_regime<<EN) + delta_exponent;
// barrell shift the smaller fraction to the right
assign small_mantissa_sh = small_mantissa >> shamt;

logic signed [7:0] small_mantissa_sh_alt;
always_comb
case ({big_sign,small_sign})
    {POS, NEG}: small_mantissa_sh_alt = (~small_mantissa_sh) + 1'b1;
    {NEG, POS}: small_mantissa_sh_alt = (~small_mantissa_sh) + 1'b1;
    default: small_mantissa_sh_alt = small_mantissa_sh;
endcase


endmodule : mantissa_adder

