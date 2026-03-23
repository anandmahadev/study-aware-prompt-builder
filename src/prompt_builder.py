import json
import os
import re
import datetime
import hashlib
import logging
from typing import Dict, Any, Set
from dataclasses import dataclass

# Custom Exceptions
from src.exceptions import TemplateLoadError, MissingParameterError, ParameterTypeError

# Professional Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("StudyAwarePromptBuilder")

@dataclass
class PromptResult:
    """Represents a successfully generated prompt alongside trace metadata."""
    prompt_text: str
    template_version: str
    methodology: str
    generation_timestamp: str
    trace_hash: str  # Critical for reproducible UX science (RUXAILAB core requirement)

class PromptBuilder:
    """
    A strictly typed pipeline linking UX evaluation methodologies to LLM-ready variables.
    """

    def __init__(self):
        self.template_text: str = ""
        self.required_parameters: Set[str] = set()
        self.metadata: Dict[str, str] = {}

    def load_template(self, file_path: str) -> None:
        """Loads and strictly parses an evaluation methodology schema."""
        logger.debug(f"Attempting to load template from: {file_path}")
        
        if not os.path.exists(file_path):
            raise TemplateLoadError(f"Template path invalid or inaccessible: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise TemplateLoadError(f"Corrupted or invalid JSON format detected: {e}")

        if "template" not in data:
            raise TemplateLoadError("The JSON template is missing the required 'template' root key.")

        self.template_text = data["template"]
        self.metadata = data.get("metadata", {
            "version": "unknown", "methodology": "unknown", "author": "unknown"
        })
        
        self._extract_placeholders()
        logger.info(f"Loaded methodology '{self.metadata.get('methodology')}' Schema successfully.")

    def _extract_placeholders(self) -> None:
        """Regex scanning for injection points in the text template."""
        pattern = r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}"
        matches = re.findall(pattern, self.template_text)
        self.required_parameters = set(matches)
        logger.debug(f"Discovered parameters: {self.required_parameters}")

    def validate_parameters(self, parameters: Dict[str, Any]) -> None:
        """Strict schema enforcement to prevent dirty LLM outputs."""
        missing = [param for param in self.required_parameters if param not in parameters]
        if missing:
            raise MissingParameterError(f"Required placeholders absent from input: {', '.join(missing)}")
            
        for key, value in parameters.items():
            if not isinstance(value, (str, int, float)):
                raise ParameterTypeError(f"Injected value for '{key}' rejected. Must be str/int/float, got {type(value).__name__}.")

    def build_prompt(self, parameters: Dict[str, Any]) -> PromptResult:
        """Consumes evaluated parameters and generates the hashed final inference text."""
        if not self.template_text:
            raise TemplateLoadError("Builder called without a loaded template.")

        logger.debug("Validating study parameters before string generation...")
        self.validate_parameters(parameters)

        final_prompt = self.template_text
        for param, value in parameters.items():
            placeholder = f"{{{{{param}}}}}"
            final_prompt = final_prompt.replace(placeholder, str(value))

        # Scientific Auditing Hash
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        hash_input = f"{self.metadata.get('version')}-{final_prompt}-{timestamp}"
        trace_hash = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()[:12]

        logger.info(f"Prompt text built successfully. Run Hash: {trace_hash}")

        return PromptResult(
            prompt_text=final_prompt,
            template_version=self.metadata.get("version", "unknown"),
            methodology=self.metadata.get("methodology", "unknown"),
            generation_timestamp=timestamp,
            trace_hash=trace_hash
        )
