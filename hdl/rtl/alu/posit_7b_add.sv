import common::*;

module posit_7b_add (
    input logic clk,
    input logic rst,
    input logic [6:0] a,
    input logic [6:0] b,
    output logic [6:0] q
);

    // create a 7/1 size posit adder
    posit_adder #(
        .WIDTH(7),
        .EN(1)
    ) m_p7b_adder (
        .clk(clk),
        .rst(rst),
        .a  (a),
        .b  (b),
        .q  (q)
    );

endmodule : posit_7b_add
