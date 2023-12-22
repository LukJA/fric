import common::*;

module mantissa_adder #(
    parameter int WIDTH = 7,
    parameter int EN = 1,
    // Bits required for each field (+ sign bit)
    parameter int W_REG = $clog2(WIDTH),
    parameter int W_EXP = $clog2(WIDTH),
    parameter int W_MAN = WIDTH
) (
    input  sign_t                     a_sign,     b_sign,
           logic signed   [W_REG-1:0] a_regime,   b_regime,
           logic signed   [W_EXP-1:0] a_exponent, b_exponent,
           logic unsigned [W_MAN-1:0] a_mantissa, b_mantissa,

    output logic unsigned [W_MAN-1:0] mantissa_sum,
           logic signed   [W_REG-1:0] interim_regime,
           logic signed   [W_EXP-1:0] interim_exponent,
           logic                      negate_result
);

    logic big_sign, small_sign;
    logic signed [W_REG-1:0] big_regime, small_regime;
    logic signed [W_EXP-1:0] big_exponent, small_exponent;
    logic unsigned [W_MAN-1:0] big_mantissa, small_mantissa;

    comparator #(
        .W_REG(W_REG),
        .W_EXP(W_EXP),
        .W_MAN(W_MAN)
    ) m_comp (.*);

    // collect the interim values
    assign interim_regime = big_regime;

    // calulate the necessary addition offsets
    logic signed [W_REG-1:0] shamt;
    logic signed [W_REG-1:0] delta_regime, delta_exponent;

    assign delta_regime = big_regime - small_regime;
    assign delta_exponent = big_exponent - small_exponent;
    assign shamt = (delta_regime << EN) + delta_exponent;

    // unify sign description
    // B+ S- => smaller frac is negative - TC for a subtraction
    // B- S+ => Bigger frac is negative - TC smaller and negate result
    // B- S- => Negate Answer
    // B+ S+ => Default

    // NOTE using implicit twos complement signed repr
    logic unsigned [W_MAN-1:0] small_mantissa_sh;
    logic unsigned [W_MAN-1:0] small_mantissa_sh_alt;
    // barrel shift the smaller fraction to the right
    assign small_mantissa_sh = small_mantissa >> shamt;

    logic neg_in_sum;
    always_comb begin
        // in which situations do we negate the smaller value for the binary add
        case ( {big_sign, small_sign} )
            {POS, NEG}, {NEG, POS}: neg_in_sum = 1'b1;
            default:                neg_in_sum = 1'b0;
        endcase

        // in which situations should we negate our final answer
        case ( {big_sign, small_sign} )
            {NEG, POS}, {NEG, NEG}: negate_result = 1'b1;
            default:                negate_result = 1'b0;
        endcase
    end

    logic unsigned [W_MAN-1:0] small_mantissa_sh_comp;
    two_comp #(W_MAN) small_mantissa_two_comp (
        .a(small_mantissa_sh), .q(small_mantissa_sh_comp)
    );
    
    assign small_mantissa_sh_alt = neg_in_sum ?
        small_mantissa_sh_comp : small_mantissa_sh;

    // sum the final fraction sections
    logic unsigned [W_MAN:0] s_mantissa_sum;
    logic ovf;

    // True Sum
    assign s_mantissa_sum = big_mantissa + small_mantissa_sh_alt;
    assign ovf = s_mantissa_sum[W_MAN];

    always_comb begin
        // if there was an overflow, and neither of the inputs were negative
        // the ovf bit is valid - inject it
        if (ovf & ~neg_in_sum) begin
            interim_exponent = big_exponent;
            mantissa_sum = {1'b1, {$bits(mantissa_sum) - 1{1'b0}}} | (s_mantissa_sum[W_MAN-1:0] >> 1);

        // otherwise if one of the sums was negative or
        // there was no overflow do this
        end else begin
            interim_exponent = big_exponent - 1;
            mantissa_sum = s_mantissa_sum[W_MAN-1:0];
        end
    end

endmodule : mantissa_adder
