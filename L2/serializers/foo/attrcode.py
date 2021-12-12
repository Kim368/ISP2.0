import inspect
import types


def serialize_obj(obj):
    if obj is None:
        return None

    if isinstance(obj, (int, float, bool, str)):
        return obj

    if type(obj) == bytes:
        return list(obj)

    if isinstance(obj, (list, tuple)):
        lst = []
        for elem in obj:
            lst.append(serialize_obj(elem))
        return lst

    if type(obj) == dict:
        _dict = {}
        for key in obj:
            _dict[key] = serialize_obj(obj[key])
        return _dict

    if inspect.isroutine(obj):
        return serialize_function(obj)

    _dict = {}
    for key, val in inspect.getmembers(obj):
        if callable(val):
            if not "__" in val.__name__:
                _dict[key] = serialize_function(val)
        else:
            _dict[key] = serialize_obj(val)
    return _dict


IMPORTANT_ATTRIBUTES = [
    "__code__",
    "__name__",
    "__defaults__",
    "__closure__",
]


def serialize_function(f: object) -> dict:
    _dict = {}
    for member_name, val in inspect.getmembers(f):
        if member_name in IMPORTANT_ATTRIBUTES:
            _dict[member_name] = serialize_obj(val)
        if member_name == "__code__":
            _dict["__globals__"] = {}
            global_var = f.__globals__
            for co_name in val.co_names:
                if co_name == f.__name__:
                    _dict["__globals__"][co_name] = f.__name__
                elif not inspect.isbuiltin(co_name):
                    if co_name in global_var:
                        if not inspect.ismodule(global_var[co_name]):
                            _dict["__globals__"][co_name] = serialize_obj(global_var[co_name])
    return _dict


def deserialize_co_consts(co_consts: list):
    lst = []
    for elem in co_consts:
        if type(elem) == dict and "co_code" in elem:
            lst.append(deserialize_codeobject(elem))
        else:
            lst.append(elem)
    return tuple(lst)


def deserialize_codeobject(code: dict):
    return types.CodeType(
        code['co_argcount'],
        code['co_posonlyargcount'],
        code['co_kwonlyargcount'],
        code['co_nlocals'],
        code['co_stacksize'],
        code['co_flags'],
        bytes(code['co_code']),
        deserialize_co_consts(code['co_consts']),
        tuple(code['co_names']),
        tuple(code['co_varnames']),
        code['co_filename'],
        code['co_name'],
        code['co_firstlineno'],
        bytes(code['co_lnotab']),
        tuple(code['co_freevars']),
        tuple(code['co_cellvars'])
    )


def deserialize_function(f: dict):
    code = f["__code__"]
    details = []
    details.append(deserialize_codeobject(code))

    globs = {"__builtins__": __builtins__}
    for elem in f["__globals__"]:
        val = f["__globals__"][elem]
        if type(val) == dict and "__code__" in val:
            globs[elem] = deserialize_function(val)
        else:
            globs[elem] = val
    details.append(globs)

    for attr in IMPORTANT_ATTRIBUTES:
        if attr != "__code__":
            details.append(f[attr])

    result_func = types.FunctionType(*details)

    result_func.__globals__[result_func.__name__] = result_func

    return result_func


import json


def function_dumps(func) -> str:
    dct = serialize_obj(func)
    return json.dumps(dct, indent=4)


def function_dump(func, fp: str):
    s = function_dumps(func)
    with open(fp, "w") as f:
        f.write(s)


def function_loads(s: str) -> object:
    dct = json.loads(s)
    func = deserialize_function(dct)
    return func


def function_load(fp: str):
    with open(fp, "r") as f:
        s = f.read()
    return function_loads(s)
