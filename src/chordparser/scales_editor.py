from chordparser.keys import Key
from chordparser.scales import Scale
from chordparser.keys_editor import KeyEditor


class ScaleEditor:
    """
    ScaleEditor class that can create a Scale from a Key (or arguments required to create a Key).

    The ScaleEditor class can create a Scale using the 'create_scale' method by accepting either a Key or the necessary arguments to create a Key (i.e. root, mode and submode). The ScaleEditor can change a scale using the 'change_scale' method.
    """
    KE = KeyEditor()

    def create_scale(self, value, *args, **kwargs):
        """Create a scale from a key or the arguments for creating a key (i.e. root, mode and submode)."""
        if not isinstance(value, Key):
            key = self.KE.create_key(value, *args, **kwargs)
        else:
            key = value
        return Scale(key)

    def change_scale(self, scale, *args, inplace=True, **kwargs):
        """Change the scale by specifying root, mode and/or submode."""
        if not inplace:
            scale = self.create_scale(scale.key)
        self.KE.change_key(scale.key, *args, **kwargs)
        scale.build()
        return scale
