{% set uvm_block_name = block.block_type.lower() + "_reg_model" %}
`ifndef {{ uvm_block_name | upper }}__SV
`define {{ uvm_block_name | upper }}__SV

{% for register in block.registers %}
{% set uvm_reg_type = register.name.upper() %}
class {{ uvm_reg_type }} extends uvm_reg;
  `uvm_object_utils({{ uvm_reg_type }})
  {% for field in register.fields %}
    {% if field.name != "-" %}
  uvm_reg_field {{ field.name | lower }};
    {% endif %}
  {% endfor %}

  function new(string name = "{{ uvm_reg_type }}", int unsigned n_bits = {{ block.data_width }});
    super.new(name, n_bits, UVM_NO_COVERAGE);
  endfunction: new

  virtual function void build();
  {% for field in register.fields %}
    {% if field.name != "-" %}
    {% set field_size = field.msb - field.lsb + 1 %}
    {{ field.name | lower }} = uvm_reg_field::type_id::create("{{ field.name | lower }}");
    {{ field.name | lower }}.configure(this, {{ field_size }}, {{ field.lsb }}, "{{ field.access }}", 0, {{ field_size }}'h{{ '%x' | format(field.default) }}, 1, 1, 1);
    {% endif %}
  {% endfor %}
  endfunction: build

endclass: {{ uvm_reg_type }}

{% endfor %}

class {{ uvm_block_name }} extends uvm_reg_block;
  `uvm_object_utils({{ uvm_block_name }})
  {% for register in block.registers %}
  {{ register.name | upper }}    {{ register.name | lower }};
  {% endfor %}

  function new(string name = "{{ uvm_block_name }}");
    super.new(name);
  endfunction: new

  virtual function void build();
    default_map = create_map("default_map", 0, {{ (block.data_width / 8) | int }}, UVM_BIG_ENDIAN, 0);

    {% for register in block.registers %}
    {% set reg_inst = register.name.lower() %}
    {% set reg_type = register.name.upper() %}
    {% set reg_offset = register.offset %}
    {{ reg_inst }} = {{ reg_type }}::type_id::create("{{ reg_inst }}");
    {{ reg_inst }}.configure(this, , "");
    {{ reg_inst }}.build();
    default_map.add_reg({{ reg_inst }}, {{ block.addr_width }}'h{{ '%x' | format(reg_offset) }});

    {% endfor %}
  endfunction: build
endclass: {{ uvm_block_name }}
`endif
