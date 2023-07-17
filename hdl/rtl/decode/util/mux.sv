module mux #(
    parameter WIDTH = 1,
    parameter NUM_INPUTS = 2, 
    localparam W_SELECT = $clog2(NUM_INPUTS)
) (
    input logic [W_SELECT-1:0] sel,

    input logic [WIDTH-1:0] i [NUM_INPUTS-1:0],                   
    output logic [WIDTH-1:0] o
);
  
  assign o = i[sel];
    
endmodule  