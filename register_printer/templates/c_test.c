#include "test_common.h"
typedef struct {
    char* name;
    uint32_t addr;
    uint32_t resetvalue;
    uint32_t mask;
    char* access_type;
    char* user_visible;
} registet_s;

registet_s register_inst[] = {
    {% for field in fields %}
    [{{loop.index0}}] = {
        .name = "{{field.name}}",
        .addr = {{field.addr}},
        .resetvalue = {{field.default}},
        .mask = {{field.mask}},
        .access_type = "RW",
        .user_visible = "PUB",
    },
    {% endfor %}
};
const uint32_t  ttl_register_num = sizeof register_inst / sizeof register_inst[0];
int main() {
    puts("start register test.\n");
    for (int i=0; i<ttl_register_num; i++) {
        int rdata = 0;
        *(volatile int *) (register_inst[i].addr) = (0xa5a5a5a5 & register_inst[i].mask);
        rdata = *(volatile int *) (register_inst[i].addr);

        if ((rdata & register_inst[i].mask) != (0xa5a5a5a5 & register_inst[i].mask)) {
            printk("E: register test 0xa5a5a5a5: %0d read mismatch (%0x,%0x).\n",i,(rdata & register_inst[i].mask),(0xa5a5a5a5 & register_inst[i].mask));
        } else {
            printk("register test 0xa5a5a5a5: %0d read pass.\n",i);
        }
        
        *(volatile int *) (register_inst[i].addr) = (0x5a5a5a5a & register_inst[i].mask);
        rdata = *(volatile int *) (register_inst[i].addr);

        if ((rdata & register_inst[i].mask) != (0x5a5a5a5a & register_inst[i].mask)) {
            printk("E: register test 0x5a5a5a5a: %0d read mismatch (%0x,%0x).\n",i,(rdata & register_inst[i].mask),(0x5a5a5a5a & register_inst[i].mask));
        } else {
            printk("register test 0x5a5a5a5a: %0d read pass.\n",i);
        }
    }
    gm_sim_end();
    return 0;
}
