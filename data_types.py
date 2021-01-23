from enum import Enum


class DataTypes(Enum):
    char = 'string'
    varchar = 'string'
    bit = 'boolean'
    int = 'int'
    decimal = 'decimal'
    money = 'decimal'
    date = 'DateTime'
    datetime = 'DateTime'
    varbinary = 'byte[]'
