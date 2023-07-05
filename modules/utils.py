from typing import Callable

def update_add(dic : dict, key, op : Callable[[any], any], default):
    s = dic.get(key, default)
    dic[key] = op(s)
