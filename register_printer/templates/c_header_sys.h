#ifndef __{{ include_macro_name }}__
#define __{{ include_macro_name }}__

{% for include_filename in include_filenames %}
#include "{{ include_filename }}"
{% endfor %}

{% for block_instance in block_instances %}
#define  {{ "%s_BASE\t\t0x%x" | format(block_instance.name, block_instance.base_address) }}
#define  {{ "%s\t\t((volatile %s_TypeDef  *)\t\t%s_BASE)" | format(
    block_instance.name,
    block_instance.type.upper(),
    block_instance.name)
}}

{% endfor %}

#endif
