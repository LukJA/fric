module priority_encoder_16_tb (
    input  logic leading_bit,
    input  logic [15:0] i,

    output logic [3:0] c,
    output logic valid
);
    
    count_regime_16 i_count_regime_16(
        .leading_bit(leading_bit), .i(i),
        .c(c), .valid(valid)
    );

endmodule
