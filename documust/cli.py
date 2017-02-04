"""CLI module"""

import os
import ast
import argparse

from documust.utils import path_utils
from documust.utils import tree_utils


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
                module_documented = tree_utils.is_documentation(tree.body[0])
                tree_objs = tree_utils.get_tree_objs(tree.body)

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
                print("{relative_path}:{obj_name} {obj_type} has no documentation!".format(
                    relative_path=relative_path, obj_name=tree_obj['name'], obj_type=tree_obj['type']))

            printed = self.print_obj_warnings(relative_path + ":" + tree_obj['name'], tree_obj['nodes']) or printed
        return printed


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
