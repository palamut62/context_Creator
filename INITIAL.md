## FEATURE:

Python ve Flask kullanarak Context Engineering PRP Generator uygulaması geliştir. Bu uygulama:

- **Multi-LLM Provider Desteği**: Gemini API, OpenRouter API, OpenAI API, DeepSeek API gibi çeşitli yapay zeka modellerini destekler
- **Pydantic AI Tabanlı Yazılım Mühendisliği Ekibi**: Farklı uzmanlık alanlarına sahip AI ajanları (Sistem Analisti, Yazılım Mimarı, Test Uzmanı, Dokümantasyon Uzmanı) kullanır
- **Context Engineering Uyumluluğu**: Sadece Claude değil, tüm AI kod geliştirme araçları için kullanılabilir PRP dosyaları üretir
- **Kapsamlı Bilgi Toplama**: Kullanıcıdan proje gereksinimleri, teknoloji tercihleri, kısıtlamalar ve özel gereksinimler alır
- **Otomatik PRP Üretimi**: Toplanan bilgileri kullanarak Context Engineering standartlarına uygun prp.md dosyası oluşturur

## EXAMPLES:

Context Engineering template'lerini referans alarak:
- `examples/flask_patterns.py` - Flask web patterns ve form yönetimi
- `examples/pydantic_agents/` - Multi-agent sistem mimarisi
- `examples/api_integrations/` - Farklı LLM provider entegrasyonları
- `examples/prp_templates/` - Context Engineering PRP şablonları

## DOCUMENTATION:

- **Flask**: https://flask.palletsprojects.com/
- **Pydantic AI**: https://ai.pydantic.dev/
- **Context Engineering**: https://github.com/coleam00/context-engineering-intro
- **OpenAI API**: https://platform.openai.com/docs/api-reference
- **Google Gemini API**: https://ai.google.dev/docs
- **OpenRouter API**: https://openrouter.ai/docs
- **DeepSeek API**: https://platform.deepseek.com/api-docs

## OTHER CONSIDERATIONS:

- **Güvenlik**: API anahtarları güvenli şekilde yönetilmeli (.env dosyası)
- **Hata Yönetimi**: API çağrılarında robust hata yakalama
- **Kullanıcı Deneyimi**: Sezgisel form arayüzü ve real-time feedback
- **Performans**: Async işlemler ve progress bar'lar
- **Extensibility**: Yeni LLM provider'ları kolayca eklenebilir olmalı
- **Validation**: Üretilen PRP dosyalarının kalite kontrolü
- **Export Options**: Farklı formatlarda (markdown, JSON) export desteği
- **Template Customization**: Farklı proje türleri için özelleştirilebilir şablonlar 