import posit/posit_types::*
import alu/operations::*

module posit32_alu #(
    parameter int unsigned es = 2
) (
    input posit32_t p1, p2,
    input operations_t op,

    output posit32_t o
);

    /* Example of how maybe to construct the posit ALU/testbench?
     * We really just need to create the decode hardware for each input
     * and then the arithmetic modules can just operate on their decoded
     * intermediaries.
     */

    posit32_decode i_posit32_decode_1(
        .p(p1),
        //...
    );

    posit32_decode i_posit32_decode_2(
        .p(p1),
        //...
    );

    // ...

    // arithmetic modules (e.g. add, sub) go here

    // ...

    // this might feature a quire to posit converter or similar?

    // then finally an encoder connected to the output

endmodule