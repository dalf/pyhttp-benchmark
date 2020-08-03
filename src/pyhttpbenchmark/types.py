from typing import Type, Union
import pathlib

from . import model

Step = Type[model.Step]
Pathlike = Union[str, pathlib.Path]
