import os
import os.path
import logging
from .print_uvm_block import print_uvm_block
from .print_uvm_sys import print_uvm_sys
from .print_sv_defines import print_sv_defines

LOGGER = logging.getLogger(__name__)


def print_uvm(top_sys, output_path):
    LOGGER.debug("Generating UVM register model...")

    out_dir = os.path.join(
        output_path,
        "regmodels")
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    for block in top_sys.blocks:
        print_uvm_block(block, out_dir)

    print_uvm_sys(top_sys, out_dir)

    print_sv_defines(top_sys, out_dir)

    LOGGER.debug("UVM register model generated in directory %s", out_dir)
    return
