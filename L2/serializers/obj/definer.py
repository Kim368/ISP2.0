from serializers.obj.serializer import SerializerCreator
from serializers.obj.json import JsonSerializerCreator
from serializers.obj.pickle import PickleSerializerCreator
from serializers.obj.toml import TomlSerializerCreator
from serializers.obj.yaml import YamlSerializerCreator


def get_creator(extension: str) -> SerializerCreator:
    if extension == 'json':
        return JsonSerializerCreator()
    if extension == 'pickle':
        return PickleSerializerCreator()
    if extension == 'toml':
        return TomlSerializerCreator()
    if extension == 'yaml':
        return YamlSerializerCreator()
    raise ValueError('Unknown extension: ' + extension)
