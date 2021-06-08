cmp_str = {
    'ORTH' :    lambda x : x.str,
    'TEXT' :    lambda x : x.str,
    'LOWER' :    lambda x : x.str.lower(),
    'LEMMA' :    lambda x : x.lemma,
    'POS' :      lambda x : x.pos,
    'DEP' :      lambda x : x.dep,
    'ENT_TYPE' : lambda x : x.ner.get('type', [''])[0],
    'CATEGORY_SUPER' : lambda x : [k[0] for k in x.meaning],
    'CATEGORY_SUB' : lambda x : [k[1] for k in x.meaning],
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
    'IS_SENT_START': lambda x: x.idx == 0,
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

types_check = {
    "IN": [list],
    "NOT IN": [list],
    "ISSUBSET": [list],
    "ISSUPERSET": [list],
}

valid_keys = list(cmp_str.keys()) + list(cmp_bool.keys()) + list(cmp_int.keys()) + list(quantifiers.keys()) + ['OP']

def compare_attr(token, node):
    attributes = [k for k in node.keys() if k != 'OP']
    for attribute in attributes:
        if attribute not in valid_keys:
            raise Exception("Error attribute " + attribute +  " does not exist.")
    for attribute in attributes:
        if isinstance(node[attribute], list):
            node_ops = ['IN']
            node[attribute] = {'IN':node[attribute]}
        elif not isinstance(node[attribute], dict):
            node_ops = ['==']
            node[attribute] = {'==':node[attribute]}
        else:
            node_ops = node[attribute].keys()
        if cmp_str.get(attribute, None):
            res = cmp_str[attribute](token)
            for op in node_ops:
                if op == '==' and not isinstance(node[attribute][op], str):
                    raise Exception(attribute + " attribute expects a string value.")
                elif types_check.get(op, '') and type(node[attribute][op]) not in types_check[op]:
                    raise Exception(attribute + " attribute and operator " + op + " expect one of " + str(types_check[op]))
                if not ops[op](res, node[attribute][op]):
                    return False
        elif cmp_int.get(attribute, None):
            res = cmp_int[attribute](token)
            for op in node_ops:
                if op == '==' and not isinstance(node[attribute][op], int):
                    raise Exception(attribute + " attribute expects an integer value.")
                elif types_check.get(op, '') and type(node[attribute][op]) not in types_check[op]:
                    raise Exception(attribute + " attribute and operator " + op + " expect one of " + str(types_check[op]))
                if not ops[op](res, node[attribute][op]):
                    return False
        elif cmp_bool.get(attribute, None):
            if not isinstance(node[attribute].get('==', None), bool):
                raise Exception(attribute + " attribute expects a boolean value.")
            if not cmp_bool[attribute](token) == node[attribute]['==']:
                return False
    return True