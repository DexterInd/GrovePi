import importlib
import unittest

class TestMethods(unittest.TestCase):

    def test_imports(self):
        modules = [
            'grovepi',
            'dextergps',
            'lsm303d',
            'adxl345',
            'grove_barometer_lib'
        ]

        for module in modules:
            try:
                importlib.import_module(module)
            except ImportError:
                self.fail('import ' + module + ' failed')
