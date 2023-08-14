// returns the signed integer value of the index of the first chosen bit
import common::*;

module count_lead_one #(
    parameter W_IN = 8,
    parameter W_OUT = 8,
    parameter __LEVEL = 1
) (
    input logic  [W_IN-1:0] a,
    output logic [W_OUT-1:0] q
);

generate
    if (__LEVEL == 1) begin: wrapper // TOP EXPANDER

        logic [$clog2(W_IN)-1:0] leading_ones;
        count_lead_one #(.W_IN(W_IN), .W_OUT($clog2(W_IN)), .__LEVEL(0)) clo (.a(a), .q(leading_ones));

        logic all_one;
        assign all_one = &a;
        assign q = (all_one) ? W_IN : {{W_OUT-$clog2(W_IN){1'b0}}, leading_ones};

    end else if (W_IN == 2) begin: base // BASE CASE
        always_comb begin
        case (a[1])
            1'b1    :  q = 1'b1;
            1'b0    :  q = 1'b0;
            default  :  q = 1'b0;
        endcase
        end
    end else begin  // INTERIM LEVELS
        logic [W_OUT-2:0] half_count_rhs;
        logic [W_OUT-2:0] half_count_lhs;

        logic [(W_IN/2)-1:0] lhs;
        logic [(W_IN/2)-1:0] rhs;
        logic lhs_all_one;

        assign lhs =  a[W_IN-1:(W_IN/2)];
        assign rhs =  a[(W_IN/2)-1:0];
        assign lhs_all_one = (&lhs);

        count_lead_one #(.W_IN(W_IN/2), .W_OUT($clog2(W_IN)-1), .__LEVEL(0)) inner_block_r (.a(rhs), .q(half_count_rhs));
        count_lead_one #(.W_IN(W_IN/2), .W_OUT($clog2(W_IN)-1), .__LEVEL(0)) inner_block_l (.a(lhs), .q(half_count_lhs));
        
        assign q = (lhs_all_one) ?  {1'b1, half_count_rhs} : {1'b0, half_count_lhs};
    end
endgenerate

endmodule
