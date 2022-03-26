#ifndef __REGS_TYPE2_H__
#define __REGS_TYPE2_H__

typedef struct
{
    volatile short          	REG1                    	;
    volatile const char     	RSVD0[6]                	;
    volatile short          	REG2                    	;
    volatile const char     	RSVD1[6]                	;
} TYPE2_TypeDef;


#define    REG1_FIELD1_Pos                                                  1
#define    REG1_FIELD1_Msk                                                  (0x7fU << REG1_FIELD1_Pos)

#define    REG1_FIELD2_Pos                                                  8
#define    REG1_FIELD2_Msk                                                  (0x7U << REG1_FIELD2_Pos)

#define    REG2_FIELD2_Pos                                                  1
#define    REG2_FIELD2_Msk                                                  (0x7fU << REG2_FIELD2_Pos)

#define    REG2_FIELD3_Pos                                                  9
#define    REG2_FIELD3_Msk                                                  (0xfU << REG2_FIELD3_Pos)


#endif