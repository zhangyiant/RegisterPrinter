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
        self._addr_width = addr_width
        self._data_width = data_width

        if self.parent is not None:
            self.parent.block_instances.append(self)

        return

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
    def raw_data_width(self):
        return self._data_width

    @raw_data_width.setter
    def raw_data_width(self, value):
        self._data_width = value
        return
