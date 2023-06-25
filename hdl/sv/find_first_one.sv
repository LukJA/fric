// returns the input with only the MSB 1 set
import common::*;

module find_first_one #(
    parameter W = 8
) (
    input logic  [W-1:0] a,
    output logic [W-1:0] q
);

assign q[W-1] =  a[W-1];

generate
    genvar i;
    for (i = W-2; i >= 0; i--) begin
        assign q[i] = a[i] & (~a[i+1]);
    end
endgenerate

endmodule : find_first_one
