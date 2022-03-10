{% set uvm_sys_name = top_sys.name.lower() + "_reg_model" %}
`ifndef {{ uvm_sys_name | upper }}__SV
`define {{ uvm_sys_name | upper }}__SV

{% for block in top_sys.blocks %}
`include "{{ block.block_type | lower }}_reg_model.sv"
{% endfor %}

class {{ uvm_sys_name }} extends uvm_reg_block;
  `uvm_object_utils({{ uvm_sys_name }})

  {% for block_instance in top_sys.block_instances %}
  {{ block_instance.block_type | lower }}_reg_model    {{ block_instance.name }};
  {% endfor %}

  function new(string name = "{{ uvm_sys_name }}");
    super.new(name);
  endfunction: new

virtual function void build();
  default_map = create_map("default_map", 0, {{ (top_sys.data_width // 8) | int }}, UVM_BIG_ENDIAN, 0);

  {% for block_instance in top_sys.block_instances %}
  {% set block_instance_name = block_instance.name.lower() %}
  {% set block_type_name = block_instance.block_type.lower() %}
  {% set base_address = block_instance.base_address %}
  {{ block_instance_name }} = {{ block_type_name }}_reg_model::type_id::create("{{ block_instance_name }}");
  {{ block_instance_name }}.configure(this, "");
  {{ block_instance_name }}.build();
  default_map.add_submap({{ block_instance_name }}.default_map, {{ top_sys.addr_width }}'h{{ "%x" | format(base_address) }});

  {% endfor %}
endfunction: build
endclass: {{ uvm_sys_name }}
`endif
