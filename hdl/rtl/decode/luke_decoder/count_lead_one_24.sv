module count_lead_one_24 #(
    parameter int W_IN = 24,
    parameter int W_OUT = 8
) (
    input logic  [W_IN-1:0] a,
    output logic [W_OUT-1:0] q
);

count_lead_one #(W_IN, W_OUT) clo (.a(a), .q(q));

endmodule : count_lead_one_24
