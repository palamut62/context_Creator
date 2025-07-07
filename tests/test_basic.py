"""
Temel Testler
============

Uygulamanın temel fonksiyonalitelerini test eder.
"""

import pytest
import sys
import os
from pathlib import Path

# Proje dizinini Python path'ine ekle
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.utils.config import load_config, ApplicationConfig
from src.models.project_data import ProjectData, ProjectRequirements
from src.api.llm_factory import LLMProviderFactory

def test_config_loading():
    """Konfigürasyon yükleme testi"""
    
    # Test modunu aktif et
    os.environ['TEST_MODE'] = 'true'
    
    try:
        config = load_config()
        assert isinstance(config, ApplicationConfig)
        assert config.test_mode == True
        print("✅ Konfigürasyon başarıyla yüklendi")
    except Exception as e:
        pytest.fail(f"Konfigürasyon yükleme hatası: {str(e)}")

def test_project_data_creation():
    """Proje veri modeli oluşturma testi"""
    
    try:
        project_data = ProjectData(
            name="Test Projesi",
            type="Web Uygulaması", 
            description="Bu bir test projesidir",
            language="Python"
        )
        
        assert project_data.name == "Test Projesi"
        assert project_data.type == "Web Uygulaması"
        assert project_data.language == "Python"
        print("✅ Proje veri modeli başarıyla oluşturuldu")
    except Exception as e:
        pytest.fail(f"Proje veri modeli oluşturma hatası: {str(e)}")

def test_project_requirements():
    """Proje gereksinimleri testi"""
    
    try:
        requirements = ProjectRequirements(
            functional_requirements="Test gereksinimi",
            frameworks="FastAPI",
            database="PostgreSQL"
        )
        
        assert requirements.functional_requirements == "Test gereksinimi"
        assert requirements.frameworks == "FastAPI"
        assert requirements.database == "PostgreSQL"
        print("✅ Proje gereksinimleri başarıyla oluşturuldu")
    except Exception as e:
        pytest.fail(f"Proje gereksinimleri oluşturma hatası: {str(e)}")

def test_llm_factory_mock():
    """LLM Factory mock testi"""
    
    # Test modunu aktif et
    os.environ['TEST_MODE'] = 'true'
    
    try:
        config = load_config()
        factory = LLMProviderFactory(config)
        
        # Mock client oluştur
        mock_client = factory.create_client("mock")
        assert mock_client is not None
        print("✅ Mock LLM client başarıyla oluşturuldu")
    except Exception as e:
        pytest.fail(f"LLM Factory mock test hatası: {str(e)}")

def test_available_providers():
    """Kullanılabilir provider'lar testi"""
    
    # Test modunu aktif et
    os.environ['TEST_MODE'] = 'true'
    
    try:
        config = load_config()
        factory = LLMProviderFactory(config)
        
        available = factory.get_available_providers()
        assert len(available) > 0
        assert "mock" in available
        print(f"✅ Kullanılabilir provider'lar: {list(available.keys())}")
    except Exception as e:
        pytest.fail(f"Available providers test hatası: {str(e)}")

def test_project_validation():
    """Proje validasyon testi"""
    
    try:
        # Geçersiz proje adı ile test
        with pytest.raises(ValueError):
            ProjectData(
                name="",  # Boş ad
                type="Web Uygulaması",
                description="Test",
                language="Python"
            )
        
        # Geçersiz açıklama ile test
        with pytest.raises(ValueError):
            ProjectData(
                name="Test",
                type="Web Uygulaması", 
                description="",  # Boş açıklama
                language="Python"
            )
        
        print("✅ Proje validasyon testleri başarılı")
    except Exception as e:
        pytest.fail(f"Proje validasyon test hatası: {str(e)}")

if __name__ == "__main__":
    """Testleri doğrudan çalıştır"""
    
    print("🧪 Temel testler başlatılıyor...\n")
    
    try:
        test_config_loading()
        test_project_data_creation()
        test_project_requirements()
        test_llm_factory_mock()
        test_available_providers()
        test_project_validation()
        
        print("\n🎉 Tüm testler başarılı!")
        
    except Exception as e:
        print(f"\n❌ Test hatası: {str(e)}")
        sys.exit(1) 