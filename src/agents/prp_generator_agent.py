"""
PRP Generator Agent
==================

Bu modül, sample_prp.md formatında eksiksiz Product Requirements Prompt üreten AI agent'ı içerir.
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from ..api.llm_factory import LLMClient
from ..utils.logger import LoggerMixin

class PRPGeneratorAgent(LoggerMixin):
    """Sample PRP formatında eksiksiz PRP üreten agent"""
    
    def __init__(self, llm_client: LLMClient, logger=None):
        super().__init__()
        self.llm_client = llm_client
        self.logger = logger
        
        self.log_info("PRP Generator Agent başlatıldı")
    
    async def generate_comprehensive_prp(self, 
                                       project_data: Dict[str, Any], 
                                       requirements: Dict[str, Any]) -> str:
        """
        Eksiksiz PRP üret
        
        Args:
            project_data: Proje temel bilgileri
            requirements: Proje gereksinimleri
            
        Returns:
            Sample PRP formatında eksiksiz PRP metni
        """
        
        self.log_info("Eksiksiz PRP üretimi başlatılıyor")
        
        try:
            # Sistem prompt'u
            system_prompt = self._get_system_prompt()
            
            # User prompt'u
            user_prompt = f"""
            Lütfen aşağıdaki proje bilgilerini kullanarak sample_prp.md formatında eksiksiz bir Product Requirements Prompt oluştur:

            PROJE BİLGİLERİ:
            {json.dumps(project_data, indent=2, ensure_ascii=False)}

            GEREKSİNİMLER:
            {json.dumps(requirements, indent=2, ensure_ascii=False)}

            Lütfen sample_prp.md formatında tüm bölümleri içeren eksiksiz bir PRP oluştur.
            """
            
            # LLM'den yanıt al
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            response = await self.llm_client.generate_response(full_prompt)
            
            self.log_info("Eksiksiz PRP başarıyla üretildi")
            return response
                
        except Exception as e:
            self.log_error(f"PRP üretme hatası: {str(e)}")
            return self._get_fallback_prp(project_data, requirements)
    
    def _get_system_prompt(self) -> str:
        """Sistem prompt'unu döndür"""
        
        return """
        Sen bir Product Requirements Prompt (PRP) uzmanısın. Görevin, verilen proje bilgilerini kullanarak 
        sample_prp.md formatında eksiksiz ve profesyonel bir PRP oluşturmak.

        PRP FORMATI (sample_prp.md'deki gibi):

        ```
        name: "Proje Adı"
        description: |
        
        ## Purpose
        [Projenin amacı ve neden önemli olduğu]
        
        ## Core Principles
        1. **Context is King**: Include ALL necessary documentation, examples, and caveats
        2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
        3. **Information Dense**: Use keywords and patterns from the codebase
        4. **Progressive Success**: Start simple, validate, then enhance
        
        ---
        
        ## Goal
        [Net ve ölçülebilir hedef]
        
        ## Why
        - **Business value**: [İş değeri]
        - **Integration**: [Entegrasyon faydaları]
        - **Problems solved**: [Çözülen problemler]
        
        ## What
        [Detaylı proje açıklaması ve özellikler]
        
        ### Success Criteria
        - [ ] [Başarı kriteri 1]
        - [ ] [Başarı kriteri 2]
        - [ ] [Başarı kriteri 3]
        
        ## All Needed Context
        
        ### Documentation & References
        ```yaml
        # MUST READ - Include these in your context window
        - url: [İlgili dokümantasyon URL'leri]
          why: [Neden önemli]
        
        - file: [İlgili dosyalar]
          why: [Neden önemli]
        ```
        
        ### Current Codebase tree
        ```bash
        [Mevcut proje yapısı]
        ```
        
        ### Desired Codebase tree with files to be added
        ```bash
        [Hedeflenen proje yapısı]
        ```
        
        ### Known Gotchas & Library Quirks
        ```python
        # CRITICAL: [Önemli uyarılar ve kütüphane özellikleri]
        ```
        
        ## Implementation Blueprint
        
        ### Data models and structure
        ```python
        [Veri modelleri ve yapıları]
        ```
        
        ### List of tasks to be completed
        ```yaml
        Task 1: [Görev adı]
        CREATE [dosya]:
          - PATTERN: [Kullanılacak pattern]
          - [Detaylı açıklama]
        
        Task 2: [Görev adı]
        [Devamı...]
        ```
        
        ### Per task pseudocode
        ```python
        # Task 1: [Görev adı]
        [Pseudocode örneği]
        ```
        
        ### Integration Points
        ```yaml
        ENVIRONMENT:
          - add to: .env
          - vars: |
              [Environment variables]
              
        CONFIG:
          - [Konfigürasyon detayları]
          
        DEPENDENCIES:
          - [Bağımlılıklar]
        ```
        
        ## Validation Loop
        
        ### Level 1: Syntax & Style
        ```bash
        [Syntax ve style kontrolleri]
        ```
        
        ### Level 2: Unit Tests
        ```python
        [Unit test örnekleri]
        ```
        
        ### Level 3: Integration Test
        ```bash
        [Entegrasyon testleri]
        ```
        
        ## Final Validation Checklist
        - [ ] [Kontrol listesi öğeleri]
        
        ---
        
        ## Anti-Patterns to Avoid
        - ❌ [Kaçınılması gereken pattern'lar]
        
        ## Confidence Score: X/10
        [Güven skoru ve açıklaması]
        ```

        KURALLARI:
        1. Tüm bölümleri sample_prp.md formatında eksiksiz doldur
        2. Proje türüne uygun teknoloji stack ve pattern'lar öner
        3. Gerçekçi görevler ve zaman çizelgesi oluştur
        4. Executable kod örnekleri ve testler ekle
        5. Proje karmaşıklığına uygun detay seviyesi kullan
        6. Markdown formatını tam olarak koru
        """
    
    def _get_fallback_prp(self, project_data: Dict[str, Any], requirements: Dict[str, Any]) -> str:
        """Hata durumunda fallback PRP"""
        
        project_name = project_data.get('project_name', 'Yeni Proje')
        project_type = project_data.get('project_type', 'Web Application')
        description = project_data.get('description', 'Modern web uygulaması')
        
        return f'''name: "{project_name}"
description: |

## Purpose
{description} geliştirmek ve kullanıcılara değer katmak.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance

---

## Goal
{project_type} türünde kullanıcı dostu ve ölçeklenebilir bir uygulama geliştirmek.

## Why
- **Business value**: Kullanıcı ihtiyaçlarını karşılar ve iş süreçlerini optimize eder
- **Integration**: Modern teknoloji stack ile entegre çalışır
- **Problems solved**: Mevcut manual süreçleri otomatikleştirir

## What
{description}

### Success Criteria
- [ ] Tüm fonksiyonel gereksinimler karşılanmalı
- [ ] Performans testleri başarılı olmalı
- [ ] Güvenlik testleri geçilmeli
- [ ] Kullanıcı kabul testleri tamamlanmalı

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: https://docs.example.com/api
  why: API entegrasyonu için gerekli
  
- file: src/components/
  why: Mevcut component yapısı
```

### Current Codebase tree
```bash
.
├── src/
│   ├── components/
│   ├── pages/
│   └── utils/
├── public/
├── package.json
└── README.md
```

### Desired Codebase tree with files to be added
```bash
.
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   └── utils/
├── tests/
├── docs/
└── deployment/
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: Always handle async operations properly
# CRITICAL: Validate user inputs before processing
# CRITICAL: Use environment variables for sensitive data
```

## Implementation Blueprint

### Data models and structure
```python
class ProjectModel:
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
```

### List of tasks to be completed
```yaml
Task 1: Setup Project Structure
CREATE src/structure:
  - PATTERN: Standard React/Node.js structure
  - Create necessary directories and base files

Task 2: Implement Core Features
CREATE src/features:
  - PATTERN: Feature-based architecture
  - Implement main functionality
```

### Per task pseudocode
```python
# Task 1: Setup Project Structure
def setup_project():
    create_directory_structure()
    initialize_package_json()
    setup_development_environment()
```

### Integration Points
```yaml
ENVIRONMENT:
  - add to: .env
  - vars: |
      NODE_ENV=development
      API_URL=http://localhost:3000
      
CONFIG:
  - Database connection setup
  - API endpoints configuration
  
DEPENDENCIES:
  - {chr(10).join([f"  - {tech}" for tech in project_data.get('tech_stack', ['React', 'Node.js'])])}
```

## Validation Loop

### Level 1: Syntax & Style
```bash
npm run lint
npm run type-check
```

### Level 2: Unit Tests
```python
def test_core_functionality():
    assert project.is_valid()
    assert project.meets_requirements()
```

### Level 3: Integration Test
```bash
npm run test:integration
npm run test:e2e
```

## Final Validation Checklist
- [ ] All tests pass
- [ ] Code quality checks pass
- [ ] Documentation is complete
- [ ] Security review completed

---

## Anti-Patterns to Avoid
- ❌ Don't hardcode sensitive data
- ❌ Don't skip error handling
- ❌ Don't ignore performance implications

## Confidence Score: 8/10

High confidence due to standard technology stack and clear requirements. Minor uncertainty on specific integration details.

---
*Bu PRP, Context Engineering PRP Generator tarafından {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} tarihinde oluşturulmuştur.*
''' 