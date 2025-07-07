"""
Proje Template'leri
==================

Bu modül, kullanıcıların hızlı başlangıç yapabilmesi için 
hazır proje template'leri içerir.
"""

from typing import Dict, Any
from ..models.project_data import ProjectData, ProjectRequirements, ProgrammingLanguage, Platform, TeamSize, Timeline, ProjectType

class ProjectTemplates:
    """Proje template'leri sınıfı"""
    
    @staticmethod
    def get_templates() -> Dict[str, Dict[str, Any]]:
        """Tüm template'leri döndür"""
        
        return {
            "todo_app": {
                "title": "📝 Modern Todo App",
                "description": "React/TypeScript ile modern todo uygulaması",
                "icon": "📝",
                "category": "Web Application",
                "difficulty": "Başlangıç",
                "estimated_time": "2-3 hafta",
                "project_data": {
                    "project_name": "Modern Todo App",
                    "project_type": "Web Application",
                    "description": "Kullanıcıların görevlerini organize etmelerine yardımcı olan modern, responsive todo uygulaması",
                    "main_goals": [
                        "Görev ekleme, düzenleme ve silme",
                        "Kategori bazlı görev organizasyonu", 
                        "Drag & drop ile görev sıralama",
                        "Local storage ile veri saklama",
                        "Dark/Light mode desteği",
                        "Responsive tasarım"
                    ],
                    "tech_stack": ["React", "TypeScript", "Tailwind CSS", "Local Storage"],
                    "deployment_target": "Vercel",
                    "timeline": "2-3 hafta",
                    "budget_range": "Kişisel proje"
                },
                "requirements": {
                    "functional_requirements": [
                        "Kullanıcı görev ekleyebilmeli",
                        "Görevleri kategori bazlı filtreleyebilmeli",
                        "Görev durumunu (tamamlandı/beklemede) değiştirebilmeli",
                        "Görevleri öncelik seviyesine göre sıralayabilmeli",
                        "Arama fonksiyonu ile görev bulabilmeli"
                    ],
                    "technical_requirements": [
                        "React 18+ kullanılmalı",
                        "TypeScript ile type safety sağlanmalı",
                        "Responsive design (mobile-first)",
                        "PWA desteği",
                        "Offline çalışabilme"
                    ],
                    "non_functional_requirements": [
                        "Sayfa yükleme süresi < 2 saniye",
                        "Mobil uyumlu tasarım",
                        "Accessibility (a11y) standartları",
                        "SEO optimize edilmiş"
                    ],
                    "constraints": [
                        "Backend gerektirmeyecek",
                        "Sadece client-side teknolojiler",
                        "Modern browser desteği",
                        "Hızlı geliştirme süreci"
                    ]
                }
            },
            
            "portfolio": {
                "title": "🎨 Professional Portfolio",
                "description": "Next.js ile profesyonel portfolyo sitesi",
                "icon": "🎨",
                "category": "Web Application", 
                "difficulty": "Orta",
                "estimated_time": "2-3 hafta",
                "project_data": {
                    "project_name": "Professional Portfolio",
                    "project_type": "Web Application",
                    "description": "Profesyonel portfolyo ve blog sitesi",
                    "main_goals": [
                        "Kişisel brand oluşturma",
                        "Proje showcase alanı",
                        "Blog yazıları paylaşma",
                        "İletişim formu",
                        "CV indirme özelliği",
                        "SEO optimizasyonu"
                    ],
                    "tech_stack": ["Next.js", "React", "TypeScript", "Tailwind CSS", "MDX"],
                    "deployment_target": "Vercel",
                    "timeline": "2-3 hafta",
                    "budget_range": "Kişisel proje"
                },
                "requirements": {
                    "functional_requirements": [
                        "Ana sayfa ile kişisel tanıtım",
                        "Projeler sayfası ile portfolio showcase",
                        "Blog sayfası ile yazı paylaşımı",
                        "Hakkımda sayfası ile detaylı bilgi",
                        "İletişim sayfası ile form",
                        "CV indirme linki"
                    ],
                    "technical_requirements": [
                        "Next.js 14+ App Router",
                        "MDX ile blog yazıları",
                        "Responsive design",
                        "Image optimization",
                        "Static site generation"
                    ],
                    "non_functional_requirements": [
                        "Core Web Vitals optimizasyonu",
                        "SEO dostu URL yapısı",
                        "Social media entegrasyonu",
                        "Analytics entegrasyonu",
                        "Accessibility compliance"
                    ],
                    "constraints": [
                        "Statik site olmalı",
                        "Hızlı yükleme süreleri",
                        "Minimal maintenance",
                        "Cost-effective hosting"
                    ]
                }
            },
            
            "landing_page": {
                "title": "🚀 High-Converting Landing Page",
                "description": "Yüksek dönüşüm oranları için optimize edilmiş landing page",
                "icon": "🚀",
                "category": "Web Application",
                "difficulty": "Orta",
                "estimated_time": "2-3 hafta",
                "project_data": {
                    "project_name": "High-Converting Landing Page",
                    "project_type": "Web Application",
                    "description": "Yüksek dönüşüm oranları için optimize edilmiş modern landing page",
                    "main_goals": [
                        "Yüksek conversion rate",
                        "A/B testing desteği",
                        "Lead generation",
                        "Analytics entegrasyonu",
                        "Mobile-first tasarım",
                        "Performance optimization"
                    ],
                    "tech_stack": ["React", "Next.js", "TypeScript", "Tailwind CSS", "Framer Motion"],
                    "deployment_target": "Vercel",
                    "timeline": "2-3 hafta",
                    "budget_range": "Kişisel proje"
                },
                "requirements": {
                    "functional_requirements": [
                        "Hero section ile güçlü açılış",
                        "Feature showcase bölümü",
                        "Testimonials ve social proof",
                        "Pricing table",
                        "Contact/signup form",
                        "FAQ bölümü"
                    ],
                    "technical_requirements": [
                        "Next.js ile SSG/SSR",
                        "Form validation ve submission",
                        "Animation ve micro-interactions",
                        "Email marketing entegrasyonu",
                        "Analytics tracking"
                    ],
                    "non_functional_requirements": [
                        "Sayfa hızı optimizasyonu",
                        "Conversion tracking",
                        "A/B testing capability",
                        "Mobile performance",
                        "SEO optimization"
                    ],
                    "constraints": [
                        "Minimum loading time",
                        "High conversion focus",
                        "Budget-friendly tools",
                        "Easy content updates"
                    ]
                }
            },
            
            "financial_dashboard": {
                "title": "📊 Professional Financial Dashboard",
                "description": "React/Next.js ile finansal veri dashboard'u",
                "icon": "📊",
                "category": "Web Application",
                "difficulty": "İleri",
                "estimated_time": "3-6 ay",
                "project_data": {
                    "project_name": "Professional Financial Dashboard",
                    "project_type": "Web Application",
                    "description": "Finansal verileri görselleştiren ve analiz eden profesyonel dashboard uygulaması",
                    "main_goals": [
                        "Finansal veri görselleştirme",
                        "Real-time data updates",
                        "Çoklu kullanıcı desteği",
                        "Rapor oluşturma",
                        "Data export özelliği",
                        "Güvenli authentication"
                    ],
                    "tech_stack": ["React", "TypeScript", "Next.js", "Chart.js", "Tailwind CSS", "Prisma", "PostgreSQL"],
                    "deployment_target": "AWS",
                    "timeline": "3-6 ay",
                    "budget_range": "Kurumsal proje"
                },
                "requirements": {
                    "functional_requirements": [
                        "Kullanıcı authentication ve authorization",
                        "Dashboard ile finansal metriklerin görselleştirilmesi",
                        "Grafik ve chart'lar ile veri analizi",
                        "Rapor oluşturma ve export",
                        "Real-time veri güncellemeleri",
                        "Kullanıcı bazlı izin yönetimi"
                    ],
                    "technical_requirements": [
                        "Next.js 14+ App Router",
                        "PostgreSQL veritabanı",
                        "Prisma ORM",
                        "Chart.js/D3.js entegrasyonu",
                        "WebSocket ile real-time updates"
                    ],
                    "non_functional_requirements": [
                        "Yüksek güvenlik standartları",
                        "Scalable architecture",
                        "Performance optimization",
                        "Data backup ve recovery",
                        "Audit logging"
                    ],
                    "constraints": [
                        "GDPR compliance gerekli",
                        "Financial data security",
                        "High availability requirement",
                        "Enterprise-level support"
                    ]
                }
            },
            
            "pyqt5_desktop": {
                "title": "🖥️ PyQt5 Desktop Application",
                "description": "Python PyQt5 ile modern masaüstü uygulaması",
                "icon": "🖥️",
                "category": "Desktop Application",
                "difficulty": "Orta",
                "estimated_time": "1-2 ay",
                "project_data": {
                    "project_name": "Modern Desktop Application",
                    "project_type": "Desktop Application",
                    "description": "PyQt5 kullanarak geliştirilmiş modern, kullanıcı dostu masaüstü uygulaması",
                    "main_goals": [
                        "Cross-platform masaüstü uygulaması",
                        "Modern ve sezgisel kullanıcı arayüzü",
                        "Dosya işleme ve yönetimi",
                        "Veritabanı entegrasyonu",
                        "Settings ve konfigürasyon yönetimi",
                        "Auto-update mekanizması"
                    ],
                    "tech_stack": ["Python", "PyQt5", "SQLite", "PyInstaller"],
                    "deployment_target": "Self-hosted",
                    "timeline": "1-2 ay",
                    "budget_range": "Kişisel proje"
                },
                "requirements": {
                    "functional_requirements": [
                        "Ana pencere ile merkezi kontrol paneli",
                        "Menu bar ve toolbar ile kolay erişim",
                        "Dosya açma, kaydetme ve düzenleme",
                        "Veritabanı CRUD işlemleri",
                        "Settings dialog ile kullanıcı tercihleri",
                        "About dialog ve help sistemi"
                    ],
                    "technical_requirements": [
                        "PyQt5 framework kullanımı",
                        "SQLite veritabanı entegrasyonu",
                        "MVC pattern implementasyonu",
                        "Exception handling ve logging",
                        "Unit testing ile kod kalitesi"
                    ],
                    "non_functional_requirements": [
                        "Windows, macOS, Linux desteği",
                        "Responsive UI design",
                        "Memory efficient çalışma",
                        "Fast startup time",
                        "Intuitive user experience"
                    ],
                    "constraints": [
                        "Python 3.8+ gereksinimi",
                        "Offline çalışabilme",
                        "Minimal external dependencies",
                        "Easy installation process"
                    ]
                }
            },
            
            "electron_desktop": {
                "title": "⚡ Electron Desktop App",
                "description": "Electron ile cross-platform masaüstü uygulaması",
                "icon": "⚡",
                "category": "Desktop Application",
                "difficulty": "Orta",
                "estimated_time": "2-3 ay",
                "project_data": {
                    "project_name": "Cross-Platform Electron App",
                    "project_type": "Desktop Application",
                    "description": "Electron framework kullanarak geliştirilmiş modern, cross-platform masaüstü uygulaması",
                    "main_goals": [
                        "Web teknolojileri ile masaüstü uygulaması",
                        "Windows, macOS, Linux desteği",
                        "Native OS entegrasyonu",
                        "Auto-updater mekanizması",
                        "Tray icon ve notifications",
                        "Modern UI/UX tasarımı"
                    ],
                    "tech_stack": ["Electron", "React", "TypeScript", "Node.js", "Webpack"],
                    "deployment_target": "Self-hosted",
                    "timeline": "2-3 ay",
                    "budget_range": "Orta bütçe ($1K - $10K)"
                },
                "requirements": {
                    "functional_requirements": [
                        "Main window ile ana uygulama arayüzü",
                        "Menu bar ve context menu'ler",
                        "File system erişimi ve dosya işlemleri",
                        "Native dialogs (open, save, message)",
                        "System tray integration",
                        "Keyboard shortcuts ve hotkeys"
                    ],
                    "technical_requirements": [
                        "Electron latest stable version",
                        "React 18+ ile modern UI",
                        "TypeScript ile type safety",
                        "IPC (Inter-Process Communication)",
                        "Native Node.js modules kullanımı"
                    ],
                    "non_functional_requirements": [
                        "Fast application startup",
                        "Memory optimization",
                        "Secure content loading",
                        "Code signing for distribution",
                        "Crash reporting ve analytics"
                    ],
                    "constraints": [
                        "Chromium engine dependency",
                        "Larger bundle size consideration",
                        "Platform-specific packaging",
                        "Security sandboxing requirements"
                    ]
                }
            },
            
            "ios_mobile": {
                "title": "📱 iOS Mobile Application",
                "description": "Swift ile native iOS mobil uygulaması",
                "icon": "📱",
                "category": "Mobile App",
                "difficulty": "İleri",
                "estimated_time": "2-3 ay",
                "project_data": {
                    "project_name": "Native iOS Mobile App",
                    "project_type": "Mobile App",
                    "description": "Swift ve SwiftUI kullanarak geliştirilmiş modern, native iOS mobil uygulaması",
                    "main_goals": [
                        "Native iOS user experience",
                        "SwiftUI ile modern UI tasarımı",
                        "Core Data ile veri yönetimi",
                        "Push notifications entegrasyonu",
                        "App Store optimizasyonu",
                        "iOS ecosystem entegrasyonu"
                    ],
                    "tech_stack": ["Swift", "SwiftUI", "Core Data", "Combine", "UIKit"],
                    "deployment_target": "App Store",
                    "timeline": "2-3 ay",
                    "budget_range": "Orta bütçe ($1K - $10K)"
                },
                "requirements": {
                    "functional_requirements": [
                        "Onboarding flow ile kullanıcı karşılama",
                        "Tab-based navigation yapısı",
                        "List ve detail view'lar",
                        "Search ve filtering özellikleri",
                        "User profile ve settings",
                        "Offline data synchronization"
                    ],
                    "technical_requirements": [
                        "iOS 15+ target deployment",
                        "SwiftUI ile declarative UI",
                        "Core Data stack kurulumu",
                        "Network layer ile API entegrasyonu",
                        "Push notifications setup"
                    ],
                    "non_functional_requirements": [
                        "60 FPS smooth animations",
                        "Fast app launch time",
                        "Memory efficient data handling",
                        "Battery life optimization",
                        "Accessibility (VoiceOver) support"
                    ],
                    "constraints": [
                        "Apple Developer Program membership",
                        "App Store Review Guidelines compliance",
                        "iOS Human Interface Guidelines",
                        "Privacy policy ve GDPR compliance"
                    ]
                }
            }
        }
    
    @staticmethod
    def get_template(template_id: str) -> Dict[str, Any]:
        """Belirli bir template'i döndür"""
        
        templates = ProjectTemplates.get_templates()
        return templates.get(template_id, {})
    
    @staticmethod
    def create_project_data_from_template(template_id: str) -> ProjectData:
        """Template'den ProjectData oluştur"""
        
        template = ProjectTemplates.get_template(template_id)
        if not template:
            raise ValueError(f"Template bulunamadı: {template_id}")
        
        project_data = template["project_data"]
        
        return ProjectData(
            name=project_data["project_name"],
            type=ProjectType.WEB_APP,  # Tüm template'ler Web Uygulaması
            description=project_data["description"],
            language=ProgrammingLanguage.JAVASCRIPT,  # Default olarak JavaScript
            platform=[Platform.WEB],  # Default olarak Web
            team_size=TeamSize.SOLO,  # Default olarak Solo
            timeline=Timeline(project_data["timeline"]) if project_data.get("timeline") else None
        )
    
    @staticmethod
    def create_requirements_from_template(template_id: str) -> ProjectRequirements:
        """Template'den ProjectRequirements oluştur"""
        
        template = ProjectTemplates.get_template(template_id)
        if not template:
            raise ValueError(f"Template bulunamadı: {template_id}")
        
        requirements = template["requirements"]
        
        return ProjectRequirements(
            functional_requirements="\n".join(requirements["functional_requirements"]),
            user_stories=None,
            frameworks="\n".join(requirements["technical_requirements"]),
            database=None,
            authentication=None,
            deployment=None,
            performance="\n".join(requirements["non_functional_requirements"]),
            security=None,
            constraints="\n".join(requirements["constraints"]),
            special_requirements=None
        ) 