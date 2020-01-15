{% set uvm_sys_name = top_sys.name.lower() + "_reg_model" %}
`ifndef {{ uvm_sys_name | upper }}__SV
`define {{ uvm_sys_name | upper }}__SV

{% for block in top_sys.blocks %}
`include "{{ block.block_type | lower }}_reg_model.sv"
{% endfor %}

class {{ uvm_sys_name }} extends uvm_reg_block;
  `uvm_object_utils({{ uvm_sys_name }})

  {% for addr_map_entry in top_sys.addr_map %}
  {{ addr_map_entry["block_type"] | lower }}_reg_model    {{ addr_map_entry["block_instance"] }};
  {% endfor %}

  function new(string name = "{{ uvm_sys_name }}");
    super.new(name);
  endfunction: new

virtual function void build();
  default_map = create_map("default_map", 0, {{ (top_sys.data_width / 8) | int }}, UVM_BIG_ENDIAN, 0);

  {% for addr_map_entry in top_sys.addr_map %}
  {% set block_instance_name = addr_map_entry["block_instance"].lower() %}
  {% set block_type_name = addr_map_entry["block_type"].lower() %}
  {% set base_address = addr_map_entry["base_address"] %}
  {{ block_instance_name }} = {{ block_type_name }}_reg_model::type_id::create("{{ block_instance_name }}");
  {{ block_instance_name }}.configure(this, "");
  {{ block_instance_name }}.build();
  default_map.add_submap({{ block_instance_name }}.default_map, {{ top_sys.addr_width }}'h{{ "%x" | format(base_address) }});

  {% endfor %}
endfunction: build
endclass: {{ uvm_sys_name }}
`endif
