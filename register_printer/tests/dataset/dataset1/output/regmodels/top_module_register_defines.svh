`ifndef TOP_MODULE_REGISTER_DEFINES__SVH
`define TOP_MODULE_REGISTER_DEFINES__SVH

    `define INSTANCE2_BASE_ADDR    'h10000
    `define INSTANCE2_REG1_ADDR                                 `INSTANCE2_BASE_ADDR              + 'h0
    `define INSTANCE2_REG2_ADDR                                 `INSTANCE2_BASE_ADDR              + 'h8

    `define INSTANCE3_BASE_ADDR    'h20000
    `define INSTANCE3_REG1_ADDR                                 `INSTANCE3_BASE_ADDR              + 'h0
    `define INSTANCE3_REG2_ADDR                                 `INSTANCE3_BASE_ADDR              + 'h4
    `define INSTANCE3_REG_ARRAY1_BASE_ADDR                      `INSTANCE3_BASE_ADDR              + 'h10
    `define INSTANCE3_REG_ARRAY2_BASE_ADDR                      `INSTANCE3_BASE_ADDR              + 'h100
    `define INSTANCE3_REGTT_ADDR                                `INSTANCE3_BASE_ADDR              + 'h1a0

`endif