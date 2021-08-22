from collections import OrderedDict

from manimlib.mobject.svg.tex_mobject import Tex
from manimlib.utils.config_ops import digest_config

import re


class Registry(OrderedDict):
    """An ordered dictionary with additional methods to allow easy popping an indexing."""

    def register(self, item, key=None):
        """Adds an item to the registry.

        Args:
            item: The item to add.
            key: The key under which to add the item. If None, picks '__' + str(len(self))
        """
        if key is None:
            key = "__" + str(len(self))
        self[key] = item

    def pop(self, key=None):
        """Pops an item from the registry.

        If no key is specified, pops the last item. If a key is specified, pops the corresponding key/value pair.

        Args:
            key: If provided, will pop the given key.

        Returns:
            The value for the popped item.
        """
        if key is None:
            return super().popitem()[1]
        return super().pop(key)

    def get_index(self, ix):
        """Returns the value for the ixth item in the ordered dictionary.

        Args:
            ix (int): The index to get the value for.

        Returns:
            The value for the item at the given index.
        """
        return list(self.items())[ix]


class EasyTex(Tex):
    """Class to make dealing with LaTex in manim slightly easier in most (but not all) cases.

    Args:
        tex_string (str): The LaTex string to display.
        split_regex (str): The regex used to split items passed to manim's Tex class.
        **kwargs: Any additional keyword arguments to manim's Tex class.
    """

    CONFIG = {
        "arg_separator": " ",
    }

    def __init__(self, tex_string, split_regex=r"\s", **kwargs):
        digest_config(self, kwargs)
        tex_strings = re.split(split_regex, tex_string)
        super().__init__(*tex_strings, **kwargs)
