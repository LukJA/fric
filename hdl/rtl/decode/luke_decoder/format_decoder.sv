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

// debug signals
logic [WIDTH-2:0] nought_masked;
logic [WIDTH-2:0] exp_masked;
logic [WIDTH-2:0] frac_masked;
assign nought_masked = nought_mask & posit_reduced;
assign frac_masked = frac_mask & posit_reduced;
assign exp_masked = exp_mask & posit_reduced;

// Both the fraction and the exponent require alignment
// This is done with explicit generation of every version, and a muxing
// selection of the correct desired position based on a MSB/LSB bit flag
// This is likely faster than a CLO/CLZ tree and a barrell shifter

// the fraction is missing it's leading 1 that signifies the point location
// and needs to be aligned to the MSB, as it is right-expanding

// create an MSB+1 bit identifier
logic [WIDTH-2:0] frac_MSB_bit;
assign frac_MSB_bit[WIDTH-2] = frac_mask[WIDTH-2];
genvar k;
for (k = WIDTH-3; k >= 0; k--)
    assign frac_MSB_bit[k] = (frac_mask[k] & ~frac_mask[k+1]);

// Now generate all shifted versions of the frac region and select the right one
logic [WIDTH-2:0] frac_shifted_array [WIDTH-2:0];
logic [2*WIDTH-2:0] extended_f;
assign extended_f =  {frac_mask & posit_reduced, {WIDTH{1'b0}}};
genvar m;
for (m = 0; m <= WIDTH-2; m++)
    assign frac_shifted_array[m] = (frac_MSB_bit[m]==1'b1) ? extended_f[m+WIDTH:m+2] : 'b0;

always_comb 
    mantissa = {1'b1, frac_shifted_array.or(), {9-WIDTH-1{1'b0}}};

// The exponent needs to be correctly shifted to remove trailing zeroes but 
// can be right aligned as a valid whole number value

// create a LSB bit identifier
logic [WIDTH-2:0] exp_LSB_bit;
assign exp_LSB_bit[0] = exp_mask[0];
genvar j;
for (j = 1; j <= WIDTH-2; j++)
    assign exp_LSB_bit[j] = (exp_mask[j] & ~exp_mask[j-1]);

// Now generate all shifted versions of the exp region and select the right one
logic [2*WIDTH-2:0] extended_e;
assign extended_e =  {{WIDTH{1'b0}}, exp_mask & posit_reduced};
logic [WIDTH-2:0] exp_shifted_array [WIDTH-2:0];
genvar l;
for (l = 0; l <= WIDTH-2; l++)
    assign exp_shifted_array[l] = (exp_LSB_bit[l]==1'b1) ? extended_e[WIDTH-2+l:l] : 'b0;

always_comb 
    exponent = {{9-WIDTH{1'b0}}, exp_shifted_array.or()};

endmodule

