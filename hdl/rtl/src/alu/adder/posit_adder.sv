import common::*;

module posit_adder #(
    parameter int WIDTH = 7,
    parameter int EN = 1,
    parameter int SF = int'($pow(2, EN)),
    // Bits required for each field (+ sign bit)
    parameter int W_REG = $clog2(WIDTH) - 1,
    parameter int W_EXP = $clog2(WIDTH),
    parameter int W_MAN = WIDTH
) (
    input logic clk,
    input logic rst,
    input logic [WIDTH-1:0] a,
    input logic [WIDTH-1:0] b,
    output logic [WIDTH-1:0] q
);

    sign_t a_sign, b_sign;
    logic signed [W_REG-1:0] a_regime, b_regime;
    logic signed [W_EXP-1:0] a_exponent, b_exponent;
    logic unsigned [W_MAN-1:0] a_mantissa, b_mantissa;

    sign_t dc_a_sign, dc_b_sign;
    logic signed [W_REG-1:0] dc_a_regime, dc_b_regime;
    logic signed [W_EXP-1:0] dc_a_exponent, dc_b_exponent;
    logic unsigned [W_MAN-1:0] dc_a_mantissa, dc_b_mantissa;

    logic signed [W_REG-1:0] interim_regime;
    logic signed [W_EXP-1:0] interim_exponent;
    logic unsigned [W_MAN-1:0] mantissa_sum;
    logic n_r;

    logic signed [W_REG-1:0] cn_interim_regime;
    logic signed [W_EXP-1:0] cn_interim_exponent;
    logic unsigned [W_MAN-1:0] cn_mantissa_sum;
    logic cn_n_r;

    logic signed [W_REG-1:0] regime_norm;
    logic signed [W_EXP-1:0] exponent_norm;
    logic unsigned [W_MAN-1:0] mantissa_norm;

    logic signed [W_REG-1:0] nd_regime;
    logic signed [W_EXP-1:0] nd_exponent;
    logic unsigned [W_MAN-1:0] nd_mantissa;
    logic nd_n_r;


    // stage 1 - posit format decoding

    format_decoder #(
        .WIDTH(WIDTH),
        .EN(EN)
    ) a_decode (
        .posit(a),
        .sign(a_sign),
        .regime(a_regime),
        .exponent(a_exponent),
        .mantissa(a_mantissa)
    );

    format_decoder #(
        .WIDTH(WIDTH),
        .EN(EN)
    ) b_decode (
        .posit(b),
        .sign(b_sign),
        .regime(b_regime),
        .exponent(b_exponent),
        .mantissa(b_mantissa)
    );

    // first pipeline register

    always_ff @(posedge clk) begin
        if (~rst) begin
            dc_a_sign <= POS;
            dc_a_regime <= 'b0;
            dc_a_exponent <= 'b0;
            dc_a_mantissa <= 'b0;
            dc_b_sign <= POS;
            dc_b_regime <= 'b0;
            dc_b_exponent <= 'b0;
            dc_b_mantissa <= 'b0;
        end else begin
            dc_a_sign <= a_sign;
            dc_a_regime <= a_regime;
            dc_a_exponent <= a_exponent;
            dc_a_mantissa <= a_mantissa;
            dc_b_sign <= b_sign;
            dc_b_regime <= b_regime;
            dc_b_exponent <= b_exponent;
            dc_b_mantissa <= b_mantissa;
        end
    end

    // stage 2 - bigger/smaller and fraction addition

    mantissa_adder #(
        .WIDTH(WIDTH),
        .EN(EN)
    ) mant_add (
        .a_sign(dc_a_sign),
        .b_sign(dc_b_sign),
        .a_regime(dc_a_regime),
        .a_exponent(dc_a_exponent),
        .a_mantissa(dc_a_mantissa),
        .b_regime(dc_b_regime),
        .b_exponent(dc_b_exponent),
        .b_mantissa(dc_b_mantissa),
        .mantissa_sum(mantissa_sum),
        .interim_regime(interim_regime),
        .interim_exponent(interim_exponent),
        .negate_result(n_r)
    );


    // second pipeline register

    always_ff @(posedge clk) begin
        if (~rst) begin
            cn_interim_regime <= 'b0;
            cn_interim_exponent <= 'b0;
            cn_mantissa_sum <= 'b0;
            cn_mantissa_sum <= 'b0;
            cn_n_r <= 'b0;
        end else begin
            cn_interim_regime <= interim_regime;
            cn_interim_exponent <= interim_exponent;
            cn_mantissa_sum <= mantissa_sum;
            cn_n_r <= n_r;
        end
    end

    // stage 3 - normalisation

    normalise #(
        .WIDTH(WIDTH),
        .EN(EN)
    ) p_norm (
        .mantissa_sum(cn_mantissa_sum),
        .interim_regime(cn_interim_regime),
        .interim_exponent(cn_interim_exponent),
        .mantissa(mantissa_norm),
        .regime(regime_norm),
        .exponent(exponent_norm)
    );

    // third pipeline register

    always_ff @(posedge clk) begin
        if (~rst) begin
            nd_regime <= 'b0;
            nd_exponent <= 'b0;
            nd_mantissa <= 'b0;
            nd_n_r <= 'b0;
        end else begin
            nd_regime <= regime_norm;
            nd_exponent <= exponent_norm;
            nd_mantissa <= mantissa_norm;
            nd_n_r <= cn_n_r;
        end
    end

    format_encoder #(
        .WIDTH(WIDTH),
        .EN(EN)
    ) p_encode (
        .regime(nd_regime),
        .exponent(nd_exponent),
        .mantissa(nd_mantissa),
        .n_r(nd_n_r),
        .q(q)
    );

    // Output buffer register


endmodule : posit_adder

