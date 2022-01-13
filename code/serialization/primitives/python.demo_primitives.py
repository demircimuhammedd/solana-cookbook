import base64
from borsh_construct import *

# Schema to deserialize various types
primitiveSchema = CStruct(
        "U8" / U8,
        "U16" / U16,
        "U32" / U32,
        "FIXED_STRING_ARRAY" / String[2],
        "FIXED_U8_ARRAY" / U8[5],
        "MAP_STRING_STRING" / HashMap(String, String)
    })


def common():
    map = dict()
    map["cookbook"] = "recipe"
    map["recipe"] = "ingredient"

    # Serialize
    dser = primitiveSchema.build({
        'U8': 255,
        'U16': 65535,
        'U32': 4294967295,
        "FIXED_STRING_ARRAY": ['hello', 'world'],
        "FIXED_U8_ARRAY": [1, 2, 3, 4, 5],
        "MAP_STRING_STRING": map})
    print(dser)
    # => b'\xff\xff\xff\xff\xff\xff\xff\x05\x00\x00\x00hello\x05\x00\x00\x00world\x01\x02\x03\x04\x05\x02\x00\x00\x00\x08\x00\x00\x00cookbook\x06\x00\x00\x00recipe\x06\x00\x00\x00recipe\n\x00\x00\x00ingredient'
    # Deserialize
    new_value = primitiveSchema.parse(dser)
    # Viola
    print(new_value)
    # => Container:
    # =>    U8 = 255
    # =>    U16 = 65535
    # =>    U32 = 4294967295
    # =>    FIXED_STRING_ARRAY = ListContainer:
    # =>        hello
    # =>        world
    # =>    FIXED_U8_ARRAY = ListContainer:
    # =>        1
    # =>        2
    # =>        3
    # =>        4
    # =>        5
    # =>    MAP_STRING_STRING = {'cookbook': 'recipe', 'recipe': 'ingredient'}
