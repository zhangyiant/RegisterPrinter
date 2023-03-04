module Type1_reg
#(
    parameter int ADDR_WIDTH = 12
)
(
    input     reg_clk                                                       ,
    input     reg_rstn                                                      ,
    input     wp_dis                                                        ,
    output logic[ 6: 0]     Field1                                          ,
    output logic[ 2: 0]     Field2                                          ,
    output logic[ 6: 0]     Field2                                          ,
    output logic[ 3: 0]     Field3                                          ,
    input       [ 3: 0]     REG_A1_0_Field4                                 ,
    output logic[10: 0]     REG_A1_0_Field5                                 ,
    input       [ 3: 0]     REG_A1_1_Field4                                 ,
    output logic[10: 0]     REG_A1_1_Field5                                 ,
    input       [ 3: 0]     REG_A1_2_Field4                                 ,
    output logic[10: 0]     REG_A1_2_Field5                                 ,
    input       [ 3: 0]     REG_A1_3_Field4                                 ,
    output logic[10: 0]     REG_A1_3_Field5                                 ,
    input       [ 3: 0]     REG_A1_4_Field4                                 ,
    output logic[10: 0]     REG_A1_4_Field5                                 ,
    input       [ 3: 0]     REG_A1_5_Field4                                 ,
    output logic[10: 0]     REG_A1_5_Field5                                 ,
    input       [ 3: 0]     REG_A1_6_Field4                                 ,
    output logic[10: 0]     REG_A1_6_Field5                                 ,
    input       [ 3: 0]     REG_A1_7_Field4                                 ,
    output logic[10: 0]     REG_A1_7_Field5                                 ,
    input       [ 3: 0]     REG_A1_8_Field4                                 ,
    output logic[10: 0]     REG_A1_8_Field5                                 ,
    input       [ 3: 0]     REG_A1_9_Field4                                 ,
    output logic[10: 0]     REG_A1_9_Field5                                 ,
    input       [ 3: 0]     REG_A1_10_Field4                                ,
    output logic[10: 0]     REG_A1_10_Field5                                ,
    input       [ 3: 0]     REG_A1_11_Field4                                ,
    output logic[10: 0]     REG_A1_11_Field5                                ,
    input       [ 3: 0]     REG_A1_12_Field4                                ,
    output logic[10: 0]     REG_A1_12_Field5                                ,
    input       [ 3: 0]     REG_A1_13_Field4                                ,
    output logic[10: 0]     REG_A1_13_Field5                                ,
    input       [ 3: 0]     REG_A1_14_Field4                                ,
    output logic[10: 0]     REG_A1_14_Field5                                ,
    input       [ 3: 0]     REG_A1_15_Field4                                ,
    output logic[10: 0]     REG_A1_15_Field5                                ,
    output logic[10: 0]     REG_A2_0_Field6                                 ,
    output logic[20: 0]     REG_A2_0_Field7                                 ,
    output logic[ 3: 0]     reg_a3_0_Field9                                 ,
    output logic[10: 0]     REG_A2_1_Field6                                 ,
    output logic[20: 0]     REG_A2_1_Field7                                 ,
    output logic[ 3: 0]     reg_a3_1_Field9                                 ,
    output logic[10: 0]     REG_A2_2_Field6                                 ,
    output logic[20: 0]     REG_A2_2_Field7                                 ,
    output logic[ 3: 0]     reg_a3_2_Field9                                 ,
    output logic[10: 0]     REG_A2_3_Field6                                 ,
    output logic[20: 0]     REG_A2_3_Field7                                 ,
    output logic[ 3: 0]     reg_a3_3_Field9                                 ,
    output logic[10: 0]     Field9                                          ,
    input                   reg_wr                                          ,
    input                   reg_rd                                          ,
    input       [ 3: 0]     reg_we                                          ,
    input[ADDR_WIDTH-1:0]   reg_addr                                        ,
    input       [31: 0]     reg_wdat                                        ,
    output logic[31: 0]     reg_rdat
);

logic[31:0]     reg1;
logic[31:0]     reg2;
logic[31:0]     REG_A1_0;
logic[31:0]     REG_A1_1;
logic[31:0]     REG_A1_2;
logic[31:0]     REG_A1_3;
logic[31:0]     REG_A1_4;
logic[31:0]     REG_A1_5;
logic[31:0]     REG_A1_6;
logic[31:0]     REG_A1_7;
logic[31:0]     REG_A1_8;
logic[31:0]     REG_A1_9;
logic[31:0]     REG_A1_10;
logic[31:0]     REG_A1_11;
logic[31:0]     REG_A1_12;
logic[31:0]     REG_A1_13;
logic[31:0]     REG_A1_14;
logic[31:0]     REG_A1_15;
logic[31:0]     REG_A2_0;
logic[31:0]     reg_a3_0;
logic[31:0]     REG_A2_1;
logic[31:0]     reg_a3_1;
logic[31:0]     REG_A2_2;
logic[31:0]     reg_a3_2;
logic[31:0]     REG_A2_3;
logic[31:0]     reg_a3_3;
logic[31:0]     regtt;

localparam int REG1_ADDR = 'h0;
localparam int REG2_ADDR = 'h4;
localparam int REG_A1_0_ADDR = 'h10;
localparam int REG_A1_1_ADDR = 'h14;
localparam int REG_A1_2_ADDR = 'h18;
localparam int REG_A1_3_ADDR = 'h1c;
localparam int REG_A1_4_ADDR = 'h20;
localparam int REG_A1_5_ADDR = 'h24;
localparam int REG_A1_6_ADDR = 'h28;
localparam int REG_A1_7_ADDR = 'h2c;
localparam int REG_A1_8_ADDR = 'h30;
localparam int REG_A1_9_ADDR = 'h34;
localparam int REG_A1_10_ADDR = 'h38;
localparam int REG_A1_11_ADDR = 'h3c;
localparam int REG_A1_12_ADDR = 'h40;
localparam int REG_A1_13_ADDR = 'h44;
localparam int REG_A1_14_ADDR = 'h48;
localparam int REG_A1_15_ADDR = 'h4c;
localparam int REG_A2_0_ADDR = 'h100;
localparam int REG_A3_0_ADDR = 'h118;
localparam int REG_A2_1_ADDR = 'h120;
localparam int REG_A3_1_ADDR = 'h138;
localparam int REG_A2_2_ADDR = 'h140;
localparam int REG_A3_2_ADDR = 'h158;
localparam int REG_A2_3_ADDR = 'h160;
localparam int REG_A3_3_ADDR = 'h178;
localparam int REGTT_ADDR = 'h1a0;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        reg1[ 7: 1] <= 'h1;
        reg1[10: 8] <= 'h1;
    end
    else begin
        reg1[7:1] <= (reg_wr && reg_addr == REG1_ADDR && reg_we[0]) ? reg_wdat[7:1] : reg1[7:1];
        reg1[10:8] <= (reg_wr && reg_addr == REG1_ADDR && reg_we[1]) ? reg_wdat[10:8] : reg1[10:8];
    end
end
assign Field1 = reg1[7:1];
assign Field2 = reg1[10:8];

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

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_0[14: 4] <= 'h2;
    end
    else begin
        REG_A1_0[14:8] <= (reg_wr && reg_addr == REG_A1_0_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_0[14:8];
        REG_A1_0[7:4] <= (reg_wr && reg_addr == REG_A1_0_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_0[7:4];
    end
end
assign REG_A1_0_Field5 = REG_A1_0[14:4];
assign REG_A1_0[3:0] = REG_A1_0_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_1[14: 4] <= 'h2;
    end
    else begin
        REG_A1_1[14:8] <= (reg_wr && reg_addr == REG_A1_1_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_1[14:8];
        REG_A1_1[7:4] <= (reg_wr && reg_addr == REG_A1_1_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_1[7:4];
    end
end
assign REG_A1_1_Field5 = REG_A1_1[14:4];
assign REG_A1_1[3:0] = REG_A1_1_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_2[14: 4] <= 'h2;
    end
    else begin
        REG_A1_2[14:8] <= (reg_wr && reg_addr == REG_A1_2_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_2[14:8];
        REG_A1_2[7:4] <= (reg_wr && reg_addr == REG_A1_2_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_2[7:4];
    end
end
assign REG_A1_2_Field5 = REG_A1_2[14:4];
assign REG_A1_2[3:0] = REG_A1_2_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_3[14: 4] <= 'h2;
    end
    else begin
        REG_A1_3[14:8] <= (reg_wr && reg_addr == REG_A1_3_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_3[14:8];
        REG_A1_3[7:4] <= (reg_wr && reg_addr == REG_A1_3_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_3[7:4];
    end
end
assign REG_A1_3_Field5 = REG_A1_3[14:4];
assign REG_A1_3[3:0] = REG_A1_3_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_4[14: 4] <= 'h2;
    end
    else begin
        REG_A1_4[14:8] <= (reg_wr && reg_addr == REG_A1_4_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_4[14:8];
        REG_A1_4[7:4] <= (reg_wr && reg_addr == REG_A1_4_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_4[7:4];
    end
end
assign REG_A1_4_Field5 = REG_A1_4[14:4];
assign REG_A1_4[3:0] = REG_A1_4_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_5[14: 4] <= 'h2;
    end
    else begin
        REG_A1_5[14:8] <= (reg_wr && reg_addr == REG_A1_5_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_5[14:8];
        REG_A1_5[7:4] <= (reg_wr && reg_addr == REG_A1_5_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_5[7:4];
    end
end
assign REG_A1_5_Field5 = REG_A1_5[14:4];
assign REG_A1_5[3:0] = REG_A1_5_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_6[14: 4] <= 'h2;
    end
    else begin
        REG_A1_6[14:8] <= (reg_wr && reg_addr == REG_A1_6_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_6[14:8];
        REG_A1_6[7:4] <= (reg_wr && reg_addr == REG_A1_6_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_6[7:4];
    end
end
assign REG_A1_6_Field5 = REG_A1_6[14:4];
assign REG_A1_6[3:0] = REG_A1_6_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_7[14: 4] <= 'h2;
    end
    else begin
        REG_A1_7[14:8] <= (reg_wr && reg_addr == REG_A1_7_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_7[14:8];
        REG_A1_7[7:4] <= (reg_wr && reg_addr == REG_A1_7_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_7[7:4];
    end
end
assign REG_A1_7_Field5 = REG_A1_7[14:4];
assign REG_A1_7[3:0] = REG_A1_7_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_8[14: 4] <= 'h2;
    end
    else begin
        REG_A1_8[14:8] <= (reg_wr && reg_addr == REG_A1_8_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_8[14:8];
        REG_A1_8[7:4] <= (reg_wr && reg_addr == REG_A1_8_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_8[7:4];
    end
end
assign REG_A1_8_Field5 = REG_A1_8[14:4];
assign REG_A1_8[3:0] = REG_A1_8_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_9[14: 4] <= 'h2;
    end
    else begin
        REG_A1_9[14:8] <= (reg_wr && reg_addr == REG_A1_9_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_9[14:8];
        REG_A1_9[7:4] <= (reg_wr && reg_addr == REG_A1_9_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_9[7:4];
    end
end
assign REG_A1_9_Field5 = REG_A1_9[14:4];
assign REG_A1_9[3:0] = REG_A1_9_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_10[14: 4] <= 'h2;
    end
    else begin
        REG_A1_10[14:8] <= (reg_wr && reg_addr == REG_A1_10_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_10[14:8];
        REG_A1_10[7:4] <= (reg_wr && reg_addr == REG_A1_10_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_10[7:4];
    end
end
assign REG_A1_10_Field5 = REG_A1_10[14:4];
assign REG_A1_10[3:0] = REG_A1_10_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_11[14: 4] <= 'h2;
    end
    else begin
        REG_A1_11[14:8] <= (reg_wr && reg_addr == REG_A1_11_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_11[14:8];
        REG_A1_11[7:4] <= (reg_wr && reg_addr == REG_A1_11_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_11[7:4];
    end
end
assign REG_A1_11_Field5 = REG_A1_11[14:4];
assign REG_A1_11[3:0] = REG_A1_11_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_12[14: 4] <= 'h2;
    end
    else begin
        REG_A1_12[14:8] <= (reg_wr && reg_addr == REG_A1_12_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_12[14:8];
        REG_A1_12[7:4] <= (reg_wr && reg_addr == REG_A1_12_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_12[7:4];
    end
end
assign REG_A1_12_Field5 = REG_A1_12[14:4];
assign REG_A1_12[3:0] = REG_A1_12_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_13[14: 4] <= 'h2;
    end
    else begin
        REG_A1_13[14:8] <= (reg_wr && reg_addr == REG_A1_13_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_13[14:8];
        REG_A1_13[7:4] <= (reg_wr && reg_addr == REG_A1_13_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_13[7:4];
    end
end
assign REG_A1_13_Field5 = REG_A1_13[14:4];
assign REG_A1_13[3:0] = REG_A1_13_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_14[14: 4] <= 'h2;
    end
    else begin
        REG_A1_14[14:8] <= (reg_wr && reg_addr == REG_A1_14_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_14[14:8];
        REG_A1_14[7:4] <= (reg_wr && reg_addr == REG_A1_14_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_14[7:4];
    end
end
assign REG_A1_14_Field5 = REG_A1_14[14:4];
assign REG_A1_14[3:0] = REG_A1_14_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A1_15[14: 4] <= 'h2;
    end
    else begin
        REG_A1_15[14:8] <= (reg_wr && reg_addr == REG_A1_15_ADDR && reg_we[1]) ? reg_wdat[14:8] : REG_A1_15[14:8];
        REG_A1_15[7:4] <= (reg_wr && reg_addr == REG_A1_15_ADDR && reg_we[0]) ? reg_wdat[7:4] : REG_A1_15[7:4];
    end
end
assign REG_A1_15_Field5 = REG_A1_15[14:4];
assign REG_A1_15[3:0] = REG_A1_15_Field4;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A2_0[10: 0] <= 'h4;
        REG_A2_0[31:11] <= 'h4;
    end
    else begin
        REG_A2_0[10:8] <= (reg_wr && reg_addr == REG_A2_0_ADDR && reg_we[1]) ? reg_wdat[10:8] : REG_A2_0[10:8];
        REG_A2_0[7:0] <= (reg_wr && reg_addr == REG_A2_0_ADDR && reg_we[0]) ? reg_wdat[7:0] : REG_A2_0[7:0];
        REG_A2_0[31:24] <= (reg_wr && reg_addr == REG_A2_0_ADDR && reg_we[3]) ? reg_wdat[31:24] : REG_A2_0[31:24];
        REG_A2_0[23:16] <= (reg_wr && reg_addr == REG_A2_0_ADDR && reg_we[2]) ? reg_wdat[23:16] : REG_A2_0[23:16];
        REG_A2_0[15:11] <= (reg_wr && reg_addr == REG_A2_0_ADDR && reg_we[1]) ? reg_wdat[15:11] : REG_A2_0[15:11];
    end
end
assign REG_A2_0_Field6 = REG_A2_0[10:0];
assign REG_A2_0_Field7 = REG_A2_0[31:11];

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        reg_a3_0[15:12] <= 'h7;
    end
    else begin
        reg_a3_0[15:12] <= (reg_wr && reg_addr == REG_A3_0_ADDR && reg_we[1]) ? reg_wdat[15:12] : reg_a3_0[15:12];
    end
end
assign reg_a3_0_Field9 = reg_a3_0[15:12];
assign reg_a3_0[11:0] = 'h5;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A2_1[10: 0] <= 'h4;
        REG_A2_1[31:11] <= 'h4;
    end
    else begin
        REG_A2_1[10:8] <= (reg_wr && reg_addr == REG_A2_1_ADDR && reg_we[1]) ? reg_wdat[10:8] : REG_A2_1[10:8];
        REG_A2_1[7:0] <= (reg_wr && reg_addr == REG_A2_1_ADDR && reg_we[0]) ? reg_wdat[7:0] : REG_A2_1[7:0];
        REG_A2_1[31:24] <= (reg_wr && reg_addr == REG_A2_1_ADDR && reg_we[3]) ? reg_wdat[31:24] : REG_A2_1[31:24];
        REG_A2_1[23:16] <= (reg_wr && reg_addr == REG_A2_1_ADDR && reg_we[2]) ? reg_wdat[23:16] : REG_A2_1[23:16];
        REG_A2_1[15:11] <= (reg_wr && reg_addr == REG_A2_1_ADDR && reg_we[1]) ? reg_wdat[15:11] : REG_A2_1[15:11];
    end
end
assign REG_A2_1_Field6 = REG_A2_1[10:0];
assign REG_A2_1_Field7 = REG_A2_1[31:11];

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        reg_a3_1[15:12] <= 'h7;
    end
    else begin
        reg_a3_1[15:12] <= (reg_wr && reg_addr == REG_A3_1_ADDR && reg_we[1]) ? reg_wdat[15:12] : reg_a3_1[15:12];
    end
end
assign reg_a3_1_Field9 = reg_a3_1[15:12];
assign reg_a3_1[11:0] = 'h5;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A2_2[10: 0] <= 'h4;
        REG_A2_2[31:11] <= 'h4;
    end
    else begin
        REG_A2_2[10:8] <= (reg_wr && reg_addr == REG_A2_2_ADDR && reg_we[1]) ? reg_wdat[10:8] : REG_A2_2[10:8];
        REG_A2_2[7:0] <= (reg_wr && reg_addr == REG_A2_2_ADDR && reg_we[0]) ? reg_wdat[7:0] : REG_A2_2[7:0];
        REG_A2_2[31:24] <= (reg_wr && reg_addr == REG_A2_2_ADDR && reg_we[3]) ? reg_wdat[31:24] : REG_A2_2[31:24];
        REG_A2_2[23:16] <= (reg_wr && reg_addr == REG_A2_2_ADDR && reg_we[2]) ? reg_wdat[23:16] : REG_A2_2[23:16];
        REG_A2_2[15:11] <= (reg_wr && reg_addr == REG_A2_2_ADDR && reg_we[1]) ? reg_wdat[15:11] : REG_A2_2[15:11];
    end
end
assign REG_A2_2_Field6 = REG_A2_2[10:0];
assign REG_A2_2_Field7 = REG_A2_2[31:11];

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        reg_a3_2[15:12] <= 'h7;
    end
    else begin
        reg_a3_2[15:12] <= (reg_wr && reg_addr == REG_A3_2_ADDR && reg_we[1]) ? reg_wdat[15:12] : reg_a3_2[15:12];
    end
end
assign reg_a3_2_Field9 = reg_a3_2[15:12];
assign reg_a3_2[11:0] = 'h5;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        REG_A2_3[10: 0] <= 'h4;
        REG_A2_3[31:11] <= 'h4;
    end
    else begin
        REG_A2_3[10:8] <= (reg_wr && reg_addr == REG_A2_3_ADDR && reg_we[1]) ? reg_wdat[10:8] : REG_A2_3[10:8];
        REG_A2_3[7:0] <= (reg_wr && reg_addr == REG_A2_3_ADDR && reg_we[0]) ? reg_wdat[7:0] : REG_A2_3[7:0];
        REG_A2_3[31:24] <= (reg_wr && reg_addr == REG_A2_3_ADDR && reg_we[3]) ? reg_wdat[31:24] : REG_A2_3[31:24];
        REG_A2_3[23:16] <= (reg_wr && reg_addr == REG_A2_3_ADDR && reg_we[2]) ? reg_wdat[23:16] : REG_A2_3[23:16];
        REG_A2_3[15:11] <= (reg_wr && reg_addr == REG_A2_3_ADDR && reg_we[1]) ? reg_wdat[15:11] : REG_A2_3[15:11];
    end
end
assign REG_A2_3_Field6 = REG_A2_3[10:0];
assign REG_A2_3_Field7 = REG_A2_3[31:11];

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        reg_a3_3[15:12] <= 'h7;
    end
    else begin
        reg_a3_3[15:12] <= (reg_wr && reg_addr == REG_A3_3_ADDR && reg_we[1]) ? reg_wdat[15:12] : reg_a3_3[15:12];
    end
end
assign reg_a3_3_Field9 = reg_a3_3[15:12];
assign reg_a3_3[11:0] = 'h5;

always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
        regtt[10: 0] <= 'h5;
    end
    else begin
        regtt[10:8] <= (reg_wr && reg_addr == REGTT_ADDR && reg_we[1]) ? reg_wdat[10:8] : regtt[10:8];
        regtt[7:0] <= (reg_wr && reg_addr == REGTT_ADDR && reg_we[0]) ? reg_wdat[7:0] : regtt[7:0];
    end
end
assign Field9 = regtt[10:0];



always @(negedge reg_rstn or posedge reg_clk) begin
    if (~reg_rstn) begin
        reg_rdat <= 32'h0;
    end
    else if (reg_rd) begin
        case(reg_addr)
        REG1_ADDR                                        : reg_rdat <= reg1;
        REG2_ADDR                                        : reg_rdat <= reg2;
        REG_A1_0_ADDR                                    : reg_rdat <= REG_A1_0;
        REG_A1_1_ADDR                                    : reg_rdat <= REG_A1_1;
        REG_A1_2_ADDR                                    : reg_rdat <= REG_A1_2;
        REG_A1_3_ADDR                                    : reg_rdat <= REG_A1_3;
        REG_A1_4_ADDR                                    : reg_rdat <= REG_A1_4;
        REG_A1_5_ADDR                                    : reg_rdat <= REG_A1_5;
        REG_A1_6_ADDR                                    : reg_rdat <= REG_A1_6;
        REG_A1_7_ADDR                                    : reg_rdat <= REG_A1_7;
        REG_A1_8_ADDR                                    : reg_rdat <= REG_A1_8;
        REG_A1_9_ADDR                                    : reg_rdat <= REG_A1_9;
        REG_A1_10_ADDR                                   : reg_rdat <= REG_A1_10;
        REG_A1_11_ADDR                                   : reg_rdat <= REG_A1_11;
        REG_A1_12_ADDR                                   : reg_rdat <= REG_A1_12;
        REG_A1_13_ADDR                                   : reg_rdat <= REG_A1_13;
        REG_A1_14_ADDR                                   : reg_rdat <= REG_A1_14;
        REG_A1_15_ADDR                                   : reg_rdat <= REG_A1_15;
        REG_A2_0_ADDR                                    : reg_rdat <= REG_A2_0;
        REG_A3_0_ADDR                                    : reg_rdat <= reg_a3_0;
        REG_A2_1_ADDR                                    : reg_rdat <= REG_A2_1;
        REG_A3_1_ADDR                                    : reg_rdat <= reg_a3_1;
        REG_A2_2_ADDR                                    : reg_rdat <= REG_A2_2;
        REG_A3_2_ADDR                                    : reg_rdat <= reg_a3_2;
        REG_A2_3_ADDR                                    : reg_rdat <= REG_A2_3;
        REG_A3_3_ADDR                                    : reg_rdat <= reg_a3_3;
        REGTT_ADDR                                       : reg_rdat <= regtt;
        default: reg_rdat <= 32'h0;
        endcase
    end
    else begin
       reg_rdat <= 32'h0;
    end
end

endmodule