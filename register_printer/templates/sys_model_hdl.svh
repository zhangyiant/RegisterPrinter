{% set uvm_sys_name = top_sys.name.lower() + "_hdl" %}
`ifndef {{ uvm_sys_name | upper }}__SV
`define {{ uvm_sys_name | upper }}__SV

virtual function void build_hdl();
  {% for block_instance in top_sys.block_instances %}
  {% set block_instance_name = block_instance.name.lower() %}
  {% set block_type_name = block_instance.block_type.lower() %}
  {{ block_instance_name }}.add_hdl_path("{{ block_type_name | upper }}_reg_inst");
  {% endfor %}
endfunction

`endif
