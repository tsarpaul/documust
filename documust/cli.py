"""CLI module"""

import os
import ast
import argparse

from six.moves import input

from documust.utils import path_utils


class DocUMustCLI(object):
    """CLI object"""
    description = "Lets make sure you don't forget to document this time.\n"

    def __init__(self):
        """init"""
        pwd = os.getcwd()
        self.pwd = os.path.join(pwd, '')  # Add trailing slash because this is a dir

    def handle(self, argv=None):
        """CLI handler"""
        parser = argparse.ArgumentParser(description=self.description)

        parser.add_argument('-r', action='store_true', default=False, dest='recursively', help='Run recursively')

        args = parser.parse_args(argv)

        self.recursively = args.recursively

        self.docu_warn()

    def docu_warn(self):
        """Warns about missing documentation"""
        warn_triggered = False
        module_paths = path_utils.matches_in_path(self.pwd, self.recursively, "*.py")
        for module_path in module_paths:
            relative_path = module_path.replace(self.pwd, '')

            source = path_utils.load_source(module_path)
            tree = ast.parse(source, module_path)

            if tree.body:  # Module isn't empty
                module_documented = self.is_documentation(tree.body[0])
                tree_objs = self.get_tree_objs(tree.body)

                if not module_documented:
                    print(relative_path + " module has no documentation!")
                printed = self.print_obj_warnings(relative_path, tree_objs)
                if printed:
                    warn_triggered = printed
                    print('')

        if not warn_triggered:
            print('Everything is documented! Great job!')

    def print_obj_warnings(self, relative_path, tree_objs):
        """Prints undocumented objects, returns True if something was printed"""
        printed = False
        for tree_obj in tree_objs:
            if not tree_obj['documented']:
                printed = True
                print("{relative_path}:{obj_name}[{lineno}:{col_offset}] {obj_type} has no documentation!".format(
                    relative_path=relative_path, obj_name=tree_obj['name'], obj_type=tree_obj['type'],
                    lineno=tree_obj['lineno'], col_offset=tree_obj['col_offset']))

            printed = self.print_obj_warnings(relative_path + ":" + tree_obj['name'], tree_obj['nodes']) or printed
        return printed

    def is_documentation(self, header):
        """Returns True if module documented else False"""
        try:
            assert isinstance(header, ast.Expr)
            assert isinstance(header.value, ast.Str)
        except AssertionError:
            return False
        else:
            return True

    def get_tree_objs(self, tree_body):
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

                is_documented = self.is_documentation(node.body[0])
                if not is_documented:
                    node_obj['documented'] = False
                internal_node_objs = self.get_tree_objs(node.body)
                node_obj['nodes'].extend(internal_node_objs)
                tree_objs.append(node_obj)
        return tree_objs


def handle(command=None):
    """CLI handler"""
    cli = DocUMustCLI()
    if command:  # Debug
        cli.handle(argv=command)
    else:
        cli.handle()


if __name__ == "__main__":  # Debug
    command = input('Insert command: ')
    command = command.split()
    handle(command)
