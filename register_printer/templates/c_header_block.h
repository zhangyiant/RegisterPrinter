#ifndef __REGS_{{ block_type | upper }}_H__
#define __REGS_{{ block_type | upper }}_H__

#include <stdint.h>
#pragma pack(1)

{% for c_struct in c_structs %}
typedef struct {
{% for struct_field in c_struct.struct_fields %}
    {{ "%-24s\t%-24s\t;" | format(struct_field.type, struct_field.name) }}
{% endfor %}
} {{ c_struct.name }};

{% endfor %}
typedef struct
{
{% for struct_field in struct_fields %}
    {{ "%-24s\t%-24s\t;" | format(struct_field.type, struct_field.name) }}
{% endfor %}
} {{ block_type | upper }}_TypeDef;

#pragma pack()

{% for pos_mask_macro in pos_mask_macros %}
#define    {{ "%-64s" | format(pos_mask_macro.prefix + "_Pos") }} {{ pos_mask_macro.pos_value }}
#define    {{ "%-64s" | format(pos_mask_macro.prefix + "_Msk") }} ({{ "0x%xU" | format(pos_mask_macro.mask_value) }} << {{ pos_mask_macro.prefix }}_Pos)

{% endfor %}

#endif
