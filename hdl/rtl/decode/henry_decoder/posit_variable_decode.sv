import posit/posit_types::sign_t

module posit_variable_decode #(
    parameter int unsigned width = 32,
    parameter int unsigned es    = 2
) (
    input logic [width-1:0] p,

    output sign_t sign,
    output logic signed   [width-2:0] regime, exponent,
    output logic unsigned [width-2:0] fraction
);

    /* DECODE A VARIABLE WIDTH POSIT
     * Any fixed/standard posit types (e.g. 32- or 64-bit)
     * just need to be wrappers around this.
     */

    always_comb sign = p[width-1];

    // start with a leading zeros/ones counter

endmodule
