{% set sv_def_name = top_sys.name.lower() + "_register_defines" %}
`ifndef {{ sv_def_name | upper }}__SVH
`define {{ sv_def_name | upper }}__SVH

{% for block_instance in top_sys.block_instances %}
{% set block_type = block_instance.block_type %}
{% set block_instance_name = block_instance.name.lower() %}
{% set base_address = block_instance.base_address %}
    `define {{ block_instance_name | upper }}_BASE_ADDR    'h{{ "%x" | format(base_address) }}
    {% set block = block_instance.block %}
    {% for register in block.registers %}
    {% set block_instance_reg_name = (block_instance_name + '_' + register.name + "_addr").upper() %}
    `define {{ "%-48s" | format(block_instance_reg_name) }}    `{{ "%-32s" | format(block_instance_name.upper() + "_BASE_ADDR") }} + 'h{{ "%x" | format(register.offset )}}
    {% endfor %}

{% endfor %}
`endif
