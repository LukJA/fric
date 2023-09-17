module dff #(
	parameter WIDTH=8
) (
	input logic clk,
	input logic signed [WIDTH-1:0] a, b,
	output logic signed [WIDTH-1:0] q
);

// assign q = a + b;

always_ff @(posedge clk) begin
	q <= a + b;
end

// `ifdef COCOTB_SIM
// initial begin
//   $dumpfile ("trace.vcd");
//   $dumpvars (0, signed_add);
// end
// `endif
endmodule : dff
