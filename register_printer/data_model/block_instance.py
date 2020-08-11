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

        if self.parent is not None:
            self.parent.block_instances.append(self)

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
