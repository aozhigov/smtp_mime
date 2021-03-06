# -*- coding: utf-8 -*-

import gc
import sys
from pathlib import Path


def get_files(path: Path) -> (str, bytes):
    def get_text(file) -> bytes:
        with open(file, "rb") as f:
            temp = f.read()
        return temp

    if path.is_dir():
        for i in path.iterdir():
            if i.is_file():
                yield str(i), get_text(i)


def get_size(obj) -> int:
    marked = {id(obj)}
    obj_q = [obj]
    size = 0

    while obj_q:
        size += sum(map(sys.getsizeof, obj_q))
        all_refr = ((id(o), o) for o in gc.get_referents(*obj_q))
        new_refr = {o_id: o for o_id, o in all_refr
                    if o_id not in marked and not isinstance(o, type)}
        obj_q = new_refr.values()
        marked.update(new_refr.keys())

    return size
