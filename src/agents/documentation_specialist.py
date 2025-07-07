"""
Dokümantasyon Uzmanı Ajanı
==========================

Bu modül, Context Engineering standartlarında PRP oluşturan AI ajanını içerir.
Tüm analiz sonuçlarını birleştirerek kapsamlı PRP dökümanı üretir.
"""

from typing import Dict, Any
from ..models.project_data import (
    ProjectData, AnalysisResult, ArchitectureResult, 
    TestStrategy, PRPContent
)
from ..api.llm_factory import LLMClient
from ..utils.logger import LoggerMixin, log_async_function_call

class DocumentationSpecialistAgent(LoggerMixin):
    """Dokümantasyon Uzmanı AI Ajanı"""
    
    def __init__(self, llm_client: LLMClient, logger=None):
        super().__init__()
        self.llm_client = llm_client
        self.logger = logger
        
        self.system_prompt = """
Sen deneyimli bir Dokümantasyon Uzmanı'sın ve Context Engineering konusunda uzmansın. 

Görevin, yazılım projelerinin analiz sonuçlarını kullanarak EXAMPLE_multi_agent_prp.md formatında Context Engineering standartlarına uygun PRP (Product Requirements Prompt) dökümanları oluşturmak.

ZORUNLU FORMAT (EXAMPLE_multi_agent_prp.md'den):

```
name: "[Proje Adı]: [Kısa Açıklama]"
description: |

## Purpose
[Projenin amacını açıkla - neden bu proje gerekli]

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance

---

## Goal
[Spesifik, ölçülebilir hedefleri tanımla]

## Why
- **Business value**: [İş değeri]
- **Integration**: [Entegrasyon faydaları]  
- **Problems solved**: [Çözülen problemler]

## What
[Detaylı proje açıklaması]

### Success Criteria
- [ ] [Spesifik başarı kriteri 1]
- [ ] [Spesifik başarı kriteri 2]
- [ ] [Spesifik başarı kriteri 3]

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: [relevant_documentation_url]
  why: [neden bu dokümantasyon gerekli]
  
- file: [relevant_file_path]
  why: [neden bu dosya gerekli]
```

### Current Codebase tree
```bash
[Mevcut proje yapısı]
```

### Desired Codebase tree with files to be added
```bash
[Hedeflenen proje yapısı - eklenecek dosyalar]
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: [Kritik dikkat edilmesi gerekenler]
# GOTCHA: [Yaygın hatalar ve çözümleri]
```

## Implementation Blueprint

### Data models and structure
```python
[Pydantic models ve veri yapıları]
```

### List of tasks to be completed
```yaml
Task 1: [Görev başlığı]
CREATE/UPDATE [dosya_yolu]:
  - PATTERN: [Hangi pattern'i takip et]
  - [Spesifik gereksinimler]

Task 2: [Görev başlığı]
[...]
```

### Per task pseudocode
```python
# Task X: [Görev açıklaması]
def example_function():
    # PATTERN: [Hangi pattern'i kullan]
    # GOTCHA: [Dikkat edilecek noktalar]
    pass
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
  - Update requirements.txt with:
    - [Yeni bağımlılıklar]
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
[Syntax ve style kontrol komutları]
```

### Level 2: Unit Tests
```python
# [Test dosyası adı]
async def test_[feature]():
    \"\"\"[Test açıklaması]\"\"\"
    [Test kodu]
```

### Level 3: Integration Test
```bash
# Test CLI interaction
[Integration test adımları]
```

## Final Validation Checklist
- [ ] [Kontrol listesi 1]
- [ ] [Kontrol listesi 2]
- [ ] [Kontrol listesi 3]

## Anti-Patterns to Avoid
- ❌ [Kaçınılması gereken pattern 1]
- ❌ [Kaçınılması gereken pattern 2]

## Confidence Score: X/10
[Güven skoru açıklaması]
```

ÖNEMLI KURALLAR:
- CLAUDE.md ve INITIAL.md dosyalarındaki talimatları takip et
- Context Engineering prensiplerini tam olarak uygula
- Tüm AI kod geliştirme araçları ile uyumlu olmalı
- Executable code examples ekle
- YAML, Python, Bash kod blokları kullan
- Comprehensive validation loops oluştur
- Türkçe açıklamalar ama teknik terimler İngilizce
"""
    
    @log_async_function_call
    async def generate_prp(self, 
                          project_data: ProjectData,
                          analysis_result: AnalysisResult,
                          architecture_result: ArchitectureResult,
                          test_strategy: TestStrategy) -> str:
        """PRP dökümanı oluştur"""
        
        self.log_info(
            f"PRP oluşturuluyor: {project_data.name}",
            complexity_score=analysis_result.complexity_score,
            architecture_pattern=architecture_result.architecture_pattern
        )
        
        prp_prompt = self._create_prp_prompt(
            project_data, analysis_result, architecture_result, test_strategy
        )
        
        try:
            agent = self.llm_client.create_agent(
                system_prompt=self.system_prompt,
                output_type=str  # Markdown string döndür
            )
            
            result = await agent.run(prp_prompt)
            
            if hasattr(result, 'output'):
                prp_content = result.output
            else:
                prp_content = result
            
            self.log_info(
                "PRP başarıyla oluşturuldu",
                content_length=len(prp_content)
            )
            
            return prp_content
            
        except Exception as e:
            self.log_error(f"PRP oluşturma hatası: {str(e)}")
            return self._create_fallback_prp(project_data, analysis_result, architecture_result, test_strategy)
    
    def _create_prp_prompt(self, 
                          project_data: ProjectData,
                          analysis_result: AnalysisResult,
                          architecture_result: ArchitectureResult,
                          test_strategy: TestStrategy) -> str:
        """PRP oluşturma prompt'unu hazırla"""
        
        prompt = f"""
Context Engineering standartlarına uygun bir PRP (Product Requirements Prompt) oluştur:

# Proje Bilgileri
- **Proje Adı**: {project_data.name}
- **Proje Türü**: {project_data.type}
- **Programlama Dili**: {project_data.language}
- **Hedef Platformlar**: {', '.join(project_data.platform) if project_data.platform else 'Belirtilmemiş'}
- **Ekip Büyüklüğü**: {project_data.team_size or 'Belirtilmemiş'}
- **Hedef Süre**: {project_data.timeline or 'Belirtilmemiş'}

## Proje Açıklaması
{project_data.description}

# Sistem Analizi Sonuçları
- **Karmaşıklık Skoru**: {analysis_result.complexity_score}/10
- **Risk Faktörleri**: {', '.join(analysis_result.risk_factors)}
- **Önerilen Yaklaşım**: {analysis_result.recommended_approach}
- **Ana Zorluklar**: {', '.join(analysis_result.key_challenges)}
- **Başarı Kriterleri**: {', '.join(analysis_result.success_criteria)}
- **Tahmini Efor**: {analysis_result.estimated_effort}

# Mimari Tasarım
- **Mimari Pattern**: {architecture_result.architecture_pattern}
- **Teknoloji Stack**: {', '.join(f"{k}: {v}" for k, v in architecture_result.technology_stack.items())}
- **Sistem Bileşenleri**: {', '.join(architecture_result.system_components)}
- **Veri Akışı**: {architecture_result.data_flow}
- **Güvenlik Değerlendirmeleri**: {', '.join(architecture_result.security_considerations)}
- **Ölçeklenebilirlik Planı**: {architecture_result.scalability_plan}

# Test Stratejisi
- **Test Seviyeleri**: {', '.join(test_strategy.test_levels)}
- **Test Framework'leri**: {', '.join(test_strategy.test_frameworks)}
- **Kapsam Hedefleri**: {', '.join(f"{k}: %{v}" for k, v in test_strategy.coverage_targets.items())}
- **Kalite Kontrol Noktaları**: {', '.join(test_strategy.quality_gates)}
- **Performans Testleri**: {', '.join(test_strategy.performance_tests)}
"""
        
        # Gereksinimler varsa ekle
        if project_data.requirements:
            req = project_data.requirements
            prompt += f"""
# Detaylı Gereksinimler
## Fonksiyonel Gereksinimler
{req.functional_requirements}

## Teknik Gereksinimler
- **Framework/Kütüphaneler**: {req.frameworks or 'Belirtilmemiş'}
- **Veritabanı**: {req.database or 'Belirtilmemiş'}
- **Kimlik Doğrulama**: {req.authentication or 'Belirtilmemiş'}
- **Deployment**: {req.deployment or 'Belirtilmemiş'}
- **Performans**: {req.performance or 'Belirtilmemiş'}
- **Güvenlik**: {req.security or 'Belirtilmemiş'}

## Kullanıcı Hikayeleri
{req.user_stories or 'Belirtilmemiş'}

## Kısıtlamalar
{req.constraints or 'Belirtilmemiş'}

## Özel Gereksinimler
{req.special_requirements or 'Belirtilmemiş'}

## AI Araç Uyumluluğu
Hedef AI Araçları: {', '.join(req.ai_tools)}
Context Tercihleri: {req.context_preferences or 'Belirtilmemiş'}
"""
        
        prompt += """
# PRP Oluşturma Görevin

Yukarıdaki tüm bilgileri kullanarak Context Engineering standartlarına uygun bir PRP oluştur. 

PRP şu bölümleri içermeli:

1. **Purpose**: Bu PRP'nin amacı ve hedefi
2. **Core Principles**: Context Engineering prensipleri
3. **Goal**: Spesifik proje hedefleri
4. **Implementation Blueprint**: 
   - Data Models (kod örnekleri ile)
   - Task List (öncelik sırasına göre)
   - Architecture Overview
   - Technology Stack Details
5. **Validation Loop**: 
   - Syntax & Style checks
   - Testing requirements
   - Performance benchmarks
   - Security validations
6. **Confidence Score**: Bu PRP'nin güven skoru (1-10)

## Önemli Notlar:
- Tüm AI kod geliştirme araçları (Claude, Cursor, GitHub Copilot, etc.) ile uyumlu olmalı
- Kod örnekleri dahil et
- Spesifik ve actionable olmalı
- Context Engineering yaklaşımını tam olarak uygula
- Markdown formatında çıktı ver

Lütfen kapsamlı ve detaylı bir PRP oluştur.
"""
        
        return prompt
    
    def _create_fallback_prp(self, 
                            project_data: ProjectData,
                            analysis_result: AnalysisResult,
                            architecture_result: ArchitectureResult,
                            test_strategy: TestStrategy) -> str:
        """Fallback PRP oluştur"""
        
        ai_tools = "Claude, Cursor, GitHub Copilot"
        if project_data.requirements and project_data.requirements.ai_tools:
            ai_tools = ', '.join(project_data.requirements.ai_tools)
        
        prp_content = f"""# {project_data.name} - Product Requirements Prompt (PRP)

## Purpose
Bu PRP, **{project_data.name}** projesinin Context Engineering yaklaşımına uygun şekilde geliştirilmesi için oluşturulmuştur. Proje, {project_data.type.lower()} türünde olup {project_data.language} programlama dili kullanılarak geliştirilecektir.

## Core Principles
1. **Context is King**: Kapsamlı kontekst sağlama ve bilgi yoğunluğu
2. **Validation Loops**: Sürekli doğrulama ve kalite kontrol döngüleri
3. **Information Dense**: Her adımda maksimum bilgi ve açıklama
4. **Progressive Success**: Aşamalı başarı ve iteratif geliştirme
5. **AI Tool Compatibility**: {ai_tools} gibi tüm AI araçları ile uyumlu

## Goal
{project_data.description}

### Spesifik Hedefler:
{chr(10).join(f"- {criterion}" for criterion in analysis_result.success_criteria)}

## Implementation Blueprint

### Architecture Overview
- **Pattern**: {architecture_result.architecture_pattern}
- **Karmaşıklık Seviyesi**: {analysis_result.complexity_score}/10
- **Önerilen Yaklaşım**: {analysis_result.recommended_approach}

### Technology Stack
```yaml
"""
        
        # Technology stack'i ekle
        for category, tech in architecture_result.technology_stack.items():
            prp_content += f"{category}: {tech}\n"
        
        prp_content += f"""```

### System Components
{chr(10).join(f"- {component}" for component in architecture_result.system_components)}

### Data Flow
```
{architecture_result.data_flow}
```

### Task List
1. **Proje Kurulumu**
   - Geliştirme ortamı hazırlığı
   - Dependency yönetimi
   - Version control kurulumu

2. **Core Architecture**
   - {architecture_result.architecture_pattern} pattern implementasyonu
   - Temel sistem bileşenlerinin oluşturulması
   - Veri akışının kurulması

3. **Feature Development**
"""
        
        # Fonksiyonel gereksinimleri ekle
        if project_data.requirements and project_data.requirements.functional_requirements:
            requirements_lines = project_data.requirements.functional_requirements.split('\n')
            for i, req in enumerate(requirements_lines[:5], 1):  # İlk 5 gereksinimi al
                if req.strip():
                    prp_content += f"   - {req.strip()}\n"
        
        prp_content += f"""
4. **Quality Assurance**
   - {', '.join(test_strategy.test_levels)}
   - Code coverage: {test_strategy.coverage_targets.get('Unit Tests', 80)}%+ hedefi
   - Performans optimizasyonu

5. **Deployment & Monitoring**
   - Production deployment
   - Monitoring ve logging
   - Güvenlik validasyonu

### Security Considerations
{chr(10).join(f"- {consideration}" for consideration in architecture_result.security_considerations)}

### Performance & Scalability
- **Ölçeklenebilirlik**: {architecture_result.scalability_plan}
- **Performans Testleri**: {', '.join(test_strategy.performance_tests[:3])}

## Validation Loop

### Code Quality Checks
- **Syntax & Style**: Linting ve formatting araçları
- **Type Safety**: Type checking (TypeScript, mypy, etc.)
- **Security Scan**: Güvenlik açığı taraması
- **Dependency Check**: Güvenlik açığı olan dependency kontrolü

### Testing Requirements
{chr(10).join(f"- **{level}**: {test_strategy.coverage_targets.get(level, 'Belirtilmemiş')}% kapsam hedefi" for level in test_strategy.test_levels)}

### Quality Gates
{chr(10).join(f"- {gate}" for gate in test_strategy.quality_gates)}

### Performance Benchmarks
- Response time < 2 saniye
- Throughput > 1000 req/saniye
- Memory usage < 512MB
- CPU utilization < 70%

## Risk Mitigation
### Tespit Edilen Riskler:
{chr(10).join(f"- **{risk}**: Düzenli monitoring ve proaktif çözümler" for risk in analysis_result.risk_factors)}

### Ana Zorluklar:
{chr(10).join(f"- {challenge}" for challenge in analysis_result.key_challenges)}

## AI Tool Integration
Bu PRP aşağıdaki AI kod geliştirme araçları ile optimize edilmiştir:
- **{ai_tools}**

### Context Engineering Optimizasyonları:
- Detaylı kod örnekleri ve açıklamalar
- Adım adım implementasyon kılavuzu
- Hata yakalama ve debugging stratejileri
- Best practices ve code review kriterleri

## Confidence Score: {min(analysis_result.complexity_score + 2, 10)}/10

Bu PRP, sistem analizi, mimari tasarım ve test stratejisi uzmanlarının kapsamlı analizi sonucunda oluşturulmuştur.

### Tahmini Efor: {analysis_result.estimated_effort}

---
*Bu PRP, Context Engineering yaklaşımı kullanılarak AI yazılım mühendisliği ekibi tarafından oluşturulmuştur.*
"""
        
        return prp_content
    
    async def quick_health_check(self, test_project: ProjectData) -> bool:
        """Hızlı sağlık kontrolü"""
        
        try:
            simple_prompt = f"Bu proje için basit bir PRP başlığı oluştur: {test_project.name}"
            
            agent = self.llm_client.create_agent(
                system_prompt="Sen bir dokümantasyon uzmanı'sın. Kısa ve net cevaplar ver.",
                output_type=str
            )
            
            result = await agent.run(simple_prompt)
            return bool(result)
            
        except Exception as e:
            self.log_error(f"Dokümantasyon uzmanı sağlık kontrolü hatası: {str(e)}")
            return False 