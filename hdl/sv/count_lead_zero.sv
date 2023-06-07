// returns the signed integer value of the index of the first chosen bit
import common::*;

module count_lead_zero #(
    parameter W_IN = 8,
    parameter W_OUT = 8,
    parameter __LEVEL = 1
) (
    input logic  [W_IN-1:0] a,
    output logic [W_OUT-1:0] q
);

generate
    if (__LEVEL == 1) begin: wrapper

        logic [$clog2(W_IN)-1:0] leading_zeroes;
        count_lead_zero #(.W_IN(W_IN), .W_OUT($clog2(W_IN)), .__LEVEL(0)) clo (.a(a), .q(leading_zeroes));

        logic all_zero;
        assign all_zero = ~(|a);
        assign q = (all_zero) ? W_IN : leading_zeroes;

    end else if (W_IN == 2) begin: base
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

        count_lead_zero #(.W_IN(W_IN/2), .W_OUT($clog2(W_IN)-1), .__LEVEL(0)) inner_block_r (.a(rhs), .q(half_count_rhs));
        count_lead_zero #(.W_IN(W_IN/2), .W_OUT($clog2(W_IN)-1), .__LEVEL(0)) inner_block_l (.a(lhs), .q(half_count_lhs));

        assign q = (lhs_all_zero) ?  {1'b1, half_count_rhs} : {1'b0, half_count_lhs};
    end
endgenerate

endmodule
