// returns the signed integer value of the index of the first chosen bit

module clz_internal #(
    parameter W_IN = 8,
    parameter W_OUT = 8
) (
    input logic  [W_IN-1:0] a,
    output logic [W_OUT-1:0] q
);

generate
    if (W_IN == 2) begin: base
        always_comb begin
        case (a[1])
            1'b0    :  q = 1'b1;
            1'b1    :  q = 1'b0;
            default  :  q = 1'b0;
        endcase
        end
    end else begin 
        logic [W_OUT-2:0] half_count_rhs;
        logic [W_OUT-2:0] half_count_lhs;

        logic [(W_IN/2)-1:0] lhs;
        logic [(W_IN/2)-1:0] rhs;
        logic lhs_all_zero;
        logic all_zero;

        assign lhs =  a[W_IN-1:(W_IN/2)];
        assign rhs =  a[(W_IN/2)-1:0];
        assign lhs_all_zero = ~(|lhs);

        clz_internal #(.W_IN(W_IN/2), .W_OUT($clog2(W_IN)-1)) inner_block_r (.a(rhs), .q(half_count_rhs));
        clz_internal #(.W_IN(W_IN/2), .W_OUT($clog2(W_IN)-1)) inner_block_l (.a(lhs), .q(half_count_lhs));

        assign q = (lhs_all_zero) ?  {1'b1, half_count_rhs} : {1'b0, half_count_lhs};
    end
endgenerate

endmodule


module count_lead_zero #(
    parameter W_IN = 8,
    parameter W_OUT = 8,
    parameter int CLO_IN = int'($pow(2, $clog2(W_IN)))
) (
    input logic  [W_IN-1:0] a,
    output logic [W_OUT-1:0] q
);

// expand input
logic [CLO_IN-1:0] expanded_a;
assign expanded_a = {a, {CLO_IN-W_IN{1'b0}}};

// create the ideal tree structure
logic [$clog2(W_IN)-1:0] leading_zeroes;
clz_internal #(.W_IN(CLO_IN), .W_OUT($clog2(W_IN))) clz (.a(expanded_a), .q(leading_zeroes));

logic all_zero;
assign all_zero = ~(|expanded_a);
assign q = (all_zero) ? W_IN : {{(W_OUT-$bits(leading_zeroes)){1'b0}}, leading_zeroes};

endmodule
