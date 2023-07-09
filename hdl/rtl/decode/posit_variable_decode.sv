import posit/posit_types::*

module posit_variable_decode #(
    parameter int unsigned width = 32,
    parameter int unsigned es    = 1
) (
    input logic [width-1:0] p,

    output sign_t sign,
    output logic signed   [width-2:0] regime, exponent,
    output logic unsigned [width-2:0] fraction
);

    /* DECODE A VARIABLE WIDTH POSIT */

    always_comb sign = p[width-1];

    

endmodule
