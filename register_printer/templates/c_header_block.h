#ifndef __REGS_{{ block_type | upper }}_H__
#define __REGS_{{ block_type | upper }}_H__

#include <stdint.h>
#pragma pack(1)

{% for c_struct in c_structs %}
typedef struct {
{% for struct_field in c_struct.struct_fields %}
    {% if struct_field.category == "reserved" %}
    {{ "%s %s;" | format(struct_field.type, struct_field.name) }}
    {% elif struct_field.category == "register" %}
    union {
        struct {
            {% for field in struct_field.fields %}
            {{ "%s %s:%d;" | format(field.type, field.name, field.length) }}
            {% endfor %}
        } {{ struct_field.name }}_B;
        {{ "%s %s;" | format(struct_field.type, struct_field.name) }}
    };
    {% endif %}
{% endfor %}
} {{ c_struct.name }};

{% endfor %}
typedef struct
{
{% for struct_field in struct_fields %}
    {% if struct_field.category == "reserved" or struct_field.category == "array" %}
    {{ "%s %s;" | format(struct_field.type, struct_field.name) }}
    {% elif struct_field.category == "register" %}
    union {
        struct {
            {% for field in struct_field.fields %}
            {{ "%s %s:%d;" | format(field.type, field.name, field.length) }}
            {% endfor %}
        } {{ struct_field.name }}_B;
        {{ "%s %s;" | format(struct_field.type, struct_field.name) }}
    };
    {% endif %}
{% endfor %}
} {{ block_type | upper }}_TypeDef;

#pragma pack()

{% for pos_mask_macro in pos_mask_macros %}
#define    {{ "%-64s" | format(pos_mask_macro.prefix + "_Pos") }} {{ pos_mask_macro.pos_value }}
#define    {{ "%-64s" | format(pos_mask_macro.prefix + "_Msk") }} ({{ "0x%xU" | format(pos_mask_macro.mask_value) }} << {{ pos_mask_macro.prefix }}_Pos)

{% endfor %}

#endif
