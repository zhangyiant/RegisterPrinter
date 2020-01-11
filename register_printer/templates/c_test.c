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
    {% for addr_map_entry in top_sys.addr_map %}
    {% set block = top_sys.find_block_by_type(addr_map_entry["block_type"]) %}
    {% set default_value = block.registers[0].calculate_register_default() %}
    single_test("{{ addr_map_entry["block_instance"] }}", 0x{{ "%x" | format(addr_map_entry["base_address"]) }}, 0x{{ "%x" | format(addr_map_entry["block_size"]) }}, 0x{{ "%x" | format(default_value) }});
    {% endfor %}
    return 0;
}
