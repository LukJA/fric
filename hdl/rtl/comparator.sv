import common::*;

module comparator (
    input sign_t a_sign, b_sign,
    input logic signed [7:0] a_regime, a_exponent,
    input logic unsigned [7:0] a_mantissa,
    input logic signed [7:0] b_regime, b_exponent, 
    input logic unsigned [7:0] b_mantissa, 

    output logic big_sign, small_sign,
    output logic signed [7:0] big_regime, big_exponent,
    output logic unsigned [7:0] big_mantissa,
    output logic signed [7:0] small_regime, small_exponent, 
    output logic unsigned [7:0] small_mantissa
    );

logic a;
assign a = (a_regime > b_regime) | 
           ((a_regime == b_regime) & (a_exponent > b_exponent)) |
            ((a_regime == b_regime) & (a_exponent == b_exponent) & (a_mantissa > b_mantissa));

// Output Muxing
assign big_sign = (a) ? a_sign: b_sign;
assign small_sign = (~a) ? a_sign: b_sign;

assign big_regime = (a) ? a_regime: b_regime;
assign small_regime = (~a) ? a_regime: b_regime;

assign big_exponent = (a) ? a_exponent: b_exponent;
assign small_exponent = (~a) ? a_exponent: b_exponent;

assign big_mantissa = (a) ? a_mantissa: b_mantissa;
assign small_mantissa = (~a) ? a_mantissa: b_mantissa;


endmodule : comparator

