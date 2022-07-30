#ifndef __REGS_TOP_MODULE_H__
#define __REGS_TOP_MODULE_H__

#include "regs_type2.h"
#include "regs_type1.h"

#define  INSTANCE2_BASE		0x10000
#define  INSTANCE2		((volatile TYPE2_TypeDef  *)		INSTANCE2_BASE)

#define  INSTANCE3_BASE		0x20000
#define  INSTANCE3		((volatile TYPE1_TypeDef  *)		INSTANCE3_BASE)


#endif