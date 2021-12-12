import toml
from serializers.obj.serializer import *


class TomlSerializerCreator(SerializerCreator):
    def create_serializer(self) -> ISerializer:
        serializer = TomlSerializer()
        return serializer


class TomlSerializer(ISerializer):
    def dumps(self, obj: object) -> str:
        return toml.dumps(object_to_dict(obj))
    
    def loads(self, s: str) -> object:
        return toml.loads(s)
