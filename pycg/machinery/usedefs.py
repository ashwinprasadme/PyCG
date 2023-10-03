import ast
import beniget
import gast


class UseDefManager(gast.NodeVisitor):
    def __init__(self):
        # compute the def-use of the module
        self.chains = beniget.DefUseChains()
        self.attributes = set()  # attributes of current class

    def build_chains(self, module_path):
        mod_node = gast.parse(open(module_path).read())
        self.chains.visit(mod_node)

    def visit_ClassDef(self, node):
        # walk methods and fill users of `self`
        for stmt in node.body:
            if isinstance(stmt, ast.FunctionDef):
                self_def = self.chains.chains[stmt.args.args[0]]
                self.users.update(use.node for use in self_def.users())
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # any attribute of `self` is registered
        if node.value in self.users:
            self.attributes.add(node.attr)
