import common::*;

module mantissa_adder #(
    parameter int WIDTH=7,
    parameter int EN=1)(
    input sign_t a_sign, b_sign,
    input logic signed [7:0] a_regime, a_exponent,
    input logic unsigned [7:0] a_mantissa,
    input logic signed [7:0] b_regime, b_exponent, 
    input logic unsigned [7:0] b_mantissa,
    output logic unsigned [7:0] mantissa_sum,
    output logic signed [7:0] interim_regime, interim_exponent,
    output logic negate_result
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
assign interim_regime = big_regime;

// calulate the necessary addition offsets
logic signed [7:0] shamt;
logic signed [7:0] delta_regime, delta_exponent;

assign delta_regime = big_regime - small_regime;
assign delta_exponent = big_exponent - small_exponent;
assign shamt = (delta_regime<<EN) + delta_exponent;

// unify sign description
// B+ S- => smaller frac is negative - TC for a subtraction
// B- S+ => Bigger frac is negative - TC smaller and negate result
// B- S- => Negate Answer
// B+ S+ => Default

// NOTE using implicit twos complement signed repr
logic unsigned [7:0] small_mantissa_sh;
logic unsigned [7:0] small_mantissa_sh_alt;
// barrel shift the smaller fraction to the right
assign small_mantissa_sh = small_mantissa >> shamt;

logic neg_in_sum;
always_comb
begin
// in which situations do we negate the smaller value for the binary add
case ({big_sign,small_sign})
    {POS, NEG}: neg_in_sum = 1'b1;
    {NEG, POS}: neg_in_sum = 1'b1;
    default:    neg_in_sum = 1'b0;
endcase

// in which situations should we negate our final answer
case ({big_sign,small_sign})
    {NEG, POS}: negate_result = 1'b1;
    {NEG, NEG}: negate_result = 1'b1;
    default:    negate_result = 1'b0;
endcase
end

assign small_mantissa_sh_alt = neg_in_sum ? (~small_mantissa_sh) + 1'b1 : small_mantissa_sh;

// sum the final fraction sections
logic unsigned [8:0] s_mantissa_sum;
logic ovf;
assign s_mantissa_sum = big_mantissa + small_mantissa_sh_alt;
assign ovf = s_mantissa_sum[8];

always_comb
begin
    if (ovf & ~neg_in_sum) begin
        interim_exponent = big_exponent;
        mantissa_sum = {1'b1, 7'b0} | (s_mantissa_sum[7:0]>>1);
    end else begin
        interim_exponent = big_exponent - 1;
        mantissa_sum = s_mantissa_sum[7:0];
    end
end

// this is enough for the second stage, return data
endmodule : mantissa_adder

