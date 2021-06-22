from .attribute_checker import compare_attr

class DepTree:
    def __init__(self, sentence_data, idx, root, parent_ref = None):
        self.data = sentence_data
        self.root = self if root is None else root
        self.idx = idx
        self.parent_ref = parent_ref
        self.children = []
        self.grow_children()
        self.tokens = None
    
    def grow_children(self):
        for i, item in enumerate(self.data):
            if item['ref'] == self.idx:
                self.children.append(DepTree(self.data, i, self.root, self))
    
    # def __repr__(self):
    #     return self.print_tree()

    # def __str__(self):
    #     return self.print_tree()

    def print_tree(self, depth = 0, last = False):
        phrase = ""
        for _ in range(depth - 1):
            phrase += '|\t' if last == False else '\t'
        if depth > 0:
            phrase += '|______'
        phrase += "{} [{}]({}) {} {}".format(self.str, self.idx, self.root.tokens[self.idx].dep, \
                                    self.root.tokens[self.idx].pos, self.root.tokens[self.idx].dep)
        phrase += '\n'
        if self.children:
            for _, child in enumerate(self.children):
                phrase += child.print_tree(depth = depth + 1, last = False)
        if self.parent_ref == None:
            print(phrase)
        else:
            return (phrase)

    @property
    def str(self):
        return self.root.tokens[self.idx].str

    @property
    def child(self):
        return self.children
    
    @property
    def descendants(self):
        res = []
        for child in self.children:
            res += [child] + child.descendants
        return res
    
    @property
    def parent(self):
        return self.parent_ref

    @property
    def parents(self):
        parents = []
        tmp = self
        while tmp.parent:
            parents.append(tmp.parent)
            tmp = tmp.parent
        return parents

    @property
    def siblings(self):
        return self.parent.children if self.parent else []
    
    @property
    def left_siblings(self):
        return [child for child in self.parent.children if child.idx < self.idx]
    
    @property
    def right_siblings(self):
        return [child for child in self.parent.children if child.idx > self.idx]

    @property
    def prev(self):
        if self.idx >= 1:
            return self.root.find_node(self.idx - 1)
        else:
            return None
    
    @property
    def prevs(self):
        res = []
        for i in range(0, self.idx):
            res.append(self.root.find_node(i))
        return res

    @property
    def next(self):
        if self.idx < len(self.root.tokens):
            return self.root.find_node(self.idx + 1)
        else:
            return None

    @property
    def nexts(self):
        res = []
        for i in range(self.idx + 1, len(self.root.tokens)):
            res.append(self.root.find_node(i))
        return res

    def find_node(self, idx):
        if self.idx == idx:
            return self
        for child in self.children:
            tmp = child.find_node(idx)
            if tmp != None:
                return tmp 
        return None     

    def find_node_attribute(self, pattern):
        ret = []
        if compare_attr(self.root.tokens[self.idx], pattern):
            ret.append(self)
        for child in self.children:
            tmp = child.find_node_attribute(pattern)
            if tmp != None:
                ret += tmp
        return ret     


    @classmethod
    def grow_tree(self, sentence_data):
        root = None
        for i, item in enumerate(sentence_data['synthesis']):
            if item['dep'] == 'root' or item['ref'] == -1:
                root = DepTree(sentence_data['synthesis'], i, None, None)
                break
        return root