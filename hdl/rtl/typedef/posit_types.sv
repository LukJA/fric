package posit_types;

    /* handy logic type for sign bit */
    typedef enum logic { POS = 0, NEG = 1 } sign_t;

    /*
     * POSIT STRUCTURES
     * These are a bit useless because fields are variable width, but each
     * struct provides the sign bit and combined regime, exponent & fraction
     * region for both 32- and 64-bit posits.
     */

    typedef struct packed {
        sign_t s;
        logic [30:0] ref_block;
    } posit32_t;

    typedef struct packed {
        sign_t s;
        logic [62:0] ref_block;
    } posit64_t;

endpackage
