from __future__ import annotations


def redefine(obj: object, name: str, new: callable,
             new_name: str = None) -> None:
    if not new_name:
        new_name = name + '_old'
    if hasattr(obj, name):
        setattr(obj, new_name, getattr(obj, name))
    setattr(obj, name, new)


def redefine_class(original_cls: object, cls: object) -> None:
    for method in cls._redefine_methods:
        redefine(original_cls, method, getattr(cls, method))
