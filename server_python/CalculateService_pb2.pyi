from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Input(_message.Message):
    __slots__ = ("L", "T", "nx", "nt", "c")
    L_FIELD_NUMBER: _ClassVar[int]
    T_FIELD_NUMBER: _ClassVar[int]
    NX_FIELD_NUMBER: _ClassVar[int]
    NT_FIELD_NUMBER: _ClassVar[int]
    C_FIELD_NUMBER: _ClassVar[int]
    L: float
    T: float
    nx: float
    nt: float
    c: float
    def __init__(self, L: _Optional[float] = ..., T: _Optional[float] = ..., nx: _Optional[float] = ..., nt: _Optional[float] = ..., c: _Optional[float] = ...) -> None: ...

class Output(_message.Message):
    __slots__ = ("X", "T", "u")
    X_FIELD_NUMBER: _ClassVar[int]
    T_FIELD_NUMBER: _ClassVar[int]
    U_FIELD_NUMBER: _ClassVar[int]
    X: _containers.RepeatedScalarFieldContainer[float]
    T: _containers.RepeatedScalarFieldContainer[float]
    u: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, X: _Optional[_Iterable[float]] = ..., T: _Optional[_Iterable[float]] = ..., u: _Optional[_Iterable[float]] = ...) -> None: ...
