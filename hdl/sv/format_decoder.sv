// takes a posit bus and extracts the relevant
// regions as digital signed byte values 
import common::*;

// Comb
module format_decoder #(
	parameter WIDTH=7,
    parameter EN=1)(
	input logic [WIDTH-1:0] posit,
    output sign_t sign,
	output logic signed [7:0] regime, exponent,
    output logic unsigned [7:0] mantissa
    );

logic [WIDTH-1:0] posit_comp;
logic [WIDTH-2:0] posit_reduced;

// generate complements of the inputs
two_comp #(WIDTH) input_comp (.a(posit), .q(posit_comp));

// Extract sign bit 
always_comb begin : sign_extract
    if (posit[WIDTH-1] == 0) begin
        sign = POS;
    end else begin
        sign = NEG;
    end
end
// Explicit select the positive form
assign posit_reduced = (sign==POS) ? posit[WIDTH-2:0] : posit_comp[WIDTH-2:0];

// Now the hard part - length decomposition
// find the length of the regime region
// TODO DOES NOT SUPPORT ALL_REGIME FORMATS - CANNOT COUNT ALL
// HARDCODED to 8
logic [7:0] leading_ones;
count_lead_one #( 8 ) clo (.a({posit_reduced, {8-$bits(posit_reduced){1'b0}}}), .q(leading_ones));
logic [7:0] leading_zeroes;
count_lead_zero #( 8 ) clz (.a({posit_reduced, {8-$bits(posit_reduced){1'b0}}}), .q(leading_zeroes));
logic [7:0] regime_len;
assign regime_len = (posit_reduced[WIDTH-2]==1) ? leading_ones : leading_zeroes;

logic signed [7:0] neg_reg;
logic signed [7:0] sub_reg;
two_comp #(8) regime_comp (.a(regime_len), .q(neg_reg));
assign sub_reg = regime_len - 1;
assign regime = (posit_reduced[WIDTH-2]==0) ? neg_reg : sub_reg;

// The remaining sections may or may not exist
// The logic here is a bit dodgy
// we are extracting region lengths, and then 'muxing' the outputs using them as indices
// how about generating a mask, and then doing the realignment as a mux :)
logic unsigned [7:0] rem_bits;
logic unsigned [7:0] exp_len;
logic unsigned [7:0] man_len;
assign rem_bits = (WIDTH-2) - regime_len;
assign exp_len = (rem_bits < EN) ? rem_bits : EN;
assign man_len = rem_bits - exp_len;



`ifdef COCOTB_SIM
initial begin
  $dumpfile ("x.vcd");
  $dumpvars (0, format_decoder);
  #1;
end
`endif 

endmodule : format_decoder
