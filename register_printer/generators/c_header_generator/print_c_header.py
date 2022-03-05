import os
import os.path
import logging
from .print_c_header_block import print_c_header_block
from .print_c_test import print_c_test
from .print_c_header_sys import print_c_header_sys


LOGGER = logging.getLogger(__name__)


def print_c_header(top_sys, output_path="."):
    LOGGER.debug("Generating C header files...")

    out_dir = os.path.join(
        output_path,
        "regheaders")
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    for block in top_sys.blocks:
        print_c_header_block(block, out_dir)

    print_c_header_sys(top_sys, out_dir)
    print_c_test(top_sys, out_dir)
    LOGGER.debug("C header files generated in directory %s", out_dir)
    return
