`ifndef {{ sv_def_name | upper }}__SVH
`define {{ sv_def_name | upper }}__SVH

{% for instance in instances %}
{% set block_type = instance.block_type %}
{% set block_instance_name = instance.name.lower() %}
    `define {{ instance.name | upper }}_BASE_ADDR    'h{{ "%x" | format(instance.base_address) }}
    {% for register in instance.registers %}
    {% set block_instance_reg_name = (instance.name + '_' + register.name + "_addr").upper() %}
    `define {{ "%-48s" | format(block_instance_reg_name) }}    `{{ "%-32s" | format(instance.name.upper() + "_BASE_ADDR") }} + 'h{{ "%x" | format(register.offset )}}
    {% endfor %}

{% endfor %}
`endif
