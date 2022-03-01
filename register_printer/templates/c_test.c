void single_test(char* inst, uint32_t addr, uint32_t size, uint32_t def_val) {
    if (*(volatile uint32_t *)(addr) != def_val) {
        printk("E: %s base err/n", inst);
    }
    if (*(volatile uint32_t *)(addr + size - 4) != def_val) {
        printk("E: %s end err/n", inst);
    }
    return;
}


int main() {
    {% for test_parameters in test_parameters_list %}
    single_test("{{ test_parameters.instance_name }}", 0x{{ "%x" | format(test_parameters.base_address) }}, 0x{{ "%x" | format(test_parameters.block_size) }}, 0x{{ "%x" | format(test_parameters.default_value) }});
    {% endfor %}
    return 0;
}
