import importlib
import unittest
import os
import sys

def get_file_with_parents(filepath, levels=1):
    common = filepath
    for i in range(levels + 1):
        common = os.path.dirname(common)
    return os.path.relpath(filepath, common)

class TestMethods(unittest.TestCase):

    def test_imports(self):
        with open('package_modules.txt', 'r') as fmodules:
            modules = list(map(lambda module: module.strip(), fmodules.readlines()))

        for module in modules:
            try:
                importlib.import_module(module)
            except ImportError:
                self.fail('import ' + module + ' failed')
