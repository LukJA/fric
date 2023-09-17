module count_regime #(
    parameter int unsigned width = 31
) (
    input  bit [width-1:0] v,
    output integer unsigned c
);

    /* COUNT THE NUMBER OF LEADING ZEROS/ONES TO FIND THE REGIME LENGTH */

    /* Using the below method, we can slice off the leading bit and feed that
     * to the encoders. Then the rest of the architecture stays identical but
     * the encoder mapping between 0/1 changes to detect 1s instead of 0s.
     */

    /* Count leading zeros method stolen from here:
     * https://electronics.stackexchange.com/questions/196914/verilog-synthesize-high-speed-leading-zero-count
     * (also see https://en.wikipedia.org/wiki/Find_first_set)
     */

    /* To apply this method, consider a 32b posit:
     * We have 1 sign bit and 31 bits which together make all of R, E, & F.
     * Slicing off the msb tells us whether we're counting leading ones or
     * zeros, leaving an even 30 bits to work with. These bits can be divided
     * into pairs and then counted accordingly.
     */

    logic [width-2:0] v_enc;

    // generate
    //     for (genvar i = 0; i < (width-1) / 2; i++) begin
    //         count_leading_encoder(leading = b) i_count_leading_encoder (
    //             .leading_bit(v[width-1]),
    //             .i(v[2*i + 1: 2*i]),
    //             .o(v_enc[2*i + 1: 2*i])
    //         )
    //     end
    // endgenerate

endmodule