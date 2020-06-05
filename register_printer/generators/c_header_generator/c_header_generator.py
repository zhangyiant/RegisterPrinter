import logging

from .print_c_header import print_c_header


LOGGER = logging.getLogger(__name__)


class CHeaderGenerator:

    def __init__(self, top_sys, output_path="."):
        self.top_sys = top_sys
        self.output_path = output_path
        return

    def generate(self):
        LOGGER.debug("Generating C header files...")
        print_c_header(self.top_sys, self.output_path)
        return
