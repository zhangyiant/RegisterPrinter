`ifndef {{ uvm_block.name | upper }}_COVERGROUP__SV
`define {{ uvm_block.name | upper }}_COVERGROUP__SV
uvm_event {{ uvm_block.name | lower }}_sample_event = uvm_event_pool::get_global("{{ uvm_block.name | lower }}_sample_event");
`define create_{{uvm_block.name | lower}}_covergroup \
    begin \
        {{ uvm_block.name | lower}}_covergroup = new();\
        fork\
            forever begin\
                {{ uvm_block.name | lower}}_sample_event.wait_trigger();\
                {{ uvm_block.name | lower}}_covergroup.sample();\
            end\
        join_none \
    end
//`create_{{uvm_block.name | lower}}_covergroup --- add in new function

covergroup {{uvm_block.name | lower}}_covergroup();
{% for item in uvm_block.registers %}
    {% for register in item.registers %}
        {% for field in register.fields %}
            {% if field.access == "RW" or field.access == "RWP" %}
                {% if item.is_struct %}
                    {% for i in range(item.length) %}
    {{register.name | lower}}_{{i}}_{{field.name | lower}}_cp: coverpoint(m_reg_model.{{item.name | lower}}[{{i}}].{{register.name | lower}}.{{field.name | lower}}.get()) {
                        {% if field.size > 2 %}
        bins min = {{'{'}}{{ field.size }}'h0{{'}'}};
        bins little = {{'{'}}[{{ field.size }}'d1:{{ field.size }}'d{{ '%f' | format((2**field.size-1)/3) | int }}]{{'}'}};
        bins normal = {{'{'}}[{{ field.size }}'d{{ '%f' | format((2**field.size-1)/3+1) | int }}:{{ field.size }}'d{{ '%f' | format((2**field.size-1)*2/3) | int }}]{{'}'}};
        bins larger = {{'{'}}[{{ field.size }}'d{{ '%f' | format((2**field.size-1)*2/3+1) | int }}:{{ field.size }}'d{{ '%f' | format((2**field.size-2)) | int }}]{{'}'}};
        bins max = {{'{'}}{{ field.size }}'h{{ '%x' | format(2**field.size-1) }}{{'}'}};
                        {% else %}
                            {% for index in range(2**field.size) %}
        bins value{{index}} = {{'{'}}{{ field.size }}'h{{index}}{{'}'}};
                            {% endfor %}
                        {% endif %}
    }
                    {% endfor %}
                {% else %}
    {{register.name | lower}}_{{field.name | lower}}_cp: coverpoint(m_reg_model.{{register.name | lower}}.{{field.name | lower}}.get()) {
                    {% if field.size > 2 %}
        bins min = {{'{'}}{{ field.size }}'h0{{'}'}};
        bins little = {{'{'}}[{{ field.size }}'d1:{{ field.size }}'d{{ '%f' | format((2**field.size-1)/3) | int }}]{{'}'}};
        bins normal = {{'{'}}[{{ field.size }}'d{{ '%f' | format((2**field.size-1)/3+1) | int }}:{{ field.size }}'d{{ '%f' | format((2**field.size-1)*2/3) | int }}]{{'}'}};
        bins larger = {{'{'}}[{{ field.size }}'d{{ '%f' | format((2**field.size-1)*2/3+1) | int }}:{{ field.size }}'d{{ '%f' | format((2**field.size-2)) | int }}]{{'}'}};
        bins max = {{'{'}}{{ field.size }}'h{{ '%x' | format(2**field.size-1) }}{{'}'}};
                    {% else %}
                        {% for index in range(2**field.size) %}
        bins value{{index}} = {{'{'}}{{ field.size }}'h{{index}}{{'}'}};
                        {% endfor %}
                    {% endif %}
    }
                {% endif %}
            {% endif %}
        {% endfor %}
    {% endfor %}
{% endfor %}
endgroup
`endif
