import inspect
from enum import Enum
from abc import ABC, abstractmethod
from database import BaseModel


class StatusCode(Enum):
    OK = 200,
    FAIL = 400


class Builder(ABC):
    @abstractmethod
    def build(self):
        pass

    def get_attributes(self, obj):
        result = []
        for attr in inspect.getmembers(obj):
            if not attr[0].startswith('_'):
                if not inspect.ismethod(attr[1]):
                    result.append(attr)

        return result


class ResponseBuilder(Builder):
    def __init__(self, status=StatusCode.OK):
        self.set_status(status)

    def set_status(self, status):
        if isinstance(status, StatusCode):
            if type(status.value) == tuple:
                self.status = status.value[0]
            else:
                self.status = status.value
        else:
            self.status = status

        return self

    def add_attribute(self, name, value, **kwargs):
        self.__setattr__(name, value)
        for key in kwargs:
            self.__setattr__(key, kwargs.get(key))
        return self

    def add_attribute_status(self, name, status: StatusCode):
        status_name = status.name
        self.__setattr__(name, status_name)
        return self

    def add_list(self, name, list):
        self.__setattr__(name, list)
        return self

    def add_object(self, name, obj):
        self.__setattr__(name, obj)
        return self

    def build(self):
        attrs = super(ResponseBuilder, self).get_attributes(self)
        attrs.reverse()
        self.__setattr__("result", "{")
        for attr in attrs:
            key = attr[0]
            value = attr[1]
            if type(value) == str:
                self.result += f'"{key}": "{value}", '
            elif type(value) == int or type(value) == float:
                self.result += f'"{key}": {value}, '
            elif type(value) == list:
                list_str = f'"{key}": ['
                for el in value:
                    if type(el) == tuple and len(el) == 2:
                        list_str += f'"{el[0]}": "{el[1]}", '
                    elif type(el) == dict:
                        for k in el.keys():
                            list_str += f'"{k}": "{el.get(k)}", '
                    elif isinstance(el, BaseModel):
                        attrs = super(ResponseBuilder, self).get_attributes(el)
                        obj_str = "{"
                        for at in attrs:
                            ke = at[0]
                            va = at[1]
                            if type(va) == str:
                                obj_str += f'"{ke}": "{va}", '
                            elif type(va) == int or type(va) == float:
                                obj_str += f'"{ke}": {va}, '

                        obj_str = obj_str.strip(', ')
                        obj_str += "}, "
                        list_str += obj_str

                list_str = list_str.strip(', ')
                list_str += '], '
                self.result += list_str
            elif isinstance(value, BaseModel):
                attrs = super(ResponseBuilder, self).get_attributes(value)
                obj_str = f'"{key}": ' + "{"
                for at in attrs:
                    ke = at[0]
                    va = at[1]
                    if type(va) == str:
                        obj_str += f'"{ke}": "{va}", '
                    elif type(va) == int or type(va) == float:
                        obj_str += f'"{ke}": {va}, '

                obj_str = obj_str.strip(', ')
                obj_str += "}, "
                self.result += obj_str

        self.result = self.result.strip(', ')
        self.result += '}'
        return self.result
