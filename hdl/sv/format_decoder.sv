// takes a posit bus and extracts the relevant
// regions as digital signed byte values 

module format_decoder #(
	parameter WIDTH=7,
    parameter EN=1)(
	input logic [WIDTH-1:0] posit,
    output logic sign,
	output logic signed [7:0] regime, exponent,
    output logic unsigned [7:0] mantissa
    );

assign sign = 0;
assign regime = 0;
assign exponent = 0;
assign mantissa = 1;

endmodule : format_decoder