// takes a logic bus and reports the twos complement of it
`include "common.svh"

import common::*;

module two_comp #(
	parameter WIDTH=8)(
	input logic [WIDTH-1:0] a,
	output logic [WIDTH-1:0] q
    );
logic [WIDTH-1:0] nota;
logic ovf;

assign nota = ~a;
assign {ovf, q} = nota + 1'b1;

endmodule : two_comp
