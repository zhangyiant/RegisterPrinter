`ifndef TYPE1_REG_MODEL__SV
`define TYPE1_REG_MODEL__SV

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

class REG_A1 extends uvm_reg;
  `uvm_object_utils(REG_A1)
  uvm_reg_field field4;
  uvm_reg_field field5;

  function new(string name = "REG_A1", int unsigned n_bits = 16);
    super.new(name, n_bits, UVM_NO_COVERAGE);
  endfunction: new

  virtual function void build();
    field4 = uvm_reg_field::type_id::create("field4");
    field4.configure(this, 4, 0, "RO", 0, 'h1, 1, 1, 1);
    field5 = uvm_reg_field::type_id::create("field5");
    field5.configure(this, 11, 4, "RW", 0, 'h2, 1, 1, 1);
  endfunction: build

endclass: REG_A1

class REG_A2 extends uvm_reg;
  `uvm_object_utils(REG_A2)
  uvm_reg_field field6;
  uvm_reg_field field7;

  function new(string name = "REG_A2", int unsigned n_bits = 32);
    super.new(name, n_bits, UVM_NO_COVERAGE);
  endfunction: new

  virtual function void build();
    field6 = uvm_reg_field::type_id::create("field6");
    field6.configure(this, 11, 0, "RW", 0, 'h4, 1, 1, 1);
    field7 = uvm_reg_field::type_id::create("field7");
    field7.configure(this, 21, 11, "RW", 0, 'h4, 1, 1, 1);
  endfunction: build

endclass: REG_A2

class REG_A3 extends uvm_reg;
  `uvm_object_utils(REG_A3)
  uvm_reg_field field8;
  uvm_reg_field field9;

  function new(string name = "REG_A3", int unsigned n_bits = 16);
    super.new(name, n_bits, UVM_NO_COVERAGE);
  endfunction: new

  virtual function void build();
    field8 = uvm_reg_field::type_id::create("field8");
    field8.configure(this, 12, 0, "RW", 0, 'h5, 1, 1, 1);
    field9 = uvm_reg_field::type_id::create("field9");
    field9.configure(this, 4, 12, "RW", 0, 'h7, 1, 1, 1);
  endfunction: build

endclass: REG_A3

class REGTT extends uvm_reg;
  `uvm_object_utils(REGTT)
  uvm_reg_field field9;

  function new(string name = "REGTT", int unsigned n_bits = 16);
    super.new(name, n_bits, UVM_NO_COVERAGE);
  endfunction: new

  virtual function void build();
    field9 = uvm_reg_field::type_id::create("field9");
    field9.configure(this, 11, 0, "RW", 0, 'h5, 1, 1, 1);
  endfunction: build

endclass: REGTT


class REG_ARRAY1 extends uvm_reg_block;
  `uvm_object_utils(REG_ARRAY1)

  REG_A1 reg_a1;

  extern function new(string name="REG_ARRAY1");
  extern virtual function void build();

endclass: REG_ARRAY1

function REG_ARRAY1::new(string name="REG_ARRAY1");
  super.name(name);
endfunction: new

function void REG_ARRAY1::build();
  default_map = create_map("default_map", 0, 4, UVM_BIG_ENDIAN, 0);

  reg_a1 = REG_A1::type_id::create("reg_a1");
  reg_a1.configure(this, , "");
  reg_a1.build();
  default_map.add_reg(reg_a1, 12'h0);

endfunction: build

class REG_ARRAY2 extends uvm_reg_block;
  `uvm_object_utils(REG_ARRAY2)

  REG_A2 reg_a2;
  REG_A3 reg_a3;

  extern function new(string name="REG_ARRAY2");
  extern virtual function void build();

endclass: REG_ARRAY2

function REG_ARRAY2::new(string name="REG_ARRAY2");
  super.name(name);
endfunction: new

function void REG_ARRAY2::build();
  default_map = create_map("default_map", 0, 4, UVM_BIG_ENDIAN, 0);

  reg_a2 = REG_A2::type_id::create("reg_a2");
  reg_a2.configure(this, , "");
  reg_a2.build();
  default_map.add_reg(reg_a2, 12'h0);

  reg_a3 = REG_A3::type_id::create("reg_a3");
  reg_a3.configure(this, , "");
  reg_a3.build();
  default_map.add_reg(reg_a3, 12'h18);

endfunction: build


class type1_reg_model extends uvm_reg_block;
  `uvm_object_utils(type1_reg_model)
  REG1    reg1;
  REG2    reg2;
  REG_ARRAY1    reg_array1[16];
  REG_ARRAY2    reg_array2[4];
  REGTT    regtt;

  function new(string name = "type1_reg_model");
    super.new(name);
  endfunction: new

  virtual function void build();
    default_map = create_map("default_map", 0, 4, UVM_BIG_ENDIAN, 0);

    reg1 = REG1::type_id::create("reg1");
    reg1.configure(this, , "");
    reg1.build();
    default_map.add_reg(reg1, 12'h0);

    reg2 = REG2::type_id::create("reg2");
    reg2.configure(this, , "");
    reg2.build();
    default_map.add_reg(reg2, 12'h4);

    for(int i=0; i<16; i++) begin
      reg_array1[i] = REG_ARRAY1::type_id::create($sformatf("reg_array1[%0d]", i));
      reg_array1[i].configure(this, "");
      reg_array1[i].build();
      default_map.add_submap(reg_array1[i].default_map, 'h10 + i * 'h4);
    end

    for(int i=0; i<4; i++) begin
      reg_array2[i] = REG_ARRAY2::type_id::create($sformatf("reg_array2[%0d]", i));
      reg_array2[i].configure(this, "");
      reg_array2[i].build();
      default_map.add_submap(reg_array2[i].default_map, 'h100 + i * 'h20);
    end
    reg_array2[1].reg_a2.Field6.set_default('h5);
    reg_array2[1].reg_a2.Field7.set_default('h6);

    regtt = REGTT::type_id::create("regtt");
    regtt.configure(this, , "");
    regtt.build();
    default_map.add_reg(regtt, 12'h1a0);

  endfunction: build
endclass: type1_reg_model
`endif