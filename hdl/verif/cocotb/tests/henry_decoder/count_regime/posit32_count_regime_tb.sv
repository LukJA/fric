module posit32_count_regime_tb (
    input  logic [31:0] i,

    output logic [4:0] c,
    output logic valid
);

    posit32_t tmp;

    assign tmp = i;

    posit32_count_regime i_posit32_count_regime(
        .i(tmp), .c(c), .valid(valid)
    );

endmodule
