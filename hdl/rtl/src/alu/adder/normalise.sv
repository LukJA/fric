import common::*;

module normalise #(
    parameter int WIDTH = 7,
    parameter int EN = 1,
    // Bits required for each field (+ sign bit)
    parameter int W_REG = $clog2(WIDTH) + 1,
    parameter int W_EXP = $clog2(WIDTH) + 1,
    parameter int W_MAN = WIDTH
) (
    input  logic unsigned [W_MAN-1:0] mantissa_sum,
    input  logic signed   [W_REG-1:0] interim_regime,
    input  logic signed   [W_EXP-1:0] interim_exponent,
    output logic unsigned [W_MAN-1:0] mantissa,
    output logic signed   [W_REG-1:0] regime,
    output logic signed   [W_EXP-1:0] exponent
);

    // get normalisation shift
    logic signed [W_REG-1:0] normz;
    count_lead_zero #(
        .W_IN (W_MAN)
    ) m_mantossa_clz (
        .vec(mantissa_sum),
        .cnt(normz)
    );

    // implicit barrell shift to exclude leading '1'
    // TODO
    // - check what if there is no leading 1 (i.e. mantissa is 0)
    logic signed [W_MAN-1:0] mantissa_lo;
    assign mantissa_lo = mantissa_sum << (normz + 1'b1);

    // do the re-regime and re-exponent shifts
    logic signed [W_EXP-1:0] a_exponent;
    assign a_exponent = interim_exponent + 1'b1 - normz;


    // for a too big exponent:
    // - allowed bits equals es - so shift is the position of the first 1 minus es
    // for a negative exponent:
    // -  shift up until its positive
    logic signed [W_REG-1:0] b_regime;
    logic signed [W_EXP-1:0] b_exponent, b_exp_tc;

    logic unsigned [W_REG-1:0] shamt_exp, shamt_bar;

    two_comp #(W_EXP) negate_exponent (
        .a(a_exponent),
        .q(b_exp_tc)
    );

    count_lead_zero #(
        .W_IN (W_EXP)
    ) m_clz_exp (
        .vec(a_exponent),
        .cnt(shamt_exp)
    );

    count_lead_zero #(
        .W_IN (W_EXP)
    ) m_clz_exp_bar (
        .vec(b_exp_tc),
        .cnt(shamt_bar)
    );

    logic unsigned [W_EXP-1:0] exp_adj_a, exp_adj_b;
    assign exp_adj_a = (W_EXP[W_EXP-1:0] - shamt_exp - EN[W_EXP-1:0]);
    assign exp_adj_b = (W_EXP[W_EXP-1:0] - shamt_bar);

    logic dbg_exp_big, dbg_exp_small;

    always_comb begin
        // for a too big exponent
        if (a_exponent >= 2 ** EN) begin
            dbg_exp_big = 1'b1;
            dbg_exp_small = 1'b0;

            b_exponent = a_exponent - (exp_adj_a << EN);
            b_regime = interim_regime + exp_adj_a;
            // for a negative exponent
        end else if (a_exponent < 0) begin
            dbg_exp_big = 1'b0;
            dbg_exp_small = 1'b1;

            b_exponent = a_exponent + (exp_adj_b << EN);
            b_regime = interim_regime - exp_adj_b;
        end else begin
            b_exponent = a_exponent;
            b_regime = interim_regime;
            dbg_exp_big = 1'b0;
            dbg_exp_small = 1'b0;
        end
    end

    always_comb begin
        // if all zeros we have the special == 0 case
        if (&(~mantissa_sum) == 1'b1) begin
            mantissa = 'b0;
            exponent = 'b0;
            regime   = {1'b1, {$bits(regime) - 1{1'b0}}};
            // otherwise feed forward the computed values
        end else begin
            mantissa = mantissa_lo;
            exponent = b_exponent;
            regime   = b_regime;
        end
    end

endmodule : normalise

