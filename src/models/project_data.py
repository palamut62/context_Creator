"""
Proje Veri Modelleri
===================

Bu modül, proje verilerini temsil eden Pydantic modellerini içerir.
Type safety ve validation için kullanılır.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator

class ProjectType(str, Enum):
    """Proje türleri"""
    WEB_APP = "Web Uygulaması"
    MOBILE_APP = "Mobil Uygulama"
    DESKTOP_APP = "Desktop Uygulaması"
    API_BACKEND = "API/Backend Servisi"
    MICROSERVICE = "Mikroservis"
    CLI_TOOL = "CLI Aracı"
    LIBRARY = "Kütüphane/Framework"
    DEVOPS = "DevOps/Infrastructure"
    DATA_PIPELINE = "Data Pipeline"
    MACHINE_LEARNING = "Machine Learning"
    OTHER = "Diğer"

class TeamSize(str, Enum):
    """Ekip büyüklüğü"""
    SOLO = "Solo (1 kişi)"
    SMALL = "Küçük (2-5 kişi)"
    MEDIUM = "Orta (6-15 kişi)"
    LARGE = "Büyük (16+ kişi)"

class Timeline(str, Enum):
    """Proje süresi"""
    SHORT = "1-2 hafta"
    MEDIUM_SHORT = "2-3 hafta"
    MONTH = "1-2 ay"
    QUARTER = "2-3 ay"
    HALF_YEAR = "3-6 ay"
    LONG_TERM = "6+ ay"

class ProgrammingLanguage(str, Enum):
    """Programlama dilleri"""
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript/TypeScript"
    JAVA = "Java"
    CSHARP = "C#"
    GO = "Go"
    RUST = "Rust"
    CPP = "C++"
    SWIFT = "Swift"
    KOTLIN = "Kotlin"
    PHP = "PHP"
    RUBY = "Ruby"
    OTHER = "Diğer"

class Platform(str, Enum):
    """Hedef platformlar"""
    WEB = "Web (Browser)"
    IOS = "iOS"
    ANDROID = "Android"
    WINDOWS = "Windows"
    MACOS = "macOS"
    LINUX = "Linux"
    CLOUD = "Cloud (AWS/Azure/GCP)"
    DOCKER = "Docker/Kubernetes"
    SERVERLESS = "Serverless"

class AITool(str, Enum):
    """AI kod geliştirme araçları"""
    CLAUDE = "Claude (Anthropic)"
    CURSOR = "Cursor"
    GITHUB_COPILOT = "GitHub Copilot"
    CODEIUM = "Codeium"
    TABNINE = "Tabnine"
    REPLIT = "Replit Ghostwriter"
    AMAZON_CODEWHISPERER = "Amazon CodeWhisperer"
    OTHER = "Diğer AI araçları"

class ProjectRequirements(BaseModel):
    """Proje gereksinimleri"""
    
    # Functional Requirements
    functional_requirements: str = Field(
        ...,
        description="Ana özellikler ve fonksiyonlar",
        min_length=10
    )
    
    user_stories: Optional[str] = Field(
        None,
        description="Kullanıcı hikayeleri"
    )
    
    # Technical Requirements
    frameworks: Optional[str] = Field(
        None,
        description="Kullanılacak framework ve kütüphaneler"
    )
    
    database: Optional[str] = Field(
        None,
        description="Veritabanı tercihi"
    )
    
    authentication: Optional[str] = Field(
        None,
        description="Kimlik doğrulama yöntemi"
    )
    
    deployment: Optional[str] = Field(
        None,
        description="Deployment platform"
    )
    
    performance: Optional[str] = Field(
        None,
        description="Performans gereksinimleri"
    )
    
    security: Optional[str] = Field(
        None,
        description="Güvenlik gereksinimleri"
    )
    
    # Constraints
    constraints: Optional[str] = Field(
        None,
        description="Proje kısıtlamaları"
    )
    
    special_requirements: Optional[str] = Field(
        None,
        description="Özel gereksinimler"
    )
    
    # AI Tools
    ai_tools: List[AITool] = Field(
        default_factory=lambda: [AITool.CLAUDE, AITool.CURSOR],
        description="Kullanılacak AI kod geliştirme araçları"
    )
    
    context_preferences: Optional[str] = Field(
        None,
        description="Context Engineering tercihleri"
    )

class ProjectData(BaseModel):
    """Ana proje veri modeli"""
    
    # Basic Information
    name: str = Field(
        ...,
        description="Proje adı",
        min_length=2,
        max_length=100
    )
    
    type: ProjectType = Field(
        ...,
        description="Proje türü"
    )
    
    description: str = Field(
        ...,
        description="Proje açıklaması",
        min_length=10,
        max_length=2000
    )
    
    # Technical Details
    language: ProgrammingLanguage = Field(
        ...,
        description="Ana programlama dili"
    )
    
    platform: List[Platform] = Field(
        default_factory=list,
        description="Hedef platformlar"
    )
    
    # Project Management
    team_size: Optional[TeamSize] = Field(
        None,
        description="Ekip büyüklüğü"
    )
    
    timeline: Optional[Timeline] = Field(
        None,
        description="Hedef süre"
    )
    
    # Requirements
    requirements: Optional[ProjectRequirements] = Field(
        None,
        description="Detaylı proje gereksinimleri"
    )
    
    # Metadata
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Oluşturulma zamanı"
    )
    
    updated_at: Optional[datetime] = Field(
        None,
        description="Son güncelleme zamanı"
    )
    
    @validator('name')
    def validate_name(cls, v):
        """Proje adını validate et"""
        if not v.strip():
            raise ValueError("Proje adı boş olamaz")
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        """Proje açıklamasını validate et"""
        if not v.strip():
            raise ValueError("Proje açıklaması boş olamaz")
        return v.strip()

class AnalysisResult(BaseModel):
    """Sistem analisti sonucu"""
    
    complexity_score: int = Field(
        ...,
        description="Karmaşıklık skoru (1-10)",
        ge=1,
        le=10
    )
    
    risk_factors: List[str] = Field(
        default_factory=list,
        description="Tespit edilen risk faktörleri"
    )
    
    recommended_approach: str = Field(
        ...,
        description="Önerilen yaklaşım"
    )
    
    key_challenges: List[str] = Field(
        default_factory=list,
        description="Ana zorluklar"
    )
    
    success_criteria: List[str] = Field(
        default_factory=list,
        description="Başarı kriterleri"
    )
    
    estimated_effort: str = Field(
        ...,
        description="Tahmini efor"
    )

class ArchitectureResult(BaseModel):
    """Yazılım mimarı sonucu"""
    
    architecture_pattern: str = Field(
        ...,
        description="Önerilen mimari pattern"
    )
    
    technology_stack: Dict[str, str] = Field(
        default_factory=dict,
        description="Teknoloji stack'i"
    )
    
    system_components: List[str] = Field(
        default_factory=list,
        description="Sistem bileşenleri"
    )
    
    data_flow: str = Field(
        ...,
        description="Veri akış açıklaması"
    )
    
    security_considerations: List[str] = Field(
        default_factory=list,
        description="Güvenlik değerlendirmeleri"
    )
    
    scalability_plan: str = Field(
        ...,
        description="Ölçeklenebilirlik planı"
    )

class TestStrategy(BaseModel):
    """Test stratejisi"""
    
    test_levels: List[str] = Field(
        default_factory=list,
        description="Test seviyeleri (unit, integration, e2e)"
    )
    
    test_frameworks: List[str] = Field(
        default_factory=list,
        description="Önerilen test framework'leri"
    )
    
    coverage_targets: Dict[str, int] = Field(
        default_factory=dict,
        description="Kapsam hedefleri"
    )
    
    quality_gates: List[str] = Field(
        default_factory=list,
        description="Kalite kontrol noktaları"
    )
    
    performance_tests: List[str] = Field(
        default_factory=list,
        description="Performans test senaryoları"
    )

class PRPContent(BaseModel):
    """Üretilen PRP içeriği"""
    
    title: str = Field(
        ...,
        description="PRP başlığı"
    )
    
    purpose: str = Field(
        ...,
        description="PRP amacı"
    )
    
    core_principles: List[str] = Field(
        default_factory=list,
        description="Temel prensipler"
    )
    
    goal: str = Field(
        ...,
        description="Proje hedefi"
    )
    
    implementation_blueprint: str = Field(
        ...,
        description="İmplementasyon planı"
    )
    
    validation_loop: List[str] = Field(
        default_factory=list,
        description="Doğrulama döngüsü"
    )
    
    confidence_score: int = Field(
        ...,
        description="Güven skoru (1-10)",
        ge=1,
        le=10
    )
    
    generated_at: datetime = Field(
        default_factory=datetime.now,
        description="Oluşturulma zamanı"
    )
    
    def to_markdown(self) -> str:
        """PRP'yi markdown formatına çevir"""
        
        md_content = f"""# {self.title}

## Purpose
{self.purpose}

## Core Principles
"""
        
        for i, principle in enumerate(self.core_principles, 1):
            md_content += f"{i}. **{principle}**\n"
        
        md_content += f"""
## Goal
{self.goal}

## Implementation Blueprint
{self.implementation_blueprint}

## Validation Loop
"""
        
        for item in self.validation_loop:
            md_content += f"- {item}\n"
        
        md_content += f"""
## Confidence Score: {self.confidence_score}/10

Generated at: {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return md_content 