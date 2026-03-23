import os
import sys

# Add the src folder to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.prompt_builder import PromptBuilder

def main():
    print("="*60)
    print(" RUNNING STUDY-AWARE PROMPT BUILDER EXAMPLE ")
    print("="*60)
    
    # 1. Initialize the system
    builder = PromptBuilder()

    # 2. Path to the template
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'heuristic_template.json')
    
    # 3. Load the template
    print(f"\n[*] Loading template from: {os.path.basename(template_path)}")
    builder.load_template(template_path)

    # 4. Define study parameters
    parameters = {
        "interface_type": "mobile banking application",
        "user_type": "elderly users (65+)",
        "heuristic_focus": "Error Prevention and Recovery"
    }

    # 5. Build the final prompt (Success Case)
    print("\n[+] Generating Prompt (Success Case)...")
    try:
        result = builder.build_prompt(parameters)
        
        print("\n--- Traceability Metadata ---")
        print(f" methodology: {result.methodology} (v{result.template_version})")
        print(f" timestamp:   {result.generation_timestamp}")
        print(f" trace_hash:  {result.trace_hash}")
        
        print("\n--- Generated Prompt ---")
        print(result.prompt_text)
        print("-" * 24)
    except Exception as e:
        print(f"Error generating prompt: {e}")

    # 6. Build a prompt with missing parameters (Error Case)
    print("\n[!] Generating Prompt (Error Case - Missing Parameter)...")
    bad_parameters = {
        "interface_type": "desktop dashboard",
        # Missing user_type and heuristic_focus intentionally
    }
    
    try:
        builder.build_prompt(bad_parameters)
    except Exception as e:
        print(f" [Caught expected error] -> {e}")
        
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
