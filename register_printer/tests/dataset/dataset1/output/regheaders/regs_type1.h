#ifndef __REGS_TYPE1_H__
#define __REGS_TYPE1_H__

#include <stdint.h>
#pragma pack(1)

typedef struct {
    union {
        struct {
            uint32_t FIELD4:4;
            uint32_t FIELD5:11;
            uint32_t RSVD0:1;
        } REG_A1_B;
        uint16_t REG_A1;
    };
    const uint8_t RSVD0[2];
} REG_ARRAY1_TypeDef;

typedef struct {
    union {
        struct {
            uint32_t FIELD6:11;
            uint32_t FIELD7:21;
        } REG_A2_B;
        uint32_t REG_A1;
    };
    const uint8_t RSVD0[20];
    union {
        struct {
            uint32_t FIELD8:12;
            uint32_t FIELD9:4;
        } REG_A3_B;
        uint16_t REG_A3;
    };
    const uint8_t RSVD1[6];
} REG_ARRAY2_TypeDef;

typedef struct
{
    union {
        struct {
            uint32_t RSVD0:1;
            uint32_t FIELD1:7;
            uint32_t FIELD2:3;
            uint32_t RSVD1:5;
        } REG1_B;
        uint16_t REG1;
    };
    const uint8_t RSVD0[2];
    union {
        struct {
            uint32_t RSVD0:1;
            uint32_t FIELD2:7;
            uint32_t RSVD1:1;
            uint32_t FIELD3:4;
            uint32_t RSVD2:3;
        } REG2_B;
        uint16_t REG2;
    };
    const uint8_t RSVD1[10];
    REG_ARRAY1_TypeDef REG_ARRAY1[16];
    const uint8_t RSVD2[176];
    REG_ARRAY2_TypeDef REG_ARRAY2[4];
    const uint8_t RSVD3[32];
    union {
        struct {
            uint32_t FIELD9:11;
            uint32_t RSVD0:5;
        } REGTT_B;
        uint16_t REGTT;
    };
    const uint8_t RSVD4[2];
} TYPE1_TypeDef;

#pragma pack()

#define    REG1_FIELD1_Pos                                                  1
#define    REG1_FIELD1_Msk                                                  (0x7fU << REG1_FIELD1_Pos)

#define    REG1_FIELD2_Pos                                                  8
#define    REG1_FIELD2_Msk                                                  (0x7U << REG1_FIELD2_Pos)

#define    REG2_FIELD2_Pos                                                  1
#define    REG2_FIELD2_Msk                                                  (0x7fU << REG2_FIELD2_Pos)

#define    REG2_FIELD3_Pos                                                  9
#define    REG2_FIELD3_Msk                                                  (0xfU << REG2_FIELD3_Pos)

#define    REG_A1_FIELD4_Pos                                                0
#define    REG_A1_FIELD4_Msk                                                (0xfU << REG_A1_FIELD4_Pos)

#define    REG_A1_FIELD5_Pos                                                4
#define    REG_A1_FIELD5_Msk                                                (0x7ffU << REG_A1_FIELD5_Pos)

#define    REG_A2_FIELD6_Pos                                                0
#define    REG_A2_FIELD6_Msk                                                (0x7ffU << REG_A2_FIELD6_Pos)

#define    REG_A2_FIELD7_Pos                                                11
#define    REG_A2_FIELD7_Msk                                                (0x1fffffU << REG_A2_FIELD7_Pos)

#define    REG_A3_FIELD8_Pos                                                0
#define    REG_A3_FIELD8_Msk                                                (0xfffU << REG_A3_FIELD8_Pos)

#define    REG_A3_FIELD9_Pos                                                12
#define    REG_A3_FIELD9_Msk                                                (0xfU << REG_A3_FIELD9_Pos)

#define    REGTT_FIELD9_Pos                                                 0
#define    REGTT_FIELD9_Msk                                                 (0x7ffU << REGTT_FIELD9_Pos)


#endif