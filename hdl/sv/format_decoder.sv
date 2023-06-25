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
// find the length of the regime region and convert it to a regime value
logic [7:0] leading_ones;
count_lead_one #(8,8) clo (.a({posit_reduced, {8-$bits(posit_reduced){1'b0}}}), .q(leading_ones));
logic [7:0] leading_zeroes;
count_lead_zero #(8,8) clz (.a({posit_reduced, {8-$bits(posit_reduced){1'b0}}}), .q(leading_zeroes));
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

// Step 1: Create a regime region MSB mask 
/* verilator lint_off UNOPTFLAT */ 
logic [WIDTH-2:0] r_mask;
logic [WIDTH-2:0] r_unmask;
assign r_mask[WIDTH-2] = 1'b1; // first bit is always part of the regime
assign r_unmask = ~r_mask;
generate
    genvar i;
    for (i = WIDTH-3; i >= 0; i--) begin
        assign r_mask[i] = r_mask[i+1] & (posit_reduced[i+1] == posit_reduced[i]);
    end
endgenerate
// Step 2: split the remainder mask into nought, exp, and fraction masks
logic [WIDTH-2:0] nought_mask;
logic [WIDTH-2:0] exp_mask;
logic [WIDTH-2:0] frac_mask;

// Nought is the first 1 that appears
// set only the first 1 in its mask 
find_first_one #(WIDTH-1) ffo_nought (.a(r_unmask), .q(nought_mask));
// exp is the next #EN ones:
find_first_n_ones #(WIDTH-1, EN) ffnx (.a(r_unmask & ~nought_mask), .q(exp_mask));
// finally the fraction is just the remaining mask
assign frac_mask = r_unmask & (~nought_mask) & (~exp_mask);

// `ifdef COCOTB_SIM
// initial begin
//   $dumpfile ("x.vcd");
//   $dumpvars (0, format_decoder);
//   #1;
// end
// `endif 

endmodule : format_decoder
