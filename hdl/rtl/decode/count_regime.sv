module count_leading_encoder #(
    parameter bit leading
) (
    input  bit       leading_bit,
    input  bit [1:0] i,
    output bit [1:0] o
)

    always_comb begin
        // the leading bit is variable so bake it into this logic.
        if (leading_bit) begin
            case (d[1:0])
                2'b00    :  q = 2'b10;
                2'b01    :  q = 2'b01;
                default  :  q = 2'b00;
            endcase
        end
        else begin
            case (d[1:0])
                2'b11    :  q = 2'b10;
                2'b10    :  q = 2'b01;
                default  :  q = 2'b00;
            endcase
        end
   end

endmodule

module count_regime #(
    parameter int unsigned width = 30,
    parameter bit b
) (
    input  bit [width-1:0] v,
    output integer unsigned c
);

    /* COUNT THE NUMBER OF LEADING ZEROS/ONES TO FIND THE REGIME LENGTH */

    /* using the below method, we can slice off the leading one and feed that
     * to the encoders. Then the rest of the architecture stays identical but
     * the encoder mapping between 0/1 changes to detect 1s instead of 0s.
     */

    /* count leading zeros method stolen from here:
     * https://electronics.stackexchange.com/questions/196914/verilog-synthesize-high-speed-leading-zero-count
     * (also see https://en.wikipedia.org/wiki/Find_first_set)
     */

    logic [width-1:0] v_enc;

    generate
        for (genvar i = 0; i < width / 2; i++) begin
            count_leading_encoder(leading = b) i_count_leading_encoder (
                .leading_bit(b),
                .i(v[2*i + 1: 2*i]),
                .o(v_enc[2*i + 1: 2*i])
            )
        end
    endgenerate

endmodule