import os

debug = os.getenv('DEBUG') == '1' or os.getenv('DEBUG') == 'True'
flatten=lambda l: sum(map(flatten,l),[]) if isinstance(l,list) else [l]

#Accepted arguments for hierarchical levels
GLOBAL =    ['g', 'global', 'glob']
DOC =       ['d', 'doc', 'document', 'documents']
SENT =      ['s', 'sentence', 'sent', 'sentences']
SUB =       ['sub', 'subsentence', 'subsentences']
TOK =       ['t', 'token', 'tok', 'tokens']


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

class IntProperty(property):
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
                return 0

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