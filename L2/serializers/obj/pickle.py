import pickle
from serializers.obj.serializer import *


class PickleSerializer(ISerializer):
    
    def dumps(self, obj: object) -> str:
        return pickle.dumps(obj)
    
    def loads(self, s: str) -> object:
        return pickle.loads(s)


class PickleSerializerCreator(SerializerCreator):
    
    def create_serializer(self) -> ISerializer:
        serializer = PickleSerializer()
        return serializer
    
    def loads(self, s: str, cls=None) -> object:
        serializer = self.create_serializer()
        obj = serializer.loads(s)
        return obj
    
    def dump(self, obj: object, fp: str) -> None:
        s = self.dumps(obj)
        with open(fp, "wb") as f:
            f.write(s)
    
    def load(self, fp: str, cls=None) -> object:
        with open(fp, "rb") as f:
            s = f.read()
        obj = self.loads(s, cls)
        return obj
