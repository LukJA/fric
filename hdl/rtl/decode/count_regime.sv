module count_leading_encoder #(
    parameter bit leading
) (
    input  bit [1:0] i,
    output bit [1:0] o
)

endmodule

module count_regime #(
    parameter int unsigned width = 30,
    parameter bit b
) (
    input  bit [width-1:0] v,
    output integer unsigned c
);

    /* count leading zeros method stolen from here:
     * https://electronics.stackexchange.com/questions/196914/verilog-synthesize-high-speed-leading-zero-count
     * (also see https://en.wikipedia.org/wiki/Find_first_set)
     */

    logic [width-1:0] v_enc;

    generate
        if (b == 1'h1) begin
            for (genvar i = 0; i < width / 2; i++) begin
                count_leading_encoder(leading = b) i_count_leading_encoder (
                    .i(v[2*i + 1: 2*i]),
                    .o(v_enc[2*i + 1: 2*i])
                )
            end
        end
        else begin

        end
    endgenerate

endmodule