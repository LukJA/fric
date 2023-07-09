import posit/posit_types::sign_t

module posit32_decode #(
    parameter int unsigned es = 2
) (
    input posit32_t p,

    output sign_t sign,
    output logic signed [31:0] regime, exponent,
    output logic unsigned [31:0] fraction
);

    /* setting the sign bit is trivial */
    always_comb sign = p.sign;

    posit_variable_decode(32, es) i_posit_variable_decode(
        .p(p),
        .sign(sign),
        .regime(regime),
        .exponent(exponent),
        .fraction(fraction)
    )

endmodule
