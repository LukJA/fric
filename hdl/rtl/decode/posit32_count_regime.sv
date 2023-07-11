module posit32_count_regime (
    input  bit [30:0] v,

    output integer unsigned c
);

    /* COUNT THE NUMBER OF LEADING ZEROS/ONES TO FIND THE REGIME LENGTH */

    /* see posit_variable_count_regime.sv for a detailed explanation. */

    logic [2:0] counts [5:0];
    logic valid;

    logic [3:0] intr_counts   [1:0]; // intermediate counts

    logic [2:0] intr_valids_1 [1:0]; // intermediate valids level 1
    logic [1:0] intr_select_1 [1:0]; // intermediate select level 1

    logic [1:0] intr_valids_2;       // intermediate valids level 2
    logic       intr_select_2;       // intermediate select level 2

    generate
        for (genvar i = 0; i < 2; i++) begin

            for (genvar j = 0; j < 3; j += 1) begin
                localparam tmp_idx = j + 3*i
                localparam tmp_count = 5 * tmp_idx;

                priority_encoder_5 i_priority_encoder_5 (
                    .leading_bit(v[30]),
                    .slice( v[tmp_count+4:tmp_count] ),
                    .count( counts[tmp_idx] ),
                    .valid( intr_valids_1[i][j] )
                );
            end
            
            priority_encoder_3 i_priority_encoder_3(
                .leading_bit(1'b1),
                .slice( intr_valids_1[i] ),
                .count( intr_select_1[i] ),
                .valid( intr_valids_2[i] )
            );

            localparam count_idx = 3 * i;

            mux_3_4 i_mux_3_4(
                .select( intr_select_1[i] ),

                .i0( counts[count_idx] ),
                .i1( counts[count_idx + 1] )
                .i2( counts[count_idx + 2] )

                .o( intr_counts[i] )
            )

        end

        /* FIXME: need to add modules that add the correct offsets to each
                  intermediate count (and also adjust width) */

        priority_encoder_2 i_priority_encoder_2(
            .leading_bit(1'b1),
            .slice( intr_valids_2 ),
            .count( intr_select_2 ),
            .valid( valid )
        );

        mux_3_4 i_mux_2_5(
            .select( intr_select_2 ),

            .i0( intr_counts[0] ),
            .i1( intr_counts[1] )

            .o( c )
        )

    endgenerate

endmodule