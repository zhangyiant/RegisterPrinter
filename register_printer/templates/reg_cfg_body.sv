`ifndef {{ uvm_block.name | upper }}_CFG_BODY__SV
`define {{ uvm_block.name | upper }}_CFG_BODY__SV
{% for item in uvm_block.registers %}
        {% for register in item.registers %}
            {% for field in register.fields %}
                {% if field.access == "RW" or field.access == "RWP" %}
                    {% if item.is_struct %}
foreach(m_reg_model.{{item.name | lower}}[i]) m_reg_model.{{item.name | lower}}[i].{{register.name | lower}}.{{field.name | lower}}.set({{field.name | lower}}[i]);
                    {% else %}
m_reg_model.{{register.name | lower}}.{{field.name | lower}}.set({{field.name | lower}});
                    {% endif %}
                {% endif %}
            {% endfor %}
        {% endfor %}
{% endfor %}
`endif
