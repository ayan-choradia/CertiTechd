import re
from typing import Any, Iterable, Optional

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.ext.mutable import Mutable


def resolve_table_name(name):
    """Resolves table names to their mapped names."""
    names = re.split("(?=[A-Z])", name)  # noqa
    return "_".join([x.lower() for x in names if x])


@as_declarative()
class Base:
    """
    Base class for SQLAlchemy declarative models, providing an automated tablename generation,
    and a method of converting the model instance to a dictionary. 

    ...

    Attributes:
    ------------------
    id (any): Unique identifier of the Model
    __name__(str): Name of the derived model class.

    Methods:
    ------------------
    __tablename__(self) -> str
         Automatically generates the tablename based on the class name of the model.
    to_dict(self, include: Optional[Iterable] = None, exclude: Optional[Iterable] = None)
        Converts the Model Instance to a Python dictionary with the ability to include and exclude certain attributes of the model.


    """
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return resolve_table_name(self.__name__)

    def to_dict(
        self, include: Optional[Iterable] = None, exclude: Optional[Iterable] = None
    ):
        if include is None:
            include = self.__dict__
        if exclude is None:
            exclude = {}
        else:
            exclude = set(exclude)
        return {
            attrname: getattr(self, attrname)
            for attrname in include
            if attrname not in exclude
        }


class MutableList(Mutable, list):
    """
    Custom List Class that extends both a Mutable and list classes. 
    It provides tracking of operations to a list such as appending and poping elements
    from the list. 

    Methods:
    --------------
    append(self,value) -> None
         Appends a value to a list and marks the MutableList as changed.

    pop(self, index =0) -> Any
        Removes and returns an element from the list then marks the MutableList as changed

    corece(cls, key, value) -> Any
        Ensures that a value is an instance of a MutableList, if it is it returns the value,
        if not it checks if it is a list, if it is it creates a MutableList from it. Else, it tries to create a Mutable instance of it.

    """
    def append(self, value):
        list.append(self, value)
        self.changed()

    def pop(self, index=0):
        value = list.pop(self, index)
        self.changed()
        return value

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value
