import textwrap
import logging
from .register_template import RegisterTemplate


LOGGER = logging.getLogger(__name__)


class Block:
    def __init__(
            self,
            parent,
            block_template,
            addr_width=None,
            data_width=None):
        self.parent = parent
        self._block_template = block_template
        self._addr_width = addr_width
        self._data_width = data_width
        self._registers = None
        return

    @property
    def block_type(self):
        return self._block_template.block_type

    @property
    def addr_width(self):
        if self._addr_width is not None:
            return self._addr_width

        if self.parent is not None:
            return self.parent.addr_width

        return None

    @property
    def raw_addr_width(self):
        return self._addr_width

    @raw_addr_width.setter
    def raw_addr_width(self, value):
        self._addr_width = value
        return

    @property
    def data_width(self):
        if self._data_width is not None:
            return self._data_width

        if self.parent is not None:
            return self.parent.data_width

        return None

    @property
    def data_width_in_bytes(self):
        if self.data_width % 8 == 0:
            return self.data_width // 8
        else:
            msg = "Block({}) data width({}) is not multiples of 8.".format(
                self.block_type, self.data_width
            )
            LOGGER.error(msg)
            raise Exception(msg)

    @property
    def raw_data_width(self):
        return self._data_width

    @raw_data_width.setter
    def raw_data_width(self, value):
        self._data_width = value
        return

    @property
    def block_template(self):
        return self._block_template

    @block_template.setter
    def block_template(self, value):
        self._block_template = value
        return

    @property
    def registers(self):
        if self._registers is None:
            self._registers = self.block_template.generate_registers(self.data_width)
        return self._registers

    def __str__(self):
        result = "Block " + str(self.block_type) + "\n"
        result += "    Address width: " + str(self.addr_width) + "\n"
        result += "    Data width   : " + str(self.data_width) + "\n"
        result += "    Block templates: \n"
        block_template_string = str(self.block_template)
        block_template_string = textwrap.indent(block_template_string, " " * 8)
        result += block_template_string + "\n"
        result += "    Registers:\n"
        register_strings = []
        for register in self.registers:
            register_string = str(register)
            register_string = textwrap.indent(register_string, "        ")
            register_strings.append(register_string)
        result += "\n".join(register_strings)
        return result
