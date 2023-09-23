module count_tail_zero #(
    parameter W_IN = 8,
    parameter W_OUT = 8
) (
    input logic  [W_IN-1:0] a,
    output logic [W_OUT-1:0] q
);

logic  [W_IN-1:0] a_bar;

// reverse input vector
for(genvar i=0; i<W_IN; i=i+1)
begin 
    assign a_bar[i] = a[W_IN-i-1];
end

count_lead_zero #(W_IN, W_OUT) mod_clz (.a(a_bar), .q(q));

endmodule
