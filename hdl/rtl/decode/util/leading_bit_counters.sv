module leading_bit_counter_2 #(
    parameter bit leading
) (
    input  bit       leading_bit,
    input  bit [1:0] slice,
    output bit [1:0] count
)

    always_comb begin
        // the leading bit is variable so bake it into this logic.
        if (leading_bit) begin
            case (slice)
                2'b11       :  count = 2'b10;
                2'b10       :  count = 2'b01;
                default     :  count = 2'b00;
            endcase
        end
        else begin
            case (slice)
                2'b00       :  count = 2'b10;
                2'b01       :  count = 2'b01;
                default     :  count = 2'b00;
            endcase
        end
   end
endmodule

module leading_bit_counter_4 #(
    parameter bit leading
) (
    input  bit       leading_bit,
    input  bit [3:0] slice,
    output bit [2:0] count
)

    always_comb begin
        // the leading bit is variable so bake it into this logic.
        if (leading_bit) begin
            case (slice)
                4'b1111     :  count = 3'b100;
                4'b1110     :  count = 3'b011;
                4'b1100     :  count = 3'b010;
                4'b1000     :  count = 3'b001;
                default     :  count = 3'b000;
            endcase
        end
        else begin
            case (slice)
                4'b0000     :  count = 3'b100;
                4'b0001     :  count = 3'b011;
                4'b0011     :  count = 3'b010;
                4'b0111     :  count = 3'b001;
                default     :  count = 3'b000;
            endcase
        end
   end
endmodule
