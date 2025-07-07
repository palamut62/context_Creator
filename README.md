# 🤖 Context Engineering PRP Generator

**AI destekli yazılım geliştirme projeleriniz için Context Engineering standartlarına uygun PRP (Product Requirements Prompt) dosyaları oluşturun.**

## ✨ Özellikler

### 🔄 Multi-LLM Provider Desteği
- **OpenAI** (GPT-4, GPT-4o)
- **Google Gemini** (Gemini 2.5 Flash)
- **Anthropic Claude** (Claude 3.5 Sonnet)
- **OpenRouter** (Çoklu model desteği)
- **DeepSeek** (DeepSeek Chat)

### 👥 AI Yazılım Mühendisliği Ekibi
- **🔍 Sistem Analisti**: Proje gereksinimlerini analiz eder, karmaşıklık skorunu belirler
- **🏗️ Yazılım Mimarı**: Sistem mimarisini tasarlar, teknoloji stack'ini önerir
- **🧪 Test Uzmanı**: Test stratejisi oluşturur, kalite kontrol planı yapar
- **📚 Dokümantasyon Uzmanı**: Context Engineering standartlarında PRP üretir

### 🎯 Context Engineering Uyumluluğu
- **Tüm AI kod geliştirme araçları** ile uyumlu (Claude, Cursor, GitHub Copilot, Codeium, vb.)
- **Kapsamlı kontekst** sağlama
- **Doğrulama döngüleri** ile kalite kontrolü
- **Bilgi yoğunluğu** maksimizasyonu
- **Aşamalı başarı** metrikleri

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
# Repository'yi klonlayın
git clone https://github.com/your-username/context-engineering-prp-generator.git
cd context-engineering-prp-generator

# Sanal ortam oluşturun
python -m venv venv

# Sanal ortamı aktif edin
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 2. Konfigürasyon

`.env.example` dosyasını `.env` olarak kopyalayın ve API anahtarlarınızı ekleyin:

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Google Gemini API Configuration  
GOOGLE_API_KEY=your-google-gemini-api-key-here

# Anthropic Claude API Configuration
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here

# OpenRouter API Configuration
OPENROUTER_API_KEY=sk-or-your-openrouter-api-key-here

# DeepSeek API Configuration
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here

# Default LLM Provider
DEFAULT_LLM_PROVIDER=openai
```

### 3. Uygulamayı Çalıştırın

```bash
python flask_app.py
```

Tarayıcınızda `http://localhost:5000` adresine gidin.

## 📋 Kullanım

### 1. Proje Kurulumu
- Proje adı, türü ve temel bilgileri girin
- Programlama dili ve hedef platformları seçin
- Ekip büyüklüğü ve hedef süreyi belirtin

### 2. Gereksinim Toplama
- Fonksiyonel gereksinimleri detaylandırın
- Teknik gereksinimleri (framework, veritabanı, vb.) belirtin
- Kullanıcı hikayelerini ekleyin
- Kısıtlamaları ve özel gereksinimleri tanımlayın

### 3. AI Ekip Analizi
- Sistem Analisti projeyi değerlendirir
- Yazılım Mimarı mimari tasarımı oluşturur
- Test Uzmanı test stratejisini planlar
- Dokümantasyon Uzmanı PRP'yi üretir

### 4. Sonuç ve Export
- Oluşturulan PRP'yi önizleyin
- Markdown, JSON veya TXT formatında indirin
- Kalite metriklerini inceleyin

## 🏗️ Proje Yapısı

```
context-engineering-prp-generator/
├── flask_app.py                   # Ana Flask uygulaması
├── requirements.txt               # Python bağımlılıkları
├── .env.example                  # Environment variables örneği
├── INITIAL.md                    # Context Engineering tanımı
├── CLAUDE.md                     # Proje kuralları
├── README.md                     # Bu dosya
│
├── templates/                    # Flask HTML template'leri
│   ├── base.html                 # Temel layout
│   ├── index.html                # Ana sayfa
│   ├── project_setup.html        # Proje kurulum sayfası
│   ├── requirements.html         # Gereksinimler sayfası
│   ├── generation.html           # PRP üretim sayfası
│   └── results.html              # Sonuçlar sayfası
│
├── src/                          # Ana kaynak kodu
│   ├── __init__.py
│   ├── agents/                   # AI Ajanları
│   │   ├── __init__.py
│   │   ├── team_manager.py       # Ekip yöneticisi
│   │   ├── system_analyst.py     # Sistem analisti
│   │   ├── software_architect.py # Yazılım mimarı
│   │   ├── test_specialist.py    # Test uzmanı
│   │   ├── documentation_specialist.py # Dokümantasyon uzmanı
│   │   ├── form_filler_agent.py  # AI form doldurma ajanı
│   │   └── prp_generator_agent.py # PRP üretim ajanı
│   │
│   ├── api/                      # LLM Provider entegrasyonları
│   │   ├── __init__.py
│   │   └── llm_factory.py        # LLM factory pattern
│   │
│   ├── models/                   # Pydantic veri modelleri
│   │   ├── __init__.py
│   │   └── project_data.py       # Proje veri modelleri
│   │
│   ├── ui/                       # UI yardımcı modülleri
│   │   ├── __init__.py
│   │   └── project_templates.py  # Proje template'leri
│   │
│   └── utils/                    # Yardımcı modüller
│       ├── __init__.py
│       ├── config.py             # Konfigürasyon yönetimi
│       └── logger.py             # Logging sistemi
│
├── tests/                        # Test dosyaları
│   └── test_basic.py             # Temel testler
│
├── examples/                     # Örnek dosyalar
├── logs/                         # Log dosyaları
├── output/                       # Üretilen PRP dosyaları
└── temp/                         # Geçici dosyalar ve session'lar
```

## 🧪 Testler

Temel testleri çalıştırmak için:

```bash
# Pytest ile
pytest tests/

# Veya doğrudan
python tests/test_basic.py
```

## 🔧 Konfigürasyon

### Environment Variables

| Değişken | Açıklama | Varsayılan |
|----------|----------|------------|
| `OPENAI_API_KEY` | OpenAI API anahtarı | - |
| `GOOGLE_API_KEY` | Google Gemini API anahtarı | - |
| `ANTHROPIC_API_KEY` | Anthropic Claude API anahtarı | - |
| `OPENROUTER_API_KEY` | OpenRouter API anahtarı | - |
| `DEEPSEEK_API_KEY` | DeepSeek API anahtarı | - |
| `DEFAULT_LLM_PROVIDER` | Varsayılan LLM provider | `openai` |
| `LOG_LEVEL` | Log seviyesi | `INFO` |
| `TEST_MODE` | Test modu | `false` |

### Provider Konfigürasyonu

Her provider için ayrı konfigürasyon ayarları:

```env
# Model seçimi
OPENAI_DEFAULT_MODEL=gpt-4o
GEMINI_DEFAULT_MODEL=gemini-2.5-flash
ANTHROPIC_DEFAULT_MODEL=claude-3-5-sonnet-20241022

# Rate limiting
OPENAI_RPM=60
GEMINI_RPM=60
ANTHROPIC_RPM=50
```

## 📖 Context Engineering Nedir?

Context Engineering, geleneksel "prompt engineering"den çok daha kapsamlı bir yaklaşımdır:

### Geleneksel Prompt Engineering
- Sadece kelime oyunları ve akıllı ifadeler
- Tek seferlik talimatlar
- Sticky note gibi kısa mesajlar

### Context Engineering
- **Kapsamlı sistem ve metodoloji**
- **Dokümantasyon, örnekler, kurallar ve doğrulama döngüleri**
- **Tam bir senaryo yazımı gibi detaylı**

### Temel Prensipler

1. **Context is King**: Kapsamlı kontekst sağlama
2. **Validation Loops**: Doğrulama döngüleri
3. **Information Dense**: Yoğun bilgi içeriği
4. **Progressive Success**: Aşamalı başarı
5. **AI Tool Compatibility**: Tüm AI araçları ile uyumlu

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 🙏 Teşekkürler

- [Context Engineering Community](https://github.com/coleam00/context-engineering-intro) - Temel metodoloji
- [Pydantic AI](https://github.com/pydantic/pydantic-ai) - AI agent framework
- [Flask](https://flask.palletsprojects.com/) - Web app framework

## 📞 Destek

Sorularınız veya sorunlarınız için:

- GitHub Issues açın
- Dokümantasyonu inceleyin
- Community Discord'a katılın

---

**Context Engineering ile yazılım geliştirme sürecinizi devrim niteliğinde değiştirin! 🚀** #   c o n t e x t _ C r e a t o r  
 