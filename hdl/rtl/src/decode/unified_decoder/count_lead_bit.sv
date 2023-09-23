// returns the unsigned integer value of the index of the first chosen bit

module count_lead_bit #(
    parameter   W_IN    = 8,
    parameter   W_OUT   = 3
) (
    input  logic [W_IN-1:0]  vec,   /* bit vector              */
    output logic [W_OUT-1:0] cnt,   /* count                   */
    output logic             valid  /* is output not all 0/1 ? */
);

// leading bit
parameter bit L_BIT = 0; // this doesn't have a default value

// we don't need users to be able to override this
parameter int CLB_IN = int'($pow(2, $clog2(W_IN)));

// we need our tree to be a power of 2 to match our tree structure
// so we pad the right hand side of our vector
logic [CLB_IN-1:0] expanded_vec;
assign expanded_vec = { vec, { (CLB_IN-W_IN) {L_BIT} } };

clb_tree_node #( .W_IN(CLB_IN), .BRANCHES(2), .L_BIT(0))
    i_clb_tree (
        .vec(expanded_vec),
        .cnt(cnt),
        .valid(valid)
    );

endmodule : count_lead_bit

module clb_tree_node #(
    parameter W_IN = 8,
    parameter BRANCHES = 2
) (
    input  logic [W_IN-1  : 0] vec,
    output logic [$clog2(W_IN)-1 : 0] cnt,
    output logic valid
);
    parameter bit L_BIT;

    generate
        if (W_IN == 2) begin
            priority_encoder_2 i_priority_encoder_2 (
                .leading_bit(L_BIT),
                .slice(vec),
                .count(cnt),
                .valid(valid)
            );
        end else if (W_IN == 4) begin
            priority_encoder_4 i_priority_encoder_4 (
                .leading_bit(L_BIT),
                .slice(vec),
                .count(cnt),
                .valid(valid)
            );
        end else begin
            parameter SUB_WIDTH = W_IN / BRANCHES;
            parameter SUB_CNT_W = $clog2(SUB_WIDTH);

            logic [SUB_CNT_W-1:0] counts [BRANCHES-1:0];
            logic [BRANCHES-1:0] valids;
            logic [$clog2(BRANCHES)-1:0] select;

            for (genvar j = 0; j < BRANCHES; j += 1) begin
                clb_tree_node #(
                    .W_IN(SUB_WIDTH),
                    .BRANCHES(BRANCHES),
                    .L_BIT(L_BIT)
                ) i_clb_tree_node (
                    .vec( vec[ (SUB_WIDTH*j) +: SUB_WIDTH ] ),
                    .cnt( counts[j] ),
                    .valid( valids[j] )
                );
            end

            if (BRANCHES == 2) begin
                priority_encoder_2 i_priority_encoder_2_valid (
                    .leading_bit( L_BIT ),
                    .slice( valids ),
                    .count( select ),
                    .valid( valid )
                );
            end else if (BRANCHES == 4) begin
                priority_encoder_4 i_priority_encoder_4_valid (
                    .leading_bit( L_BIT ),
                    .slice( valids ),
                    .count( select ),
                    .valid( valid )
                );
            end else begin
                $error("Unsupported branch structure: %d!", BRANCHES);
            end

            mux #( .WIDTH(SUB_CNT_W), .NUM_INPUTS(BRANCHES) ) i_mux(
                .sel( ~select ),
                .i( counts ),
                .o( cnt[SUB_CNT_W-1:0] )
            );

            assign cnt[SUB_CNT_W +: $clog2(BRANCHES)] = select;
        end
    endgenerate
endmodule : clb_tree_node
