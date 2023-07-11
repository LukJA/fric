module mux_2_5 (
    input  bit [4:0]
        i0, i1, // 2x input
        o,      // 1x output

    input bit select
);
    /* 2-WAY 5-BIT MUX */

    assign o = select ? i2 : i1;

endmodule

module mux_3_4 (
    input  bit [3:0]
        i0, i1, i2, // 3x input
        o,          // 1x output

    input bit [1:0] select
);
    /* 3-WAY 4-BIT MUX */

    always_comb begin
        case (select) begin
            0: o = i0,
            1: o = i1,
            2: o = i2,
            3: o = 4'bxxxx
        end
    end
    
endmodule

