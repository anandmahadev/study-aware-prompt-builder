# Study-Aware Prompt Builder

A methodology-aware Python framework that generates, manages, and strict-validates LLM prompts for UX research and heuristics evaluation. 

Designed explicitly as a foundational prototype for **RUXAILAB (GSoC)**, this system targets the core scientific need for **reproducibility** in AI-assisted evaluations.

## 🎯 Architecture Paradigm & Scientific Rigor
1. **Traceability (The "Audit Hash")**: Generates a standard UTC timestamp and a unique `trace_hash` (SHA-256) for every prompt executed. Research papers can publish these hashes to prove methodology validity.
2. **Framework Safety**: Uses custom `PromptBuilderError` exception hierarchies (`MissingParameterError`, `TemplateLoadError`) ensuring the pipeline gracefully halts rather than feeding junk data to an LLM. 
3. **Advanced Python Tooling**: Embraces strict static type hinting (`typing`), `dataclasses`, and the runtime `logging` module to serve as an industrial-grade backend service.
4. **Command-Line Interface (CLI)**: Features an `argparse`-powered shell utility, mimicking standard data-science UX workflows.

## 📂 Folder Structure
```
study-aware-prompt-builder/
│── templates/
│   └── heuristic_template.json   # Methodological schema with metadata
│
│── src/
│   ├── prompt_builder.py         # Main execution, logging & Dataclass logic
│   ├── exceptions.py             # Custom hierarchical exception objects
│   └── cli.py                    # argparse Command-Line Interface integration
│
│── tests/
│   └── test_prompt_builder.py    # Standard unittest suite
│
│── examples/
│   └── example_usage.py          # Python programmatic demonstrator
│
│── README.md
│── requirements.txt              # Zero dependencies! Standard library only.
```

## 🚀 How to Run It

Because it avoids heavy frameworks (no Flask/FastAPI), it relies entirely on the built-in Python standard library.

### Option 1: The Command Line Interface (CLI)
*The most professional way to integrate this into bash/shell pipelines .*

Navigate into the root directory of the project, then run the `cli.py` passing the template and JSON parameters.

**For Linux / macOS / Windows Command Prompt (cmd.exe):**
```bash
python -m src.cli -t templates/heuristic_template.json -p "{\"interface_type\": \"Medical Dashboard\", \"user_type\": \"Nurses\", \"heuristic_focus\": \"Visibility of system status\"}"
```

**For Windows PowerShell:**
*(PowerShell string parsing can strip JSON quotes. Prefixing with `cmd.exe /c` is the most reliable workaround.)*
```powershell
cmd.exe /c 'python -m src.cli -t templates/heuristic_template.json -p "{\"interface_type\": \"Medical Dashboard\", \"user_type\": \"Nurses\", \"heuristic_focus\": \"Visibility of system status\"}"'
```

*Output will directly stream the traceable hash and prompt to stdout.*

### Option 2: Run the Standard Examples program
```bash
cd examples
python example_usage.py
```

### Option 3: Run the Unit Testing Suite
Verify that strict parameter evaluation, missing key detection, and JSON schemas successfully process via:
```bash
python -m unittest tests/test_prompt_builder.py
```

## 🧠 Why This Matters to RUXAILAB
This project acts as the "safety envelope" before any data touches the AI Pipeline. 

A researcher doing a Heuristic study needs zero prompt engineering knowledge—they pass `"interface_type": "Mobile Game"` into this framework, and the system securely mounts the methodology, generates the reproducible inference payload, and returns an encrypted footprint for their scientific paper appendix. 

## ⚡ Performance Benchmark

This section presents the results of a local micro-benchmark conducted over 10,000 iterations. These measurements reflect the standalone execution of the PromptBuilder core logic and exclude external I/O operations such as database access or network calls.

**Core Metrics:**
- **Throughput:** ~4,668 operations per second (ops/sec)
- **Average Latency:** ~0.214 ms per prompt generation

**Interpretation:**
The system uses deterministic, template-based variable substitution. Since no AI inference is involved during prompt construction, execution remains consistent and operates in effectively constant time. This makes the PromptBuilder lightweight and suitable for backend integration without introducing noticeable overhead.

> **Note:** End-to-end latency in a production environment will primarily depend on external factors such as Firebase operations and LLM API response times.
