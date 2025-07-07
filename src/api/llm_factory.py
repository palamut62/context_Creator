"""
LLM Provider Factory for Context Engineering PRP Generator
"""

import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.providers.openrouter import OpenRouterProvider
from pydantic_ai.providers.deepseek import DeepSeekProvider

from ..utils.config import ApplicationConfig, LLMProviderConfig
from ..utils.logger import LoggerMixin, log_function_call


class LLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    def __init__(self, config: LLMProviderConfig, logger=None):
        self.config = config
        self.logger = logger
        self.model = None
    
    @abstractmethod
    def create_agent(self, 
                    system_prompt: str,
                    output_type: Any = str,
                    tools: Optional[list] = None) -> Agent:
        """Create an agent for the LLM"""
        pass
    
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM"""
        pass


class OpenAIClient(LLMClient):
    """OpenAI client implementation"""
    
    def __init__(self, config: LLMProviderConfig, logger=None):
        super().__init__(config, logger)
        
        if not config.api_key:
            raise ValueError("OpenAI API key is required")
        
        # OpenAI model'i provider ile oluştur
        provider = OpenAIProvider(api_key=config.api_key)
        self.model = OpenAIModel(
            model_name=config.default_model,
            provider=provider
        )
    
    def create_agent(self, 
                    system_prompt: str,
                    output_type: Any = str,
                    tools: Optional[list] = None) -> Agent:
        """OpenAI agent oluştur"""
        
        return Agent(
            model=self.model,
            system_prompt=system_prompt,
            output_type=output_type,
            tools=tools or []
        )
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """OpenAI response üret"""
        
        agent = self.create_agent("You are a helpful assistant.")
        result = await agent.run(prompt)
        return result.output

class AnthropicClient(LLMClient):
    """Anthropic Claude client implementation"""
    
    def __init__(self, config: LLMProviderConfig, logger=None):
        super().__init__(config, logger)
        
        if not config.api_key:
            raise ValueError("Anthropic API key is required")
        
        # Anthropic model'i provider ile oluştur
        provider = AnthropicProvider(api_key=config.api_key)
        self.model = AnthropicModel(
            model_name=config.default_model,
            provider=provider
        )
    
    def create_agent(self, 
                    system_prompt: str,
                    output_type: Any = str,
                    tools: Optional[list] = None) -> Agent:
        """Anthropic agent oluştur"""
        
        return Agent(
            model=self.model,
            system_prompt=system_prompt,
            output_type=output_type,
            tools=tools or []
        )
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Anthropic response üret"""
        
        agent = self.create_agent("You are a helpful assistant.")
        result = await agent.run(prompt)
        return result.output

class GeminiClient(LLMClient):
    """Google Gemini client implementation"""
    
    def __init__(self, config: LLMProviderConfig, logger=None):
        super().__init__(config, logger)
        
        if not config.api_key:
            raise ValueError("Google API key is required")
        
        # Environment variable'ı ayarla
        os.environ['GEMINI_API_KEY'] = config.api_key
        
        # Gemini model'i string provider ile oluştur
        self.model = GeminiModel(
            model_name=config.default_model,
            provider='google-gla'  # String provider kullan
        )
    
    def create_agent(self, 
                    system_prompt: str,
                    output_type: Any = str,
                    tools: Optional[list] = None) -> Agent:
        """Gemini agent oluştur"""
        
        return Agent(
            model=self.model,
            system_prompt=system_prompt,
            output_type=output_type,
            tools=tools or []
        )
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Gemini response üret"""
        
        agent = self.create_agent("You are a helpful assistant.")
        result = await agent.run(prompt)
        return result.output

class OpenRouterClient(LLMClient):
    """OpenRouter client implementation"""
    
    def __init__(self, config: LLMProviderConfig, logger=None):
        super().__init__(config, logger)
        
        if not config.api_key:
            raise ValueError("OpenRouter API key is required")
        
        # OpenRouter provider ile OpenAI model oluştur
        provider = OpenRouterProvider(api_key=config.api_key)
        self.model = OpenAIModel(
            model_name=config.default_model,
            provider=provider
        )
    
    def create_agent(self, 
                    system_prompt: str,
                    output_type: Any = str,
                    tools: Optional[list] = None) -> Agent:
        """OpenRouter agent oluştur"""
        
        return Agent(
            model=self.model,
            system_prompt=system_prompt,
            output_type=output_type,
            tools=tools or []
        )
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """OpenRouter response üret"""
        
        agent = self.create_agent("You are a helpful assistant.")
        result = await agent.run(prompt)
        return result.output

class DeepSeekClient(LLMClient):
    """DeepSeek client implementation"""
    
    def __init__(self, config: LLMProviderConfig, logger=None):
        super().__init__(config, logger)
        
        if not config.api_key:
            raise ValueError("DeepSeek API key is required")
        
        # DeepSeek provider ile OpenAI model oluştur
        provider = DeepSeekProvider(api_key=config.api_key)
        self.model = OpenAIModel(
            model_name=config.default_model,
            provider=provider
        )
    
    def create_agent(self, 
                    system_prompt: str,
                    output_type: Any = str,
                    tools: Optional[list] = None) -> Agent:
        """DeepSeek agent oluştur"""
        
        return Agent(
            model=self.model,
            system_prompt=system_prompt,
            output_type=output_type,
            tools=tools or []
        )
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """DeepSeek response üret"""
        
        agent = self.create_agent("You are a helpful assistant.")
        result = await agent.run(prompt)
        return result.output

class MockClient(LLMClient):
    """Mock client for testing"""
    
    def __init__(self, config: LLMProviderConfig, logger=None):
        super().__init__(config, logger)
    
    def create_agent(self, 
                    system_prompt: str,
                    output_type: Any = str,
                    tools: Optional[list] = None) -> Agent:
        """Mock agent oluştur"""
        
        # Test modunda mock response döndür
        class MockAgent:
            def __init__(self, system_prompt, output_type):
                self.system_prompt = system_prompt
                self.output_type = output_type
            
            async def run(self, prompt):
                class MockResult:
                    def __init__(self):
                        self.output = f"Mock response for: {prompt}"
                
                return MockResult()
        
        return MockAgent(system_prompt, output_type)
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Mock response üret"""
        return f"Mock response for: {prompt}"

class LLMProviderFactory(LoggerMixin):
    """LLM Provider Factory"""
    
    # Provider mapping
    PROVIDERS = {
        "openai": OpenAIClient,
        "anthropic": AnthropicClient,
        "gemini": GeminiClient,
        "openrouter": OpenRouterClient,
        "deepseek": DeepSeekClient,
        "mock": MockClient
    }
    
    def __init__(self, config: ApplicationConfig):
        super().__init__()
        self.config = config
        self._clients = {}
    
    @log_function_call
    def create_client(self, provider_name: str) -> LLMClient:
        """Create LLM client for given provider"""
        
        try:
            # Cache kontrolü
            if provider_name in self._clients:
                return self._clients[provider_name]
            
            # Provider validation
            if provider_name not in self.PROVIDERS:
                available = ", ".join(self.PROVIDERS.keys())
                raise ValueError(f"Unknown provider: {provider_name}. Available: {available}")
            
            # Provider config al
            provider_config = self._get_provider_config(provider_name)
            
            # Client oluştur
            client_class = self.PROVIDERS[provider_name]
            client = client_class(provider_config, self.logger)
            
            # Cache'e ekle
            self._clients[provider_name] = client
            
            self.logger.info(f"Created {provider_name} client successfully")
            return client
            
        except Exception as e:
            self.logger.error(f"Failed to create {provider_name} client: {e}")
            raise
    
    def _get_provider_config(self, provider_name: str) -> LLMProviderConfig:
        """Get provider configuration"""
        
        # Mock provider için özel config
        if provider_name == "mock":
            return LLMProviderConfig(
                name="Mock",
                api_key="mock-key",
                default_model="mock-model",
                max_tokens=1000,
                rpm_limit=60
            )
        
        # Gerçek provider'lar için config.providers'dan al
        if provider_name in self.config.providers:
            return self.config.providers[provider_name]
        
        raise ValueError(f"Provider config not found: {provider_name}")
    
    def get_available_providers(self) -> Dict[str, str]:
        """Get available providers with their status"""
        
        providers = {}
        for name in self.PROVIDERS.keys():
            try:
                config = self._get_provider_config(name)
                if config and config.api_key:
                    providers[name] = "✅ Available"
                else:
                    providers[name] = "❌ Missing API Key"
            except Exception as e:
                providers[name] = f"❌ Error: {str(e)}"
        
        return providers
    
    def validate_provider(self, provider_name: str) -> bool:
        """Validate if provider is properly configured"""
        
        try:
            config = self._get_provider_config(provider_name)
            return config is not None and bool(config.api_key)
        except Exception:
            return False 