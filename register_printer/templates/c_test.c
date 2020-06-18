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
    {% for block_instance in top_sys.block_instances %}
    {% set block = block_instance.block %}
    {% set default_value = block.registers[0].calculate_register_default() %}
    single_test("{{ block_instance.name }}", 0x{{ "%x" | format(block_instance.base_address) }}, 0x{{ "%x" | format(block_instance.block_size) }}, 0x{{ "%x" | format(default_value) }});
    {% endfor %}
    return 0;
}
