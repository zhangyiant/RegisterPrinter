#ifndef __REGS_TYPE2_H__
#define __REGS_TYPE2_H__

#include <stdint.h>
#pragma pack(1)

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
    const uint8_t RSVD0[6];
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
    const uint8_t RSVD1[6];
} TYPE2_TypeDef;

#pragma pack()

#define    REG1_FIELD1_Pos                                                  1
#define    REG1_FIELD1_Msk                                                  (0x7fU << REG1_FIELD1_Pos)

#define    REG1_FIELD2_Pos                                                  8
#define    REG1_FIELD2_Msk                                                  (0x7U << REG1_FIELD2_Pos)

#define    REG2_FIELD2_Pos                                                  1
#define    REG2_FIELD2_Msk                                                  (0x7fU << REG2_FIELD2_Pos)

#define    REG2_FIELD3_Pos                                                  9
#define    REG2_FIELD3_Msk                                                  (0xfU << REG2_FIELD3_Pos)


#endif