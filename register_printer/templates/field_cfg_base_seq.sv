`ifndef {{name | upper}}_{{field.name | upper}}_CFG_SEQ__SV
`define {{name | upper}}_{{field.name | upper}}_CFG_SEQ__SV
{% if item.is_struct %}
    {% for i in range(item.length) %}
class {{name | lower}}_{{field.name | lower}}_{{i}}_min_cfg_base_seq extends {{name | lower}}_cfg_base_seq;
    `uvm_object_utils({{name | lower}}_{{field.name | lower}}_{{i}}_min_cfg_base_seq)

    function new(string name="{{name | lower}}_{{field.name | lower}}_{{i}}_min_cfg_base_seq");
        super.new(name);
    endfunction

    constraint {{field.name | lower}}_c {
        {{field.name | lower}}[{{i}}] dist {{'{'}}{{ field.size }}'h0{{'}'}};
    }
endclass

class {{name | lower}}_{{field.name | lower}}_{{i}}_max_cfg_base_seq extends {{name | lower}}_cfg_base_seq;
    `uvm_object_utils({{name | lower}}_{{field.name | lower}}_{{i}}_max_cfg_base_seq)

    function new(string name="{{name | lower}}_{{field.name | lower}}_{{i}}_max_cfg_base_seq");
        super.new(name);
    endfunction

    constraint {{field.name | lower}}_c {
        {{field.name | lower}}[{{i}}] dist {{'{'}}{{ field.size }}'h{{ '%x' | format(2**field.size-1) }}{{'}'}};
    }
endclass

class {{name | lower}}_{{field.name | lower}}_little_{{i}}_cfg_base_seq extends {{name | lower}}_cfg_base_seq;
    `uvm_object_utils({{name | lower}}_{{field.name | lower}}_{{i}}_little_cfg_base_seq)

    function new(string name="{{name | lower}}_{{field.name | lower}}_{{i}}_little_cfg_base_seq");
        super.new(name);
    endfunction

    constraint {{field.name | lower}}_c {
        {{field.name | lower}}[{{i}}] dist {{'{'}}[{{ field.size }}'d1:{{ field.size }}'d{{ '%f' | format((2**field.size-1)/3) | int }}]{{'}'}};
    }
endclass

class {{name | lower}}_{{field.name | lower}}_{{i}}_normal_cfg_base_seq extends {{name | lower}}_cfg_base_seq;
    `uvm_object_utils({{name | lower}}_{{field.name | lower}}_{{i}}_normal_cfg_base_seq)

    function new(string name="{{name | lower}}_{{field.name | lower}}_{{i}}_normal_cfg_base_seq");
        super.new(name);
    endfunction

    constraint {{field.name | lower}}_c {
        {{field.name | lower}}[{{i}}] dist {{'{'}}[{{ field.size }}'d{{ '%f' | format((2**field.size-1)/3+1) | int }}:{{ field.size }}'d{{ '%f' | format((2**field.size-1)*2/3) | int }}]{{'}'}};
    }
endclass

class {{name | lower}}_{{field.name | lower}}_{{i}}_larger_cfg_base_seq extends {{name | lower}}_cfg_base_seq;
    `uvm_object_utils({{name | lower}}_{{field.name | lower}}_{{i}}_larger_cfg_base_seq)

    function new(string name="{{name | lower}}_{{field.name | lower}}_{{i}}_larger_cfg_base_seq");
        super.new(name);
    endfunction

    constraint {{field.name | lower}}_c {
        {{field.name | lower}}[{{i}}] dist {{'{'}}[{{ field.size }}'d{{ '%f' | format((2**field.size-1)*2/3+1) | int }}:{{ field.size }}'d{{ '%f' | format((2**field.size-2)) | int }}]{{'}'}};
    }
endclass
    {% endfor %} 
{% else %}

class {{name | lower}}_{{field.name | lower}}_min_cfg_base_seq extends {{name | lower}}_cfg_base_seq;
    `uvm_object_utils({{name | lower}}_{{field.name | lower}}_min_cfg_base_seq)

    function new(string name="{{name | lower}}_{{field.name | lower}}_min_cfg_base_seq");
        super.new(name);
    endfunction

    constraint {{field.name | lower}}_c {
        {{field.name | lower}} dist {{'{'}}{{ field.size }}'h0{{'}'}};
    }
endclass

class {{name | lower}}_{{field.name | lower}}_max_cfg_base_seq extends {{name | lower}}_cfg_base_seq;
    `uvm_object_utils({{name | lower}}_{{field.name | lower}}_max_cfg_base_seq)

    function new(string name="{{name | lower}}_{{field.name | lower}}_max_cfg_base_seq");
        super.new(name);
    endfunction

    constraint {{field.name | lower}}_c {
        {{field.name | lower}} dist {{'{'}}{{ field.size }}'h{{ '%x' | format(2**field.size-1) }}{{'}'}};
    }
endclass

class {{name | lower}}_{{field.name | lower}}_little_cfg_base_seq extends {{name | lower}}_cfg_base_seq;
    `uvm_object_utils({{name | lower}}_{{field.name | lower}}_little_cfg_base_seq)

    function new(string name="{{name | lower}}_{{field.name | lower}}_little_cfg_base_seq");
        super.new(name);
    endfunction

    constraint {{field.name | lower}}_c {
        {{field.name | lower}} dist {{'{'}}[{{ field.size }}'d1:{{ field.size }}'d{{ '%f' | format((2**field.size-1)/3) | int }}]{{'}'}};
    }

endclass

class {{name | lower}}_{{field.name | lower}}_normal_cfg_base_seq extends {{name | lower}}_cfg_base_seq;
    `uvm_object_utils({{name | lower}}_{{field.name | lower}}_normal_cfg_base_seq)

    function new(string name="{{name | lower}}_{{field.name | lower}}_normal_cfg_base_seq");
        super.new(name);
    endfunction

    constraint {{field.name | lower}}_c {
        {{field.name | lower}} dist {{'{'}}[{{ field.size }}'d{{ '%f' | format((2**field.size-1)/3+1) | int }}:{{ field.size }}'d{{ '%f' | format((2**field.size-1)*2/3) | int }}]{{'}'}};
    }
endclass

class {{name | lower}}_{{field.name | lower}}_larger_cfg_base_seq extends {{name | lower}}_cfg_base_seq;
    `uvm_object_utils({{name | lower}}_{{field.name | lower}}_larger_cfg_base_seq)

    function new(string name="{{name | lower}}_{{field.name | lower}}_larger_cfg_base_seq");
        super.new(name);
    endfunction

    constraint {{field.name | lower}}_c {
        {{field.name | lower}} dist {{'{'}}[{{ field.size }}'d{{ '%f' | format((2**field.size-1)*2/3+1) | int }}:{{ field.size }}'d{{ '%f' | format((2**field.size-2)) | int }}]{{'}'}};
    }
endclass
{% endif %}
`endif
