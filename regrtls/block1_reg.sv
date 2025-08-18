module block1_reg
#(
    parameter int ADDR_WIDTH = 32                       ,
    parameter int DATA_WIDTH = 32
)
(
    input     reg_clk                                                           ,
    input     reg_rstn                                                          ,

  
    output logic[32-1: 0]       reg0_0_field0                                   ,
    output logic[32-1: 0]       reg0_1_field0                                   ,
    output logic[32-1: 0]       reg0_2_field0                                   ,
    output logic[32-1: 0]       reg0_3_field0                                   ,

  
    input                                  reg_wr                               ,
    input                                  reg_rd                               ,
    input       [DATA_WIDTH/8-1: 0]        reg_we                               ,
    input       [ADDR_WIDTH-1: 0]          reg_addr                             ,
    input       [DATA_WIDTH-1: 0]          reg_wdata                            ,
    output logic[DATA_WIDTH-1: 0]          reg_rdata
);

logic[DATA_WIDTH-1:0]     reg0_0;
logic[DATA_WIDTH-1:0]     reg0_1;
logic[DATA_WIDTH-1:0]     reg0_2;
logic[DATA_WIDTH-1:0]     reg0_3;

localparam int REG0_0_ADDR = 'h0;
localparam int REG0_1_ADDR = 'h4;
localparam int REG0_2_ADDR = 'h8;
localparam int REG0_3_ADDR = 'hc;


always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        reg0_0[31:0] <= 32'h0;
    end
    else if(reg_wr && (reg_addr == REG0_0_ADDR)) 
    begin
        reg0_0[31:24] <= reg_we[3] ? reg_wdata[31:24] : reg0_0[31:24];
        reg0_0[23:16] <= reg_we[2] ? reg_wdata[23:16] : reg0_0[23:16];
        reg0_0[15:8] <= reg_we[1] ? reg_wdata[15:8] : reg0_0[15:8];
        reg0_0[7:0] <= reg_we[0] ? reg_wdata[7:0] : reg0_0[7:0];
    end
end
assign reg0_0_field0 = reg0_0[31:0];



always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        reg0_1[31:0] <= 32'h0;
    end
    else if(reg_wr && (reg_addr == REG0_1_ADDR)) 
    begin
        reg0_1[31:24] <= reg_we[3] ? reg_wdata[31:24] : reg0_1[31:24];
        reg0_1[23:16] <= reg_we[2] ? reg_wdata[23:16] : reg0_1[23:16];
        reg0_1[15:8] <= reg_we[1] ? reg_wdata[15:8] : reg0_1[15:8];
        reg0_1[7:0] <= reg_we[0] ? reg_wdata[7:0] : reg0_1[7:0];
    end
end
assign reg0_1_field0 = reg0_1[31:0];



always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        reg0_2[31:0] <= 32'h0;
    end
    else if(reg_wr && (reg_addr == REG0_2_ADDR)) 
    begin
        reg0_2[31:24] <= reg_we[3] ? reg_wdata[31:24] : reg0_2[31:24];
        reg0_2[23:16] <= reg_we[2] ? reg_wdata[23:16] : reg0_2[23:16];
        reg0_2[15:8] <= reg_we[1] ? reg_wdata[15:8] : reg0_2[15:8];
        reg0_2[7:0] <= reg_we[0] ? reg_wdata[7:0] : reg0_2[7:0];
    end
end
assign reg0_2_field0 = reg0_2[31:0];



always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        reg0_3[31:0] <= 32'h0;
    end
    else if(reg_wr && (reg_addr == REG0_3_ADDR)) 
    begin
        reg0_3[31:24] <= reg_we[3] ? reg_wdata[31:24] : reg0_3[31:24];
        reg0_3[23:16] <= reg_we[2] ? reg_wdata[23:16] : reg0_3[23:16];
        reg0_3[15:8] <= reg_we[1] ? reg_wdata[15:8] : reg0_3[15:8];
        reg0_3[7:0] <= reg_we[0] ? reg_wdata[7:0] : reg0_3[7:0];
    end
end
assign reg0_3_field0 = reg0_3[31:0];




always @(posedge reg_clk or negedge reg_rstn)
begin
    if(~reg_rstn)
    begin
        reg_rdata <= {DATA_WIDTH{1'b0}};
    end
    else if (reg_rd) 
    begin
        case(reg_addr)
            REG0_0_ADDR : reg_rdata <= reg0_0;
            REG0_1_ADDR : reg_rdata <= reg0_1;
            REG0_2_ADDR : reg_rdata <= reg0_2;
            REG0_3_ADDR : reg_rdata <= reg0_3;
            default: reg_rdata <= {DATA_WIDTH{1'b0}};
        endcase
    end
    else
    begin
        reg_rdata <= {DATA_WIDTH{1'b0}};
    end
end



endmodule