module posit_adder #(
	parameter WIDTH=7,
    parameter EN=1)(
	input logic clk,
	input logic [WIDTH-1:0] a, b,
	output logic [WIDTH-1:0] q
    );

logic a_sign, b_sign;
logic signed [7:0] a_regime, a_exponent;
logic unsigned [7:0] a_mantissa;
logic signed [7:0] b_regime, b_exponent; 
logic unsigned [7:0] b_mantissa; 


format_decoder a_decode (.posit(a),
						.sign(a_sign),
						.regime(a_regime),
						.exponent(a_exponent),
						.mantissa(a_mantissa));

format_decoder b_decode (.posit(b),
						.sign(b_sign),
						.regime(b_regime),
						.exponent(b_exponent),
						.mantissa(b_mantissa));

assign q = a + b;

endmodule : posit_adder

