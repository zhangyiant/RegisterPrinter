`ifndef TYPE2_REG_MODEL__SV
`define TYPE2_REG_MODEL__SV

class REG1 extends uvm_reg;
  `uvm_object_utils(REG1)
  uvm_reg_field field1;
  uvm_reg_field field2;

  function new(string name = "REG1", int unsigned n_bits = 16);
    super.new(name, n_bits, UVM_NO_COVERAGE);
  endfunction: new

  virtual function void build();
    field1 = uvm_reg_field::type_id::create("field1");
    field1.configure(this, 7, 1, "RW", 0, 'h1, 1, 1, 1);
    field2 = uvm_reg_field::type_id::create("field2");
    field2.configure(this, 3, 8, "RW", 0, 'h1, 1, 1, 1);
  endfunction: build

endclass: REG1

class REG2 extends uvm_reg;
  `uvm_object_utils(REG2)
  uvm_reg_field field2;
  uvm_reg_field field3;

  function new(string name = "REG2", int unsigned n_bits = 16);
    super.new(name, n_bits, UVM_NO_COVERAGE);
  endfunction: new

  virtual function void build();
    field2 = uvm_reg_field::type_id::create("field2");
    field2.configure(this, 7, 1, "RW", 0, 'h1, 1, 1, 1);
    field3 = uvm_reg_field::type_id::create("field3");
    field3.configure(this, 4, 9, "RW", 0, 'h1, 1, 1, 1);
  endfunction: build

endclass: REG2



class type2_reg_model extends uvm_reg_block;
  `uvm_object_utils(type2_reg_model)
  REG1    reg1;
  REG2    reg2;

  function new(string name = "type2_reg_model");
    super.new(name);
  endfunction: new

  virtual function void build();
    default_map = create_map("default_map", 0, 8, UVM_BIG_ENDIAN, 0);

    reg1 = REG1::type_id::create("reg1");
    reg1.configure(this, , "");
    reg1.build();
    default_map.add_reg(reg1, 24'h0);

    reg2 = REG2::type_id::create("reg2");
    reg2.configure(this, , "");
    reg2.build();
    default_map.add_reg(reg2, 24'h8);

  endfunction: build
endclass: type2_reg_model
`endif