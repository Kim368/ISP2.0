import json
from serializers.obj.serializer import *


class JsonSerializerCreator(SerializerCreator):
    def create_serializer(self) -> ISerializer:
        serializer = JsonSerializer()
        return serializer


class JsonSerializer(ISerializer):
    def dumps(self, obj: object) -> str:
        return json.dumps(object_to_dict(obj), indent=4)

    def loads(self, s: str) -> object:
        return json.loads(s)
