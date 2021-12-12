from serializers.obj.serializer import object_to_dict
from serializers.obj.json import JsonSerializerCreator
from serializers.obj.pickle import PickleSerializerCreator
from serializers.obj.yaml import YamlSerializerCreator
from serializers.obj.toml import TomlSerializerCreator


CUR_PATH = ""
FILE_EXTENSION = ".txt"


class SubObjectParent():
    def __init__(self):
        self.a = 1
        self.b = "2"
        self.c = True

class SubObject(SubObjectParent):
    def __init__(self):
        SubObjectParent.__init__(self)
        self.d = {"a": 13, "asd": "dddd", "dlasdl": "12311231"}

class MyClass():
    num = int
    flt = float
    txt = str
    bul = bool
    arr = list
    tup = tuple
    sed = set
    dct = dict
    obj = object

    def init(self):
        self.num = 42
        self.flt = 3.1416
        self.txt = "Test de test"
        self.bul = True
        self.arr = [13, 69, 420, 0]
        self.dct = {"a": 13, "42": "13", "d": "df", "ff": ["sdf", "asdf"]}
        self.obj = SubObject()

    def __str__(self):
        s = ""
        s += type(self).__name__
        s += "\n"
        for (k, v) in object_to_dict(self).items():
            s += f"{k} = {v} \n"
        return s


my_class = MyClass()
my_class.init()
#print(my_class)


def check_creator(creator):

    s = creator.dumps(my_class)
    obj = creator.loads(s, MyClass)
    assert str(obj) == str(my_class)
    
    fn = CUR_PATH + type(creator).__name__ + FILE_EXTENSION
    s = creator.dump(my_class, fn)
    obj = creator.load(fn, MyClass)
    assert str(obj) == str(my_class)

def test_json():
    creator = JsonSerializerCreator()
    check_creator(creator)
    
def test_pickle():
    creator = PickleSerializerCreator()
    check_creator(creator)
    
def test_yaml():
    creator = YamlSerializerCreator()
    check_creator(creator)
    
def test_toml():
    creator = TomlSerializerCreator()
    check_creator(creator)
