"""
Sistem Analisti Ajanı
=====================

Bu modül, proje gereksinimlerini analiz eden AI ajanını içerir.
Karmaşıklık skorunu belirler, risk faktörlerini tespit eder ve öneriler sunar.
"""

from typing import List, Dict, Any
from ..models.project_data import ProjectData, AnalysisResult
from ..api.llm_factory import LLMClient
from ..utils.logger import LoggerMixin, log_async_function_call

class SystemAnalystAgent(LoggerMixin):
    """Sistem Analisti AI Ajanı"""
    
    def __init__(self, llm_client: LLMClient, logger=None):
        super().__init__()
        self.llm_client = llm_client
        self.logger = logger
        
        # System prompt'u tanımla - CLAUDE.md talimatlarına uygun
        self.system_prompt = """
Sen deneyimli bir Sistem Analisti'sin. CLAUDE.md ve INITIAL.md dosyalarındaki talimatları takip ederek yazılım projelerini analiz ediyorsun.

CLAUDE.md'den Ana Prensipler:
- **Context Engineering uyumluluğu**: Tüm AI kod geliştirme araçları ile uyumlu analiz
- **Multi-LLM Provider desteği**: Farklı AI araçları için optimize edilmiş analiz
- **Pydantic AI multi-agent sistem**: Diğer ajanlarla koordineli çalışma
- **Type hints ve Pydantic models**: Güçlü tip güvenliği
- **Async/await patterns**: API çağrıları için asenkron işlemler

INITIAL.md'den Gereksinimler:
- **Context Engineering PRP Generator**: Sadece Claude değil, tüm AI araçları için PRP
- **Kapsamlı bilgi toplama**: Proje gereksinimleri, teknoloji tercihleri, kısıtlamalar
- **Otomatik PRP üretimi**: Context Engineering standartlarına uygun analiz

Görevin:
1. **Proje gereksinimlerini detaylı analiz etmek** (CLAUDE.md: Comprehensive analysis)
2. **Karmaşıklık skorunu (1-10) belirlemek** (Context Engineering: Progressive Success)
3. **Risk faktörlerini tespit etmek** (CLAUDE.md: Error handling, graceful degradation)
4. **Önerilen yaklaşımı belirlemek** (CLAUDE.md: Agent specialization)
5. **Ana zorlukları listelemek** (Context Engineering: Information Dense)
6. **Başarı kriterlerini tanımlamak** (Context Engineering: Validation Loops)
7. **Tahmini efor değerlendirmesi yapmak** (CLAUDE.md: Performance optimization)

Analiz yaparken şunları dikkate al:
- **Proje türü ve kapsamı** (INITIAL.md: Multi-LLM Provider support)
- **Teknoloji karmaşıklığı** (CLAUDE.md: API Integration Standards)
- **Ekip büyüklüğü ve deneyimi** (CLAUDE.md: Agent specialization)
- **Zaman kısıtları** (CLAUDE.md: Performance optimization)
- **Teknik riskler** (CLAUDE.md: Security & Privacy)
- **İş süreçleri karmaşıklığı** (Context Engineering: Progressive Success)
- **Entegrasyon gereksinimleri** (INITIAL.md: API integrations)
- **Performans ve ölçeklenebilirlik** (CLAUDE.md: Performance optimization)
- **AI araç uyumluluğu** (INITIAL.md: Tüm AI kod geliştirme araçları)

Cevaplarını Pydantic model formatında ver ve Context Engineering prensiplerine uygun analiz yap.
"""
    
    @log_async_function_call
    async def analyze_project(self, project_data: ProjectData) -> AnalysisResult:
        """
        Projeyi analiz et ve sonuç döndür
        
        Args:
            project_data: Analiz edilecek proje verileri
            
        Returns:
            Analiz sonucu
        """
        
        self.log_info(
            f"Proje analizi başlatılıyor: {project_data.name}",
            project_type=project_data.type,
            language=project_data.language
        )
        
        # Analiz prompt'unu oluştur
        analysis_prompt = self._create_analysis_prompt(project_data)
        
        try:
            # Agent'ı oluştur ve çalıştır
            agent = self.llm_client.create_agent(
                system_prompt=self.system_prompt,
                output_type=AnalysisResult
            )
            
            result = await agent.run(analysis_prompt)
            
            # Sonucu validate et
            if hasattr(result, 'output'):
                analysis_result = result.output
            else:
                analysis_result = result
            
            self.log_info(
                "Proje analizi tamamlandı",
                complexity_score=analysis_result.complexity_score,
                risk_count=len(analysis_result.risk_factors),
                challenge_count=len(analysis_result.key_challenges)
            )
            
            return analysis_result
            
        except Exception as e:
            self.log_error(f"Proje analizi hatası: {str(e)}")
            
            # Fallback analiz sonucu
            return self._create_fallback_analysis(project_data)
    
    def _create_analysis_prompt(self, project_data: ProjectData) -> str:
        """Analiz prompt'unu oluştur"""
        
        prompt = f"""
Lütfen aşağıdaki projeyi detaylı analiz et:

## Proje Bilgileri
- **Proje Adı**: {project_data.name}
- **Proje Türü**: {project_data.type}
- **Programlama Dili**: {project_data.language}
- **Hedef Platformlar**: {', '.join(project_data.platform) if project_data.platform else 'Belirtilmemiş'}
- **Ekip Büyüklüğü**: {project_data.team_size or 'Belirtilmemiş'}
- **Hedef Süre**: {project_data.timeline or 'Belirtilmemiş'}

## Proje Açıklaması
{project_data.description}
"""
        
        # Gereksinimler varsa ekle
        if project_data.requirements:
            req = project_data.requirements
            prompt += f"""
## Fonksiyonel Gereksinimler
{req.functional_requirements}

## Teknik Detaylar
- **Framework/Kütüphaneler**: {req.frameworks or 'Belirtilmemiş'}
- **Veritabanı**: {req.database or 'Belirtilmemiş'}
- **Kimlik Doğrulama**: {req.authentication or 'Belirtilmemiş'}
- **Deployment**: {req.deployment or 'Belirtilmemiş'}
- **Performans**: {req.performance or 'Belirtilmemiş'}
- **Güvenlik**: {req.security or 'Belirtilmemiş'}

## Kısıtlamalar
{req.constraints or 'Belirtilmemiş'}

## Özel Gereksinimler
{req.special_requirements or 'Belirtilmemiş'}

## Kullanıcı Hikayeleri
{req.user_stories or 'Belirtilmemiş'}
"""
        
        prompt += """
## Analiz Görevlerin:

1. **Karmaşıklık Skoru (1-10)**: Projenin teknik ve iş karmaşıklığını değerlendir
2. **Risk Faktörleri**: Potansiyel riskleri listele
3. **Önerilen Yaklaşım**: En uygun geliştirme yaklaşımını öner
4. **Ana Zorluklar**: Karşılaşılabilecek ana zorlukları belirle
5. **Başarı Kriterleri**: Projenin başarılı sayılacağı kriterleri tanımla
6. **Tahmini Efor**: Geliştirme sürecinin zorluğunu değerlendir

Lütfen cevabını JSON formatında ver ve her alanı Türkçe olarak doldur.
"""
        
        return prompt
    
    def _create_fallback_analysis(self, project_data: ProjectData) -> AnalysisResult:
        """Hata durumunda fallback analiz sonucu oluştur"""
        
        # Basit heuristik analiz
        complexity_score = self._calculate_basic_complexity(project_data)
        
        return AnalysisResult(
            complexity_score=complexity_score,
            risk_factors=[
                "API entegrasyonu zorlukları",
                "Performans optimizasyonu ihtiyacı",
                "Güvenlik gereksinimlerinin karşılanması",
                "Kullanıcı deneyimi tasarımı"
            ],
            recommended_approach="Agile metodoloji ile iteratif geliştirme",
            key_challenges=[
                "Gereksinim belirsizlikleri",
                "Teknoloji stack seçimi",
                "Ekip koordinasyonu",
                "Kalite kontrolü"
            ],
            success_criteria=[
                "Tüm fonksiyonel gereksinimler karşılanır",
                "Performans hedefleri tutturulur",
                "Güvenlik standartları sağlanır",
                "Kullanıcı memnuniyeti yüksek olur"
            ],
            estimated_effort=f"{project_data.timeline or 'Orta'} seviyede efor gerektirir"
        )
    
    def _calculate_basic_complexity(self, project_data: ProjectData) -> int:
        """Basit karmaşıklık hesaplama"""
        
        score = 5  # Base score
        
        # Proje türüne göre
        if project_data.type in ["Mikroservis", "Machine Learning", "DevOps/Infrastructure"]:
            score += 2
        elif project_data.type in ["Web Uygulaması", "API/Backend Servisi"]:
            score += 1
        
        # Platform sayısına göre
        if len(project_data.platform) > 2:
            score += 1
        
        # Ekip büyüklüğüne göre
        if project_data.team_size == "Büyük (16+ kişi)":
            score += 1
        elif project_data.team_size == "Solo (1 kişi)":
            score -= 1
        
        # Süreye göre
        if project_data.timeline in ["1+ yıl", "1 yıl"]:
            score += 1
        elif project_data.timeline in ["1-2 hafta", "1 ay"]:
            score -= 1
        
        # Gereksinimler karmaşıklığına göre
        if project_data.requirements:
            if len(project_data.requirements.functional_requirements) > 500:
                score += 1
            if project_data.requirements.constraints:
                score += 1
            if project_data.requirements.special_requirements:
                score += 1
        
        return max(1, min(10, score))
    
    async def quick_health_check(self, test_project: ProjectData) -> bool:
        """Hızlı sağlık kontrolü"""
        
        try:
            simple_prompt = f"Bu proje için basit bir karmaşıklık skoru (1-10) ver: {test_project.name}"
            
            agent = self.llm_client.create_agent(
                system_prompt="Sen bir sistem analisti'sin. Kısa ve net cevaplar ver.",
                output_type=str
            )
            
            result = await agent.run(simple_prompt)
            
            # Sonuç varsa başarılı
            return bool(result)
            
        except Exception as e:
            self.log_error(f"Sistem analisti sağlık kontrolü hatası: {str(e)}")
            return False
    
    def get_analysis_guidelines(self) -> Dict[str, Any]:
        """Analiz kılavuzunu döndür"""
        
        return {
            "complexity_factors": {
                "technical": [
                    "Teknoloji stack karmaşıklığı",
                    "Entegrasyon sayısı",
                    "Performans gereksinimleri",
                    "Güvenlik seviyesi"
                ],
                "business": [
                    "İş süreçleri karmaşıklığı",
                    "Kullanıcı sayısı",
                    "Veri hacmi",
                    "Compliance gereksinimleri"
                ],
                "project": [
                    "Ekip büyüklüğü",
                    "Zaman kısıtları",
                    "Bütçe kısıtları",
                    "Değişim yönetimi"
                ]
            },
            "complexity_scale": {
                "1-2": "Çok Basit - Temel CRUD uygulamaları",
                "3-4": "Basit - Standart web/mobil uygulamalar",
                "5-6": "Orta - Çoklu entegrasyonlu sistemler",
                "7-8": "Karmaşık - Enterprise seviye uygulamalar",
                "9-10": "Çok Karmaşık - Kritik sistemler, ML/AI projeleri"
            },
            "risk_categories": [
                "Teknik riskler",
                "İş riskleri",
                "Proje yönetimi riskleri",
                "Dış faktör riskleri"
            ],
            "success_metrics": [
                "Fonksiyonel gereksinimler",
                "Performans metrikleri",
                "Kalite standartları",
                "Kullanıcı memnuniyeti",
                "Proje hedefleri"
            ]
        } 