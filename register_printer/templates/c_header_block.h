#ifndef __REGS_{{ block_type | upper }}_H__
#define __REGS_{{ block_type | upper }}_H__

typedef struct
{
{% for struct_field in struct_fields %}
    {{ "%-24s\t%-24s\t;" | format(struct_field.type, struct_field.name) }}
{% endfor %}
} {{ block_type | upper }}_TypeDef;


{% for pos_mask_macro in pos_mask_macros %}
#define    {{ "%-64s" | format(pos_mask_macro.prefix + "_Pos") }} {{ pos_mask_macro.pos_value }}
#define    {{ "%-64s" | format(pos_mask_macro.prefix + "_Msk") }} ({{ "0x%xU" | format(pos_mask_macro.mask_value) }} << {{ pos_mask_macro.prefix }}_Pos)

{% endfor %}

#endif
