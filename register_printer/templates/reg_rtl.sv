module {{ block.block_type }}_reg
#(
    parameter int ADDR_WIDTH = {{ block.addr_width }}
)
(
    input     reg_clk                                                       ,
    input     reg_rstn                                                      ,
    input     wp_dis                                                        ,
{% for register in registers %}
  {% for field in register.fields %}
    {% set field_bits = field.msb - field.lsb %}
    {% if field.access == "RW" %}
    output logic[{{ '%2s' | format(field_bits) }}: 0]     {{ "%-48s" | format(field.name) }},
    {% elif field.access == "RWP" %}
    output logic[{{ '%2s' | format(field_bits) }}: 0]     {{ "%-48s" | format(field.name) }},
    {% elif field.access == "RC" %}
    input       [{{ '%2s' | format(field_bits) }}: 0]     {{ "%-48s" | format(field.name) }},
    {% elif field.access == "RO" %}
    input       [{{ '%2s' | format(field_bits) }}: 0]     {{ "%-48s" | format(field.name) }},
    {% elif field.access == "RS" %}
    input       [{{ '%2s' | format(field_bits) }}: 0]     {{ "%-48s" | format(field.name) }},
    {% elif field.access == "W1C" %}
    input                   {{ "%-48s" | format(field.name + "_set")}},
    output logic[{{ '%2s' | format(field_bits) }}: 0]     {{ "%-48s" | format(field.name) }},
    {% elif field.access == "W0C" %}
    input                   {{ "%-48s" | format(field.name + "_set")}},
    output logic[{{ '%2s' | format(field_bits) }}: 0]     {{ "%-48s" | format(field.name) }},
    {% elif field.access == "WC" %}
    input                   {{ "%-48s" | format(field.name + "_set")}},
    output logic[{{ '%2s' | format(field_bits) }}: 0]     {{ "%-48s" | format(field.name) }},
    {% elif field.access == "WO" %}
    output logic[{{ '%2s' | format(field_bits) }}: 0]     {{ "%-48s" | format(field.name) }},
    {% elif field.access == "WRC" %}
    output logic[{{ '%2s' | format(field_bits) }}: 0]     {{ "%-48s" | format(field.name) }},
    {% elif field.access == "WRS" %}
    output logic[{{ '%2s' | format(field_bits) }}: 0]     {{ "%-48s" | format(field.name) }},
    {% elif field.access == "WSC" %}
    output logic[{{ '%2s' | format(field_bits) }}: 0]     {{ "%-48s" | format(field.name) }},
    {% elif field.access == "-" %}
    {% endif %}
  {% endfor %}
{% endfor %}
    input                   reg_wr                                          ,
    input                   reg_rd                                          ,
    input       [ 3: 0]     reg_we                                          ,
    input[ADDR_WIDTH-1:0]   reg_addr                                        ,
    input       [31: 0]     reg_wdat                                        ,
    output logic[31: 0]     reg_rdat
);

{% for register in registers %}
logic[31:0]     {{ register.name }};
{% endfor %}

{% for register in registers %}
localparam int {{ (register.name + "_addr") | upper }} = 'h{{ "%x" | format(register.offset) }};
{% endfor %}

{% for register in registers %}
{% if (register.rw_flds | length ) + (register.rwp_flds | length ) + (register.rc_flds | length) + (register.rs_flds | length) + (register.w1c_flds | length) + (register.w0c_flds | length) + (register.wc_flds | length) + (register.wo_flds | length) + (register.wrc_flds | length) + (register.wrs_flds | length)  > 0 %}
always @(posedge reg_clk or negedge reg_rstn) begin
    if(~reg_rstn) begin
    {% for field in register.fields %}
      {% if not field.access in ["RO", "-"] %}
        {{ register.name }}[{{ '%2s' | format(field.msb) }}:{{ "%2s" | format(field.lsb)}}] <= 'h{{ "%x" | format(field.default)}};
      {% endif %}
    {% endfor %}
    end
    {% if (register.rc_flds | length) + (register.wrc_flds | length) + (register.rs_flds | length) + (register.wrs_flds | length) > 0 %}
    else if(reg_rd && (reg_addr == {{ (register.name + "_addr") | upper }})) begin
      {% for field in (register.rc_flds + register.wrc_flds) %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= 0;
      {% endfor %}
      {% for field in (register.rs_flds + register.wrs_flds) %}
      {% set bits = field.msb - field.lsb + 1 %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb}}] <= {{ '{' }}{{ bits }}{{ '{' }}1'b1{{ '}}' }}
      {% endfor %}
    end
    {% endif %}
    {% if (register.rw_flds | length) + (register.rwp_flds | length) + (register.wo_flds | length) + (register.wrc_flds | length) + (register.wrs_flds | length) + (register.rc_flds | length) + (register.rs_flds | length) + (register.w1c_flds | length) + (register.w0c_flds | length) + (register.wc_flds | length) > 0 %}
    else begin
      {% for field in (register.rc_flds + register.rs_flds) %}
        {{ register.name }}[{{ field.msb }}:{{ field.lsb }}] <= {{ field.name }}
      {% endfor %}
      {% for field in register.w1c_flds %}
      {% set pos = (field.msb / 8) | int %}
        {{ register.name }}[{{ field.msb }}] <= {{ field.name }}_set ? 1'b1 : ((reg_wr && reg_addr=={{ (register.name + "_addr") | upper }} && reg_we[{{ pos }}] && reg_wdat[{{ field.msb }}]) ? 1'b0 : {{ register.name }}[{{ field.msb }}]);
      {% endfor %}
      {% for field in register.w0c_flds %}
      {% set pos = (field.msb / 8) | int %}
        {{ register.name }}[{{ field.msb }}] <= {{ field.name }}_set ? 1'b1 : ((reg_wr && reg_addr=={{ (register.name + "_addr") | upper }} && reg_we[{{ pos }}] && (~reg_wdat[{{ field.msb }}])) ? 1'b0 : {{ register.name }}[{{ field.msb }}]);
      {% endfor %}
      {% for field in register.wc_flds %}
      {% set pos = (field.msb / 8) | int %}
        {{ register.name }}[{{ field.msb }}] <= {{ field.name | lower }}_set ? 1'b1 : ((reg_wr && reg_addr=={{ (register.name + "_addr") | upper }} && reg_we[{{ pos }}]) ? 1'b0 : {{ register.name }}[{{ field.msb }}]);
      {% endfor %}
      {% for field in (register.rw_flds + register.rwp_flds + register.wrc_flds + register.wrs_flds + register.wo_flds) %}
      {% set msb = field.msb %}
      {% set lsb = field.lsb %}
      {% set reg_name = register.name %}
      {% set reg_offset = (register.name + "_addr") | upper %}
        {%if field.access == "WO" %}
          {% if msb < 8 %}
        {{ reg_name }}[{{ msb }}:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[0]) ? reg_wdat[{{ msb }}:{{ lsb }}] : 0;
          {% elif msb < 16 %}
            {% if lsb < 8 %}
        {{ reg_name }}[{{ msb }}:8] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[1]) ? reg_wdat[{{ msb }}:8] : 0;
        {{ reg_name }}[7:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[0]) ? reg_wdat[7:{{ lsb }}] : 0;
            {% else %}
        {{ reg_name }}[{{ msb }}:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[1]) ? reg_wdat[{{ msb }}:{{ lsb }}] : 0;
            {% endif %}
          {% elif msb < 24 %}
            {% if lsb < 8 %}
        {{ reg_name }}[{{ msb }}:16] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[2]) ? reg_wdat[{{ msb }}:16] : 0;
        {{ reg_name }}[15:8] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[1]) ? reg_wdat[15:8] : 0;
        {{ reg_name }}[7:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[0]) ? reg_wdat[7:{{ lsb }}] : 0;
            {% elif lsb < 16 %}
        {{ reg_name }}[{{ msb }}:16] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[2]) ? reg_wdat[{{ msb }}:16] : 0;
        {{ reg_name }}[15:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[1]) ? reg_wdat[15:{{ lsb }}] : 0;
            {% else %}
        {{ reg_name }}[{{ msb }}:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[2]) ? reg_wdat[{{ msb }}:{{ lsb }}] : 0;
            {% endif %}
          {% else %}
            {% if lsb < 8 %}
        {{ reg_name }}[{{ msb }}:24] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[3]) ? reg_wdat[{{ msb }}:24] : 0;
        {{ reg_name }}[23:16] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[2]) ? reg_wdat[23:16] : 0;
        {{ reg_name }}[15:8] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[1]) ? reg_wdat[15:8] : 0;
        {{ reg_name }}[7:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[0]) ? reg_wdat[7:{{ lsb }}] : 0;
            {% elif lsb < 16 %}
        {{ reg_name }}[{{ msb }}:24] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[3]) ? reg_wdat[{{ msb }}:24] : 0;
        {{ reg_name }}[23:16] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[2]) ? reg_wdat[23:16] : 0;
        {{ reg_name }}[15:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[1]) ? reg_wdat[15:{{ lsb }}] : 0;
            {% elif lsb < 24 %}
        {{ reg_name }}[{{ msb }}:24] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[3]) ? reg_wdat[{{ msb }}:24] : 0;
        {{ reg_name }}[23:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[2]) ? reg_wdat[23:{{ lsb }}] : 0;
            {% else %}
        {{ reg_name }}[{{ msb }}:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[3]) ? reg_wdat[{{ msb }}:{{ lsb }}] : 0;
            {% endif %}
          {% endif %}
        {% else %}
          {% if field.access == "RWP" %}
            {% set RWP_CONTENT = " && wp_dis" %}
          {% else %}
            {% set RWP_CONTENT = "" %}
          {% endif %}
          {% if msb < 8 %}
        {{ reg_name }}[{{ msb }}:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[0]{{ RWP_CONTENT }}) ? reg_wdat[{{ msb }}:{{ lsb }}] : {{ reg_name }}[{{ msb }}:{{ lsb }}];
          {% elif msb < 16 %}
            {% if lsb < 8 %}
        {{ reg_name }}[{{ msb }}:8] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[1]{{ RWP_CONTENT }}) ? reg_wdat[{{ msb }}:8] : {{ reg_name }}[{{ msb }}:8];
        {{ reg_name }}[7:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[0]{{ RWP_CONTENT }}) ? reg_wdat[7:{{ lsb }}] : {{ reg_name }}[7:{{ lsb }}];
            {% else %}
        {{ reg_name }}[{{ msb }}:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[1]{{ RWP_CONTENT }}) ? reg_wdat[{{ msb }}:{{ lsb }}] : {{ reg_name }}[{{ msb }}:{{ lsb }}];
            {% endif %}
          {% elif msb < 24 %}
            {% if lsb < 8 %}
        {{ reg_name }}[{{ msb }}:16] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[2]{{ RWP_CONTENT }}) ? reg_wdat[{{ msb }}:16] : {{ reg_name }}[{{ msb }}:16];
        {{ reg_name }}[15:8] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[1]) ? reg_wdat[15:8] : {{ reg_name }}[15:8];
        {{ reg_name }}[7:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[0]{{ RWP_CONTENT }}) ? reg_wdat[7:{{ lsb }}] : {{ reg_name }}[7:{{ lsb }}];
            {% elif lsb < 16 %}
        {{ reg_name }}[{{ msb }}:16] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[2]{{ RWP_CONTENT }}) ? reg_wdat[{{ msb }}:16] : {{ reg_name }}[{{ msb }}:16];
        {{ reg_name }}[15:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[1]{{ RWP_CONTENT }}) ? reg_wdat[15:{{ lsb }}] : {{ reg_name }}[15:{{ lsb }}];
            {% else %}
        {{ reg_name }}[{{ msb }}:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[2]{{ RWP_CONTENT }}) ? reg_wdat[{{ msb }}:{{ lsb }}] : {{ reg_name }}[{{ msb }}:{{ lsb }}];
            {% endif %}
          {% else %}
            {% if lsb < 8 %}
        {{ reg_name }}[{{ msb }}:24] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[3]{{ RWP_CONTENT }}) ? reg_wdat[{{ msb }}:24] : {{ reg_name }}[{{ msb }}:24];
        {{ reg_name }}[23:16] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[2]{{ RWP_CONTENT }}) ? reg_wdat[23:16] : {{ reg_name }}[23:16];
        {{ reg_name }}[15:8] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[1]{{ RWP_CONTENT }}) ? reg_wdat[15:8] : {{ reg_name }}[15:8];
        {{ reg_name }}[7:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[0]{{ RWP_CONTENT }}) ? reg_wdat[7:{{ lsb }}] : {{ reg_name }}[7:{{ lsb }}];
            {% elif lsb < 16 %}
        {{ reg_name }}[{{ msb }}:24] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[3]{{ RWP_CONTENT }}) ? reg_wdat[{{ msb }}:24] : {{ reg_name }}[{{ msb }}:24];
        {{ reg_name }}[23:16] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[2]{{ RWP_CONTENT }}) ? reg_wdat[23:16] : {{ reg_name }}[23:16];
        {{ reg_name }}[15:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[1]{{ RWP_CONTENT }}) ? reg_wdat[15:{{ lsb }}] : {{ reg_name }}[15:{{ lsb }}];
            {% elif lsb < 24 %}
        {{ reg_name }}[{{ msb }}:24] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[3]{{ RWP_CONTENT }}) ? reg_wdat[{{ msb }}:24] : {{ reg_name }}[{{ msb }}:24];
        {{ reg_name }}[23:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[2]{{ RWP_CONTENT }}) ? reg_wdat[23:{{ lsb }}] : {{ reg_name }}[23:{{ lsb }}];
            {% else %}
        {{ reg_name }}[{{ msb }}:{{ lsb }}] <= (reg_wr && reg_addr == {{ reg_offset }} && reg_we[3]{{ RWP_CONTENT }}) ? reg_wdat[{{ msb }}:{{ lsb }}] : {{ reg_name }}[{{ msb }}:{{ lsb }}];
            {% endif %}
          {% endif %}
        {% endif %}
      {% endfor %}
    {% endif %}
    end
end
{% endif %}
{% for field in (register.rw_flds + register.rwp_flds + register.w1c_flds + register.w0c_flds + register.wc_flds + register.wo_flds + register.wrc_flds + register.wrs_flds) %}
assign {{ field.name }} = {{ register.name }}[{{ field.msb }}:{{ field.lsb }}];
{% endfor %}
{% for field in register.ro_flds %}
  {% if field.name != "-" %}
assign {{ register.name }}[{{ field.msb }}:{{ field.lsb }}] = {{ field.name }};
  {% else %}
assign {{ register.name }}[{{ field.msb }}:{{ field.lsb }}] = 'h0;
  {% endif %}
{% endfor %}

{% endfor %}


always @(negedge reg_rstn or posedge reg_clk) begin
    if (~reg_rstn) begin
        reg_rdat <= 32'h0;
    end
    else if (reg_rd) begin
        case(reg_addr)
        {% for register in registers %}
        {{ "%-48s" | format((register.name + "_addr") | upper) }} : reg_rdat <= {{ register.name }};
        {% endfor %}
        default: reg_rdat <= 32'h0;
        endcase
    end
    else begin
       reg_rdat <= 32'h0;
    end
end

endmodule
