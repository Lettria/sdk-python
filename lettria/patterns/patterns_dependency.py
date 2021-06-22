from .attribute_checker import compare_attr
import copy
from .DepTree import DepTree

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
    candidates = dep_ops[op](target_node) #assume op is ok
    for c in candidates:
        if compare_attr(c.root.tokens[c.idx], step_pattern['RIGHT_ATTRS']):
            result.append(c)
    return result

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
    j = 0
    while len(current_pattern) != len(pattern):
        if j < len(pattern):
            step_pattern = pattern[j]
        else:
            break
        if step_pattern in current_pattern:
            j += 1
            continue
        target_pattern, target_node = find_pattern_by_id(current_pattern, current_nodes, step_pattern['LEFT_ID'])
        if target_pattern == None:
            j += 1
            continue
        tmp_match = find_matching_nodes(step_pattern, target_node)
        if tmp_match:
            current_pattern.append(step_pattern)
            if len(tmp_match) > 1:
                for t in tmp_match[1:]:
                    tmp_node_lst = current_nodes + [t]
                    if len(tmp_node_lst) == len(pattern):
                        result += [tmp_node_lst]
                    else:
                        result += get_match_from_root(root_node, root_pattern, pattern, copy.deepcopy(current_pattern), tmp_node_lst)
            tmp_match = tmp_match[0]
            current_nodes.append(tmp_match)
            j += 1
            if j != len(current_pattern):
                j = 0
        elif 'OP' in step_pattern.get('RIGHT_ATTRS', {}) and step_pattern['RIGHT_ATTRS']['OP'] == '?':
            current_pattern.append(step_pattern)
            current_nodes.append(None)
            j += 1
            if j != len(current_pattern):
                j = 0
        else:
            break
        if len(current_pattern) == len(pattern):
            return result + [current_nodes]
    return []

def check_pattern_dependency(sentence_data, pattern, print_tree):
    def find_root_pattern(pattern):
        for e in pattern:
            if 'LEFT_ID' not in e:
                return e
        return None
    tree = DepTree.grow_tree(sentence_data.data)
    tree.tokens = sentence_data.tokens
    if print_tree:
        tree.print_tree()
    patterns_caught = []
    root_pattern = find_root_pattern(pattern)
    if root_pattern is None:
        print("Pattern is invalid, no root is present.")
        return []
    if tree is None:
        return []
    root_nodes = tree.find_node_attribute(root_pattern['RIGHT_ATTRS'])
    for root_node in root_nodes:
        res = get_match_from_root(root_node, root_pattern, pattern)
        if res:
            patterns_caught += res
    results = []
    for p in patterns_caught:
        results.append([k.root.tokens[k.idx] if k else None for k in p])
    return results