`ifndef {{ sv_def_name | upper }}__SVH
`define {{ sv_def_name | upper }}__SVH

{% for instance in instances %}
{% set block_instance_name = instance.name.lower() %}
    `define {{ instance.name | upper }}_BASE_ADDR    'h{{ "%x" | format(instance.base_address) }}
    {% for register in instance.registers %}
    `define {{ "%-48s" | format(register.name) }}    `{{ "%-32s" | format(instance.name.upper() + "_BASE_ADDR") }} + 'h{{ "%x" | format(register.offset )}}
    {% endfor %}

{% endfor %}
`endif
