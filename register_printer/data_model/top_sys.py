import textwrap
from .block import Block
from .block_template import BlockTemplate
from .block_instance import BlockInstance


class TopSys:
    def __init__(self, name, addr_width=12, data_width=32):
        self._name = name
        self._addr_width = addr_width
        self._data_width = data_width
        self._version = None
        self._author = None
        self.blocks = []
        self.addr_map = []
        self.block_instances = []
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

    def add_block_instance(self, block_instance):
        self.block_instances.append(block_instance)
        return

    def find_block_by_type(self, block_type):
        for block in self.blocks:
            if block.block_type.upper() == block_type.upper():
                return block
        return None

    def get_blocks_name(self):
        block_names = []
        for block in self.blocks:
            block_names.append(block.block_name)
        return block_names

    def __str__(self):
        result = "-------------------------------\n"
        result += "System: " + str(self.name) + "\n"
        result += "    Author         : " + str(self.author) + "\n"
        result += "    Version        : " + str(self.version) + "\n"
        result += "    Address width  : " + str(self.addr_width) + "\n"
        result += "    Data width     : " + str(self.data_width) + "\n"
        result += "    Blocks:\n"
        for block in self.blocks:
            block_text = str(block)
            block_text = textwrap.indent(block_text, "        ")
            result += block_text + "\n"
        result += "    Address map    :\n"
        for entry in self.addr_map:
            result += "      %s\t@0x%x\n" % (entry['block_instance'], entry['base_address'])
        result += "    Block instances:\n"
        for block_instance in self.block_instances:
            result += "      %s\t@0x%x\n" % (block_instance.name, block_instance.base_address)
        result += "--------------------------------"
        return result

    @staticmethod
    def address_map_to_dict(address_map):
        result = {}
        result["blockType"] = address_map["block_type"]
        result["blockInstance"] = address_map["block_instance"]
        result["baseAddress"] = address_map["base_address"]
        result["blockSize"] = address_map["block_size"]
        return result

    @staticmethod
    def address_map_from_dict(address_map_dict):
        address_map = {}
        address_map["block_type"] = address_map_dict["blockType"]
        address_map["block_instance"] = \
            address_map_dict["blockInstance"]
        address_map["base_address"] = \
            address_map_dict["baseAddress"]
        address_map["block_size"] = \
            address_map_dict["blockSize"]
        return address_map

    def to_dict(self):
        result = {}
        result["name"] = self.name
        result["addressWidth"] = self.addr_width
        result["dataWidth"] = self.data_width
        result["version"] = self.version
        result["author"] = self.author
        result["blockTypes"] = []
        for block in self.blocks:
            result["blockTypes"].append(block.to_dict())
        result["addressMaps"] = []
        for addr_map in self.addr_map:
            addr_map_dict = TopSys.address_map_to_dict(
                addr_map)
            result["addressMaps"].append(addr_map_dict)
        return result

    @staticmethod
    def from_dict(top_sys_dict):
        name = top_sys_dict["name"]
        addr_width = top_sys_dict["addressWidth"]
        data_width = top_sys_dict["dataWidth"]
        version = top_sys_dict["version"]
        author = top_sys_dict["author"]
        top_sys = TopSys(
            name=name,
            addr_width=addr_width,
            data_width=data_width)
        top_sys.version = version
        top_sys.author = author
        block_types_dict = top_sys_dict["blockTypes"]
        for block_type_dict in block_types_dict:
            block_type = Block.from_dict(
                block_type_dict)
            top_sys.blocks.append(block_type)
        addr_maps_dict = top_sys_dict["addressMaps"]
        for addr_map_dict in addr_maps_dict:
            addr_map = TopSys.address_map_from_dict(
                addr_map_dict)
            top_sys.addr_map.append(
                addr_map)
        return top_sys

    @staticmethod
    def from_top_sys_dict(top_sys_dict):
        top_sys = TopSys(
            top_sys_dict["name"],
            top_sys_dict["default_addr_width"],
            top_sys_dict["default_data_width"]
        )
        top_sys.author = top_sys_dict["author"]
        top_sys.version = top_sys_dict["version"]
        for block_inst_dict in top_sys_dict["block_instances"]:

            block = top_sys.find_block_by_type(
                block_inst_dict["type"])
            if block is None:
                block_template = BlockTemplate(
                    block_inst_dict["type"]
                )
                block = Block(
                    top_sys,
                    block_template,
                    addr_width=block_inst_dict["addr_width"],
                    data_width=block_inst_dict["data_width"],
                    size=block_inst_dict["size"]
                )
                top_sys.add_block(block)

            new_block_instance = BlockInstance(
                top_sys,
                block_inst_dict["name"],
                block,
                block_inst_dict["base_address"],
                block_inst_dict["size"]
            )
            top_sys.add_block_to_address_map(
                block_inst_dict["type"],
                block_inst_dict["name"],
                block_inst_dict["base_address"],
                block_inst_dict["size"])
        return top_sys
