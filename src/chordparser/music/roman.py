class Roman:
    def __init__(self, root, quality, inversion):
        self.root = root
        self.quality = quality
        self.inversion = inversion
        self._build_notation()

    def _build_notation(self):
        inv_str = "".join(map(str, self.inversion))
        self.notation = self.root + self.quality + inv_str

    def __repr__(self):
        return self.notation

    def __eq__(self, other):
        if isinstance(other, Roman):
            return (
                self.root == other.root and
                self.quality == other.quality and
                self.inversion == other.inversion
            )
        if isinstance(other, str):
            return str(self) == other
        return NotImplemented
