import logging
from typing import Any, Dict, Optional, Generator
from pydantic import BaseModel
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser

logger = logging.getLogger(__name__)

class LocalLLM:
    def __init__(self, model_name: str = "qwen:3b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.llm = self._initialize_llm()

    def _initialize_llm(self) -> ChatOllama:
        return ChatOllama(
            model=self.model_name,
            base_url=self.base_url,
            temperature=0.2,
            timeout=120.0
        )

    def invoke(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        try:
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))
            
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error invoking LocalLLM: {e}")
            raise

    def stream(self, prompt: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        try:
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))
            
            for chunk in self.llm.stream(messages):
                yield chunk.content
        except Exception as e:
            logger.error(f"Error streaming LocalLLM: {e}")
            raise

    def structured_invoke(self, prompt: str, schema: BaseModel, system_prompt: Optional[str] = None) -> BaseModel:
        """
        Invokes the LLM and attempts to parse the output into the provided Pydantic schema.
        Note: True structured outputs require newer Ollama features or Langchain function calling adaptations.
        Here we use PydanticOutputParser and inject format instructions into the prompt.
        """
        parser = PydanticOutputParser(pydantic_object=schema)
        format_instructions = parser.get_format_instructions()
        
        full_prompt = f"{prompt}\n\n{format_instructions}"
        
        try:
            response_text = self.invoke(full_prompt, system_prompt)
            parsed_result = parser.invoke(response_text)
            return parsed_result
        except Exception as e:
            logger.error(f"Failed to parse structured output: {e}")
            raise

    def health_check(self) -> bool:
        # Simple health check by sending a ping prompt
        try:
            self.invoke("ping")
            return True
        except Exception:
            return False
