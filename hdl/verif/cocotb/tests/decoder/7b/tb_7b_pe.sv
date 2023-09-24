module tb_7b_pe (
    input  logic [6:0] vec,
    output logic [2:0] cnt,
    output logic       valid
);
    count_lead_one #(.W_IN(7)) i_clo_7b (.*);
endmodule : tb_7b_pe
