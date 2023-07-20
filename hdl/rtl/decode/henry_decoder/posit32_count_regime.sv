import posit_types::*;

module count_regime_16 (
    input  logic leading_bit,
    input  logic [15:0] i,

    output logic [3:0] c,
    output logic valid
);

    logic [1:0] counts [3:0];
    logic [3:0] valids;
    logic [1:0] select;

    generate
        for (genvar j = 0; j < 4; j += 1) begin
            priority_encoder_4 i_priority_encoder_4 (
                .leading_bit( leading_bit ),
                .slice( i[ (4*j) +: 4 ] ),
                .count( counts[j] ),
                .valid( valids[j] )
            );
        end

        priority_encoder_4 i_priority_encoder_4_valid (
            .leading_bit( 1'b0 ),
            .slice( valids ),
            .count( select ),
            .valid( valid )
        );

        mux #( .WIDTH(2), .NUM_INPUTS(4) ) i_mux(
            .sel( ~select ),
            .i( counts ),
            .o( c[1:0] )
        );
    endgenerate   

    assign c[3:2] = select;

endmodule

module posit32_count_regime (
    input  posit32_t i,

    output logic [4:0] c,
    output logic valid
);

    /* COUNT THE NUMBER OF LEADING ZEROS/ONES TO FIND THE REGIME LENGTH */

    /* see posit_variable_count_regime.sv for a detailed explanation. */

    logic leading_bit;
    logic [31:0] intr_v; // intermediate 32b vector

    logic [1:0] valids;
    logic [3:0] counts [1:0];
    logic select;

    // basically sign extend by 1 bit
    assign intr_v[31:1] = i.ref_block;
    assign intr_v[0] = i.ref_block[30];

    /* we can't use recursive statement because verilator is a pain, so instead
       we construct a balanced mux tree from sets of pre-defined priority
       encoders */
    /* our tree looks like this:

        ---4---[PE]--2--[   bit   ]
        ---4---[PE]--2--[ shift + ]--4--+
        ---4---[PE]--2--[  4-way  ]     |
        ---4---[PE]--2--[   mux   ]     +--[ bit shift + ]
                                           [    2-way    ]---5---
        ---4---[PE]--2--[   bit   ]     +--[     mux     ]
        ---4---[PE]--2--[ shift + ]     |
        ---4---[PE]--2--[  4-way  ]--4--+
        ---4---[PE]--2--[   mux   ]

       where the muxes are selected through priority encoding of valid bits.

       Each of the 16-bit halves are instances of count_regime_16,
       which handles any nested PE generation as well as offsetting the output
       of each PE to account for its position within the 16b slice.
     */
    generate
        for (genvar j = 0; j < 2; j++) begin

            count_regime_16 i_count_regime_16(
                .leading_bit( intr_v[31] ),
                .i( intr_v[ (16*j) +: 16 ] ),
                .c( counts[j] ),
                .valid( valids[j] )
            );

        end

        priority_encoder_2 i_priority_encoder_2 (
            .slice( valids ),
            .count( select ),
            .valid( valid )
        );

        mux #( .WIDTH(4), .NUM_INPUTS(2) ) i_mux_2(
            .sel( ~select ),
            .i( counts ),
            .o( c[3:0] )
        );

    endgenerate

    assign c[4] = select;

endmodule
