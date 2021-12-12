CUR_PATH = ""
SOURCE_NAME = "SAVED_Function_Source.txt"
CODE_NAME = "SAVED_Function_Code.txt"

from serializers.foo import sourcecode, attrcode


def check(f):
    assert f(1)(2) == 3

def test_source():
    f = sourcecode.function_load(CUR_PATH + SOURCE_NAME)
    check(f)

def test_code():
    f = attrcode.function_load(CUR_PATH + CODE_NAME)
    check(f)
