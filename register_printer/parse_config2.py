import re
import os
import logging
from .top_sys import *


LOGGER = logging.getLogger(__name__)


def parse_config(cfg_name):
    LOGGER.debug("Parsing top config file: %s", cfg_name)
    with open(cfg_name, "r") as cfg_fh:
        for line in cfg_fh.readlines():
            line = line.strip()
            if line == "":
                continue
            elif re.search(":", line):
                [attr, val] = line.split(":")
                attr = attr.strip()
                val = val.strip()
                if attr == "Top":
                    top_sys = TopSys(val)
                elif attr == "AddrWidth":
                    top_sys.addr_width = int(val)
                elif attr == "DataWidth":
                    top_sys.data_width = int(val)
                elif attr == "IP":
                    bsets = val.split(",")
                    for i in range(0, len(bsets) - 1):
                        bsets[i] = bsets[i].strip()
                    if len(bsets) < 3:
                        raise Exception("Config file IP settings are too few, at least 2")
                    else:
                        baddr = int(bsets[1], 16) # base address
                        bsize = int(bsets[2], 16) # size
                        if len(bsets) == 3:
                            bsets.append(top_sys.addr_width)
                        if len(bsets) == 4:
                            bsets.append(top_sys.data_width)
                        if len(bsets) > 3 and bsets[3] == "":  # use system address width
                            bsets[3] = sys.sys_addr_width
                        if len(bsets) > 4 and bsets[4] == "":  # use system data width
                            bsets[4] = top_sys.data_width
                        [btype, binst] = bsets[0].split('-')
                        btype = bytpe.strip()
                        binst = binst.strip()
                        baddr_len = int(bsets[3])
                        bdata_len = int(bsets[4])
                        if top_sys.find_block_by_name(btype) is None:
                            top_sys.add_block(btype, bsize, baddr_len, bdata_len)
                        top_sys.add_block_to_addrmap(btype, binst, baddr, bsize)
                elif attr == "Author":
                    top_sys.author = val.strip()
                elif attr == "Version":
                    top_sys.version = val.strip()
    return top_sys
