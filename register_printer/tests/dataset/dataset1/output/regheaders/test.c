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
    single_test("Instance2", 0x10000, 0x10, 0x102);
    single_test("Instance3", 0x20000, 0x10000, 0x102);
    return 0;
}