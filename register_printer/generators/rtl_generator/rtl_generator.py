import logging

from .print_rtl import print_rtl


LOGGER = logging.getLogger(__name__)


class RtlGenerator:

    def __init__(self, top_sys, output_path="."):
        self.top_sys = top_sys
        self.output_path = output_path
        return

    def generate(self):
        LOGGER.debug("Generating RTL files...")
        print_rtl(self.top_sys, self.output_path)
        return
