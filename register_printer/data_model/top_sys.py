import textwrap
import logging
from .block import Block
from .block_template import BlockTemplate
from .block_instance import BlockInstance


LOGGER = logging.getLogger(__name__)

def find_block_template_by_block_type(block_template_list, block_type):
    block_template = None
    for temp_block_template in block_template_list:
        if temp_block_template.block_type.upper() == \
            block_type.upper():
            block_template = temp_block_template
            break
    return block_template

class TopSys:
    def __init__(self, name, addr_width=12, data_width=32):
        self._name = name
        self._addr_width = addr_width
        self._data_width = data_width
        self._version = None
        self._author = None
        self.blocks = []
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

    @property
    def block_templates(self):
        block_templates = []
        for block in self.blocks:
            if block.block_template not in block_templates:
                block_templates.append(block.block_template)
        return block_templates

    def add_block(self, block):
        self.blocks.append(block)
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
        result += "    Block instances:\n"
        for block_instance in self.block_instances:
            result += "      %s(%s)\t@0x%x\t%s\t%s\n" % (
                block_instance.name,
                block_instance.block.block_type,
                block_instance.base_address,
                block_instance.block.raw_addr_width,
                block_instance.block.raw_data_width)
        result += "--------------------------------"
        return result

    @staticmethod
    def block_instance_to_dict(block_instance):
        result = {
            "blockType": block_instance.block_type,
            "name": block_instance.name,
            "baseAddress": block_instance.base_address,
            "blockSize": block_instance.block_size,
            "addressWidth": block_instance.block.raw_addr_width,
            "dataWidth": block_instance.block.raw_data_width
        }
        return result

    @staticmethod
    def block_instance_from_dict(block_instance_dict):
        # Todo: Need to associate the block instance to TopSys.
        block_instance = BlockInstance(
            parent=None,
            name=block_instance_dict["name"],
            block=None,
            base_address=block_instance_dict["baseAddress"],
            block_size=block_instance_dict["blockSize"]
        )
        return block_instance

    def to_dict(self):
        result = {
            "name": self.name,
            "addressWidth": self.addr_width,
            "dataWidth": self.data_width,
            "version": self.version,
            "author": self.author,
            "blockInstances": [],
            "blockTemplates": []
        }
        result["blockInstances"] = []
        for block_instance in self.block_instances:
            block_instance_dict = TopSys.block_instance_to_dict(
                block_instance)
            result["blockInstances"].append(block_instance_dict)
        for block_template in self.block_templates:
            block_template_dict = block_template.to_dict()
            result["blockTemplates"].append(block_template_dict)
        return result

    @staticmethod
    def from_dict(top_sys_dict):
        block_template_dict_list = top_sys_dict["blockTemplates"]
        top_sys = TopSys.generate_top_sys(
            top_sys_dict,
            block_template_dict_list)
        return top_sys

    @staticmethod
    def generate_top_sys(top_sys_dict, block_template_dict_list):

        block_template_list = []
        for block_template_dict in block_template_dict_list:
            block_template = BlockTemplate.from_dict(block_template_dict)
            block_template_list.append(block_template)

        top_sys = TopSys(
            top_sys_dict["name"],
            top_sys_dict["addressWidth"],
            top_sys_dict["dataWidth"]
        )
        top_sys.author = top_sys_dict["author"]
        top_sys.version = top_sys_dict["version"]
        for block_inst_dict in top_sys_dict["blockInstances"]:

            block = top_sys.find_block_by_type(
                block_inst_dict["blockType"])
            if block is None:
                block_template = find_block_template_by_block_type(
                    block_template_list,
                    block_inst_dict["blockType"]
                )

                block = Block(
                    top_sys,
                    block_template,
                    addr_width=block_inst_dict["addressWidth"],
                    data_width=block_inst_dict["dataWidth"]
                )
                top_sys.add_block(block)

            block_instance = BlockInstance(
                top_sys,
                block_inst_dict["name"],
                block,
                block_inst_dict["baseAddress"],
                block_inst_dict["blockSize"]
            )
            top_sys.block_instances.append(block_instance)

        for blk in top_sys.blocks:
            if len(blk.registers) == 0:
                LOGGER.warning(
                    "No register definition for block %s",
                    blk.block_type)
        return top_sys
