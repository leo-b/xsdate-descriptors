from typing import Any
from typing import Dict
from typing import Optional
from xsdata.codegen.models import Attr
from xsdata.formats.dataclass.filters import Filters
from xsdata.formats.dataclass.generator import DataclassGenerator
from xsdata.models.config import GeneratorConfig
from xsdata.utils.objects import literal_value


class ExtGenerator(DataclassGenerator):
    """Python code generator that uses descriptors."""

    @classmethod
    def init_filters(cls, config: GeneratorConfig) -> Filters:
        filters = ExtFilters(config)
        filters.import_patterns["xsdata_ext.xsdata_ext"] = {
            "XmlDateDescriptor": ["=XmlDateDescriptor("],
        }
        return filters

class ExtFilters(Filters):
    def field_default_value(self, attr: Attr, ns_map: Optional[Dict] = None) -> Any:
        result = super().field_default_value(attr=attr, ns_map=ns_map)
        type_names = { self.type_name(x) for x in attr.types }
        assert len(type_names) == 1
        if 'XmlDate' in type_names:
            result = f"XmlDateDescriptor(default={literal_value(result)})"
        return result
