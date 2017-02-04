"""ast tree utilities"""

import ast


def is_documentation(header):
    """Returns False if module undocumented else True"""
    try:
        assert isinstance(header, ast.Expr)
        assert isinstance(header.value, ast.Str)
    except AssertionError:
        return False
    else:
        return True


def get_tree_objs(tree_body):
    """Returns a list of parsed objects metadata"""
    tree_objs = []
    for node in tree_body:
        node_type = None
        if isinstance(node, ast.ClassDef):
            node_type = 'class'
        elif isinstance(node, ast.FunctionDef):
            node_type = 'function'

        if node_type:
            node_obj = {'name': node.name, 'lineno': node.lineno,
                        'nodes': [], 'col_offset': node.col_offset,
                        'type': node_type, 'documented': True}

            is_documented = is_documentation(node.body[0])
            if not is_documented:
                node_obj['documented'] = False
            internal_node_objs = get_tree_objs(node.body)
            node_obj['nodes'].extend(internal_node_objs)
            tree_objs.append(node_obj)
    return tree_objs
