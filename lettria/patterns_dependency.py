from .attribute_checker import compare_attr
import copy

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

    def __str__(self):
        return self.str

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
        res = [self]
        for child in self.children:
            res += child.descendants
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
            if item['dep'] == 'root':
                root = DepTree(sentence_data['synthesis'], i, None, None)
                break
        return root

#op is used on A
dep_ops = {
    '>' : lambda x: x.children,
    '>>' : lambda x: x.descendants,
    '<' : lambda x: [x.parent] if x.parent else [],
    '<<' : lambda x: x.parents,
    '.' : lambda x: [x.next],
    '.*' : lambda x: x.nexts,
    ';' : lambda x: [x.prev],
    ';*' : lambda x: x.prevs,
    '$+' : lambda x: [k for k in x.siblings if x.idx == k.idx - 1],
    '$-' : lambda x: [k for k in x.siblings if x.idx == k.idx + 1],
    '$++' : lambda x: x.right_siblings,
    '$--' : lambda x: x.left_siblings,
}

# A < B        A is the immediate dependent of B.
# A > B        A is the immediate head of B.
# A << B    A is the dependent in a chain to B following dep → head paths.
# A >> B    A is the head in a chain to B following head → dep paths.
# A . B        A immediately precedes B, i.e. A.i == B.i - 1, and both are within the same dependency tree.
# A .* B    A precedes B, i.e. A.i < B.i, and both are within the same dependency tree (not in Semgrex).
# A ; B        A immediately follows B, i.e. A.i == B.i + 1, and both are within the same dependency tree (not in Semgrex).
# A ;* B    A follows B, i.e. A.i > B.i, and both are within the same dependency tree (not in Semgrex).
# A $+ B    B is a right immediate sibling of A, i.e. A and B have the same parent and A.i == B.i - 1.
# A $- B    B is a left immediate sibling of A, i.e. A and B have the same parent and A.i == B.i + 1.
# A $++ B    B is a right sibling of A, i.e. A and B have the same parent and A.i < B.i.
# A $-- B    B is a left sibling of A, i.e. A and B have the same parent and A.i > B.i.


def find_matching_nodes(step_pattern, target_node):
    op = step_pattern["REL_OP"]
    result = []
    print("===> op",target_node,  op, step_pattern)

    candidates = dep_ops[op](target_node) #assume op is ok
    for c in candidates:
        print("====> candidate:", c, step_pattern)
        if compare_attr(c.root.tokens[c.idx], step_pattern['RIGHT_ATTRS']):
            result.append(c)
    # print("===> res", result)
    # if len(result) == 1:
        # result = result[0] #TMP A VOIR
    return result

#split pattern a gerer

def get_match_from_root(root_node, root_pattern, pattern, c_pattern = None, c_nodes = None):
    def find_pattern_by_id(pattern_list, nodes_list, id):
        for p, n in zip(pattern_list, nodes_list):
            if p['RIGHT_ID'] == id:
                return p,n
        return None, None
    current_pattern = [root_pattern] if c_pattern == None else c_pattern
    current_nodes = [root_node] if c_nodes == None else c_nodes
    if c_nodes:
        indent = '      '
    else:
        indent = ''
    result = []
    # print("=> root node", root_node)
    j = 0
    while len(current_pattern) != len(pattern):
        # print(j)
        if j < len(pattern):
            step_pattern = pattern[j]
        else:
            break
        if step_pattern in current_pattern:
            j += 1
            continue
        target_pattern, target_node = find_pattern_by_id(current_pattern, current_nodes, step_pattern['LEFT_ID'])
        # print("==> target", step_pattern, target_node)
        # print("==> target", target_pattern)
        if target_pattern == None:
            j += 1
            continue
        tmp_match = find_matching_nodes(step_pattern, target_node)
        if tmp_match:
            current_pattern.append(step_pattern)
            if len(tmp_match) > 1:
                # print("AH all", tmp_match)
                for t in tmp_match[1:]:
                    # print(indent, "AH before", t, current_nodes)
                    tmp_node_lst = current_nodes + [t]
                    # print(indent, "AH after", tmp_node_lst)
                    if len(tmp_node_lst) == len(pattern):
                        result += [tmp_node_lst]
                    else:
                        result += get_match_from_root(root_node, root_pattern, pattern, copy.deepcopy(current_pattern), tmp_node_lst)
            tmp_match = tmp_match[0]
            current_nodes.append(tmp_match)
            # print(indent, "AH3", len(current_pattern), current_nodes, j)
            j += 1
            if j != len(current_pattern):
                j = 0
        else:
            break
        if len(current_pattern) == len(pattern):
            # print(indent, "AH MATCH", current_nodes)
            return result + [current_nodes]
    return []

def check_pattern_dependency(sentence_data, pattern):
    def find_root_pattern(pattern):
        for e in pattern:
            if 'LEFT_ID' not in e:
                return e
        return None
    print("")
    tree = DepTree.grow_tree(sentence_data.data)
    tree.tokens = sentence_data.tokens
    tree.print_tree()
    patterns_caught = []
    root_pattern = find_root_pattern(pattern)
    if root_pattern is None:
        print("Pattern is invalid, no root.")
        return []
    if tree is None:
        return []
    root_nodes = tree.find_node_attribute(root_pattern['RIGHT_ATTRS'])
    print("root pattern", root_pattern)
    print("root nodes", root_nodes)
    for root_node in root_nodes:
        res = get_match_from_root(root_node, root_pattern, pattern)
        if res:
            patterns_caught += res
    print("caught", patterns_caught)

    results = []
    for p in patterns_caught:
        results.append([k.root.tokens[k.idx] for k in p])
    return results