module {{ block.block_type }}_reg
#(
    parameter int ADDR_WIDTH = {{ block.addr_width }}                       ,
    parameter int DATA_WIDTH = {{ block.data_width }}
)
(
    input     reg_clk                                                           ,
    input     reg_rstn                                                          ,

{% for register in registers %}
    {% for field in register.hw_update_flds %}
        {% set field_bits = field.msb - field.lsb %}
    input      [{{ '%2s' | format(field_bits+1) }}-1: 0]     hw_{{ "%-48s" | format(field.name) }},
    {% endfor %}
{% endfor %}
  
{% for register in registers %}
    {% for field in register.output_flds %}
        {% set field_bits = field.msb - field.lsb %}
    output logic[{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
    {% endfor %}
{% endfor %}

{% for register in registers %}
    {% for field in register.rwp_flds %}
    input                                  unlk_{{ "%-48s" | format(field.name) }},
    {% endfor %}
{% endfor %}
  
    input                                  reg_wr                               ,
    input                                  reg_rd                               ,
    input       [DATA_WIDTH/8-1: 0]        reg_we                               ,
    input       [ADDR_WIDTH-1: 0]          reg_addr                             ,
    input       [DATA_WIDTH-1: 0]          reg_wdata                            ,
    output logic[DATA_WIDTH-1: 0]          reg_rdata
);

{% for register in registers %}
logic[DATA_WIDTH-1:0]     {{ register.name }};
{% endfor %}

{% for register in registers %}
localparam int {{ (register.name + "_addr") | upper }} = 'h{{ "%x" | format(register.offset) }};
{% endfor %}

{% for register in registers %}
    {% if (register.w1_flds | length) > 0 %}
logic   [DATA_WIDTH/8-1:0] {{register.name}}_cnt;
always @(posedge reg_clk or negedge reg_rstn)
begin
    if(~reg_rstn)
    begin
        {{register.name}}_cnt <= {(DATA_WIDTH/8){1'd1}};
    end
    else if(reg_wr && (reg_addr == {{(register.name + "_addr") | upper}}))
    begin
        {{register.name}}_cnt <= (~reg_we) & {{register.name}}_cnt;
    end
end
    {% endif %}
{% endfor %}

{% for register in registers %}
    {% set rw_update_flds = register.write_update_flds + register.read_update_flds %}
    {% if (rw_update_flds | length) > 0 %}
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        {% for field in rw_update_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
        {% endfor %}
    end
        {% if (register.write_update_flds | length ) > 0 %}
    else if(reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }})) 
    begin
            {% for field in register.write_update_flds %}
                {% set pos_m = (field.msb / 8) | int %}
                {% set pos_l = (field.lsb / 8) | int %}
                {% for pos in range(pos_l,pos_m+1)[::-1] %}
                    {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
                    {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
                    {% set value = 
                            "{"+"{}".format(msb-lsb+1)+"{1'd1}}" if field.access == "WS" else
                            "{}".format(msb-lsb+1)+"'d0" if field.access == "WC" else
                            "((~reg_wdata[{}:{}])&{}[{}:{}])".format(msb,lsb,register.name,msb,lsb) if field.access == "W1C" else
                            "((reg_wdata[{}:{}])|{}[{}:{}])".format(msb,lsb,register.name,msb,lsb) if field.access == "W1S" else
                            "((reg_wdata[{}:{}])^{}[{}:{}])".format(msb,lsb,register.name,msb,lsb) if field.access == "W1T" else
                            "((reg_wdata[{}:{}])&{}[{}:{}])".format(msb,lsb,register.name,msb,lsb) if field.access == "W0C" else
                            "((~reg_wdata[{}:{}])|{}[{}:{}])".format(msb,lsb,register.name,msb,lsb) if field.access == "W0S" else
                            "((~reg_wdata[{}:{}])^{}[{}:{}])".format(msb,lsb,register.name,msb,lsb) if field.access == "W0T" else
                            "reg_wdata[{}:{}]".format(msb,lsb)
                    %}
                    {% if field.access == "RWP" %}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= unlk_{{field.name}} & reg_we[{{pos}}] ? {{value}} : {{ register.name }}[{{ msb }}:{{ lsb }}];
                    {% elif field.access == "W1" %}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= reg_we[{{pos}}] & {{register.name}}_cnt[{{pos}}] ? {{value}} : {{ register.name }}[{{ msb }}:{{ lsb }}];
                    {% else %}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= reg_we[{{pos}}] ? {{value}} : {{ register.name }}[{{ msb }}:{{ lsb }}];
                    {% endif %}
                {% endfor %}
            {% endfor %}
    end
        {% endif %}
        {% if (register.read_update_flds | length ) > 0 %}
    else if(reg_rd && (reg_addr == {{ (register.name + "_addr") | upper }})) 
    begin
            {% for field in register.read_update_flds %}
                {% set value = 
                        "{"+"{}".format(field.msb-field.lsb+1)+"{1'd1}}" if field.access in ["RS","WRS"] else
                        "{}".format(field.msb-field.lsb+1)+"'d0" if field.access in ["RC","WRC"] else
                        "{}".format(field.msb-field.lsb+1)+"'d0"
                %}
        {{ register.name }}[{{ field.msb  }}:{{ field.lsb }}] <= {{value}};
            {% endfor %}
    end
        {% endif %}
        {% if ((register.hw_update_flds | length ) + (register.wo_flds | length)) > 0 %}
    else
    begin
        {% for field in register.hw_update_flds %}
            {{ register.name }}[{{ field.msb  }}:{{ field.lsb }}] <= hw_{{field.name}};
        {% endfor %}
        {% for field in register.wo_flds %}
            {{ register.name }}[{{ field.msb  }}:{{ field.lsb }}] <= {{field.msb-field.lsb+1}}'d0;
        {% endfor %}
    end
        {% endif %}
end
    {% elif (register.hw_update_flds | length ) > 0 %}
        {% for field in register.hw_update_flds%}
assign {{ register.name }}[{{ field.msb  }}:{{ field.lsb }}] = hw_{{field.name}};
        {% endfor %}
    {% endif %}
    {% for field in register.output_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% for field in register["-_flds"] %}
assign {{register.name}}[{{field.msb}}:{{field.lsb}}] = {{field.msb-field.lsb+1}}'d0;
    {% endfor %}



{% endfor %}

alwyas @(posedge reg_clk or negedge reg_rstn)
begin
    if(~reg_rstn)
    begin
        reg_rdata <= {DATA_WIDTH{1'b0}};
    end
    else if (reg_rd) 
    begin
        case(reg_addr)
{% for register in registers %}
            {{ (register.name + "_addr") | upper }} : reg_rdata <= {{register.name}};
{% endfor %}
            default: reg_rdata <= {DATA_WIDTH{1'b0}};
        endcase
    end
    else
    begin
        reg_rdata <= {DATA_WIDTH{1'b0}};
    end
end



endmodule
