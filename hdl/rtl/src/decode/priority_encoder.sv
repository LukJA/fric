module priority_encoder_2 (
    input  bit         leading_bit,
    input  logic [1:0] slice,

    output logic       count,
    output logic       valid
);
    always_comb begin
        if (leading_bit) begin
            valid = !(&slice);

            unique  casez (slice)
                2'b0?     :   count = 0;
                2'b10     :   count = 1;
                
                default     :   count = 0;
            endcase
        end else begin
            valid = |slice;

            unique casez (slice)
                2'b1?       :   count = 0;
                2'b01       :   count = 1;

                default     :   count = 0;
            endcase
        end
   end
endmodule : priority_encoder_2

module priority_encoder_4 (
    input  bit         leading_bit,
    input  logic [3:0] slice,

    output logic [1:0] count,
    output logic       valid
);
    always_comb begin
        // the leading bit is variable so bake it into this logic.
        if (leading_bit) begin
            // output is valid if any one bit is zero
            valid = !(&slice);

            unique  casez (slice)
                4'b0???     :   count = 0;
                4'b10??     :   count = 1;
                4'b110?     :   count = 2;
                4'b1110     :   count = 3;
                
                default     :   count = 0;
            endcase
        end
        else begin
            // output is valid if any one bit is set
            valid = |slice;

            unique  casez (slice)
                4'b1???     :   count = 0;
                4'b01??     :   count = 1;
                4'b001?     :   count = 2;
                4'b0001     :   count = 3;

                default     :   count = 0;
            endcase
        end
   end
endmodule : priority_encoder_4
