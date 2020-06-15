class BlockInstance:

    def __init__(self,
                 parent,
                 name,
                 block,
                 base_address,
                 block_size,
                 addr_width=None,
                 data_width=None):
        self.parent = parent
        self.name = name
        self.block = block
        self.base_address = base_address
        self.block_size = block_size
        self.addr_width = addr_width
        self.data_width = data_width

        if self.parent is not None:
            self.parent.block_instances.append(self)

        return
