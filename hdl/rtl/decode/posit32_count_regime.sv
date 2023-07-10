module posit32_count_regime (
    input  bit [30:0] v,
    output integer unsigned c
);

    /* COUNT THE NUMBER OF LEADING ZEROS/ONES TO FIND THE REGIME LENGTH */

    /* see posit_variable_count_regime.sv for a detailed explanation. */

    logic [29:0] v_enc;

    // intermediate stages
    // FIXME: eventually we'll want to dynamically generate these,
    // but let's try and get a 32b test working first.
    logic [23:0] a;
    logic [15:0] b;
    logic [15:0] c;

    generate
        for (genvar i = 0; i < 30; i += 2) begin
            priority_encoder_4 i_priority_encoder_2 (
                .leading_bit(v[29]),
                .i(v[i+1:i]),
                .o(v_enc[i+1:i])
            )
        end
    endgenerate

endmodule