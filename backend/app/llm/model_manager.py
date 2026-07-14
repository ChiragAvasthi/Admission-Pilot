import logging
from typing import Dict, List, Optional
from app.llm.local_llm import LocalLLM

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self, default_model: str = "qwen:3b", base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.active_model_name = default_model
        self.active_llm = LocalLLM(model_name=default_model, base_url=base_url)
        self.available_models = ["qwen:3b", "llama3", "mistral", "gemma"]

    def switch_model(self, model_name: str) -> bool:
        if model_name not in self.available_models:
            logger.warning(f"Model {model_name} is not in the recognized available models list, attempting anyway.")
            
        logger.info(f"Switching active model to {model_name}")
        new_llm = LocalLLM(model_name=model_name, base_url=self.base_url)
        
        if new_llm.health_check():
            self.active_model_name = model_name
            self.active_llm = new_llm
            logger.info(f"Successfully switched to {model_name}")
            return True
        else:
            logger.error(f"Failed to connect to model {model_name}. Reverting to {self.active_model_name}")
            return False

    def get_active_model(self) -> LocalLLM:
        return self.active_llm

    def list_available_models(self) -> List[str]:
        return self.available_models

    def check_availability(self) -> bool:
        return self.active_llm.health_check()
