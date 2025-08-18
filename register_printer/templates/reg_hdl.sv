`ifndef {{ block_type | upper }}_HDL__SV
`define {{ block_type | upper }}_HDL__SV

virtual function void build_hdl();
    {% for register in uvm_block.registers %}
    {% if register.is_struct %}
    for(int i=0; i<{{ register.length }}; i++) begin
        {% for reg in register.registers %}
        {{ register.name | lower }}[i].{{ reg.name | lower }}.add_hdl_path_slice($sformatf("{{ reg.hdl_name | lower }}_%0d",i), 0, {{data_width}});
        {% endfor %}
    end
    {% else %}
    {{ register.name | lower }}.add_hdl_path_slice("{{ register.hdl_name | lower }}", 0, {{data_width}});
    {% endif %}
    {% endfor %}
endfunction

`endif
