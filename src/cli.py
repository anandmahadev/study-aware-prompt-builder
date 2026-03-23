import argparse
import sys
import os
import json

# Ensure SRC can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.prompt_builder import PromptBuilder
from src.exceptions import PromptBuilderError

def parse_inline_params(param_str: str) -> dict:
    try:
        return json.loads(param_str)
    except json.JSONDecodeError as err:
        print(f"[!] Error Parsing parameters JSON. Ensure valid dict syntax: {err}")
        sys.exit(1)

def run_cli():
    parser = argparse.ArgumentParser(
        description="Study-Aware Prompt Builder: Generate methodology-safe, traceable AI Prompts."
    )
    
    parser.add_argument(
        '-t', '--template',
        type=str,
        required=True,
        help="Path to the JSON methodology schema (e.g., templates/heuristic_template.json)"
    )
    
    parser.add_argument(
        '-p', '--params',
        type=str,
        required=True,
        help='JSON string mapping parameters to values (e.g. \'{"interface_type":"Mobile app", "user_type":"Elderly", "heuristic_focus":"Visibility"}\')'
    )

    args = parser.parse_args()
    
    # Run the core logic
    builder = PromptBuilder()
    
    try:
        parameters = parse_inline_params(args.params)
        builder.load_template(args.template)
        
        result = builder.build_prompt(parameters)
        
        print("\n=== [ RUXAILAB Traceable Prompt Result ] ===")
        print(f"[*] Methodology  : {result.methodology} (v{result.template_version})")
        print(f"[*] Generation TS: {result.generation_timestamp}")
        print(f"[*] Audit Hash   : {result.trace_hash}")
        print("---------------------------------------------")
        print(result.prompt_text)
        print("=============================================\n")

    except PromptBuilderError as e:
        print(f"\n[!] Framework Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_cli()
