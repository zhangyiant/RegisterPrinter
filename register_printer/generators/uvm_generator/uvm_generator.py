import logging

from .print_uvm import print_uvm


LOGGER = logging.getLogger(__name__)


class UvmGenerator:

    def __init__(self, top_sys, output_path="."):
        self.top_sys = top_sys
        self.output_path = output_path
        return

    def generate(self):
        LOGGER.debug("Generating UVM files...")
        print_uvm(self.top_sys, self.output_path)
        return
