import os

debug = os.getenv('DEBUG') == '1' or os.getenv('DEBUG') == 'True'
flatten=lambda l: sum(map(flatten,l),[]) if isinstance(l,list) else [l]

def flatten_lst(lst):
    return flatten(lst)

class StrProperty(property):
    def __get__(self, obj, objtype=None):
        try:
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")
            return self.fget(obj)
        except Exception as e:
            if debug:
                raise e
            else:
                return None

class ListProperty(property):
    def __get__(self, obj, objtype=None):
        try:
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")
            return self.fget(obj)
        except Exception as e:
            if debug:
                raise e
            else:
                return []

class DictProperty(property):
    def __get__(self, obj, objtype=None):
        try:
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")
            return self.fget(obj)
        except Exception as e:
            if debug:
                raise e
            else:
                return {}