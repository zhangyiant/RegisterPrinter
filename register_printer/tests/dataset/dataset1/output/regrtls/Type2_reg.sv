module Type2_reg
#(
    parameter int ADDR_WIDTH = 24
)
(
    input     reg_clk                                                       ,
    input     reg_rstn                                                      ,
    input     wp_dis                                                        ,
    output logic[ 2: 0]     Field2                                          ,
    output logic[ 6: 0]     Field2                                          ,
    output logic[ 3: 0]     Field3                                          ,
    input                   reg_wr                                          ,
    input                   reg_rd                                          ,
    input       [ 3: 0]     reg_we                                          ,
    input[ADDR_WIDTH-1:0]   reg_addr                                        ,
    input       [31: 0]     reg_wdat                                        ,
    output logic[31: 0]     reg_rdat
);

logic[31:0]     reg1;
logic[31:0]     reg2;

localparam int REG1_ADDR = 'h0;
localparam int REG2_ADDR = 'h8;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        reg1[10: 8] <= 'h1;
    end
    else begin
        reg1[10:8] <= (reg_wr && reg_addr == REG1_ADDR && reg_we[1]) ? reg_wdat[10:8] : reg1[10:8];
    end
end
assign Field2 = reg1[10:8];
assign reg1[7:1] = 'h0;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        reg2[ 7: 1] <= 'h1;
        reg2[12: 9] <= 'h1;
    end
    else begin
        reg2[7:1] <= (reg_wr && reg_addr == REG2_ADDR && reg_we[0]) ? reg_wdat[7:1] : reg2[7:1];
        reg2[12:9] <= (reg_wr && reg_addr == REG2_ADDR && reg_we[1]) ? reg_wdat[12:9] : reg2[12:9];
    end
end
assign Field2 = reg2[7:1];
assign Field3 = reg2[12:9];



always @(negedge reg_rstn or posedge reg_clk) begin
    if (~reg_rstn) begin
        reg_rdat <= 32'h0;
    end
    else if (reg_rd) begin
        case(reg_addr)
        REG1_ADDR                                        : reg_rdat <= reg1;
        REG2_ADDR                                        : reg_rdat <= reg2;
        default: reg_rdat <= 32'h0;
        endcase
    end
    else begin
       reg_rdat <= 32'h0;
    end
end

endmodule