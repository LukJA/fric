import common::*;

module posit_32b_sub (
    input logic clk,
    input logic rst,
    input logic [31:0] a,
    input logic [31:0] b,
    output logic [31:0] q
);

    logic [31:0] b_complement;

    // Negate the value of b via two's complement,
    // and forward to adder
    two_comp #(
        .WIDTH(32)
    ) m_twoc (
        .a(b),
        .q(_b)
    );

    // Create a 32/3 size posit adder
    posit_adder #(
        .WIDTH(32),
        .EN(3)
    ) m_p7b_adder (
        .clk(clk),
        .rst(rst),
        .a  (a),
        .b  (b),
        .q  (q)
    );

endmodule : posit_32b_sub
