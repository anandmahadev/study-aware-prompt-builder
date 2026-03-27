import argparse
import sys
import os
import json

# Ensure SRC can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.prompt_builder import PromptBuilder
from src.exceptions import PromptBuilderError

BANNER = r"""
  ____  _            _             _                              
 / ___|| |_ _   _  __| |_   _     / \__      ____ _ _ __ ___      
 \___ \| __| | | |/ _` | | | |   / _ \ \ /\ / / _` | '__/ _ \     
  ___) | |_| |_| | (_| | |_| |  / ___ \ V  V / (_| | | |  __/     
 |____/ \__|\__,_|\__,_|\__, | /_/   \_\_/\_/ \__,_|_|  \___|     
                        |___/                                     
  ____                            _     ____       _ _     _      
 |  _ \ _ __ ___  _ __ ___  _ __ | |_  | __ ) _  _(_) | __| | ___ _ __ 
 | |_) | '__/ _ \| '_ ` _ \| '_ \| __| |  _ \| | | | | |/ _` |/ _ \ '__|
 |  __/| | | (_) | | | | | | |_) | |_  | |_) | |_| | | | (_| |  __/ |   
 |_|   |_|  \___/|_| |_| |_| .__/ \__| |____/ \__,_|_|_|\__,_|\___|_|   
                           |_|                                          
"""

def parse_inline_params(param_str: str) -> dict:
    try:
        return json.loads(param_str)
    except json.JSONDecodeError as err:
        print(f"[!] Error Parsing parameters JSON. Ensure valid dict syntax: {err}")
        sys.exit(1)

def list_templates():
    template_dir = "templates"
    if not os.path.exists(template_dir):
        print(f"[!] Error: Could not find '{template_dir}' directory.")
        return
    
    print("\n=== [ Available RUXAILAB Methodologies ] ===")
    files = [f for f in sorted(os.listdir(template_dir)) if f.endswith('.json')]
    for file in files:
        file_path = os.path.join(template_dir, file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                methodology = data.get("metadata", {}).get("methodology", "Unknown")
                version = data.get("metadata", {}).get("version", "0.0.0")
                print(f" - {file:<30} | {methodology:<25} (v{version})")
        except:
             print(f" - {file:<30} | [ERROR PARSING]")
    print("============================================\n")

def run_cli():
    print(BANNER)
    parser = argparse.ArgumentParser(
        description="Study-Aware Prompt Builder: A scientific interface for UX Research prompts (RUXAILAB standard).",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-t', '--template',
        type=str,
        help="Path to the JSON methodology schema (e.g., templates/heuristic_template.json)"
    )
    
    parser.add_argument(
        '-p', '--params',
        type=str,
        help='JSON string mapping parameters to values. If omitted, tool enters interactive mode.'
    )

    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help="List all available methodology templates in the templates/ directory."
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        help="Path to save the generated prompt trace (supports .md or .json)"
    )

    args = parser.parse_args()
    
    if args.list:
        list_templates()
        return

    if not args.template:
        print("[!] Error: --template is required unless --list is used.")
        parser.print_help()
        sys.exit(1)

    # Run the core logic
    builder = PromptBuilder()
    
    try:
        builder.load_template(args.template)
        
        if args.params:
            parameters = parse_inline_params(args.params)
        else:
            print(f"\n[+] Entering Interactive Mode for: {args.template}")
            print("[+] Please provide the following research parameters:")
            parameters = {}
            for placeholder in sorted(builder.placeholders):
                val = input(f"    - {placeholder}: ").strip()
                if not val:
                    print(f" [!] Error: Parameter '{placeholder}' cannot be empty.")
                    sys.exit(1)
                parameters[placeholder] = val

        result = builder.build_prompt(parameters)
        
        print("\n=== [ RUXAILAB Traceable Prompt Result ] ===")
        print(f"[*] Methodology  : {result.methodology} (v{result.template_version})")
        print(f"[*] Generation TS: {result.generation_timestamp}")
        print(f"[*] Audit Hash   : {result.trace_hash}")
        print("---------------------------------------------")
        print(result.prompt_text)
        print("=============================================\n")
        print("[TIP] You've just generated a scientific prompt! Keep your RUXAILAB streak going by committing this result.")

        if args.output:
            if args.output.endswith('.md'):
                result.save_to_markdown(args.output)
            elif args.output.endswith('.json'):
                result.save_to_json(args.output)
            else:
                print(f"[!] Warning: Extension not recognized. Saving as text to {args.output}")
                with open(args.output, 'w') as f:
                    f.write(result.prompt_text)

    except PromptBuilderError as e:
        print(f"\n[!] Framework Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[!] Execution cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_cli()
