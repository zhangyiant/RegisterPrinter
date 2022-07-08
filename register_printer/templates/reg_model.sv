`ifndef {{ uvm_block.name | upper }}__SV
`define {{ uvm_block.name | upper }}__SV

{% for register in registers %}
{% set uvm_reg_type = register.name.upper() %}
class {{ uvm_reg_type }} extends uvm_reg;
  `uvm_object_utils({{ uvm_reg_type }})
  {% for field in register.fields %}
    {% if field.name != "-" %}
  uvm_reg_field {{ field.name | lower }};
    {% endif %}
  {% endfor %}

  function new(string name = "{{ uvm_reg_type }}", int unsigned n_bits = {{ register.size * 8 }});
    super.new(name, n_bits, UVM_NO_COVERAGE);
  endfunction: new

  virtual function void build();
  {% for field in register.fields %}
    {% if field.name != "-" %}
    {{ field.name | lower }} = uvm_reg_field::type_id::create("{{ field.name | lower }}");
    {% if field.access == "RWP" %}
    {{ field.name | lower }}.configure(this, {{ field.size }}, {{ field.lsb }}, "RW", 0, {{ field_size }}'h{{ '%x' | format(field.default) }}, 1, 1, 1);
    {% else %}
    {{ field.name | lower }}.configure(this, {{ field.size }}, {{ field.lsb }}, "{{ field.access }}", 0, {{ field_size }}'h{{ '%x' | format(field.default) }}, 1, 1, 1);
    {% endif %}
    {% endif %}
  {% endfor %}
  endfunction: build

endclass: {{ uvm_reg_type }}

{% endfor %}

{% for struct in structs %}
class {{ struct.name | upper }} extends uvm_reg_block;
  `uvm_object_utils({{ struct.name | upper }})

  {% for reg in struct.registers %}
  {{ reg.name | upper }} {{ reg.name }};
  {% endfor %}

  extern function new(string name="{{ struct.name | upper }}");
  extern virtual function void build();

endclass: {{ struct.name | upper }}

function {{ struct.name | upper }}::new(string name="{{ struct.name | upper }}");
  super.new(name);
endfunction: new

function void {{ struct.name | upper }}::build();
  default_map = create_map("default_map", 0, {{ data_width // 8 }}, UVM_BIG_ENDIAN, 0);

  {% for reg in struct.registers %}
  {{ reg.name }} = {{ reg.name | upper }}::type_id::create("{{ reg.name }}");
  {{ reg.name }}.configure(this, , "");
  {{ reg.name }}.build();
  default_map.add_reg({{ reg.name }}, {{ address_width }}'h{{ '%x' | format(reg.offset) }});

  {% endfor %}
endfunction: build

{% endfor %}

class {{ uvm_block.name }} extends uvm_reg_block;
  `uvm_object_utils({{ uvm_block.name }})
  {% for register in uvm_block.registers %}
  {% if register.is_struct %}
  {{ register.name | upper }}    {{ register.name | lower }}[{{ register.length }}];
  {% else %}
  {{ register.name | upper }}    {{ register.name | lower }};
  {% endif %}
  {% endfor %}

  function new(string name = "{{ uvm_block.name }}");
    super.new(name);
  endfunction: new

  virtual function void build();
    default_map = create_map("default_map", 0, {{ (data_width // 8) | int }}, UVM_BIG_ENDIAN, 0);

    {% for register in uvm_block.registers %}
    {% if register.is_struct %}
    for(int i=0; i<{{ register.length }}; i++) begin
      {{ register.name | lower }}[i] = {{ register.name | upper }}::type_id::create($sformatf("{{ register.name | lower }}[%0d]", i));
      {{ register.name | lower }}[i].configure(this, "");
      {{ register.name | lower }}[i].build();
      default_map.add_submap({{ register.name | lower }}[i].default_map, 'h{{ '%x' | format(register.start_address) }} + i * 'h{{ '%x' | format(register.offset) }});
    end
    {% for overwrite in register.default_overwrites %}
    {{ register.name | lower }}[{{ overwrite.index }}].{{ overwrite.register_name }}.{{ overwrite.field_name}}.set_default('h{{ '%x' | format(overwrite.default) }});
    {% endfor %}
    {% else %}
    {% set reg_inst = register.name.lower() %}
    {% set reg_type = register.name.upper() %}
    {% set reg_offset = register.offset %}
    {{ reg_inst }} = {{ reg_type }}::type_id::create("{{ reg_inst }}");
    {{ reg_inst }}.configure(this, , "");
    {{ reg_inst }}.build();
    default_map.add_reg({{ reg_inst }}, {{ address_width }}'h{{ '%x' | format(reg_offset) }});
    {% endif %}

    {% endfor %}
  endfunction: build
endclass: {{ uvm_block.name }}
`endif
