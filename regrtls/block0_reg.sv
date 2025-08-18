module block0_reg
#(
    parameter int ADDR_WIDTH = 32                       ,
    parameter int DATA_WIDTH = 32
)
(
    input     reg_clk                                                           ,
    input     reg_rstn                                                          ,

  
    output logic[ 5-1: 0]       field 1                                         ,
    output logic[ 3-1: 0]       field 0                                         ,
    output logic[ 8-1: 0]       field 0                                         ,
    output logic[16-1: 0]       field2                                          ,
    output logic[ 8-1: 0]       field0                                          ,

  
    input                                  reg_wr                               ,
    input                                  reg_rd                               ,
    input       [DATA_WIDTH/8-1: 0]        reg_we                               ,
    input       [ADDR_WIDTH-1: 0]          reg_addr                             ,
    input       [DATA_WIDTH-1: 0]          reg_wdata                            ,
    output logic[DATA_WIDTH-1: 0]          reg_rdata
);

logic[DATA_WIDTH-1:0]     reg0;
logic[DATA_WIDTH-1:0]     reg1;
logic[DATA_WIDTH-1:0]     reg2;

localparam int REG0_ADDR = 'h0;
localparam int REG1_ADDR = 'h4;
localparam int REG2_ADDR = 'h8;


always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        reg0[7:3] <= 5'h0;
        reg0[2:0] <= 3'h1;
    end
    else if(reg_wr && (reg_addr == REG0_ADDR)) 
    begin
        reg0[7:3] <= reg_we[0] ? reg_wdata[7:3] : reg0[7:3];
        reg0[2:0] <= reg_we[0] ? reg_wdata[2:0] : reg0[2:0];
    end
end
assign field 1 = reg0[7:3];
assign field 0 = reg0[2:0];



always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        reg1[7:0] <= 8'h0;
    end
    else if(reg_wr && (reg_addr == REG1_ADDR)) 
    begin
        reg1[7:0] <= reg_we[0] ? reg_wdata[7:0] : reg1[7:0];
    end
end
assign field 0 = reg1[7:0];



always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        reg2[31:16] <= 16'h0;
        reg2[7:0] <= 8'h0;
    end
    else if(reg_wr && (reg_addr == REG2_ADDR)) 
    begin
        reg2[31:24] <= reg_we[3] ? reg_wdata[31:24] : reg2[31:24];
        reg2[23:16] <= reg_we[2] ? reg_wdata[23:16] : reg2[23:16];
        reg2[7:0] <= reg_we[0] ? reg_wdata[7:0] : reg2[7:0];
    end
end
assign field2 = reg2[31:16];
assign field0 = reg2[7:0];
assign reg2[15:8] = 8'd0;




always @(posedge reg_clk or negedge reg_rstn)
begin
    if(~reg_rstn)
    begin
        reg_rdata <= {DATA_WIDTH{1'b0}};
    end
    else if (reg_rd) 
    begin
        case(reg_addr)
            REG0_ADDR : reg_rdata <= reg0;
            REG1_ADDR : reg_rdata <= reg1;
            REG2_ADDR : reg_rdata <= reg2;
            default: reg_rdata <= {DATA_WIDTH{1'b0}};
        endcase
    end
    else
    begin
        reg_rdata <= {DATA_WIDTH{1'b0}};
    end
end



endmodule