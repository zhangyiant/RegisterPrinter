module {{ block.block_type }}_reg
#(
    parameter int ADDR_WIDTH = {{ block.addr_width }}                       ,
    parameter int DATA_WIDTH = {{ block.data_width }}
)
(

    {% for register in registers %}
        {% for field in register.ro_flds %}
            {% set field_bits = field.msb - field.lsb %}
    input  logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       hw_{{ "%-45s" | format(field.name) }},
        {% endfor %}
        {% for field in register.rw_flds %}
            {% set field_bits = field.msb - field.lsb %}
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.rc_flds %}
            {% set field_bits = field.msb - field.lsb %}
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name+"_en") }},
    input  logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       hw_{{ "%-45s" | format(field.name) }},
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.rs_flds %}
            {% set field_bits = field.msb - field.lsb %}
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name+"_en") }},
    input  logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       hw_{{ "%-45s" | format(field.name) }},
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.wrc_flds %}
            {% set field_bits = field.msb - field.lsb %}
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name+"_en") }},
    input  logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       hw_{{ "%-45s" | format(field.name) }},
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.wrs_flds %}
            {% set field_bits = field.msb - field.lsb %}
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name+"_en") }},
    input  logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       hw_{{ "%-45s" | format(field.name) }},
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.wc_flds %}
            {% set field_bits = field.msb - field.lsb %}
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name+"_en") }},
    input  logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       hw_{{ "%-45s" | format(field.name) }},
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.ws_flds %}
            {% set field_bits = field.msb - field.lsb %}
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name+"_en") }},
    input  logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       hw_{{ "%-45s" | format(field.name) }},
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.w1c_flds %}
            {% set field_bits = field.msb - field.lsb %}
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name+"_en") }},
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name) }},
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.w1s_flds %}
            {% set field_bits = field.msb - field.lsb %}
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name+"_en") }},
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name) }},
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.w1t_flds %}
            {% set field_bits = field.msb - field.lsb %}
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name+"_en") }},
    input  logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       hw_{{ "%-45s" | format(field.name) }},
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.w0c_flds %}
            {% set field_bits = field.msb - field.lsb %}
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name+"_en") }},
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name) }},
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.w0s_flds %}
            {% set field_bits = field.msb - field.lsb %}
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name+"_en") }},
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name) }},
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.w0t_flds %}
            {% set field_bits = field.msb - field.lsb %}
    input  logic [{{ '%2s' | format(           1) }}-1: 0]       hw_{{ "%-45s" | format(field.name+"_en") }},
    input  logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       hw_{{ "%-45s" | format(field.name) }},
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.wo_flds %}
            {% set field_bits = field.msb - field.lsb %}
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.w1_flds %}
            {% set field_bits = field.msb - field.lsb %}
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
        {% for field in register.rwp_flds %}
            {% set field_bits = field.msb - field.lsb %}
    input                                  unlk_{{ "%-48s" | format(field.name) }},
    output logic [{{ '%2s' | format(field_bits+1) }}-1: 0]       {{ "%-48s" | format(field.name) }},
        {% endfor %}
    {% endfor %}

    input  logic                            reg_clk                              ,
    input  logic                            reg_rstn                             ,

    input  logic                            reg_wr                               ,
    input  logic                            reg_rd                               ,
    input  logic [DATA_WIDTH/8-1: 0]        reg_we                               ,
    input  logic [ADDR_WIDTH-1: 0]          reg_addr                             ,
    input  logic [DATA_WIDTH-1: 0]          reg_wdata                            ,
    output logic [DATA_WIDTH-1: 0]          reg_rdata
);

{% for register in registers %}
logic[DATA_WIDTH-1:0]     {{ register.name }};
{% endfor %}

{% for register in registers %}
localparam int {{ (register.name + "_addr") | upper }} = 'h{{ "%x" | format(register.offset) }};
{% endfor %}

{% for register in registers %}
    {% if (register.ro_flds | length) > 0 %}
//{{register.name}}.ro_flds
    {% for field in register.ro_flds %}
assign {{ register.name }}[{{ field.msb  }}:{{ field.lsb }}] = hw_{{field.name}};
    {% endfor %}
    {% endif %}
    {% if (register.rw_flds | length) > 0 %}
//{{register.name}}.rw_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
    {% for field in register.rw_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
    {% endfor %}
    end
    else if(reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }})) 
    begin
    {% for field in register.rw_flds %}
        {% set pos_m = (field.msb / 8) | int %}
        {% set pos_l = (field.lsb / 8) | int %}
        {% for pos in range(pos_l,pos_m+1)[::-1] %}
            {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
            {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
            {% set value = "reg_wdata[{}:{}]".format(msb,lsb)%}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= reg_we[{{pos}}] ? {{value}} : {{ register.name }}[{{ msb }}:{{ lsb }}];
        {% endfor %}
    {% endfor %}
    end
end
    {% for field in register.rw_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.rc_flds | length) > 0 %}
//{{register.name}}.rc_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
    {% for field in register.rc_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
    {% endfor %}
    end
    else
    begin
    {% for field in register.rc_flds %}
        {% set value = "{}".format(field.msb-field.lsb+1)+"'d0"%}
        {{ register.name }}[{{ field.msb  }}:{{ field.lsb }}] <= hw_{{field.name}}_en ? hw_{{field.name}} : reg_rd && (reg_addr == {{ (register.name + "_addr") | upper }}) ? {{value}} : {{ register.name }}[{{ field.msb  }}:{{ field.lsb }}];
    {% endfor %}
    end
end
    {% for field in register.rc_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.rs_flds | length) > 0 %}
//{{register.name}}.rs_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
    {% for field in register.rs_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
    {% endfor %}
    end
    else
    begin
        {% for field in register.rs_flds %}
        {% set value = "{"+"{}".format(field.msb-field.lsb+1)+"{1'b1}}"%}
        {{ register.name }}[{{ field.msb  }}:{{ field.lsb }}] <= hw_{{field.name}}_en ? hw_{{field.name}} : reg_rd && (reg_addr == {{ (register.name + "_addr") | upper }}) ? {{value}} : {{ register.name }}[{{ field.msb  }}:{{ field.lsb }}];
        {% endfor %}
    end
end
    {% for field in register.rs_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.wrc_flds | length) > 0 %}
//{{register.name}}.wrc_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
    {% for field in register.wrc_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
    {% endfor %}
    end
    else
    begin
    {% for field in register.wrc_flds %}
        {% set pos_m = (field.msb / 8) | int %}
        {% set pos_l = (field.lsb / 8) | int %}
        {% for pos in range(pos_l,pos_m+1)[::-1] %}
            {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
            {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
            {% set value = "{}".format(field.msb-field.lsb+1)+"'d0" %}
        {{ register.name }}[{{ field.msb  }}:{{ field.lsb }}] <= hw_{{field.name}}_en ? hw_{{field.name}} : reg_rd && (reg_addr == {{ (register.name + "_addr") | upper }}) ? {{value}} : reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }}) && reg_we[{{pos}}] ? reg_wdata[{{msb}}:{{lsb}}] : {{ register.name }}[{{ msb }}:{{ lsb }}];
        {% endfor %}
    {% endfor %}
    end
end
    {% for field in register.wrc_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.wrs_flds | length) > 0 %}
//{{register.name}}.wrs_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
    {% for field in register.wrs_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
    {% endfor %}
    end
    else
    begin
    {% for field in register.wrs_flds %}
        {% set pos_m = (field.msb / 8) | int %}
        {% set pos_l = (field.lsb / 8) | int %}
        {% for pos in range(pos_l,pos_m+1)[::-1] %}
            {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
            {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
            {% set value = "{"+"{}".format(field.msb-field.lsb+1)+"{1'd1}}" %}
        {{ register.name }}[{{ field.msb  }}:{{ field.lsb }}] <= hw_{{field.name}}_en ? hw_{{field.name}} : reg_rd && (reg_addr == {{ (register.name + "_addr") | upper }}) ? {{value}} : reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }}) && reg_we[{{pos}}] ? reg_wdata[{{msb}}:{{lsb}}] : {{ register.name }}[{{ msb }}:{{ lsb }}];
        {% endfor %}
    {% endfor %}
    end
end
    {% for field in register.wrs_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.wc_flds | length) > 0 %}
//{{register.name}}.wc_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
    {% for field in register.wc_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
    {% endfor %}
    end
    else
    begin
    {% for field in register.wc_flds %}
        {% set pos_m = (field.msb / 8) | int %}
        {% set pos_l = (field.lsb / 8) | int %}
        {% for pos in range(pos_l,pos_m+1)[::-1] %}
            {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
            {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
            {% set value = "{}".format(msb-lsb+1)+"'d0" %}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= hw_{{field.name}}_en ? hw_{{field.name}} : reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }}) && reg_we[{{pos}}] ? {{value}} : {{ register.name }}[{{ msb }}:{{ lsb }}];
        {% endfor %}
    {% endfor %}
    end
end
    {% for field in register.wc_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.ws_flds | length) > 0 %}
//{{register.name}}.ws_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        {% for field in register.ws_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
        {% endfor %}
    end
    else
    begin
        {% for field in register.ws_flds %}
            {% set pos_m = (field.msb / 8) | int %}
            {% set pos_l = (field.lsb / 8) | int %}
            {% for pos in range(pos_l,pos_m+1)[::-1] %}
                {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
                {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
                {% set value = "{"+"{}".format(msb-lsb+1)+"{1'd1}}" %}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= hw_{{field.name}}_en ? hw_{{field.name}} : reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }}) && reg_we[{{pos}}] ? {{value}} : {{ register.name }}[{{ msb }}:{{ lsb }}];
            {% endfor %}
        {% endfor %}
    end
end
    {% for field in register.ws_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.w1c_flds | length) > 0 %}
//{{register.name}}.w1c_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        {% for field in register.w1c_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
        {% endfor %}
    end
    else
    begin
        {% for field in register.w1c_flds %}
            {% set pos_m = (field.msb / 8) | int %}
            {% set pos_l = (field.lsb / 8) | int %}
            {% for pos in range(pos_l,pos_m+1)[::-1] %}
                {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
                {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= hw_{{field.name}}_en ? hw_{{field.name}} : reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }}) && reg_we[{{pos}}] ? (~reg_wdata[{{msb}}:{{lsb}}]) & {{ register.name }}[{{ msb }}:{{ lsb }}]: {{ register.name }}[{{ msb }}:{{ lsb }}];
            {% endfor %}
        {% endfor %}
    end
end
    {% for field in register.w1c_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.w1s_flds | length) > 0 %}
//{{register.name}}.w1s_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        {% for field in register.w1s_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
        {% endfor %}
    end
    else
    begin
        {% for field in register.w1s_flds %}
            {% set pos_m = (field.msb / 8) | int %}
            {% set pos_l = (field.lsb / 8) | int %}
            {% for pos in range(pos_l,pos_m+1)[::-1] %}
                {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
                {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= hw_{{field.name}}_en ? hw_{{field.name}} : reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }}) && reg_we[{{pos}}] ? reg_wdata[{{msb}}:{{lsb}}] | {{ register.name }}[{{ msb }}:{{ lsb }}]: {{ register.name }}[{{ msb }}:{{ lsb }}];
            {% endfor %}
        {% endfor %}
    end
end
    {% for field in register.w1s_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.w1t_flds | length) > 0 %}
//{{register.name}}.w1t_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        {% for field in register.w1t_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
        {% endfor %}
    end
    else
    begin
        {% for field in register.w1t_flds %}
            {% set pos_m = (field.msb / 8) | int %}
            {% set pos_l = (field.lsb / 8) | int %}
            {% for pos in range(pos_l,pos_m+1)[::-1] %}
                {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
                {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= hw_{{field.name}}_en ? hw_{{field.name}} : reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }}) && reg_we[{{pos}}] ?  (reg_wdata[{{msb}}:{{lsb}}] ^ {{ register.name }}[{{ msb }}:{{ lsb }}]) : {{ register.name }}[{{ msb }}:{{ lsb }}];
            {% endfor %}
        {% endfor %}
    end
end
    {% for field in register.w1t_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.w0c_flds | length) > 0 %}
//{{register.name}}.w0c_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        {% for field in register.w0c_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
        {% endfor %}
    end
    else
    begin
        {% for field in register.w0c_flds %}
            {% set pos_m = (field.msb / 8) | int %}
            {% set pos_l = (field.lsb / 8) | int %}
            {% for pos in range(pos_l,pos_m+1)[::-1] %}
                {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
                {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= hw_{{field.name}}_en ? hw_{{field.name}} : reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }}) && reg_we[{{pos}}] ? reg_wdata[{{msb}}:{{lsb}}] & {{ register.name }}[{{ msb }}:{{ lsb }}] : {{ register.name }}[{{ msb }}:{{ lsb }}];
            {% endfor %}
        {% endfor %}
    end
end
    {% for field in register.w0c_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.w0s_flds | length) > 0 %}
//{{register.name}}.w0s_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        {% for field in register.w0s_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
        {% endfor %}
    end
    else
    begin
        {% for field in register.w0s_flds %}
            {% set pos_m = (field.msb / 8) | int %}
            {% set pos_l = (field.lsb / 8) | int %}
            {% for pos in range(pos_l,pos_m+1)[::-1] %}
                {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
                {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= hw_{{field.name}}_en ? hw_{{field.name}} : reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }}) && reg_we[{{pos}}] ? (~reg_wdata[{{msb}}:{{lsb}}]) | {{ register.name }}[{{ msb }}:{{ lsb }}] : {{ register.name }}[{{ msb }}:{{ lsb }}];
            {% endfor %}
        {% endfor %}
    end
end
    {% for field in register.w0s_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.w0t_flds | length) > 0 %}
//{{register.name}}.w0t_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        {% for field in register.w0t_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
        {% endfor %}
    end
    else
    begin
        {% for field in register.w0t_flds %}
            {% set pos_m = (field.msb / 8) | int %}
            {% set pos_l = (field.lsb / 8) | int %}
            {% for pos in range(pos_l,pos_m+1)[::-1] %}
                {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
                {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= hw_{{field.name}}_en ? hw_{{field.name}} : reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }}) && reg_we[{{pos}}] ? (~reg_wdata[{{msb}}:{{lsb}}]) ^ {{ register.name }}[{{ msb }}:{{ lsb }}] : {{ register.name }}[{{ msb }}:{{ lsb }}];
            {% endfor %}
        {% endfor %}
    end
end
    {% for field in register.w0t_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.wo_flds | length) > 0 %}
//{{register.name}}.wo_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        {% for field in register.wo_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
        {% endfor %}
    end
    else if(reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }})) 
    begin
        {% for field in register.wo_flds %}
            {% set pos_m = (field.msb / 8) | int %}
            {% set pos_l = (field.lsb / 8) | int %}
            {% for pos in range(pos_l,pos_m+1)[::-1] %}
                {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
                {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
                {% set value = "reg_wdata[{}:{}]".format(msb,lsb) %}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= reg_we[{{pos}}] ? {{value}} : {{ register.name }}[{{ msb }}:{{ lsb }}];
            {% endfor %}
        {% endfor %}
    end
    else
    begin
        {% for field in register.wo_flds %}
        {{ register.name }}[{{ field.msb  }}:{{ field.lsb }}] <= {{field.msb-field.lsb+1}}'d0;
        {% endfor %}
    end
end
    {% for field in register.wo_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.w1_flds | length) > 0 %}
//{{register.name}}.w1_flds
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
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        {% for field in register.w1_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
        {% endfor %}
    end
    else if(reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }})) 
    begin
        {% for field in register.w1_flds %}
            {% set pos_m = (field.msb / 8) | int %}
            {% set pos_l = (field.lsb / 8) | int %}
            {% for pos in range(pos_l,pos_m+1)[::-1] %}
                {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
                {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
                {% set value = "reg_wdata[{}:{}]".format(msb,lsb) %}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= reg_we[{{pos}}] & {{register.name}}_cnt[{{pos}}] ? {{value}} : {{ register.name }}[{{ msb }}:{{ lsb }}];
            {% endfor %}
        {% endfor %}
    end
end
    {% for field in register.w1_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register.rwp_flds | length) > 0 %}
//{{register.name}}.rwp_flds
always @(posedge reg_clk or negedge reg_rstn) 
begin
    if(~reg_rstn) 
    begin
        {% for field in register.rwp_flds %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ field.msb - field.lsb + 1}}'h{{ "%x" | format(field.default)}};
        {% endfor %}
    end
    else if(reg_wr && (reg_addr == {{ (register.name + "_addr") | upper }})) 
    begin
        {% for field in register.rwp_flds %}
            {% set pos_m = (field.msb / 8) | int %}
            {% set pos_l = (field.lsb / 8) | int %}
            {% for pos in range(pos_l,pos_m+1)[::-1] %}
                {% set msb = field.msb if field.msb < pos*8 + 7 else pos*8 + 7 %}
                {% set lsb = field.lsb if field.lsb > pos*8  else pos*8 %}
                {% set value = "reg_wdata[{}:{}]".format(msb,lsb) %}
        {{ register.name }}[{{ msb  }}:{{ lsb }}] <= unlk_{{field.name}} & reg_we[{{pos}}] ? {{value}} : {{ register.name }}[{{ msb }}:{{ lsb }}];
            {% endfor %}
        {% endfor %}
    end
end
    {% for field in register.rwp_flds %}
assign {{field.name}} = {{register.name}}[{{field.msb}}:{{field.lsb}}];
    {% endfor %}
    {% endif %}
    {% if (register["-_flds"] | length) > 0 %}
//{{register.name}}.-_flds
    {% for field in register["-_flds"] %}
assign {{register.name}}[{{field.msb}}:{{field.lsb}}] = {{field.msb-field.lsb+1}}'d0;
    {% endfor %}
    {% endif %}

{% endfor %}

always @(posedge reg_clk or negedge reg_rstn)
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
