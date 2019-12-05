class essai:
    def __init__(self, b = 0):
        self.a = 12
        pass
    # def __getattribute__(self, name = ''):
    #     print(name)
    #     class test:
    #         def __init__(self):
    #             print('test')
    #     name = test
    #     name()
    def __getattribute__(self, key):
        "Emulate type_getattro() in Objects/typeobject.c"
        if hasattr(object, key):
            v = object.__getattribute__(self, key)
        else:
            self.__dict__[key] = 'test'
            v = object.__getattribute__(self, key)
        if hasattr(v, '__get__'):
            return v.__get__(None, self)
        return v

essai = essai()
# print(essai.__get__(essai,'a'))
print(essai.b)
# essai.a
