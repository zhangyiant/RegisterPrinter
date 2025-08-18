`ifndef {{name | upper}}_CFG_BASE_SEQ__SV
`define {{name | upper}}_CFG_BASE_SEQ__SV

class {{name | lower}}_cfg_base_seq extends uvm_sequence;
    `uvm_object_utils({{name | lower}}_cfg_base_seq)

    {{name | lower}}_reg_model  m_reg_model;
    uvm_status_e reg_st;

    `include "{{name | lower}}_reg_vars.svh"
    `include "{{name | lower}}_reg_vars_def_cons.svh"
    `include "{{name | lower}}_reg_covergroup.svh"


    extern function new(string name="{{name | lower}}_cfg_base_seq");
    extern virtual task body();

endclass: {{name | lower}}_cfg_base_seq

function {{name | lower}}_cfg_base_seq::new(string name="{{name | lower}}_cfg_base_seq");
    super.new(name);
    `create_{{name | lower}}_reg_model_covergroup
endfunction: new

task {{name | lower}}_cfg_base_seq::body();
    `include "{{name | lower}}_reg_cfg_body.svh"
    m_reg_model.update(reg_st);
endtask: body
`endif
