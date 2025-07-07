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
        
        # Detay seviyesi kontrolü
        detail_level = project_data.get('detail_level', 'detailed')
        include_examples = project_data.get('include_examples', True)
        
        self.log_info(f"PRP üretimi başlatılıyor - Detay seviyesi: {detail_level}")
        
        # Giriş validasyonu
        validation_result = self._validate_inputs(project_data, requirements, detail_level)
        if not validation_result['valid']:
            self.log_error(f"Giriş validasyon hatası: {validation_result['error']}")
            return self._get_error_prp(validation_result['error'], project_data)
        
        try:
            # Detay seviyesine göre sistem prompt'u
            system_prompt = self._get_system_prompt(detail_level, include_examples)
            
            # Detay seviyesine göre user prompt'u
            user_prompt = self._create_user_prompt(project_data, requirements, detail_level)
            
            # LLM'den yanıt al
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            response = await self.llm_client.generate_response(full_prompt)
            
            # Çıktı validasyonu
            validated_response = self._validate_output(response, detail_level)
            
            self.log_info(f"PRP başarıyla üretildi - Detay seviyesi: {detail_level}, Uzunluk: {len(validated_response)} karakter")
            return validated_response
                
        except Exception as e:
            self.log_error(f"PRP üretme hatası: {str(e)}")
            return self._get_fallback_prp(project_data, requirements, detail_level)
    
    def _validate_inputs(self, project_data: Dict[str, Any], requirements: Dict[str, Any], detail_level: str) -> Dict[str, Any]:
        """Giriş verilerini validate et"""
        
        errors = []
        
        # Zorunlu alanları kontrol et
        required_fields = ['project_name', 'project_type']
        for field in required_fields:
            if not project_data.get(field):
                errors.append(f"Zorunlu alan eksik: {field}")
        
        # Detay seviyesi kontrolü
        valid_detail_levels = ['basic', 'detailed', 'comprehensive']
        if detail_level not in valid_detail_levels:
            errors.append(f"Geçersiz detay seviyesi: {detail_level}. Geçerli seçenekler: {', '.join(valid_detail_levels)}")
        
        # Proje türü kontrolü
        valid_project_types = ['Web Application', 'Mobile App', 'Desktop Application', 'API Service', 'Machine Learning', 'Data Analysis', 'DevOps Tool', 'Other']
        project_type = project_data.get('project_type')
        if project_type and project_type not in valid_project_types:
            self.log_warning(f"Bilinmeyen proje türü: {project_type}")
        
        # Detay seviyesine göre minimum gereksinimler
        if detail_level == 'comprehensive':
            if not project_data.get('description'):
                errors.append("Kapsamlı seviye için proje açıklaması zorunludur")
            # Tech stack kontrolü - boş liste veya None kontrolü
            tech_stack = project_data.get('tech_stack')
            if not tech_stack or (isinstance(tech_stack, list) and len(tech_stack) == 0):
                errors.append("Kapsamlı seviye için teknoloji stack bilgisi zorunludur")
        
        # Requirements kontrolü
        if not requirements:
            if detail_level != 'basic':
                errors.append(f"{detail_level} seviyesi için gereksinimler zorunludur")
        
        return {
            'valid': len(errors) == 0,
            'error': '; '.join(errors) if errors else None,
            'warnings': []
        }
    
    def _create_user_prompt(self, project_data: Dict[str, Any], requirements: Dict[str, Any], detail_level: str) -> str:
        """Detay seviyesine göre user prompt oluştur"""
        
        base_prompt = f"""
        Lütfen aşağıdaki proje bilgilerini kullanarak sample_prp.md formatında bir Product Requirements Prompt oluştur:

        PROJE BİLGİLERİ:
        {json.dumps(project_data, indent=2, ensure_ascii=False)}

        GEREKSİNİMLER:
        {json.dumps(requirements, indent=2, ensure_ascii=False)}
        """
        
        # Detay seviyesine göre özel talimatlar
        if detail_level == 'basic':
            base_prompt += """
            
            DETAY SEVİYESİ: TEMEL
            - Temel bölümleri içeren kısa ve öz bir PRP oluştur
            - Purpose, Goal, Implementation Blueprint ve Validation Loop bölümlerini dahil et
            - Kod örnekleri basit ve anlaşılır olsun
            - Maksimum 2000 kelime ile sınırla
            """
        elif detail_level == 'detailed':
            base_prompt += """
            
            DETAY SEVİYESİ: DETAYLI
            - Standart PRP formatında tüm ana bölümleri dahil et
            - Kod örnekleri ve pseudocode ekle
            - Test stratejileri ve validation adımları detaylandır
            - Orta seviye karmaşıklıkta içerik üret
            """
        elif detail_level == 'comprehensive':
            base_prompt += """
            
            DETAY SEVİYESİ: KAPSAMLI
            - Sample_prp.md formatında TÜM bölümleri eksiksiz dahil et
            - Detaylı kod örnekleri, pseudocode ve implementasyon adımları
            - Kapsamlı test stratejileri ve validation döngüleri
            - Architecture patterns ve best practices dahil et
            - Integration points ve deployment stratejileri ekle
            - Anti-patterns ve gotchas bölümlerini detaylandır
            """
        
        return base_prompt
    
    def _validate_output(self, response: str, detail_level: str) -> str:
        """Çıktıyı validate et ve gerekirse düzelt"""
        
        if not response or len(response.strip()) < 100:
            self.log_error("PRP çıktısı çok kısa veya boş")
            return self._get_fallback_prp({}, {}, detail_level)
        
        # Zorunlu bölümlerin varlığını kontrol et
        required_sections = ['Purpose', 'Goal', 'Implementation Blueprint']
        missing_sections = []
        
        for section in required_sections:
            if f"## {section}" not in response and f"# {section}" not in response:
                missing_sections.append(section)
        
        if missing_sections:
            self.log_warning(f"Eksik bölümler tespit edildi: {', '.join(missing_sections)}")
        
        # Detay seviyesine göre ek kontroller
        if detail_level == 'comprehensive':
            comprehensive_sections = ['All Needed Context', 'Validation Loop', 'Anti-Patterns', 'Confidence Score']
            missing_comprehensive = []
            
            for section in comprehensive_sections:
                if section not in response:
                    missing_comprehensive.append(section)
            
            if missing_comprehensive:
                self.log_warning(f"Kapsamlı seviye için eksik bölümler: {', '.join(missing_comprehensive)}")
        
        # Minimum uzunluk kontrolü
        min_lengths = {
            'basic': 1000,
            'detailed': 3000,
            'comprehensive': 5000
        }
        
        min_length = min_lengths.get(detail_level, 2000)
        if len(response) < min_length:
            self.log_warning(f"PRP çıktısı beklenen uzunluktan kısa: {len(response)} < {min_length}")
        
        return response
    
    def _get_error_prp(self, error_message: str, project_data: Dict[str, Any]) -> str:
        """Hata durumunda özel PRP"""
        
        project_name = project_data.get('project_name', 'Bilinmeyen Proje')
        
        return f'''name: "{project_name} - HATA"
description: |

## HATA DURUMU
PRP üretimi sırasında aşağıdaki hata oluştu:

**Hata:** {error_message}

## Çözüm Önerileri
1. Proje bilgilerini kontrol edin
2. Zorunlu alanları doldurun
3. Geçerli bir detay seviyesi seçin
4. Tekrar deneyin

## Minimum Gereksinimler
- **Proje Adı**: Zorunlu
- **Proje Türü**: Zorunlu
- **Detay Seviyesi**: basic, detailed, veya comprehensive

Lütfen eksik bilgileri tamamlayıp tekrar deneyin.

---
*Hata zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
'''
    
    def _get_system_prompt(self, detail_level: str = 'detailed', include_examples: bool = True) -> str:
        """Detay seviyesine göre sistem prompt'unu döndür"""
        
        base_prompt = """
        Sen bir Product Requirements Prompt (PRP) uzmanısın. Görevin, verilen proje bilgilerini kullanarak 
        sample_prp.md formatında profesyonel bir PRP oluşturmak.

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
        
        # Detay seviyesine göre özel talimatlar
        if detail_level == 'basic':
            base_prompt += """
            
            DETAY SEVİYESİ: TEMEL
            - Sadece temel bölümleri dahil et (Purpose, Goal, Implementation Blueprint, Validation Loop)
            - Kısa ve öz açıklamalar yap
            - Basit kod örnekleri kullan
            - Maksimum 2000 kelime ile sınırla
            """
        elif detail_level == 'detailed':
            base_prompt += """
            
            DETAY SEVİYESİ: DETAYLI
            - Standart PRP formatında tüm ana bölümleri dahil et
            - Orta seviye detayda açıklamalar yap
            - Kod örnekleri ve pseudocode ekle
            - Test stratejileri dahil et
            """
        elif detail_level == 'comprehensive':
            base_prompt += """
            
            DETAY SEVİYESİ: KAPSAMLI
            - Sample_prp.md formatında TÜM bölümleri eksiksiz dahil et
            - Maksimum detay seviyesinde açıklamalar yap
            - Kapsamlı kod örnekleri, pseudocode ve implementasyon adımları
            - Detaylı test stratejileri ve validation döngüleri
            - Architecture patterns ve best practices
            - Integration points ve deployment stratejileri
            - Anti-patterns ve gotchas bölümleri
            - Confidence score ile birlikte
            """
        
        if not include_examples:
            base_prompt += """
            
            NOT: Kod örneklerini minimum seviyede tut, sadece gerekli yerlerde kullan.
            """
        
        return base_prompt
    
    def _get_fallback_prp(self, project_data: Dict[str, Any], requirements: Dict[str, Any], detail_level: str = 'detailed') -> str:
        """Hata durumunda fallback PRP"""
        
        project_name = project_data.get('project_name', 'Yeni Proje')
        project_type = project_data.get('project_type', 'Web Application')
        description = project_data.get('description', 'Modern web uygulaması')
        
        # Detay seviyesine göre farklı fallback içerikleri
        if detail_level == 'basic':
            return self._get_basic_fallback_prp(project_name, project_type, description)
        elif detail_level == 'comprehensive':
            return self._get_comprehensive_fallback_prp(project_name, project_type, description, project_data, requirements)
        else:
            return self._get_detailed_fallback_prp(project_name, project_type, description, project_data)
    
    def _get_basic_fallback_prp(self, project_name: str, project_type: str, description: str) -> str:
        """Temel seviye fallback PRP"""
        
        return f'''name: "{project_name}"
description: |

## Purpose
{description} geliştirmek ve temel ihtiyaçları karşılamak.

## Goal
{project_type} türünde basit ve kullanışlı bir uygulama geliştirmek.

## Implementation Blueprint

### Basic Structure
```
{project_name.lower().replace(' ', '_')}/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
├── requirements.txt
└── README.md
```

### Core Tasks
1. **Setup**: Proje yapısını oluştur
2. **Development**: Temel fonksiyonları geliştir
3. **Testing**: Basit testleri yaz
4. **Documentation**: README dosyasını hazırla

## Validation Loop

### Basic Checks
- Code syntax kontrolü
- Basit unit testler
- Functionality test

---
*Temel seviye PRP - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
'''
    
    def _get_detailed_fallback_prp(self, project_name: str, project_type: str, description: str, project_data: Dict[str, Any]) -> str:
        """Detaylı seviye fallback PRP"""
        
        tech_stack = project_data.get('tech_stack', 'Python, Flask')
        
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
    
    def _get_comprehensive_fallback_prp(self, project_name: str, project_type: str, description: str, 
                                      project_data: Dict[str, Any], requirements: Dict[str, Any]) -> str:
        """Kapsamlı seviye fallback PRP"""
        
        tech_stack = project_data.get('tech_stack', 'Python, Flask, PostgreSQL')
        target_platform = project_data.get('target_platform', 'Web')
        
        return f'''name: "{project_name}"
description: |

## Purpose
{description} geliştirmek ve kullanıcılara maksimum değer katmak. Bu proje, modern yazılım geliştirme standartlarını takip ederek ölçeklenebilir ve sürdürülebilir bir çözüm sunmayı amaçlar.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance

---

## Goal
{project_type} türünde enterprise-grade, kullanıcı dostu ve yüksek performanslı bir uygulama geliştirmek.

## Why
- **Business value**: Kullanıcı ihtiyaçlarını karşılar ve iş süreçlerini optimize eder
- **Integration**: Modern teknoloji stack ile entegre çalışır
- **Problems solved**: Mevcut manual süreçleri otomatikleştirir ve verimliliği artırır

## What
{description}

### Success Criteria
- [ ] Tüm fonksiyonel gereksinimler karşılanmış
- [ ] Performance benchmarks'ları geçmiş
- [ ] Security audit'i tamamlanmış
- [ ] Scalability test'leri başarılı
- [ ] User acceptance test'leri geçmiş
- [ ] Production deployment hazır

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: https://docs.python.org/3/
  why: Python best practices and standards
  
- url: https://flask.palletsprojects.com/
  why: Framework documentation
  
- file: requirements.txt
  why: Dependencies and versions
  
- file: README.md
  why: Project setup and usage instructions
```

### Current Codebase tree
```bash
{project_name.lower().replace(' ', '_')}/
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── models/
│   ├── views/
│   ├── utils/
│   └── config/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Desired Codebase tree with files to be added
```bash
{project_name.lower().replace(' ', '_')}/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── middleware.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── business_logic.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── migrations/
│   └── frontend/
│       ├── static/
│       └── templates/
├── deployment/
│   ├── docker/
│   ├── kubernetes/
│   └── scripts/
├── monitoring/
│   ├── logs/
│   └── metrics/
└── security/
    ├── ssl/
    └── auth/
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: Flask application context
# GOTCHA: Always use app.app_context() for database operations outside request context
with app.app_context():
    db.session.commit()

# CRITICAL: SQL injection prevention
# GOTCHA: Always use parameterized queries
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# CRITICAL: Memory management
# GOTCHA: Close database connections properly
try:
    result = db.session.execute(query)
finally:
    db.session.close()
```

## Implementation Blueprint

### Data models and structure
```python
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {{
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }}
    
    def validate(self):
        errors = []
        if not self.name:
            errors.append("Name is required")
        if not self.type:
            errors.append("Type is required")
        return errors
```

### List of tasks to be completed
```yaml
Task 1: Project Setup and Configuration
CREATE project_structure:
  - PATTERN: Standard Python project layout
  - Setup virtual environment
  - Configure requirements.txt
  - Setup .env configuration
  - Initialize git repository

Task 2: Database Design and Setup
CREATE database/:
  - PATTERN: SQLAlchemy ORM with migrations
  - Design database schema
  - Create migration scripts
  - Setup connection pooling
  - Configure backup strategy

Task 3: Core API Development
CREATE src/api/:
  - PATTERN: RESTful API with Flask-RESTful
  - Implement CRUD operations
  - Add input validation
  - Setup error handling
  - Add rate limiting

Task 4: Business Logic Implementation
CREATE src/services/:
  - PATTERN: Service layer pattern
  - Implement business rules
  - Add data validation
  - Setup transaction management
  - Add logging and monitoring

Task 5: Frontend Development
CREATE src/frontend/:
  - PATTERN: Modern responsive design
  - Implement user interface
  - Add client-side validation
  - Setup state management
  - Add accessibility features

Task 6: Security Implementation
CREATE security/:
  - PATTERN: Defense in depth
  - Implement authentication
  - Add authorization checks
  - Setup HTTPS/TLS
  - Add input sanitization

Task 7: Testing Suite
CREATE tests/:
  - PATTERN: Comprehensive test coverage
  - Write unit tests (80%+ coverage)
  - Add integration tests
  - Setup e2e tests
  - Add performance tests

Task 8: Deployment and DevOps
CREATE deployment/:
  - PATTERN: Containerized deployment
  - Setup Docker containers
  - Configure CI/CD pipeline
  - Add monitoring and logging
  - Setup backup and recovery
```

### Per task pseudocode
```python
# Task 1: Project Setup
def setup_project():
    # PATTERN: Standard Python project initialization
    # GOTCHA: Always use virtual environments
    create_virtual_environment()
    install_dependencies()
    setup_configuration()
    initialize_git()

# Task 2: Database Setup
def setup_database():
    # PATTERN: SQLAlchemy with Alembic migrations
    # GOTCHA: Always use migrations for schema changes
    create_database_models()
    generate_migration_scripts()
    apply_migrations()
    setup_connection_pooling()

# Task 3: API Development
def create_api_endpoints():
    # PATTERN: RESTful API design
    # GOTCHA: Always validate input data
    for endpoint in api_endpoints:
        validate_input(endpoint.data)
        process_request(endpoint)
        return_response(endpoint)
```

### Integration Points
```yaml
ENVIRONMENT:
  - add to: .env
  - vars: |
      DATABASE_URL=postgresql://user:pass@localhost/db
      SECRET_KEY=your-secret-key-here
      DEBUG=False
      FLASK_ENV=production
      
CONFIG:
  - Database connection pooling
  - Redis for caching
  - Celery for background tasks
  - Nginx for reverse proxy
  
DEPENDENCIES:
  - Update requirements.txt with:
    - Flask>=2.0.0
    - SQLAlchemy>=1.4.0
    - psycopg2-binary>=2.9.0
    - redis>=4.0.0
    - celery>=5.2.0
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
flake8 src/ --max-line-length=88
black src/ --check
isort src/ --check-only
mypy src/
bandit -r src/
```

### Level 2: Unit Tests
```python
# test_models.py
async def test_project_model():
    project = Project(name="Test", type="Web App")
    assert project.validate() == []
    assert project.name == "Test"
    
# test_api.py
async def test_create_project():
    response = client.post('/api/projects', json={{'name': 'Test', 'type': 'Web App'}})
    assert response.status_code == 201
    assert response.json['name'] == 'Test'
```

### Level 3: Integration Test
```bash
# Run full integration test suite
pytest tests/integration/ -v --cov=src --cov-report=html
```

### Level 4: Performance Test
```bash
# Load testing with locust
locust -f tests/performance/locustfile.py --host=http://localhost:5000
```

### Level 5: Security Test
```bash
# Security scanning
bandit -r src/
safety check
```

## Final Validation Checklist
- [ ] All unit tests pass (80%+ coverage)
- [ ] Integration tests pass
- [ ] Performance benchmarks met
- [ ] Security scan clean
- [ ] Code quality checks pass
- [ ] Documentation complete
- [ ] Deployment scripts tested

---

## Anti-Patterns to Avoid
- ❌ Don't hardcode sensitive data (use environment variables)
- ❌ Don't skip input validation (always validate user input)
- ❌ Don't ignore error handling (implement comprehensive error handling)
- ❌ Don't use global variables (use dependency injection)
- ❌ Don't skip database migrations (always use migration scripts)
- ❌ Don't ignore performance implications (profile and optimize)
- ❌ Don't skip security considerations (implement defense in depth)

## Confidence Score: 9/10

Very high confidence due to comprehensive approach and established patterns. Minor uncertainty on specific business requirements that may emerge during development.

---
*Kapsamlı seviye PRP - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
''' 