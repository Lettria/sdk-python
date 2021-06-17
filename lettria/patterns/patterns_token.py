from .patterns_dependency import check_pattern_dependency
from .attribute_checker import compare_attr

def check_pattern(data, pattern, print_tree):
    if 'RIGHT_ID' in pattern[0] or 'LEFT_ID' in pattern[0]:
        return check_pattern_dependency(data, pattern, print_tree)
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
            else:
                j = 0
                current_pattern = []
        elif op == '+':
            if compare_attr(current_token, current_node):
                has_matched = True
                current_pattern.append(current_token)
            else:
                if has_matched == True:
                    i -= 1
                    j += 1
                    has_matched = False
                else:
                    j = 0
                    current_pattern = []
        elif op == '*':
            if compare_attr(current_token, current_node):
                has_matched = True
                current_pattern.append(current_token)
            else:
                if has_matched == True:
                    i -= 1
                    j += 1
                    has_matched = False
                else:
                    i -= 1
                    j += 1
        elif op == '!':
            if not compare_attr(current_token, current_node):
                j += 1
                current_pattern.append(current_token)
            else:
                j = 0
                current_pattern = []
        elif op == '?':
            j += 1
            if compare_attr(current_token, current_node):
                current_pattern.append(current_token)
            else:
                i -= 1
        i += 1
        if j == len(pattern):
            patterns_caught.append(current_pattern)
            current_pattern = []
            j = 0
        if i == len(data.tokens):
            break
    return patterns_caught
