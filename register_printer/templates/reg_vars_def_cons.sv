`ifndef {{ uvm_block.name | upper }}_VARS_DEF_CONS__SV
`define {{ uvm_block.name | upper }}_VARS_DEF_CONS__SV
default constraint c_def_{{uvm_block.name | lower}} {
    {% for item in uvm_block.registers %}
            {% for register in item.registers %}
                {% for field in register.fields %}
                    {% if field.access == "RW" or field.access == "RWP" %}
                        {% if item.is_struct %}
    foreach({{field.name | lower}}[i]) {{field.name | lower}}[i] == {{field.size}}'h{{ '%x' | format(field.default) }};
                        {% else %}
    {{field.name | lower}} == {{field.size}}'h{{ '%x' | format(field.default) }};
                        {% endif %}
                    {% endif %}
                {% endfor %}
            {% endfor %}
    {% endfor %}
}
`endif
