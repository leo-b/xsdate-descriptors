"""custom extensions to xsdata"""

from xsdata.models.datatype import XmlDate, XmlDateTime
import datetime

import dataclasses
def patch_dataclasses_default_descr(dataclass_module):
    if not hasattr(dataclass_module, '_get_field_default_descr'):
        # not already patched
        _get_field_orig = dataclass_module._get_field_default_descr \
                          = dataclasses._get_field
        def make_patched_get_field():
            def _get_field(cls, a_name, a_type, *args, **kwargs):
                orig_attr_is_field = isinstance(getattr(cls, a_name, None),
                                                dataclass_module.Field)
                f = _get_field_orig(cls, a_name, a_type, *args, **kwargs)
                if orig_attr_is_field and hasattr(f.default, '__get__'):
                    # field default is a descriptor object
                    # set the descriptor as class attribute
                    setattr(cls, a_name, f.default)
                    # obtain the default value by calling the descriptors
                    # __get__ method using its class access form
                    f.default = f.default.__get__(None, f)
                return f
            return _get_field
        dataclass_module._get_field = make_patched_get_field()

patch_dataclasses_default_descr(dataclasses)


class DataclassDesc:
    def __init__(self, *, default=None):
        self._default = default
    def __set_name__(self, owner, name):
        self._name = '_' + name
    def __get__(self, obj, type):
        if obj is None:
            return self._default
        return getattr(obj, self._name, self._default)
    def __set__(self, obj, value):
        setattr(obj, self._name, value)



class XmlDateDescriptor(DataclassDesc):
    def __set__(self, obj, value):
        if isinstance(value, str):
            setattr(obj, self._name, XmlDate.from_string(value))
        elif isinstance(value, datetime.datetime):
            setattr(obj, self._name, XmlDate.from_datetime(value))
        elif isinstance(value, datetime.date):
            setattr(obj, self._name, XmlDate.from_date(value))
        else:
            setattr(obj, self._name, value)
