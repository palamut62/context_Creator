"""
Test Uzmanı Ajanı
=================

Bu modül, test stratejisi oluşturan AI ajanını içerir.
Test seviyelerini belirler, framework önerileri yapar ve kalite kontrol planı oluşturur.
"""

from typing import Dict, Any, List
from ..models.project_data import ProjectData, ArchitectureResult, TestStrategy
from ..api.llm_factory import LLMClient
from ..utils.logger import LoggerMixin, log_async_function_call

class TestSpecialistAgent(LoggerMixin):
    """Test Uzmanı AI Ajanı"""
    
    def __init__(self, llm_client: LLMClient, logger=None):
        super().__init__()
        self.llm_client = llm_client
        self.logger = logger
        
        self.system_prompt = """
Sen deneyimli bir Test Uzmanı'sın. CLAUDE.md ve INITIAL.md dosyalarındaki talimatları takip ederek test stratejisi oluşturuyorsun.

CLAUDE.md'den Test ve Kalite Standartları:
- **Testing & Quality**: pytest ile comprehensive test coverage
- **Integration tests**: API endpoints ve agent interactions
- **PRP validation**: Generated PRP files için quality checks
- **Performance tests**: Response time ve memory usage
- **User acceptance tests**: Real-world scenarios
- **Validation Loops**: Executable tests/lints the AI can run and fix
- **Progressive Success**: Start simple, validate, then enhance

INITIAL.md'den Gereksinimler:
- **Context Engineering PRP Generator**: Validation sistemleri gerekli
- **Multi-LLM Provider Desteği**: Farklı API'lar için test stratejisi
- **Pydantic AI Tabanlı**: Agent interactions için test coverage
- **Robust hata yakalama**: API çağrılarında hata yönetimi testleri
- **Performans**: Async işlemler ve progress bar testleri
- **Validation**: Üretilen PRP dosyalarının kalite kontrolü

Görevin:
1. **Test seviyelerini belirlemek** (CLAUDE.md: Unit, Integration, User acceptance)
2. **Uygun test framework'lerini önermek** (CLAUDE.md: pytest comprehensive coverage)
3. **Kapsam hedeflerini belirlemek** (CLAUDE.md: 80%+ coverage)
4. **Kalite kontrol noktalarını tanımlamak** (Context Engineering: Validation Loops)
5. **Performans test senaryolarını oluşturmak** (CLAUDE.md: Response time, memory usage)

Özel Test Alanları:
- **PRP Quality Validation**: Context Engineering standartlarına uygunluk
- **Multi-LLM Provider Testing**: API entegrasyonu ve fallback mekanizmaları
- **Agent Interaction Testing**: Pydantic AI multi-agent koordinasyonu
- **Flask web Testing**: HTTP endpoints, template rendering, form validation
- **Context Engineering Compliance**: PRP formatı ve içerik kalitesi
- **API Rate Limiting Tests**: Provider limits ve retry logic
- **Security Testing**: API key management ve input sanitization

Test stratejisini proje mimarisine, gereksinimlerine ve Context Engineering prensiplerine göre planla.
Cevaplarını Pydantic model formatında ver ve CLAUDE.md standartlarına uygun test planı oluştur.
"""
    
    @log_async_function_call
    async def create_test_strategy(self, project_data: ProjectData, architecture_result: ArchitectureResult) -> TestStrategy:
        """Test stratejisi oluştur"""
        
        self.log_info(
            f"Test stratejisi oluşturuluyor: {project_data.name}",
            architecture_pattern=architecture_result.architecture_pattern
        )
        
        test_prompt = self._create_test_prompt(project_data, architecture_result)
        
        try:
            agent = self.llm_client.create_agent(
                system_prompt=self.system_prompt,
                output_type=TestStrategy
            )
            
            result = await agent.run(test_prompt)
            
            if hasattr(result, 'output'):
                test_strategy = result.output
            else:
                test_strategy = result
            
            self.log_info(
                "Test stratejisi tamamlandı",
                test_levels=len(test_strategy.test_levels),
                frameworks=len(test_strategy.test_frameworks)
            )
            
            return test_strategy
            
        except Exception as e:
            self.log_error(f"Test stratejisi hatası: {str(e)}")
            return self._create_fallback_test_strategy(project_data, architecture_result)
    
    def _create_test_prompt(self, project_data: ProjectData, architecture_result: ArchitectureResult) -> str:
        """Test stratejisi prompt'unu oluştur"""
        
        prompt = f"""
Lütfen aşağıdaki proje için test stratejisi oluştur:

## Proje Bilgileri
- **Proje Adı**: {project_data.name}
- **Proje Türü**: {project_data.type}
- **Programlama Dili**: {project_data.language}

## Mimari Bilgileri
- **Mimari Pattern**: {architecture_result.architecture_pattern}
- **Sistem Bileşenleri**: {', '.join(architecture_result.system_components)}
- **Teknoloji Stack**: {', '.join(f"{k}: {v}" for k, v in architecture_result.technology_stack.items())}

## Proje Açıklaması
{project_data.description}
"""
        
        if project_data.requirements:
            req = project_data.requirements
            prompt += f"""
## Fonksiyonel Gereksinimler
{req.functional_requirements}

## Performans Gereksinimleri
{req.performance or 'Belirtilmemiş'}

## Güvenlik Gereksinimleri
{req.security or 'Belirtilmemiş'}
"""
        
        prompt += """
## Test Stratejisi Görevlerin:

1. **Test Seviyeleri**: Hangi test seviyelerinin gerekli olduğunu belirle
2. **Test Framework'leri**: Her test seviyesi için uygun framework'leri öner
3. **Kapsam Hedefleri**: Her test seviyesi için kapsam hedeflerini belirle
4. **Kalite Kontrol Noktaları**: Kalite kontrol noktalarını tanımla
5. **Performans Testleri**: Performans test senaryolarını oluştur

Cevabını JSON formatında ver ve Türkçe açıkla.
"""
        
        return prompt
    
    def _create_fallback_test_strategy(self, project_data: ProjectData, architecture_result: ArchitectureResult) -> TestStrategy:
        """Fallback test stratejisi"""
        
        # Temel test stratejisi
        test_levels = ["Unit Tests", "Integration Tests", "End-to-End Tests"]
        frameworks = self._suggest_test_frameworks(project_data)
        
        return TestStrategy(
            test_levels=test_levels,
            test_frameworks=frameworks,
            coverage_targets={
                "Unit Tests": 80,
                "Integration Tests": 70,
                "End-to-End Tests": 60
            },
            quality_gates=[
                "All tests must pass",
                "Code coverage minimum %80",
                "No critical security vulnerabilities",
                "Performance benchmarks met",
                "Code quality score > 8/10"
            ],
            performance_tests=[
                "Load testing - normal traffic",
                "Stress testing - peak traffic",
                "Spike testing - sudden traffic increase",
                "Volume testing - large data sets",
                "Endurance testing - extended periods"
            ]
        )
    
    def _suggest_test_frameworks(self, project_data: ProjectData) -> List[str]:
        """Test framework'leri öner"""
        
        frameworks = []
        
        # Programlama diline göre
        if project_data.language == "Python":
            frameworks.extend([
                "pytest - Unit testing",
                "pytest-cov - Coverage",
                "pytest-asyncio - Async testing",
                "Selenium - E2E testing",
                "locust - Performance testing"
            ])
        elif project_data.language == "JavaScript/TypeScript":
            frameworks.extend([
                "Jest - Unit testing",
                "Cypress - E2E testing",
                "Playwright - E2E testing",
                "Artillery - Performance testing",
                "Supertest - API testing"
            ])
        elif project_data.language == "Java":
            frameworks.extend([
                "JUnit 5 - Unit testing",
                "Mockito - Mocking",
                "TestContainers - Integration testing",
                "Selenium - E2E testing",
                "JMeter - Performance testing"
            ])
        
        # Proje türüne göre ek framework'ler
        if project_data.type == "Web Uygulaması":
            frameworks.append("Accessibility testing - axe-core")
        elif project_data.type == "API/Backend Servisi":
            frameworks.append("Contract testing - Pact")
        elif project_data.type == "Mobil Uygulama":
            frameworks.append("Appium - Mobile testing")
        
        return frameworks
    
    async def quick_health_check(self, test_project: ProjectData) -> bool:
        """Hızlı sağlık kontrolü"""
        
        try:
            simple_prompt = f"Bu proje için temel test seviyeleri öner: {test_project.name}"
            
            agent = self.llm_client.create_agent(
                system_prompt="Sen bir test uzmanı'sın. Kısa ve net cevaplar ver.",
                output_type=str
            )
            
            result = await agent.run(simple_prompt)
            return bool(result)
            
        except Exception as e:
            self.log_error(f"Test uzmanı sağlık kontrolü hatası: {str(e)}")
            return False 