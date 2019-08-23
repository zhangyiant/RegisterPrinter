{% set sv_def_name = top_sys.name.lower() + "_register_defines" %}
`ifndef {{ sv_def_name | upper }}__SVH
`define {{ sv_def_name | upper }}__SVH

{% for addr_map_entry in top_sys.addr_map %}
{% set block_type = addr_map_entry["block_type"] %}
{% set block_instance_name = addr_map_entry["block_instance"].lower() %}
{% set base_address = addr_map_entry["base_address"] %}
    `define {{ block_instance_name | upper }}_BASE_ADDR    'h{{ "%x" | format(base_address) }}
    {% set block = top_sys.find_block_by_name(block_type) %}
    {% for register in block.registers %}
    {% set block_instance_reg_name = (block_instance_name + '_' + register.name + "_addr").upper() %}
    `define {{ "%-48s" | format(block_instance_reg_name) }}    `{{ "%-32s" | format(block_instance_name.upper() + "_BASE_ADDR") }} + 'h{{ "%x" | format(register.offset )}}
    {% endfor %}

{% endfor %}
`endif
