from .block import *


class TopSys:
    def __init__(self, name, addr_width=12, data_width=32):
        self._name = name
        self._addr_width = addr_width
        self._data_width = data_width
        self._version = None
        self._author = None
        self.blocks = []
        self.addr_map = []
        return

    @property
    def name(self):
        return self._name

    @property
    def addr_width(self):
        return self._addr_width

    @addr_width.setter
    def addr_width(self, addr_width):
        self._addr_width = addr_width
        return

    @property
    def data_width(self):
        return self._data_width

    @data_width.setter
    def data_width(self, data_width):
        self._data_width = data_width
        return

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version
        return

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        self._author = author
        return

    def add_block(self, block):
        self.blocks.append(block)
        return

    def add_block_to_address_map(self, block_type, block_instance, base_address, block_size):
        address_map_entry = {
            "block_type": block_type,
            "block_instance": block_instance,
            "base_address": base_address,
            "block_size": block_size
        }
        self.addr_map.append(address_map_entry)
        return

    def find_block_by_name(self, name):
        for block in self.blocks:
            if block.block_name.upper() == name.upper():
                return block
        return None

    def get_blocks_name(self):
        block_names = []
        for block in self.blocks:
            block_names.append(block.block_name)
        return block_names

    def __str__(self):
        result = "-------------------------------\n"
        result += "System " + str(self.name) + "\n"
        result += "    Author         : " + str(self.author) + "\n"
        result += "    Version        : " + str(self.version) + "\n"
        result += "    Address width  : " + str(self.addr_width) + "\n"
        result += "    Data width     : " + str(self.data_width) + "\n"
        result += "Blocks:\n"
        for block in self.blocks:
            result += str(block) + "\n"
        result += "    Address map    :\n"
        for entry in self.addr_map:
            result += "      %s\5@0x%x\n" % (entry['block_inst'], entry['base_addr'])
        result += "--------------------------------"
        return result

    @staticmethod
    def parse(config_file, excels_path):
        top_sys = TopSys("abc", 50, 60)
        # reg_sys = parse_config(opts.config_file)
        # reg_sys.display()
        # reg_sys = parse_excels(reg_sys, opts.work_path)
        return top_sys
