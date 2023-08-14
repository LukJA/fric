package alu_ctrl;
    typedef enum logic[3:0] { // FIXME: change width?
        NOP,
        ADD,
        SUB
    } operations_t;
endpackage