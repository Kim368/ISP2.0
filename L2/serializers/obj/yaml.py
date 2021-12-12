
import yaml
from serializers.obj.serializer import *


class YamlSerializerCreator(SerializerCreator):
    def create_serializer(self) -> ISerializer:
        serializer = YamlSerializer()
        return serializer


class YamlSerializer(ISerializer):

    def dumps(self, obj: object) -> str:
        return yaml.dump(object_to_dict(obj), sort_keys=False)
    
    def loads(self, s: str) -> object:
        return yaml.full_load(s)
