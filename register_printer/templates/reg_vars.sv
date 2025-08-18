`ifndef {{ uvm_block.name | upper }}_VARS__SV
`define {{ uvm_block.name | upper }}_VARS__SV
{% for item in uvm_block.registers %}
        {% for register in item.registers %}
            {% for field in register.fields %}
                {% if field.access == "RW" or field.access == "RWP" %}
                    {% if item.is_struct %}
rand bit[{{field.size -1}}:0] {{field.name | lower}}[{{item.length}}];
                    {% else %}
rand bit[{{field.size -1}}:0] {{field.name | lower}};
                    {% endif %}
                {% endif %}
            {% endfor %}
        {% endfor %}
{% endfor %}
`endif
