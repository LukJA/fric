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
        for (genvar i = 0; i < 15; i++) begin
            count_leading_encoder(leading = b) i_count_leading_encoder (
                .leading_bit(v[29]),
                .i(v[2*i + 1: 2*i]),
                .o(v_enc[2*i + 1: 2*i])
            )
        end
    endgenerate

endmodule