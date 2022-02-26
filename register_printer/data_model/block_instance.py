import logging

LOGGER = logging.getLogger(__name__)

class BlockInstance:

    def __init__(self,
                 parent,
                 name,
                 block,
                 base_address,
                 block_size):
        self.parent = parent
        self.name = name
        self.block = block
        self.base_address = base_address
        self.block_size = block_size

        self._registers = None

        return

    @property
    def addr_width(self):
        return self.block.addr_width

    @property
    def data_width(self):
        return self.block.data_width

    @property
    def block_type(self):
        return self.block.block_type

    @property
    def size(self):
        return self.block_size

    @property
    def data_width_in_bytes(self):
        if self.data_width % 8 == 0:
            return self.data_width / 8
        else:
            msg = "Block instance({}) data width({}) is not multiples of 8.".format(
                self.name, self.data_width
            )
            LOGGER.error(msg)
            raise Exception(msg)

    def refresh_registers(self):
        self._registers = []
        self.data_width_in_bytes
        return

    @property
    def registers(self):
        return self._registers