import unittest
import os
import json
import sys

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.prompt_builder import PromptBuilder
from src.exceptions import TemplateLoadError, MissingParameterError, ParameterTypeError

class TestPromptBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = PromptBuilder()
        self.test_template_path = "test_template.json"
        
        # Create a temporary test template in JSON format
        test_data = {
            "metadata": {
                "version": "1.0",
                "methodology": "Test Methodology"
            },
            "template": "Hello {{name}}, welcome to {{place}}!"
        }
        with open(self.test_template_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)

    def tearDown(self):
        if os.path.exists(self.test_template_path):
            os.remove(self.test_template_path)

    def test_load_valid_template(self):
        self.builder.load_template(self.test_template_path)
        
        self.assertIn("name", self.builder.required_parameters)
        self.assertIn("place", self.builder.required_parameters)
        self.assertEqual(self.builder.metadata["version"], "1.0")

    def test_build_prompt_success(self):
        self.builder.load_template(self.test_template_path)
        params = {"name": "Alice", "place": "Wonderland"}
        
        result = self.builder.build_prompt(params)
        
        self.assertEqual(result.prompt_text, "Hello Alice, welcome to Wonderland!")
        self.assertEqual(result.methodology, "Test Methodology")
        self.assertIsNotNone(result.trace_hash)
        self.assertIsNotNone(result.generation_timestamp)

    def test_missing_parameters_raises_custom_error(self):
        self.builder.load_template(self.test_template_path)
        params = {"name": "Bob"} # Missing 'place'
        
        with self.assertRaises(MissingParameterError) as context:
            self.builder.build_prompt(params)
        self.assertIn("Required placeholders absent from input", str(context.exception))

    def test_invalid_parameter_type_raises_custom_error(self):
        self.builder.load_template(self.test_template_path)
        params = {"name": "Bob", "place": {"complex": "object"}} # Invalid type dict
        
        with self.assertRaises(ParameterTypeError) as context:
            self.builder.build_prompt(params)
        self.assertIn("rejected", str(context.exception))

    def test_invalid_json_raises_custom_error(self):
        bad_file = "bad_template.json"
        with open(bad_file, 'w') as f:
            f.write("{ bad json... }")
            
        with self.assertRaises(TemplateLoadError):
            self.builder.load_template(bad_file)
            
        os.remove(bad_file)

if __name__ == '__main__':
    unittest.main()
