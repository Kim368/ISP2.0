def object_to_dict(obj: object):
    if not hasattr(obj, '__dict__'):
        return obj
    _dict = {}
    aa = vars(obj)
    for elem in vars(obj):
        _dict[elem] = object_to_dict(getattr(obj, elem))
    return _dict


def dict_to_object(_dict: dict, cls) -> object:
    obj = cls()
    for elem in _dict:
        setattr(obj, elem, _dict[elem])
    return obj


class ISerializer:
    def dumps(self, obj: object) -> str:
        raise NotImplementedError

    def loads(self, s: str) -> object:
        raise NotImplementedError


class SerializerCreator:

    def create_serializer(self) -> ISerializer:
        raise NotImplementedError

    def dumps(self, obj: object) -> str:
        serializer = self.create_serializer()
        s = serializer.dumps(obj)
        return s

    def loads(self, s: str, cls=None) -> object:
        serializer = self.create_serializer()
        _dict = serializer.loads(s)
        if cls is not None:
            return dict_to_object(_dict, cls)
        else:
            return _dict

    def dump(self, obj: object, fp: str) -> None:
        s = self.dumps(obj)
        with open(fp, 'w') as f:
            f.write(s)

    def load(self, fp: str, cls=None) -> object:
        with open(fp, 'r') as f:
            s = f.read()
        obj = self.loads(s, cls)
        return obj
