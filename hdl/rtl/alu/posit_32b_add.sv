import common::*;

module posit_32b_add (
    input logic clk,
    input logic rst,
    input logic [31:0] a,
    input logic [31:0] b,
    output logic [31:0] q
);

    // create a 32/2 size posit adder
    posit_adder #(
        .WIDTH(32),
        .EN(2)
    ) m_p32b_adder (
        .clk(clk),
        .rst(rst),
        .a  (a),
        .b  (b),
        .q  (q)
    );

endmodule : posit_32b_add
