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
        src_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        modules = [script.split('.')[0] for script in os.listdir(src_path + '/src')]

        for module in modules:
            try:
                importlib.import_module(module)
            except ImportError:
                self.fail('import ' + module + ' failed')
