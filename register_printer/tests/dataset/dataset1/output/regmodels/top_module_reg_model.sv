`ifndef TOP_MODULE_REG_MODEL__SV
`define TOP_MODULE_REG_MODEL__SV

`include "type2_reg_model.sv"
`include "type1_reg_model.sv"

class top_module_reg_model extends uvm_reg_block;
  `uvm_object_utils(top_module_reg_model)

  type2_reg_model    Instance2;
  type1_reg_model    Instance3;

  function new(string name = "top_module_reg_model");
    super.new(name);
  endfunction: new

virtual function void build();
  default_map = create_map("default_map", 0, 4, UVM_BIG_ENDIAN, 0);

  instance2 = type2_reg_model::type_id::create("instance2");
  instance2.configure(this, "");
  instance2.build();
  default_map.add_submap(instance2.default_map, 12'h10000);

  instance3 = type1_reg_model::type_id::create("instance3");
  instance3.configure(this, "");
  instance3.build();
  default_map.add_submap(instance3.default_map, 12'h20000);

endfunction: build
endclass: top_module_reg_model
`endif