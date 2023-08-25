import common::*;

module posit_adder #(
	parameter WIDTH=7,
    parameter EN=1,
	parameter SF=2**EN)(
	input logic clk,
	input logic rst,
	input logic [WIDTH-1:0] a, b,
	output logic [WIDTH-1:0] q
    );

// stage 1 - posit format decoding 

sign_t a_sign, b_sign;
logic signed [7:0] a_regime, a_exponent;
logic unsigned [7:0] a_mantissa;
logic signed [7:0] b_regime, b_exponent; 
logic unsigned [7:0] b_mantissa; 


format_decoder  #(WIDTH,EN) a_decode (.posit(a),
						.sign(a_sign),
						.regime(a_regime),
						.exponent(a_exponent),
						.mantissa(a_mantissa));

format_decoder  #(WIDTH,EN) b_decode (.posit(b),
						.sign(b_sign),
						.regime(b_regime),
						.exponent(b_exponent),
						.mantissa(b_mantissa));

// first pipeline register

sign_t dc_a_sign, dc_b_sign;
logic signed [7:0] dc_a_regime, dc_a_exponent;
logic unsigned [7:0] dc_a_mantissa;
logic signed [7:0] dc_b_regime, dc_b_exponent; 
logic unsigned [7:0] dc_b_mantissa; 

always_ff @(posedge clk) begin
	if (~rst) begin
		dc_a_sign <= POS;
		dc_a_regime <= 'b0;
		dc_a_exponent <= 'b0;
		dc_a_mantissa <= 'b0;
		dc_b_sign <= POS;
		dc_b_regime <= 'b0;
		dc_b_exponent <= 'b0;
		dc_b_mantissa <= 'b0;
	end else begin	
		dc_a_sign <= a_sign;
		dc_a_regime <= a_regime;
		dc_a_exponent <= a_exponent;
		dc_a_mantissa <= a_mantissa;
		dc_b_sign <= b_sign;
		dc_b_regime <= b_regime;
		dc_b_exponent <= b_exponent;
		dc_b_mantissa <= b_mantissa;
	end
end

// stage 2 - bigger/smaller and fraction addition

logic signed [7:0] interim_regime, interim_exponent; 
logic unsigned [7:0] mantissa_sum; 

mantissa_adder #(WIDTH,EN) mant_add (.a_sign(dc_a_sign), .b_sign(dc_b_sign),
									.a_regime(dc_a_regime), 
									.a_exponent(dc_a_exponent),
									.a_mantissa(dc_a_mantissa),
									.b_regime(dc_b_regime), 
									.b_exponent(dc_b_exponent),
									.b_mantissa(dc_b_mantissa),
									.mantissa_sum(mantissa_sum),
									.interim_regime(interim_regime),
									.interim_exponent(interim_exponent)
									);


// second pipeline register

logic signed [7:0] cn_interim_regime, cn_interim_exponent; 
logic signed [7:0] cn_mantissa_sum; 

always_ff @(posedge clk) begin
	if (~rst) begin
		cn_interim_regime <= 'b0;
		cn_interim_exponent <= 'b0;
		cn_mantissa_sum <= 'b0;
	end else begin	
		cn_interim_regime <= interim_regime;
		cn_interim_exponent <= interim_exponent;
		cn_mantissa_sum <= mantissa_sum;
	end
end

// stage 3 - normalisation

logic signed [7:0] mantissa_norm;
logic signed [7:0] regime_norm, exponent_norm;

normalise #(WIDTH,EN) p_norm (.mantissa_sum(cn_mantissa_sum),
								.interim_regime(cn_interim_regime),
								.interim_exponent(cn_interim_exponent),
								.mantissa(mantissa_norm),
								.regime(regime_norm),
								.exponent(exponent_norm)
								);

assign q = a + b;

endmodule : posit_adder

