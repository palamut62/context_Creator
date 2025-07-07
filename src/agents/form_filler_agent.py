"""
Form Doldurma Uzmanı
===================

Bu modül, proje açıklamasına göre form alanlarını otomatik dolduran AI agent'ı içerir.
"""

import json
from typing import Dict, Any, List, Optional
from ..api.llm_factory import LLMClient
from ..utils.logger import LoggerMixin, log_async_function_call

class FormFillerAgent(LoggerMixin):
    """Proje açıklamasına göre form alanlarını otomatik dolduran agent"""
    
    def __init__(self, llm_client: LLMClient, logger=None):
        super().__init__()
        self.llm_client = llm_client
        self.logger = logger
        
        self.log_info("Form Doldurma Uzmanı başlatıldı")
    
    async def analyze_and_fill_form(self, project_description: str) -> Dict[str, Any]:
        """
        Proje açıklamasını analiz ederek form alanlarını otomatik doldur
        
        Args:
            project_description: Proje açıklaması
            
        Returns:
            Form alanları için önerilen değerler
        """
        
        self.log_info(
            "Proje açıklaması analiz ediliyor",
            description_length=len(project_description)
        )
        
        try:
            # Sistem prompt'u
            system_prompt = self._get_system_prompt()
            
            # User prompt'u
            user_prompt = f"""
            Lütfen aşağıdaki proje açıklamasını analiz ederek form alanlarını otomatik doldur:

            PROJE AÇIKLAMASI:
            {project_description}

            Lütfen yanıtını sadece JSON formatında ver, başka hiçbir açıklama ekleme.
            """
            
            # LLM'den yanıt al
            # Sistem ve kullanıcı prompt'larını birleştir
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            response = await self.llm_client.generate_response(full_prompt)
            
            # JSON'u parse et
            try:
                form_data = json.loads(response)
                
                self.log_info(
                    "Form alanları başarıyla dolduruldu",
                    filled_fields=len(form_data)
                )
                
                return form_data
                
            except json.JSONDecodeError as e:
                self.log_error(f"JSON parse hatası: {str(e)}")
                return self._get_fallback_response()
                
        except Exception as e:
            self.log_error(f"Form doldurma hatası: {str(e)}")
            return self._get_fallback_response()
    
    def _get_system_prompt(self) -> str:
        """Sistem prompt'unu döndür"""
        
        return """
        Sen bir Form Doldurma Uzmanısın. Verilen proje açıklamasını analiz ederek 
        proje kurulum formundaki alanları otomatik olarak doldurman gerekiyor.

        Görevin:
        1. Proje açıklamasını dikkatlice analiz et
        2. Proje türünü, hedef kitleyi, teknoloji stack'ini ve diğer detayları çıkar
        3. Form alanlarını mantıklı şekilde doldur
        4. Sadece JSON formatında yanıt ver

        FORM ALANLARI:
        - project_name: Proje adı (açıklamadan çıkar)
        - project_type: Proje türü (Web Application, Mobile App, Desktop Application, API/Backend Service, Static Website, E-commerce Platform, Dashboard/Analytics, Marketing Website, Portfolio Website, Blog/CMS, Other)
        - description: Proje açıklaması (verilen açıklamayı düzenleyip iyileştir)
        - target_audience: Hedef kitle
        - timeline: Zaman çizelgesi (1-2 hafta, 2-3 hafta, 1-2 ay, 2-3 ay, 3-6 ay, 6+ ay)
        - deployment_target: Deployment hedefi (Vercel, Netlify, AWS, Google Cloud, Azure, Heroku, DigitalOcean, Self-hosted, Other)
        - budget_range: Bütçe aralığı (Kişisel proje, Küçük bütçe (< $1K), Orta bütçe ($1K - $10K), Büyük bütçe ($10K+), Kurumsal proje)
        - main_goals: Ana hedefler (liste olarak)
        - tech_stack: Teknoloji stack (liste olarak)
        - additional_requirements: Ek gereksinimler (liste olarak)
        - functional_requirements: Fonksiyonel gereksinimler (liste olarak)
        - non_functional_requirements: Fonksiyonel olmayan gereksinimler (liste olarak)
        - technical_requirements: Teknik gereksinimler (liste olarak)
        - constraints: Kısıtlamalar (liste olarak)

        KURALLARI:
        1. Sadece JSON formatında yanıt ver
        2. Tüm alanları doldur
        3. Proje türü mutlaka verilen seçeneklerden biri olmalı
        4. Teknoloji stack'i popüler teknolojilerden seç
        5. Hedef kitle ve ana hedefleri açıklamadan çıkar
        6. Zaman çizelgesi ve bütçeyi proje karmaşıklığına göre belirle
        """
    
    def _get_fallback_response(self) -> Dict[str, Any]:
        """Hata durumunda varsayılan yanıt"""
        
        return {
            "project_name": "Yeni Proje",
            "project_type": "Web Application",
            "description": "Modern web uygulaması projesi",
            "target_audience": "Genel kullanıcılar",
            "timeline": "1-2 ay",
            "deployment_target": "Vercel",
            "budget_range": "Kişisel proje",
            "main_goals": [
                "Kullanıcı dostu arayüz",
                "Hızlı performans",
                "Güvenli sistem"
            ],
            "tech_stack": [
                "React",
                "Node.js",
                "PostgreSQL"
            ],
            "additional_requirements": [
                "Responsive tasarım",
                "SEO optimizasyonu"
            ],
            "functional_requirements": [
                "Kullanıcı kayıt ve giriş sistemi",
                "Veri görüntüleme ve düzenleme",
                "Arama ve filtreleme"
            ],
            "non_functional_requirements": [
                "Sayfa yükleme süresi 3 saniyeden az",
                "Mobil uyumlu tasarım",
                "Güvenli veri iletimi"
            ],
            "technical_requirements": [
                "Modern web teknolojileri kullanımı",
                "API tabanlı mimari",
                "Veritabanı optimizasyonu"
            ],
            "constraints": [
                "Sınırlı bütçe",
                "Hızlı geliştirme süreci"
            ]
        } 