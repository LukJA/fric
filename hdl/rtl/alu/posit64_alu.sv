import posit/posit_types::*
import alu/operations::*

module posit64_alu #(
    parameter int unsigned es = 2
) (
    input posit64_t p1, p2,
    input operations_t op,

    output posit64_t o
);

    posit32_decode i_posit64_decode_1(
        .p(p1),
        //...
    );

    posit32_decode i_posit64_decode_2(
        .p(p1),
        //...
    );

endmodule