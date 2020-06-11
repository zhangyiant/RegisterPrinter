import logging

from .print_doc import print_doc


LOGGER = logging.getLogger(__name__)


class DocGenerator:

    def __init__(self, top_sys, output_path="."):
        self.top_sys = top_sys
        self.output_path = output_path
        return

    def generate(self):
        LOGGER.debug("Generating documentation files...")
        print_doc(self.top_sys, self.output_path)
        return
