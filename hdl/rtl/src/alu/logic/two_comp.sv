// takes a logic bus and reports the twos complement of it
`include "common.svh"

import common::*;

module two_comp #(
	parameter WIDTH=8
)(
	input  logic [WIDTH-1:0] a,
	output logic [WIDTH-1:0] q
);

	wire [WIDTH-1 : 0] na = ~a;
	wire [WIDTH   : 0] complement_with_ovf = na + 1'b1;
	assign q = complement_with_ovf[WIDTH-1 : 0];

endmodule : two_comp
