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
        for item in self.data:
            if item['ref'] == self.idx:
                self.children.append(DepTree(self.data, item['index'], self.root, self))
    
    def __repr__(self):
        return self.str

    @property
    def str(self):
        return self.root.tokens[self.idx].str
    @property
    def child(self):
        return self.children
    
    @property
    def parent(self):
        return self.parent_ref

    @property
    def parents(self):
        parents = []
        tmp = self
        while tmp.parent:
            parents.append(tmp)
            tmp = tmp.parent
        return parents

    @property
    def siblings(self):
        return self.parent.children
    
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
    def next(self):
        if self.idx >= 1:
            return self.root.find_node(self.idx + 1)
        else:
            return None

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
            if item['dep'] == 'root':
                root = DepTree(sentence_data['synthesis'], i, None, None)
                break
        return root

cmp_str = {
    'ORTH' :    lambda x : x.str,
    'TEXT' :    lambda x : x.str,
    'LOWER' :    lambda x : x.str.lower(),
    'LEMMA' :    lambda x : x.lemma,
    'POS' :      lambda x : x.pos,
    'DEP' :      lambda x : x.dep,
    'ENT_TYPE' : lambda x : x.ner.get('type', []),
    'CATEGORY_SUPER' : lambda x : [k[0] for k in x.meaning], ## PB RENVOIT LISTE DONC CHECK marche pas
    'CATEGORY_SUB' : lambda x : [k[1] for k in x.meaning],  ## PB RENVOIT LISTE DONC CHECK marche pas 
}

cmp_int = {
    'LENGTH' :   lambda x : len(x.str)
}

cmp_bool = {
    'IS_ALPHA':     lambda x: x.str.isalpha(),
    'IS_ASCII':     lambda x: x.str.isascii(),
    'IS_DIGIT':     lambda x: x.str.isdigit(),
    'IS_LOWER':     lambda x: x.str.islower(),
    'IS_UPPER':     lambda x: x.str.isupper(),
    'IS_TITLE':     lambda x: x.str.istitle(),
    'IS_PUNCT':     lambda x: True if x in ['.', '!', '?', ';'] else False,
    'IS_SPACE':     lambda x: x.str.isspace(),
    # 'IS_STOP': lambda x: x.isalpha(),
    # 'IS_SENT_START': lambda x: x.isalpha(),
    'LIKE_NUM':     lambda x: x.pos == 'CD',
    'LIKE_URL':     lambda x: 'url' in x.ner.get('type', []),
    'LIKE_EMAIL':   lambda x: 'mail' in x.ner.get('type', []),
}

quantifiers = {
    "!":lambda x : True,
    "?":lambda x : True,
    "+":lambda x : True,
    "*":lambda x : True,
}

ops = {
    'IN':     lambda x, lst: x in lst if not isinstance(x, list) else ops['ISSUPERSET'](x, lst),
    'NOT IN': lambda x, lst: x not in lst if not isinstance(x, list) else not ops['ISSUPERSET'](x, lst),
    'ISSUBSET': lambda x_lst, lst: list(set(x_lst) & set(lst)) == x_lst and (x_lst or not lst),
    'ISSUPERSET': lambda x_lst, lst: list(set(x_lst) & set(lst)) == lst,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '>=': lambda x, y: x >= y,
    '<=': lambda x, y: x <= y,
    '>':  lambda x, y: x > y,
    '<':  lambda x, y: x < y,
}

dep_ops = {
    '<' : lambda x: x.children,
    '>' : lambda x: [x.parent] if x.parent else [],
}

# A < B	    A is the immediate dependent of B.
# A > B	    A is the immediate head of B.
# A << B	A is the dependent in a chain to B following dep → head paths.
# A >> B	A is the head in a chain to B following head → dep paths.
# A . B	    A immediately precedes B, i.e. A.i == B.i - 1, and both are within the same dependency tree.
# A .* B	A precedes B, i.e. A.i < B.i, and both are within the same dependency tree (not in Semgrex).
# A ; B	    A immediately follows B, i.e. A.i == B.i + 1, and both are within the same dependency tree (not in Semgrex).
# A ;* B	A follows B, i.e. A.i > B.i, and both are within the same dependency tree (not in Semgrex).
# A $+ B	B is a right immediate sibling of A, i.e. A and B have the same parent and A.i == B.i - 1.
# A $- B	B is a left immediate sibling of A, i.e. A and B have the same parent and A.i == B.i + 1.
# A $++ B	B is a right sibling of A, i.e. A and B have the same parent and A.i < B.i.
# A $-- B	B is a left sibling of A, i.e. A and B have the same parent and A.i > B.i.

def compare_attr(token, node):
    attributes = [k for k in node.keys() if k != 'OP']
    # print(node, token.str, token.lemma, token.meaning)
    # print([k[1] for k in token.meaning])
    for attribute in attributes:
        if not isinstance(node[attribute], dict):
            node_ops = ['==']
            node[attribute] = {'==':node[attribute]}
        else:
            node_ops = node[attribute].keys()
        if cmp_str.get(attribute, None):
            res = cmp_str[attribute](token)
            for op in node_ops:
                if not ops[op](res, node[attribute][op]):
                    return False
        elif cmp_int.get(attribute, None):
            res = cmp_int[attribute](token)
            for op in node_ops:
                if not ops[op](res, node[attribute][op]):
                    return False
        elif cmp_bool.get(attribute, None):
            if not cmp_bool[attribute](token):
                return False
    return True

def find_matching_nodes(step_pattern, target_node):
    op = step_pattern["REL_OP"]
    result = []
    print("op", op, step_pattern, target_node)

    candidates = dep_ops[op](target_node) #assume op is ok
    for c in candidates:
        print("candidate", c, c.root.tokens[c.idx], step_pattern)
        if compare_attr(c.root.tokens[c.idx], step_pattern['RIGHT_ATTRS']):
            result.append(c)
    print("res", result)
    return result

def check_pattern_dependency(sentence_data, pattern):
    def find_root_pattern(pattern):
        for e in pattern:
            if 'LEFT_ID' not in e:
                return e
        return None
    def find_pattern_by_id(pattern_list, nodes_list, id):
        for p, n in zip(pattern_list, nodes_list):
            if p['RIGHT_ID'] == id:
                return p,n
        return None, None
    print("")
    i = 0
    j = 0
    tree = DepTree.grow_tree(sentence_data.data)
    tree.tokens = sentence_data.tokens
    patterns_caught = []
    root_pattern = find_root_pattern(pattern)
    if root_pattern is None:
        print("Pattern is invalid, no root.")
        return []
    if tree is None:
        return []
    root_nodes = tree.find_node_attribute(root_pattern['RIGHT_ATTRS'])
    print("root pattern", root_pattern)
    print("root node", root_nodes)
    for root_node in root_nodes:
        current_pattern = [root_pattern]
        current_nodes = [root_node]
        j = 0
        while len(current_pattern) != len(pattern):
            # print(j)
            if j < len(pattern):
                step_pattern = pattern[j]
            else:
                break
            if step_pattern == root_pattern:
                j += 1
                continue
            target_pattern, target_node = find_pattern_by_id(current_pattern, current_nodes, step_pattern['LEFT_ID'])
            if target_pattern == None:
                j += 1
                continue
            tmp_match = find_matching_nodes(step_pattern, target_node)
            if tmp_match:
                current_pattern.append(step_pattern)
                current_nodes.append(tmp_match)
                j += 1
                if j != len(current_pattern):
                    j = 0
            else:
                break
            if len(current_pattern) == len(pattern):
                patterns_caught.append(current_nodes)
            ## match step_pattern else break
    # print(sentence_data.str)
    # print(tree.children)
    print("caught", patterns_caught)
    return patterns_caught
    # has_matched = False
    # patterns_caught = []
    # current_pattern = []
    # while i < len(data.tokens):
    #     current_token = data.tokens[i]
    #     current_node = pattern[j]

def check_pattern(data, pattern):
    if 'RIGHT_ID' in pattern[0] or 'LEFT_ID' in pattern[0]:
        return check_pattern_dependency(data, pattern)
    i = 0
    j = 0
    has_matched = False
    patterns_caught = []
    current_pattern = []
    while i < len(data.tokens):
        current_token = data.tokens[i]
        current_node = pattern[j]
        op = current_node.get('OP', '.')
        if op == '.':
            if compare_attr(current_token, current_node):
                j += 1
                current_pattern.append(current_token)
                # print("ok.  ", current_token, current_node)
            else:
                # print("fail.", current_token, current_node)
                j = 0
                current_pattern = []
        elif op == '+':
            if compare_attr(current_token, current_node):
                has_matched = True
                current_pattern.append(current_token)
                # print("ok.  ", current_token, current_node)
            else:
                if has_matched == True:
                    i -= 1
                    j += 1
                    has_matched = False
                else:
                    j = 0
                    current_pattern = []
                # print("fail.", current_token, current_node)
        elif op == '!':
            if not compare_attr(current_token, current_node):
                j += 1
                current_pattern.append(current_token)
                # print("ok!  ", current_token, current_node)
            else:
                # print("fail!", current_token, current_node)
                j = 0
                current_pattern = []
        elif op == '?':
            j += 1
            if compare_attr(current_token, current_node):
                # print("ok?  ", current_token, current_node)
                current_pattern.append(current_token)
            else:
                # print("fail?", current_token, current_node)
                i -= 1
        i += 1
        if j == len(pattern):
            patterns_caught.append(current_pattern)
            current_pattern = []
            j = 0
        if i == len(data.tokens):
            break
    return patterns_caught
