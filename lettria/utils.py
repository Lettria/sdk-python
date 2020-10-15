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
        except:
            return None

class ListProperty(property):
    def __get__(self, obj, objtype=None):
        try:
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")
            return self.fget(obj)
        except:
            return []

class DictProperty(property):
    def __get__(self, obj, objtype=None):
        try:
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")
            return self.fget(obj)
        except:
            return {}