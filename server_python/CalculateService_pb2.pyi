from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Input(_message.Message):
    __slots__ = ("a0", "a1", "a2", "a3", "u", "X0_0", "X0_1", "X0_2")
    A0_FIELD_NUMBER: _ClassVar[int]
    A1_FIELD_NUMBER: _ClassVar[int]
    A2_FIELD_NUMBER: _ClassVar[int]
    A3_FIELD_NUMBER: _ClassVar[int]
    U_FIELD_NUMBER: _ClassVar[int]
    X0_0_FIELD_NUMBER: _ClassVar[int]
    X0_1_FIELD_NUMBER: _ClassVar[int]
    X0_2_FIELD_NUMBER: _ClassVar[int]
    a0: float
    a1: float
    a2: float
    a3: float
    u: float
    X0_0: float
    X0_1: float
    X0_2: float
    def __init__(self, a0: _Optional[float] = ..., a1: _Optional[float] = ..., a2: _Optional[float] = ..., a3: _Optional[float] = ..., u: _Optional[float] = ..., X0_0: _Optional[float] = ..., X0_1: _Optional[float] = ..., X0_2: _Optional[float] = ...) -> None: ...

class Output(_message.Message):
    __slots__ = ("X_0", "X_1", "X_2", "X_next_0", "X_next_1", "X_next_2")
    X_0_FIELD_NUMBER: _ClassVar[int]
    X_1_FIELD_NUMBER: _ClassVar[int]
    X_2_FIELD_NUMBER: _ClassVar[int]
    X_NEXT_0_FIELD_NUMBER: _ClassVar[int]
    X_NEXT_1_FIELD_NUMBER: _ClassVar[int]
    X_NEXT_2_FIELD_NUMBER: _ClassVar[int]
    X_0: float
    X_1: float
    X_2: float
    X_next_0: float
    X_next_1: float
    X_next_2: float
    def __init__(self, X_0: _Optional[float] = ..., X_1: _Optional[float] = ..., X_2: _Optional[float] = ..., X_next_0: _Optional[float] = ..., X_next_1: _Optional[float] = ..., X_next_2: _Optional[float] = ...) -> None: ...
