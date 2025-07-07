"""
Yazılım Mühendisliği Ekibi Yöneticisi
====================================

Bu modül, AI tabanlı yazılım mühendisliği ekibini yönetir.
Farklı uzmanlık alanlarındaki ajanları koordine eder ve PRP üretimini orchestrate eder.
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..models.project_data import (
    ProjectData, AnalysisResult, ArchitectureResult, 
    TestStrategy, PRPContent
)
from ..api.llm_factory import LLMClient
from ..utils.logger import LoggerMixin, log_async_function_call
from .system_analyst import SystemAnalystAgent
from .software_architect import SoftwareArchitectAgent
from .test_specialist import TestSpecialistAgent
from .documentation_specialist import DocumentationSpecialistAgent

class SoftwareEngineeringTeam(LoggerMixin):
    """Yazılım mühendisliği ekibi yöneticisi"""
    
    def __init__(self, llm_client: LLMClient, logger=None):
        super().__init__()
        self.llm_client = llm_client
        self.logger = logger
        
        # Ekip üyelerini oluştur
        self._initialize_team()
    
    def _initialize_team(self):
        """Ekip üyelerini başlat"""
        
        self.log_info("Yazılım mühendisliği ekibi oluşturuluyor...")
        
        try:
            self.system_analyst = SystemAnalystAgent(self.llm_client, self.logger)
            self.software_architect = SoftwareArchitectAgent(self.llm_client, self.logger)
            self.test_specialist = TestSpecialistAgent(self.llm_client, self.logger)
            self.documentation_specialist = DocumentationSpecialistAgent(self.llm_client, self.logger)
            
            self.log_info("Tüm ekip üyeleri başarıyla oluşturuldu")
            
        except Exception as e:
            self.log_error(f"Ekip oluşturma hatası: {str(e)}")
            raise
    
    @log_async_function_call
    async def analyze_project(self, project_data: ProjectData) -> AnalysisResult:
        """
        Projeyi sistem analisti ile analiz et
        
        Args:
            project_data: Proje verileri
            
        Returns:
            Analiz sonucu
        """
        
        self.log_info(
            f"Proje analizi başlatılıyor: {project_data.name}",
            project_name=project_data.name,
            project_type=project_data.type
        )
        
        try:
            result = await self.system_analyst.analyze_project(project_data)
            
            self.log_info(
                "Proje analizi tamamlandı",
                complexity_score=result.complexity_score,
                risk_count=len(result.risk_factors)
            )
            
            return result
            
        except Exception as e:
            self.log_error(f"Proje analizi hatası: {str(e)}")
            raise
    
    @log_async_function_call
    async def design_architecture(self, 
                                 project_data: ProjectData, 
                                 analysis_result: AnalysisResult) -> ArchitectureResult:
        """
        Yazılım mimarisi tasarla
        
        Args:
            project_data: Proje verileri
            analysis_result: Sistem analizi sonucu
            
        Returns:
            Mimari tasarım sonucu
        """
        
        self.log_info(
            f"Mimari tasarım başlatılıyor: {project_data.name}",
            complexity_score=analysis_result.complexity_score
        )
        
        try:
            result = await self.software_architect.design_architecture(
                project_data, analysis_result
            )
            
            self.log_info(
                "Mimari tasarım tamamlandı",
                architecture_pattern=result.architecture_pattern,
                component_count=len(result.system_components)
            )
            
            return result
            
        except Exception as e:
            self.log_error(f"Mimari tasarım hatası: {str(e)}")
            raise
    
    @log_async_function_call
    async def create_test_strategy(self, 
                                  project_data: ProjectData, 
                                  architecture_result: ArchitectureResult) -> TestStrategy:
        """
        Test stratejisi oluştur
        
        Args:
            project_data: Proje verileri
            architecture_result: Mimari tasarım sonucu
            
        Returns:
            Test stratejisi
        """
        
        self.log_info(
            f"Test stratejisi oluşturuluyor: {project_data.name}",
            architecture_pattern=architecture_result.architecture_pattern
        )
        
        try:
            result = await self.test_specialist.create_test_strategy(
                project_data, architecture_result
            )
            
            self.log_info(
                "Test stratejisi tamamlandı",
                test_levels=len(result.test_levels),
                frameworks=len(result.test_frameworks)
            )
            
            return result
            
        except Exception as e:
            self.log_error(f"Test stratejisi hatası: {str(e)}")
            raise
    
    @log_async_function_call
    async def generate_prp(self, 
                          project_data: ProjectData,
                          analysis_result: AnalysisResult,
                          architecture_result: ArchitectureResult,
                          test_strategy: TestStrategy) -> str:
        """
        PRP dökümanı oluştur
        
        Args:
            project_data: Proje verileri
            analysis_result: Sistem analizi sonucu
            architecture_result: Mimari tasarım sonucu
            test_strategy: Test stratejisi
            
        Returns:
            PRP markdown içeriği
        """
        
        self.log_info(
            f"PRP oluşturuluyor: {project_data.name}",
            confidence_score=analysis_result.complexity_score
        )
        
        try:
            prp_content = await self.documentation_specialist.generate_prp(
                project_data,
                analysis_result,
                architecture_result,
                test_strategy
            )
            
            # PRPContent modelini markdown'a çevir
            if isinstance(prp_content, PRPContent):
                markdown_content = prp_content.to_markdown()
            else:
                markdown_content = prp_content
            
            self.log_info(
                "PRP başarıyla oluşturuldu",
                content_length=len(markdown_content)
            )
            
            return markdown_content
            
        except Exception as e:
            self.log_error(f"PRP oluşturma hatası: {str(e)}")
            raise
    
    @log_async_function_call
    async def full_analysis_workflow(self, project_data: ProjectData) -> Dict[str, Any]:
        """
        Tam analiz workflow'unu çalıştır
        
        Args:
            project_data: Proje verileri
            
        Returns:
            Tüm analiz sonuçları
        """
        
        self.log_info(
            f"Tam analiz workflow'u başlatılıyor: {project_data.name}",
            project_type=project_data.type,
            language=project_data.language
        )
        
        start_time = datetime.now()
        
        try:
            # 1. Sistem analizi
            self.log_info("1/4 - Sistem analizi başlatılıyor...")
            analysis_result = await self.analyze_project(project_data)
            
            # 2. Mimari tasarım
            self.log_info("2/4 - Mimari tasarım başlatılıyor...")
            architecture_result = await self.design_architecture(project_data, analysis_result)
            
            # 3. Test stratejisi
            self.log_info("3/4 - Test stratejisi oluşturuluyor...")
            test_strategy = await self.create_test_strategy(project_data, architecture_result)
            
            # 4. PRP oluşturma
            self.log_info("4/4 - PRP oluşturuluyor...")
            prp_content = await self.generate_prp(
                project_data, analysis_result, architecture_result, test_strategy
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            results = {
                'project_data': project_data,
                'analysis_result': analysis_result,
                'architecture_result': architecture_result,
                'test_strategy': test_strategy,
                'prp_content': prp_content,
                'metadata': {
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'duration_seconds': duration,
                    'team_members': ['system_analyst', 'software_architect', 'test_specialist', 'documentation_specialist']
                }
            }
            
            self.log_info(
                f"Tam analiz workflow'u tamamlandı",
                duration_seconds=duration,
                prp_length=len(prp_content)
            )
            
            return results
            
        except Exception as e:
            self.log_error(f"Workflow hatası: {str(e)}")
            raise
    
    async def validate_team_readiness(self) -> Dict[str, bool]:
        """
        Ekip üyelerinin hazır olduğunu doğrula
        
        Returns:
            Her ekip üyesi için hazırlık durumu
        """
        
        readiness = {}
        
        try:
            # Her ekip üyesini test et
            test_project = ProjectData(
                name="Test Project",
                type="Web Uygulaması",
                description="Test project for validation",
                language="Python"
            )
            
            # System Analyst
            try:
                await self.system_analyst.quick_health_check(test_project)
                readiness['system_analyst'] = True
            except Exception:
                readiness['system_analyst'] = False
            
            # Software Architect
            try:
                await self.software_architect.quick_health_check(test_project)
                readiness['software_architect'] = True
            except Exception:
                readiness['software_architect'] = False
            
            # Test Specialist
            try:
                await self.test_specialist.quick_health_check(test_project)
                readiness['test_specialist'] = True
            except Exception:
                readiness['test_specialist'] = False
            
            # Documentation Specialist
            try:
                await self.documentation_specialist.quick_health_check(test_project)
                readiness['documentation_specialist'] = True
            except Exception:
                readiness['documentation_specialist'] = False
            
            self.log_info(
                "Ekip hazırlık durumu kontrol edildi",
                ready_count=sum(readiness.values()),
                total_count=len(readiness)
            )
            
        except Exception as e:
            self.log_error(f"Hazırlık kontrolü hatası: {str(e)}")
        
        return readiness
    
    def get_team_info(self) -> Dict[str, Any]:
        """
        Ekip bilgilerini döndür
        
        Returns:
            Ekip bilgileri
        """
        
        return {
            'team_name': 'AI Yazılım Mühendisliği Ekibi',
            'members': {
                'system_analyst': {
                    'name': 'Sistem Analisti',
                    'role': 'Proje gereksinimlerini analiz eder, karmaşıklık skorunu belirler',
                    'specialties': ['Gereksinim analizi', 'Risk değerlendirmesi', 'Efor tahmini']
                },
                'software_architect': {
                    'name': 'Yazılım Mimarı',
                    'role': 'Sistem mimarisini tasarlar, teknoloji stack\'ini belirler',
                    'specialties': ['Mimari pattern\'ler', 'Teknoloji seçimi', 'Ölçeklenebilirlik']
                },
                'test_specialist': {
                    'name': 'Test Uzmanı',
                    'role': 'Test stratejisini oluşturur, kalite kontrol planlar',
                    'specialties': ['Test stratejisi', 'Kalite güvence', 'Performans testleri']
                },
                'documentation_specialist': {
                    'name': 'Dokümantasyon Uzmanı',
                    'role': 'Context Engineering standartlarında PRP oluşturur',
                    'specialties': ['Context Engineering', 'PRP yazımı', 'AI araç uyumluluğu']
                }
            },
            'workflow': [
                '1. Sistem Analizi - Proje karmaşıklığı ve riskleri değerlendirilir',
                '2. Mimari Tasarım - Sistem mimarisi ve teknoloji stack\'i belirlenir',
                '3. Test Stratejisi - Kalite kontrol ve test planı oluşturulur',
                '4. PRP Üretimi - Context Engineering standartlarında dokümantasyon hazırlanır'
            ],
            'llm_provider': self.llm_client.config.name if hasattr(self.llm_client, 'config') else 'Unknown'
        } 