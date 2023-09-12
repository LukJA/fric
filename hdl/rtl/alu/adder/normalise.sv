import common::*;

module normalise #(
	parameter WIDTH=7,
    parameter EN=1)(
    input logic signed [7:0] mantissa_sum,
    input logic signed [7:0] interim_regime, interim_exponent,
    output logic signed [7:0] mantissa,
    output logic signed [7:0] regime, exponent
    );

// get normalisation counts
logic signed [7:0] normz;
count_lead_zero #(8,8) mant_ffo (.a(mantissa_sum), .q(normz));

// implicit barrell shift to exclude leading '1'
// TODO what if there is no leading 1
logic signed [7:0] mantissa_lo;
assign mantissa_lo = mantissa_sum << (normz + 1'b1);

// do the re-regime and re-exponent 
logic signed [7:0] a_exponent;
assign a_exponent = interim_exponent + 1'b1 - normz;


// for a too big exponent:
// - allowed bits equals es - so shift is the position of the first 1 minus es
// for a negative exponent:
// -  shift up until its positive
logic signed [7:0] b_regime, b_exponent, b_exp_tc;
logic unsigned [7:0] shamt_exp, shamt_bar;

two_comp #(8) negate_exponent (.a(a_exponent), .q(b_exp_tc));
count_lead_zero #(8,8) clz_exp (.a(a_exponent), .q(shamt_exp));
count_lead_zero #(8,8) clz_bar (.a(b_exp_tc), .q(shamt_bar));

logic unsigned [7:0] exp_adj_a, exp_adj_b;
assign exp_adj_a = (8-shamt_exp-1);
assign exp_adj_b = (8-shamt_bar);

logic dbg_exp_big, dbg_exp_small;

always_comb
begin
    // for a too big exponent
    if (a_exponent >= 2**EN) begin
        dbg_exp_big = 1'b1;
        dbg_exp_small = 1'b0;

        b_exponent = a_exponent - (exp_adj_a<<EN);
        b_regime = interim_regime + exp_adj_a;
    // for a negative exponent
    end else if (a_exponent < 0) begin 
        dbg_exp_big = 1'b0;
        dbg_exp_small = 1'b1;

        b_exponent = a_exponent + (exp_adj_b<<EN);
        b_regime = interim_regime - exp_adj_b;
    end else begin
        b_exponent = a_exponent;
        b_regime = interim_regime;
        dbg_exp_big = 1'b0;
        dbg_exp_small = 1'b0;
    end
end

always_comb
begin
    // if all zeros we have the special == 0 case
    if (&(~mantissa_sum) == 1'b1) begin
        mantissa = 'b0;
        exponent = 'b0;
        regime = {1'b1, 7'b0};
    // otherwise feed forward the computed values
    end else begin
        mantissa = mantissa_lo;
        exponent = b_exponent;
        regime = b_regime;
    end
end

endmodule : normalise

