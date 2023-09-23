// returns the input with only the MSB 1 set
`include "common.svh"

import common::*;

module find_first_n_ones #(
    parameter W = 8,
    parameter N = 2
) (
    input logic  [W-1:0] a,
    output logic [W-1:0] q
);

    // The following blocks verilator from optimizing the loopy signal
    /* verilator lint_off UNOPTFLAT */ 
    logic [W-1:0] intermediary [N-1:0];
    logic [W-1:0] ones [N-1:0];

    find_first_one #(W) en0 (.a(a), .q(ones[0]) );
    assign intermediary[0] = a & (~ones[0]);

    genvar i;
    generate
        for (i=1; i<N; i++) begin : secondaries 
            find_first_one #(W) enx (
                .a(intermediary[i-1]), .q(ones[i])
            );
            assign intermediary[i] = intermediary[i-1] & (~ones[i]);
        end 
    endgenerate

    always_comb 
        q = ones.or();

endmodule : find_first_n_ones
