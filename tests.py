import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

# Import your plugin code
from main import main

class TestAzureCachePlugin(unittest.TestCase):
    def setUp(self):
        # Save original sys.stdout for later restoration
        self.original_stdout = sys.stdout

    def tearDown(self):
        # Restore original sys.stdout
        sys.stdout = self.original_stdout

    def test_missing_inputs(self):
        # Simulate missing environment variables
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit) as cm:
                main()
            
            self.assertEqual(cm.exception.code, 1)

    def test_wrong_credentials(self):
        # Simulate wrong credentials
        with patch.dict(os.environ, {"PLUGIN_CONNECTION_STRING": "invalid"}):
            with self.assertRaises(SystemExit) as cm:
                main()
            
            self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
