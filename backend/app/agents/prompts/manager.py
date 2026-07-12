import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class PromptManager:
    def __init__(self, templates_dir: str = None):
        if templates_dir is None:
            # Default to the templates directory relative to this file
            base_path = Path(__file__).parent
            self.templates_dir = base_path / "templates"
        else:
            self.templates_dir = Path(templates_dir)
            
        if not self.templates_dir.exists():
            self.templates_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created templates directory at {self.templates_dir}")

    def load_prompt(self, template_name: str, **kwargs) -> str:
        """
        Loads a prompt template by name and formats it with the provided kwargs.
        Assumes .txt extension if not provided.
        """
        if not template_name.endswith('.txt') and not template_name.endswith('.yaml'):
            template_name += '.txt'
            
        file_path = self.templates_dir / template_name
        
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt template {template_name} not found at {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
            
        try:
            return template_content.format(**kwargs)
        except KeyError as e:
            logger.error(f"Missing required formatting key {e} for template {template_name}")
            raise
