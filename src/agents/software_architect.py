"""
Yazılım Mimarı Ajanı
===================

Bu modül, sistem mimarisini tasarlayan AI ajanını içerir.
Teknoloji stack'ini belirler, mimari pattern'leri önerir ve ölçeklenebilirlik planı yapar.
"""

from typing import Dict, Any
from ..models.project_data import ProjectData, AnalysisResult, ArchitectureResult
from ..api.llm_factory import LLMClient
from ..utils.logger import LoggerMixin, log_async_function_call

class SoftwareArchitectAgent(LoggerMixin):
    """Yazılım Mimarı AI Ajanı"""
    
    def __init__(self, llm_client: LLMClient, logger=None):
        super().__init__()
        self.llm_client = llm_client
        self.logger = logger
        
        self.system_prompt = """
Sen deneyimli bir Yazılım Mimarı'sın. CLAUDE.md ve INITIAL.md dosyalarındaki talimatları takip ederek sistem mimarisi tasarlıyorsun.

CLAUDE.md'den Mimari Prensipler:
- **Modüler yapı**: Her component ayrı dosyada, clear separation of concerns
- **Async/await patterns**: API çağrıları için asenkron işlemler
- **Type hints ve Pydantic models**: Güçlü tip güvenliği
- **API Integration Standards**: Environment variables, Provider factory pattern
- **Performance Optimization**: Caching, lazy loading, memory management
- **Security & Privacy**: API key management, input sanitization, rate limiting

INITIAL.md'den Gereksinimler:
- **Multi-LLM Provider Desteği**: Gemini, OpenRouter, OpenAI, DeepSeek API entegrasyonu
- **Pydantic AI Tabanlı**: Farklı uzmanlık alanlarına sahip AI ajanları
- **Context Engineering Uyumluluğu**: Tüm AI kod geliştirme araçları için uyumlu
- **Kapsamlı Bilgi Toplama**: Teknoloji tercihleri, kısıtlamalar, özel gereksinimler
- **Extensibility**: Yeni LLM provider'ları kolayca eklenebilir

Görevin:
1. **Uygun mimari pattern'i belirlemek** (CLAUDE.md: Modüler yapı, separation of concerns)
2. **Teknoloji stack'ini önermek** (INITIAL.md: Multi-LLM Provider support)
3. **Sistem bileşenlerini tanımlamak** (CLAUDE.md: Component architecture)
4. **Veri akışını planlamak** (CLAUDE.md: Async/await patterns)
5. **Güvenlik değerlendirmesi yapmak** (CLAUDE.md: Security & Privacy)
6. **Ölçeklenebilirlik planı oluşturmak** (CLAUDE.md: Performance optimization)

Özel Dikkat Edilecek Noktalar:
- **Flask web patterns**: HTML templates, forms, Bootstrap ile responsive layout
- **Pydantic AI multi-agent sistem**: Agent specialization, dependency injection
- **LLM Provider factory pattern**: Unified interface, retry logic, rate limiting
- **Context Engineering compliance**: PRP Structure, validation loops
- **AI Tool Compatibility**: Claude, Cursor, GitHub Copilot uyumluluğu

Mimari kararlarını proje gereksinimlerine, analiz sonuçlarına ve Context Engineering prensiplerine göre al.
Cevaplarını Pydantic model formatında ver ve CLAUDE.md standartlarına uygun tasarım yap.
"""
    
    @log_async_function_call
    async def design_architecture(self, project_data: ProjectData, analysis_result: AnalysisResult) -> ArchitectureResult:
        """Sistem mimarisini tasarla"""
        
        self.log_info(
            f"Mimari tasarım başlatılıyor: {project_data.name}",
            complexity_score=analysis_result.complexity_score
        )
        
        architecture_prompt = self._create_architecture_prompt(project_data, analysis_result)
        
        try:
            agent = self.llm_client.create_agent(
                system_prompt=self.system_prompt,
                output_type=ArchitectureResult
            )
            
            result = await agent.run(architecture_prompt)
            
            if hasattr(result, 'output'):
                architecture_result = result.output
            else:
                architecture_result = result
            
            self.log_info(
                "Mimari tasarım tamamlandı",
                pattern=architecture_result.architecture_pattern,
                components=len(architecture_result.system_components)
            )
            
            return architecture_result
            
        except Exception as e:
            self.log_error(f"Mimari tasarım hatası: {str(e)}")
            return self._create_fallback_architecture(project_data, analysis_result)
    
    def _create_architecture_prompt(self, project_data: ProjectData, analysis_result: AnalysisResult) -> str:
        """Mimari tasarım prompt'unu oluştur"""
        
        prompt = f"""
Lütfen aşağıdaki proje için sistem mimarisi tasarla:

## Proje Bilgileri
- **Proje Adı**: {project_data.name}
- **Proje Türü**: {project_data.type}
- **Programlama Dili**: {project_data.language}
- **Hedef Platformlar**: {', '.join(project_data.platform) if project_data.platform else 'Belirtilmemiş'}

## Analiz Sonuçları
- **Karmaşıklık Skoru**: {analysis_result.complexity_score}/10
- **Önerilen Yaklaşım**: {analysis_result.recommended_approach}
- **Ana Zorluklar**: {', '.join(analysis_result.key_challenges)}

## Proje Açıklaması
{project_data.description}
"""
        
        if project_data.requirements:
            req = project_data.requirements
            prompt += f"""
## Teknik Gereksinimler
- **Framework/Kütüphaneler**: {req.frameworks or 'Belirtilmemiş'}
- **Veritabanı**: {req.database or 'Belirtilmemiş'}
- **Kimlik Doğrulama**: {req.authentication or 'Belirtilmemiş'}
- **Deployment**: {req.deployment or 'Belirtilmemiş'}
- **Performans**: {req.performance or 'Belirtilmemiş'}
- **Güvenlik**: {req.security or 'Belirtilmemiş'}

## Fonksiyonel Gereksinimler
{req.functional_requirements}
"""
        
        prompt += """
## Mimari Tasarım Görevlerin:

1. **Mimari Pattern**: En uygun mimari pattern'i belirle (MVC, Microservices, Layered, etc.)
2. **Teknoloji Stack**: Her katman için teknoloji seçimi yap
3. **Sistem Bileşenleri**: Ana sistem bileşenlerini listele
4. **Veri Akışı**: Veri akışını açıkla
5. **Güvenlik Değerlendirmesi**: Güvenlik konularını ele al
6. **Ölçeklenebilirlik Planı**: Nasıl ölçeklenebileceğini planla

Cevabını JSON formatında ver ve Türkçe açıkla.
"""
        
        return prompt
    
    def _create_fallback_architecture(self, project_data: ProjectData, analysis_result: AnalysisResult) -> ArchitectureResult:
        """Fallback mimari tasarım"""
        
        # Basit mimari önerileri
        pattern = self._suggest_architecture_pattern(project_data)
        tech_stack = self._suggest_tech_stack(project_data)
        
        return ArchitectureResult(
            architecture_pattern=pattern,
            technology_stack=tech_stack,
            system_components=[
                "Presentation Layer (UI/Frontend)",
                "Business Logic Layer",
                "Data Access Layer",
                "Database Layer",
                "API Gateway",
                "Authentication Service"
            ],
            data_flow="Client → API Gateway → Business Logic → Data Access → Database",
            security_considerations=[
                "Input validation",
                "Authentication & Authorization",
                "Data encryption",
                "HTTPS communication",
                "Rate limiting"
            ],
            scalability_plan="Horizontal scaling with load balancers and database replication"
        )
    
    def _suggest_architecture_pattern(self, project_data: ProjectData) -> str:
        """Mimari pattern öner"""
        
        if project_data.type == "Mikroservis":
            return "Microservices Architecture"
        elif project_data.type == "API/Backend Servisi":
            return "Layered Architecture (N-Tier)"
        elif project_data.type == "Web Uygulaması":
            return "MVC (Model-View-Controller)"
        elif project_data.type == "Mobil Uygulama":
            return "MVVM (Model-View-ViewModel)"
        else:
            return "Layered Architecture"
    
    def _suggest_tech_stack(self, project_data: ProjectData) -> Dict[str, str]:
        """Teknoloji stack öner"""
        
        stack = {}
        
        # Programlama diline göre
        if project_data.language == "Python":
            stack.update({
                "Backend Framework": "FastAPI/Django",
                "Database": "PostgreSQL",
                "Cache": "Redis",
                "Message Queue": "Celery"
            })
        elif project_data.language == "JavaScript/TypeScript":
            stack.update({
                "Backend Framework": "Node.js/Express",
                "Frontend Framework": "React/Vue.js",
                "Database": "MongoDB/PostgreSQL",
                "Cache": "Redis"
            })
        elif project_data.language == "Java":
            stack.update({
                "Backend Framework": "Spring Boot",
                "Database": "PostgreSQL/MySQL",
                "Cache": "Redis",
                "Message Queue": "RabbitMQ"
            })
        
        # Proje türüne göre ek teknolojiler
        if project_data.type == "Web Uygulaması":
            stack["Web Server"] = "Nginx"
            stack["CDN"] = "CloudFront"
        elif project_data.type == "API/Backend Servisi":
            stack["API Gateway"] = "Kong/AWS API Gateway"
            stack["Documentation"] = "Swagger/OpenAPI"
        
        return stack
    
    async def quick_health_check(self, test_project: ProjectData) -> bool:
        """Hızlı sağlık kontrolü"""
        
        try:
            simple_prompt = f"Bu proje için uygun mimari pattern öner: {test_project.name}"
            
            agent = self.llm_client.create_agent(
                system_prompt="Sen bir yazılım mimarı'sın. Kısa ve net cevaplar ver.",
                output_type=str
            )
            
            result = await agent.run(simple_prompt)
            return bool(result)
            
        except Exception as e:
            self.log_error(f"Yazılım mimarı sağlık kontrolü hatası: {str(e)}")
            return False 