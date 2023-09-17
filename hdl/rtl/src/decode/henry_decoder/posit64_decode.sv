import posit_types::*;

module posit64_decode #(
    parameter int unsigned es = 2
) (
    input posit64_t p,

    output sign_t sign,
    output logic signed [63:0] regime, exponent,
    output logic unsigned [63:0] fraction
);

    /* setting the sign bit is trivial */
    always_comb sign = p.sign;

    posit_variable_decode #(64, es) i_posit_variable_decode(
        .p(p),
        .sign(sign),
        .regime(regime),
        .exponent(exponent),
        .fraction(fraction)
    );

endmodule
