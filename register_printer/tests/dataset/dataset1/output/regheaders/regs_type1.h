#ifndef __REGS_TYPE1_H__
#define __REGS_TYPE1_H__

typedef struct {
    volatile short          	REG_A1                  	;
    volatile const char     	RSVD0[2]                	;
} REG_ARRAY1_NAME;

typedef struct {
    volatile int            	REG_A2                  	;
    volatile const char     	RSVD0[20]               	;
    volatile short          	REG_A3                  	;
    volatile const char     	RSVD1[6]                	;
} REG_ARRAY2_NAME;

typedef struct
{
    volatile short          	REG1                    	;
    volatile const char     	RSVD0[2]                	;
    volatile short          	REG2                    	;
    volatile const char     	RSVD1[10]               	;
    REG_ARRAY1_NAME         	REG_ARRAY1[16]          	;
    volatile const char     	RSVD2[176]              	;
    REG_ARRAY2_NAME         	REG_ARRAY2[4]           	;
    volatile const char     	RSVD3[32]               	;
    volatile short          	REGTT                   	;
    volatile const char     	RSVD4[2]                	;
} TYPE1_TypeDef;


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