import common::*;

module normalise #(
	parameter WIDTH=7,
    parameter EN=1)(
    input logic signed [7:0] mantissa_sum,
    input logic signed [7:0] interim_regime, interim_exponent,
    output logic signed [7:0] mantissa,
    output logic signed [7:0] regime, exponent
    );

// get normalisation counts
logic signed [7:0] normz;
count_lead_zero #(8,8) mant_ffo (.a(mantissa_sum), .q(normz));

// barrell shift to the correct leading 1 
// this maybe a crit path but we need to CLO anyway - consider a concurrent selecting mux
logic signed [7:0] mantissa_lo;
assign mantissa_lo = mantissa_sum << (normz + 1'b1);

// do the re regime and re exponent 
logic signed [7:0] a_regime, a_exponent;
assign a_exponent = exponent + 1'b1 - normz;
// for a too big exponent:
// - allowed bits equals es - so shift is the position of the first 1 minus es
// for a negative exponent:
// -  shift up until its positive

logic signed [7:0] b_regime, b_exponent;

// three way effect 
// always_comb
// begin
//     // for a too big exponent
//     if (a_exponent >= 2**EN) begin
//         mantissa = 'b0;
//     // for a negative exponent
//     end else if (a_exponent <= 0) begin 
//         mantissa = 'b0;
//     end else begin
//         mantissa = 'b0;
//     end
// end

always_comb
begin
    // if all zeros we have the special == 0 case
    if (&(~mantissa_sum) == 1'b1) begin
        mantissa = 'b0;
        exponent = 'b0;
        regime = {1'b1, 7'b0};
    // otherwise feed forward the computed values
    end else begin
        mantissa = 'b0;
        exponent = 'b0;
        regime = {1'b1, 7'b0};
    end
end

endmodule : normalise

