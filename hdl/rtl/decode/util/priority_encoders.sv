module priority_encoder_2 (
    input  bit       leading_bit,
    input  bit [1:0] slice,

    output bit       count,
    output bit       valid
);
    always_comb begin
        // the leading bit is variable so bake it into this logic.
        if (leading_bit) begin
            // output is valid if any one bit is zero
            valid = !(&slice);

            case (slice)
                2'b1x       :   count = 1;
                default     :   count = 0;
            endcase
        end
        else begin
            // output is valid if any one bit is set
            valid = |slice;

            case (slice)
                2'b0x       :   count = 1;
                default     :   count = 0;
            endcase
        end
   end
endmodule

module priority_encoder_3 (
    input  bit       leading_bit,
    input  bit [2:0] slice,

    output bit [1:0] count,
    output bit       valid
);
    always_comb begin
        // the leading bit is variable so bake it into this logic.
        if (leading_bit) begin
            // output is valid if any one bit is zero
            valid = !(&slice);

            case (slice)
                3'b1xx      :   count = 2;
                3'b01x      :   count = 1;
                default     :   count = 0;
            endcase
        end
        else begin
            // output is valid if any one bit is set
            valid = |slice;

            case (slice)
                3'b0xx      :   count = 2;
                3'b10x      :   count = 1;
                default     :   count = 0;
            endcase
        end
   end
endmodule

module priority_encoder_5 (
    input  bit       leading_bit,
    input  bit [4:0] slice,

    output bit [2:0] count,
    output bit       valid
);
    always_comb begin
        // the leading bit is variable so bake it into this logic.
        if (leading_bit) begin
            // output is valid if any one bit is zero
            valid = !(&slice);

            case (slice)
                5'b0xxxx    :   count = 4;
                5'b10xxx    :   count = 3;
                5'b110xx    :   count = 2;
                5'b1110x    :   count = 1;
                default     :   count = 0;
            endcase
        end
        else begin
            // output is valid if any one bit is set
            valid = |slice;

            case (slice)
                5'b1xxxx    :   count = 4;
                5'b01xxx    :   count = 3;
                5'b001xx    :   count = 2;
                5'b0001x    :   count = 1;
                default     :   count = 0;
            endcase
        end
   end
endmodule
