import importlib
import unittest

class TestMethods(unittest.TestCase):

    def test_imports(self):
        modules = [script.split('.')[0] for script in os.listdir('../src/')]

        for module in modules:
            try:
                importlib.import_module(module)
            except ImportError:
                self.fail('import ' + module + ' failed')
