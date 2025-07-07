"""
Konfigürasyon Yönetimi
=====================

Bu modül, uygulamanın tüm konfigürasyon ayarlarını yönetir.
Environment variables, default values ve validation işlemlerini içerir.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

class LLMProviderConfig(BaseModel):
    """LLM Provider konfigürasyonu"""
    name: str
    api_key: Optional[str] = None
    default_model: str
    rpm_limit: int = Field(default=60, description="Requests per minute")
    max_tokens: int = Field(default=8192, description="Maximum tokens per request")
    base_url: Optional[str] = None
    
    @validator('api_key')
    def validate_api_key(cls, v, values):
        """API anahtarının varlığını kontrol et"""
        if not v:
            provider_name = values.get('name', 'unknown')
            # Test modunda API anahtarı zorunlu değil
            if not os.getenv('TEST_MODE', 'false').lower() == 'true':
                print(f"⚠️  {provider_name} API anahtarı bulunamadı")
        return v



class SecurityConfig(BaseModel):
    """Güvenlik konfigürasyonu"""
    session_timeout_minutes: int = Field(default=60)
    max_concurrent_sessions: int = Field(default=100)
    max_input_length: int = Field(default=10000)
    allowed_file_types: list[str] = Field(default=[".md", ".txt", ".json"])

class ApplicationConfig(BaseSettings):
    """Ana uygulama konfigürasyonu"""
    
    # LLM Provider Configurations
    providers: Dict[str, LLMProviderConfig] = Field(default_factory=dict)
    default_provider: str = Field(default="openai")
    
    # Application Settings
    max_tokens_per_request: int = Field(default=8192)
    max_context_tokens: int = Field(default=32768)
    

    
    # Security Settings
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    
    # Logging Configuration
    log_level: str = Field(default="INFO")
    log_file: str = Field(default="logs/app.log")
    
    # Cache Configuration
    enable_caching: bool = Field(default=True)
    cache_ttl_seconds: int = Field(default=3600)
    
    # Development Settings
    debug_mode: bool = Field(default=False)
    enable_detailed_logging: bool = Field(default=False)
    test_mode: bool = Field(default=False)
    mock_api_responses: bool = Field(default=False)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Extra fields'ları ignore et

def create_provider_configs() -> Dict[str, LLMProviderConfig]:
    """LLM provider konfigürasyonlarını oluştur"""
    
    providers = {
        "openai": LLMProviderConfig(
            name="OpenAI",
            api_key=os.getenv("OPENAI_API_KEY"),
            default_model=os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o"),
            rpm_limit=int(os.getenv("OPENAI_RPM", "60")),
            max_tokens=int(os.getenv("MAX_TOKENS_PER_REQUEST", "8192"))
        ),
        
        "gemini": LLMProviderConfig(
            name="Google Gemini",
            api_key=os.getenv("GOOGLE_API_KEY"),
            default_model=os.getenv("GEMINI_DEFAULT_MODEL", "gemini-2.5-flash"),
            rpm_limit=int(os.getenv("GEMINI_RPM", "60")),
            max_tokens=int(os.getenv("MAX_TOKENS_PER_REQUEST", "8192"))
        ),
        
        "anthropic": LLMProviderConfig(
            name="Anthropic Claude",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            default_model=os.getenv("ANTHROPIC_DEFAULT_MODEL", "claude-3-5-sonnet-20241022"),
            rpm_limit=int(os.getenv("ANTHROPIC_RPM", "50")),
            max_tokens=int(os.getenv("MAX_TOKENS_PER_REQUEST", "8192"))
        ),
        
        "openrouter": LLMProviderConfig(
            name="OpenRouter",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            default_model=os.getenv("OPENROUTER_DEFAULT_MODEL", "anthropic/claude-3.5-sonnet"),
            rpm_limit=int(os.getenv("OPENROUTER_RPM", "20")),
            max_tokens=int(os.getenv("MAX_TOKENS_PER_REQUEST", "8192")),
            base_url="https://openrouter.ai/api/v1"
        ),
        
        "deepseek": LLMProviderConfig(
            name="DeepSeek",
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            default_model=os.getenv("DEEPSEEK_DEFAULT_MODEL", "deepseek-chat"),
            rpm_limit=int(os.getenv("DEEPSEEK_RPM", "60")),
            max_tokens=int(os.getenv("MAX_TOKENS_PER_REQUEST", "8192")),
            base_url="https://api.deepseek.com"
        )
    }
    
    return providers

def load_config() -> ApplicationConfig:
    """Konfigürasyonu yükle ve validate et"""
    
    # Provider konfigürasyonlarını oluştur
    providers = create_provider_configs()
    
    # Ana konfigürasyonu oluştur
    config = ApplicationConfig(
        providers=providers,
        default_provider=os.getenv("DEFAULT_LLM_PROVIDER", "openai")
    )
    
    # Konfigürasyonu validate et
    validate_config(config)
    
    return config

def validate_config(config: ApplicationConfig) -> None:
    """Konfigürasyonu doğrula"""
    
    # Default provider'ın mevcut olduğunu kontrol et
    if config.default_provider not in config.providers:
        available_providers = list(config.providers.keys())
        raise ValueError(
            f"Default provider '{config.default_provider}' mevcut değil. "
            f"Mevcut provider'lar: {available_providers}"
        )
    
    # En az bir provider'ın API anahtarına sahip olduğunu kontrol et
    if not config.test_mode:
        valid_providers = [
            name for name, provider in config.providers.items()
            if provider.api_key
        ]
        
        if not valid_providers:
            print("⚠️  Hiçbir LLM provider için API anahtarı bulunamadı!")
            print("📝 Lütfen .env dosyasını kontrol edin ve gerekli API anahtarlarını ekleyin.")
    
    # Log dizininin varlığını kontrol et
    log_dir = Path(config.log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)

def get_available_providers(config: ApplicationConfig) -> Dict[str, LLMProviderConfig]:
    """Kullanılabilir provider'ları döndür (API anahtarı olanlar)"""
    
    if config.test_mode:
        return config.providers
    
    return {
        name: provider for name, provider in config.providers.items()
        if provider.api_key
    }

def get_provider_info(config: ApplicationConfig) -> Dict[str, Any]:
    """Provider bilgilerini özetleyen dict döndür"""
    
    available = get_available_providers(config)
    
    info = {
        "total_providers": len(config.providers),
        "available_providers": len(available),
        "default_provider": config.default_provider,
        "providers": {
            name: {
                "name": provider.name,
                "model": provider.default_model,
                "rpm_limit": provider.rpm_limit,
                "has_api_key": bool(provider.api_key),
                "status": "available" if provider.api_key else "missing_api_key"
            }
            for name, provider in config.providers.items()
        }
    }
    
    return info 