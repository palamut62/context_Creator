"""
Context Engineering PRP Generator - Flask Version
=================================================

Bu uygulama, yazılım geliştirme projeleriniz için Context Engineering yaklaşımına 
uygun PRP (Product Requirements Prompt) dosyaları oluşturur.

Özellikler:
- Multi-LLM Provider desteği (OpenAI, Gemini, Anthropic, OpenRouter, DeepSeek)
- Pydantic AI tabanlı yazılım mühendisliği ekibi
- Kapsamlı proje analizi ve gereksinim toplama
- Context Engineering standartlarına uygun PRP üretimi
"""

import asyncio
import json
from pathlib import Path
import sys
from datetime import datetime, timedelta

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file, make_response
from flask_session import Session
from werkzeug.utils import secure_filename
import os
import tempfile
from flask_cors import CORS

# Proje dizinini Python path'ine ekle
sys.path.append(str(Path(__file__).parent))

from src.utils.config import load_config, get_available_providers, get_provider_info
from src.utils.logger import setup_logger
from src.agents.form_filler_agent import FormFillerAgent
from src.agents.prp_generator_agent import PRPGeneratorAgent
from src.agents.team_manager import SoftwareEngineeringTeam
from src.api.llm_factory import LLMProviderFactory
from src.models.project_data import ProjectData, ProjectRequirements, ProjectType, ProgrammingLanguage, Platform, TeamSize, Timeline
from src.ui.project_templates import ProjectTemplates
from src.utils.db import init_db, save_api_keys as db_save_keys, load_api_keys

# Geçici dosyalar için dizin
TEMP_DIR = os.path.join(os.path.dirname(__file__), 'temp')
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Flask uygulamasını oluştur
app = Flask(__name__)
app.secret_key = 'context-engineering-prp-generator-secret-key'  # Güvenlik için değiştirilmeli

# Session konfigürasyonu - sunucu tarafında sakla
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'prp_'
app.config['SESSION_FILE_DIR'] = os.path.join(TEMP_DIR, 'sessions')
app.config['SESSION_COOKIE_SECURE'] = False  # HTTPS için True yapın
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 saat

# Session dizinini oluştur
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)

# Session'ı başlat
Session(app)

# Konfigürasyon ve logger'ı yükle
try:
    config = load_config()
    logger = setup_logger()
    logger.info("Flask uygulaması başlatılıyor...")
except Exception as e:
    print(f"Konfigürasyon yüklenirken hata oluştu: {str(e)}")
    sys.exit(1)

# Template'leri yükle
templates = ProjectTemplates.get_templates()

# Veritabanını başlat
init_db()

# Senkronizasyon yardımcı fonksiyonu
def _sync_config_api_keys():
    """Veritabanındaki API anahtarlarına göre provider config'lerini günceller."""
    db_keys = load_api_keys()
    for name, provider_cfg in config.providers.items():
        db_key = db_keys.get(name, {}).get('api_key') if db_keys else None
        provider_cfg.api_key = db_key if db_key else None

    # default_provider'ı güncelle
    available = [n for n, p in config.providers.items() if p.api_key]
    if available and config.default_provider not in available:
        config.default_provider = available[0]

# Uygulama başlatılırken bir kez çalıştır
_sync_config_api_keys()

def save_to_temp_file(data, prefix='data'):
    """Büyük veriyi geçici dosyaya kaydet"""
    try:
        # Geçici dosya oluştur
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.json', 
            prefix=f'{prefix}_',
            dir=TEMP_DIR,
            delete=False,
            encoding='utf-8'
        ) as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            return f.name
    except Exception as e:
        logger.error(f"Geçici dosya kaydetme hatası: {str(e)}")
        return None

def load_from_temp_file(filepath):
    """Geçici dosyadan veri yükle"""
    try:
        if filepath and os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        logger.error(f"Geçici dosya okuma hatası: {str(e)}")
        return None

def cleanup_temp_files():
    """24 saatten eski geçici dosyaları temizle"""
    try:
        if not os.path.exists(TEMP_DIR):
            return
            
        current_time = datetime.now()
        for filename in os.listdir(TEMP_DIR):
            filepath = os.path.join(TEMP_DIR, filename)
            if os.path.isfile(filepath):
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                if current_time - file_time > timedelta(hours=24):
                    os.remove(filepath)
                    logger.info(f"Eski geçici dosya silindi: {filename}")
    except Exception as e:
        logger.error(f"Geçici dosya temizleme hatası: {str(e)}")

@app.route('/')
def index():
    """Kök URL doğrudan proje kurulumu adımına yönlendirir"""
    # İlk adım olarak proje kurulumunu işaretle
    session['current_step'] = 'project_setup'
    return redirect(url_for('project_setup'))

@app.route('/project-setup', methods=['GET', 'POST'])
def project_setup():
    """Proje kurulum sayfası"""
    session['current_step'] = 'project_setup'
    
    if request.method == 'POST':
        # POST request - JSON veri al
        data = request.get_json()
        
        # Proje verilerini kaydet
        project_data = {
            'project_name': data.get('project_name'),
            'project_type': data.get('project_type'),
            'description': data.get('description'),
            'target_audience': data.get('target_audience'),
            'timeline': data.get('timeline'),
            'deployment_target': data.get('deployment_target'),
            'budget_range': data.get('budget_range'),
            'main_goals': data.get('main_goals', []),
            'tech_stack': data.get('tech_stack', [])
        }
        
        session['project_data'] = project_data
        
        return jsonify({
            'success': True,
            'message': 'Proje verileri kaydedildi'
        })
    
    # GET request - sayfa göster
    # Template bilgilerini al
    template_data = {}
    if session.get('selected_template'):
        template_data = ProjectTemplates.get_template(session['selected_template'])
    
    # AI'dan gelen verileri al
    ai_data = session.get('ai_filled_data', {})
    
    return render_template('project_setup.html',
                         template_data=template_data,
                         ai_data=ai_data,
                         templates=templates)

@app.route('/requirements', methods=['GET', 'POST'])
def requirements():
    """Gereksinimler sayfası"""
    session['current_step'] = 'requirements'
    
    # Proje verilerini kontrol et
    if 'project_data' not in session:
        return redirect(url_for('project_setup'))
    
    if request.method == 'POST':
        # POST request - JSON veri al
        data = request.get_json()
        
        # Gereksinimler kaydet
        requirements = {
            'functional_requirements': data.get('functional_requirements'),
            'non_functional_requirements': data.get('non_functional_requirements'),
            'technical_constraints': data.get('technical_constraints'),
            'acceptance_criteria': data.get('acceptance_criteria'),
            'user_stories': data.get('user_stories'),
            'dependencies': data.get('dependencies'),
            'risks': data.get('risks')
        }
        
        session['project_requirements'] = requirements
        
        return jsonify({
            'success': True,
            'message': 'Gereksinimler kaydedildi'
        })
    
    # GET request - sayfa göster
    # Template bilgilerini al
    template_requirements = {}
    if session.get('selected_template'):
        template_data = ProjectTemplates.get_template(session['selected_template'])
        template_requirements = template_data.get('requirements', {})
    
    # AI'dan gelen verileri al
    ai_requirements = session.get('ai_filled_requirements', {})
    
    return render_template('requirements.html',
                         project_data=session['project_data'],
                         template_requirements=template_requirements,
                         ai_requirements=ai_requirements,
                         templates=templates)

@app.route('/generation')
def generation():
    """PRP üretim sayfası"""
    session['current_step'] = 'generation'
    
    # Proje verileri kontrol et
    if 'project_data' not in session:
        return redirect(url_for('project_setup'))
    
    # Eğer gereksinimler yoksa boş bir gereksinimler objesi oluştur
    if 'project_requirements' not in session:
        session['project_requirements'] = {
            'functional_requirements': '',
            'non_functional_requirements': '',
            'technical_constraints': '',
            'acceptance_criteria': '',
            'user_stories': '',
            'dependencies': '',
            'risks': ''
        }
    
    return render_template('generation.html',
                         project_data=session['project_data'])

@app.route('/results')
def results():
    """Sonuçlar sayfası"""
    session['current_step'] = 'results'
    
    # PRP'yi kontrol et - önce geçici dosyadan, sonra session'dan
    generated_prp = None
    if 'generated_prp_file' in session:
        generated_prp = load_from_temp_file(session['generated_prp_file'])
    elif 'generated_prp' in session:
        generated_prp = session['generated_prp']
    
    if not generated_prp:
        return redirect(url_for('generation'))
    
    return render_template('results.html',
                         generated_prp=generated_prp,
                         project_data=session['project_data'])

@app.route('/api/ai-fill-form', methods=['POST'])
def ai_fill_form():
    data = request.get_json()
    description = data.get('description')
    if not description:
        return jsonify({'success': False, 'error': 'Project description is required'}), 400

    expanded_desc = session.get('expanded_description', description)
    provider_name = session.get('selected_provider', config.default_provider)
    _apply_session_api_key(provider_name)
    factory = LLMProviderFactory(config)
    llm_client = factory.create_client(provider_name)
    
    try:
        agent = FormFillerAgent(llm_client, logger)
        filled_data = asyncio.run(agent.analyze_and_fill_form(expanded_desc))
        project_fields = {
            'project_name': filled_data.get('project_name'),
            'project_type': filled_data.get('project_type'),
            'description': filled_data.get('description'),
            'target_audience': filled_data.get('target_audience'),
            'timeline': filled_data.get('timeline'),
            'deployment_target': filled_data.get('deployment_target'),
            'budget_range': filled_data.get('budget_range'),
            'main_goals': filled_data.get('main_goals', []),
            'tech_stack': filled_data.get('tech_stack', [])
        }
        session['ai_filled_data'] = project_fields
        return jsonify({'success': True, 'filled_data': project_fields})
    except Exception as e:
        logger.error(f"Form filling error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ai-fill-requirements', methods=['POST'])
def ai_fill_requirements():
    data = request.get_json(silent=True) or {}
    description = data.get('description')
    
    if not description:
        project_data = session.get('project_data', {})
        description = project_data.get('description')
    
    expanded_desc = session.get('expanded_description', description)
    if not expanded_desc:
        return jsonify({'success': False, 'error': 'Project description is required'}), 400
    
    provider_name = session.get('selected_provider', config.default_provider)
    _apply_session_api_key(provider_name)
    factory = LLMProviderFactory(config)
    llm_client = factory.create_client(provider_name)
    
    try:
        agent = FormFillerAgent(llm_client, logger)
        filled_data = asyncio.run(agent.analyze_and_fill_form(expanded_desc))
        requirements_fields = {
            'functional_requirements': '\n'.join(filled_data.get('functional_requirements', [])),
            'non_functional_requirements': '\n'.join(filled_data.get('non_functional_requirements', [])),
            'technical_constraints': '\n'.join(filled_data.get('constraints', [])),
            'acceptance_criteria': '\n'.join(filled_data.get('acceptance_criteria', [])),
            'user_stories': '\n'.join(filled_data.get('user_stories', [])),
            'dependencies': '\n'.join(filled_data.get('tech_stack', [])),
            'risks': '\n'.join(filled_data.get('risks', []))
        }
        session['ai_filled_requirements'] = requirements_fields
        return jsonify({'success': True, 'filled_data': requirements_fields})
    except Exception as e:
        logger.error(f"Requirements filling error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clear-ai-data', methods=['POST'])
def clear_ai_data():
    """AI verilerini temizleme API'si"""
    try:
        data = request.get_json()
        data_type = data.get('type', 'form')  # 'form' veya 'requirements'
        
        if data_type == 'form':
            session.pop('ai_filled_data', None)
        elif data_type == 'requirements':
            session.pop('ai_filled_requirements', None)
        
        return jsonify({
            'success': True,
            'message': 'AI verileri temizlendi'
        })
        
    except Exception as e:
        logger.error(f"AI veri temizleme hatası: {str(e)}")
        return jsonify({'error': f'Veri temizleme hatası: {str(e)}'}), 500

@app.route('/api/save-project', methods=['POST'])
def save_project():
    """Proje verilerini kaydetme API'si"""
    try:
        data = request.get_json()
        
        # Project type mapping
        project_type_mapping = {
            "Web Application": ProjectType.WEB_APP,
            "Mobile App": ProjectType.MOBILE_APP,
            "Desktop Application": ProjectType.DESKTOP_APP,
            "API/Backend Service": ProjectType.API_BACKEND,
            "Static Website": ProjectType.WEB_APP,
            "E-commerce Platform": ProjectType.WEB_APP,
            "Dashboard/Analytics": ProjectType.WEB_APP,
            "Marketing Website": ProjectType.WEB_APP,
            "Portfolio Website": ProjectType.WEB_APP,
            "Blog/CMS": ProjectType.WEB_APP,
            "Other": ProjectType.OTHER
        }
        
        # Timeline mapping
        timeline_mapping = {
            "1-2 hafta": Timeline.SHORT,
            "2-3 hafta": Timeline.MEDIUM_SHORT,
            "1-2 ay": Timeline.MONTH,
            "2-3 ay": Timeline.QUARTER,
            "3-6 ay": Timeline.HALF_YEAR,
            "6+ ay": Timeline.LONG_TERM
        }
        
        # ProjectData oluştur - tutarlı field isimleri kullan
        project_data = {
            'project_name': data.get('project_name'),
            'project_type': data.get('project_type'),
            'description': data.get('description'),
            'target_audience': data.get('target_audience'),
            'timeline': data.get('timeline'),
            'deployment_target': data.get('deployment_target'),
            'budget_range': data.get('budget_range'),
            'main_goals': data.get('main_goals', []),
            'tech_stack': data.get('tech_stack', [])
        }
        
        # Session'a kaydet
        session['project_data'] = project_data
        
        return jsonify({
            'success': True,
            'message': 'Proje verileri kaydedildi'
        })
        
    except Exception as e:
        logger.error(f"Proje kaydetme hatası: {str(e)}")
        return jsonify({'error': f'Proje kaydetme hatası: {str(e)}'}), 500

@app.route('/api/save-requirements', methods=['POST'])
def save_requirements():
    """Gereksinimler kaydetme API'si"""
    try:
        data = request.get_json()
        
        # ProjectRequirements oluştur
        requirements = {
            'functional_requirements': data.get('functional_requirements'),
            'non_functional_requirements': data.get('non_functional_requirements'),
            'technical_requirements': data.get('technical_requirements'),
            'constraints': data.get('constraints'),
            'additional_info': data.get('additional_info')
        }
        
        # Session'a kaydet
        session['project_requirements'] = requirements
        
        return jsonify({
            'success': True,
            'message': 'Gereksinimler kaydedildi'
        })
        
    except Exception as e:
        logger.error(f"Gereksinim kaydetme hatası: {str(e)}")
        return jsonify({'error': f'Gereksinim kaydetme hatası: {str(e)}'}), 500

@app.route('/api/generate-prp', methods=['POST'])
def generate_prp():
    """PRP üretme API'si - Sample PRP formatında eksiksiz"""
    try:
        # Gerekli verileri kontrol et
        if 'project_data' not in session or 'project_requirements' not in session:
            return jsonify({'error': 'Proje verileri eksik'}), 400
        
        # Proje verilerini al
        session_project_data = session['project_data']
        session_requirements = session['project_requirements']
        
        # Üretim ayarlarını al
        data = request.get_json() or {}
        detail_level = data.get('detail_level', 'detailed')
        include_examples = data.get('include_examples', True)
        
        # LLM client oluştur
        selected_provider = session.get('selected_provider', config.default_provider)
        _apply_session_api_key(selected_provider)
        llm_factory = LLMProviderFactory(config)
        llm_client = llm_factory.create_client(selected_provider)
        
        # PRP Generator agent'ı oluştur
        prp_generator = PRPGeneratorAgent(llm_client, logger)
        
        # Proje verilerini PRP Generator için uygun formata çevir
        # Hem eski hem yeni format için uyumluluk sağla
        project_data = {
            'project_name': session_project_data.get('project_name') or session_project_data.get('name'),
            'project_type': session_project_data.get('project_type') or session_project_data.get('type'),
            'description': session_project_data.get('description'),
            'tech_stack': session_project_data.get('tech_stack', []),
            'target_platform': session_project_data.get('deployment_target'),
            'timeline': session_project_data.get('timeline'),
            'main_goals': session_project_data.get('main_goals'),
            'target_audience': session_project_data.get('target_audience'),
            'budget_range': session_project_data.get('budget_range'),
            'detail_level': detail_level,
            'include_examples': include_examples
        }
        
        # Requirements'ı da uygun formata çevir
        # Önce AI ile doldurulmuş verileri kontrol et, sonra manuel girilenleri
        ai_requirements = session.get('ai_filled_requirements', {})
        
        requirements = {
            'functional_requirements': session_requirements.get('functional_requirements') or ai_requirements.get('functional_requirements', ''),
            'non_functional_requirements': session_requirements.get('non_functional_requirements') or ai_requirements.get('non_functional_requirements', ''),
            'technical_constraints': session_requirements.get('technical_constraints') or ai_requirements.get('technical_constraints', ''),
            'acceptance_criteria': session_requirements.get('acceptance_criteria') or ai_requirements.get('acceptance_criteria', ''),
            'user_stories': session_requirements.get('user_stories') or ai_requirements.get('user_stories', ''),
            'dependencies': session_requirements.get('dependencies') or ai_requirements.get('dependencies', ''),
            'risks': session_requirements.get('risks') or ai_requirements.get('risks', '')
        }
        
        # Detay seviyesine göre proje verilerini zenginleştir
        if detail_level == 'comprehensive':
            # Kapsamlı detaylar ekle
            project_data['include_architecture'] = True
            project_data['include_testing'] = True
            project_data['include_deployment'] = True
        elif detail_level == 'basic':
            # Temel bilgiler yeterli
            project_data['simplified'] = True
        
        # Async fonksiyonu çalıştır
        prp_content = asyncio.run(
            prp_generator.generate_comprehensive_prp(project_data, requirements)
        )
        
        # Büyük veriyi geçici dosyaya kaydet
        prp_file = save_to_temp_file(prp_content, 'prp')
        if prp_file:
            session['generated_prp_file'] = prp_file
            # Session'dan büyük veriyi kaldır
            session.pop('generated_prp', None)
        else:
            # Geçici dosya kaydedilemezse session'da tut (son çare)
            session['generated_prp'] = prp_content
        
        session['generation_settings'] = {
            'detail_level': detail_level,
            'include_examples': include_examples,
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'content': prp_content,
            'message': 'Eksiksiz PRP başarıyla oluşturuldu',
            'settings': session['generation_settings']
        })
        
    except Exception as e:
        logger.error(f"PRP üretme hatası: {str(e)}")
        return jsonify({'error': f'PRP üretme hatası: {str(e)}'}), 500

@app.route('/api/download-prp')
def download_prp():
    """PRP dosyasını indirme API'si"""
    try:
        if 'generated_prp' not in session:
            return jsonify({'error': 'PRP bulunamadı'}), 404
        
        # Geçici dosya oluştur
        filename = f"{session['project_data']['name'].replace(' ', '_')}_PRP.md"
        filepath = Path(f"output/{filename}")
        filepath.parent.mkdir(exist_ok=True)
        
        # PRP'yi dosyaya yaz
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(session['generated_prp'])
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        logger.error(f"PRP indirme hatası: {str(e)}")
        return jsonify({'error': f'PRP indirme hatası: {str(e)}'}), 500

@app.route('/api/set-provider', methods=['POST'])
def set_provider():
    """Provider ayarlama API'si"""
    try:
        data = request.get_json()
        provider = data.get('provider')
        
        if provider not in get_available_providers(config):
            return jsonify({'error': 'Geçersiz provider'}), 400
        
        session['selected_provider'] = provider
        
        return jsonify({
            'success': True,
            'message': f'Provider {provider} olarak ayarlandı'
        })
        
    except Exception as e:
        logger.error(f"Provider ayarlama hatası: {str(e)}")
        return jsonify({'error': f'Provider ayarlama hatası: {str(e)}'}), 500

@app.route('/api/select-template', methods=['POST'])
def select_template():
    """Template seçme API'si"""
    try:
        data = request.get_json()
        template_id = data.get('template_id')
        
        if template_id not in templates:
            return jsonify({'error': 'Geçersiz template'}), 400
        
        session['selected_template'] = template_id
        session['use_template'] = True
        
        return jsonify({
            'success': True,
            'message': f'Template seçildi: {templates[template_id]["title"]}'
        })
        
    except Exception as e:
        logger.error(f"Template seçme hatası: {str(e)}")
        return jsonify({'error': f'Template seçme hatası: {str(e)}'}), 500

@app.route('/api/get-generated-content')
def get_generated_content():
    """Üretilen içeriği alma API'si"""
    try:
        # Önce geçici dosyadan, sonra session'dan dene
        content = None
        if 'generated_prp_file' in session:
            content = load_from_temp_file(session['generated_prp_file'])
        elif 'generated_prp' in session:
            content = session['generated_prp']
        
        if not content:
            return jsonify({'error': 'Üretilen içerik bulunamadı'}), 404
        
        # Markdown'ı HTML'e çevir (basit)
        html_content = content.replace('\n', '<br>')
        
        return jsonify({
            'success': True,
            'content': content,
            'html': html_content
        })
        
    except Exception as e:
        logger.error(f"İçerik alma hatası: {str(e)}")
        return jsonify({'error': f'İçerik alma hatası: {str(e)}'}), 500

@app.route('/api/download-file', methods=['POST'])
def download_file():
    """Dosya indirme API'si"""
    try:
        data = request.get_json()
        format_type = data.get('format', 'markdown')
        
        # Önce geçici dosyadan, sonra session'dan dene
        content = None
        if 'generated_prp_file' in session:
            content = load_from_temp_file(session['generated_prp_file'])
        elif 'generated_prp' in session:
            content = session['generated_prp']
        
        if not content:
            return jsonify({'error': 'İndirilecek içerik bulunamadı'}), 404
        
        # Format'a göre dosya hazırla
        if format_type == 'txt':
            # Markdown işaretlerini kaldır
            import re
            content = re.sub(r'[#*`]', '', content)
        elif format_type == 'json':
            import json
            content = json.dumps({
                'project_data': session.get('project_data', {}),
                'requirements': session.get('project_requirements', {}),
                'generated_content': content,
                'generated_at': datetime.now().isoformat()
            }, indent=2, ensure_ascii=False)
        
        # Dosya olarak döndür
        response = make_response(content)
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = f'attachment; filename=prp_{int(datetime.now().timestamp())}.{format_type}'
        
        return response
        
    except Exception as e:
        logger.error(f"Dosya indirme hatası: {str(e)}")
        return jsonify({'error': f'Dosya indirme hatası: {str(e)}'}), 500

@app.route('/api/send-email', methods=['POST'])
def send_email():
    """E-posta gönderme API'si"""
    try:
        data = request.get_json()
        
        # Mock e-posta gönderimi (gerçek SMTP konfigürasyonu gerekli)
        logger.info(f"E-posta gönderme simülasyonu: {data.get('to')}")
        
        return jsonify({
            'success': True,
            'message': 'E-posta başarıyla gönderildi'
        })
        
    except Exception as e:
        logger.error(f"E-posta gönderme hatası: {str(e)}")
        return jsonify({'error': f'E-posta gönderme hatası: {str(e)}'}), 500

@app.route('/api/submit-feedback', methods=['POST'])
def submit_feedback():
    """Geri bildirim gönderme API'si"""
    try:
        data = request.get_json()
        
        # Geri bildirimi logla (gerçek uygulamada veritabanına kaydedilir)
        logger.info(f"Geri bildirim alındı: Kalite={data.get('quality')}, Yorum={data.get('feedback')}")
        
        return jsonify({
            'success': True,
            'message': 'Geri bildirim kaydedildi'
        })
        
    except Exception as e:
        logger.error(f"Geri bildirim hatası: {str(e)}")
        return jsonify({'error': f'Geri bildirim hatası: {str(e)}'}), 500

@app.route('/api/clear-session', methods=['POST'])
def clear_session():
    """Session temizleme API'si"""
    try:
        # Geçici dosyaları temizle
        if 'generated_prp_file' in session:
            prp_file = session['generated_prp_file']
            if os.path.exists(prp_file):
                os.remove(prp_file)
        
        # Session'ı temizle
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Session temizlendi'
        })
        
    except Exception as e:
        logger.error(f"Session temizleme hatası: {str(e)}")
        return jsonify({'error': f'Session temizleme hatası: {str(e)}'}), 500

@app.route('/api/clear-template', methods=['POST'])
def clear_template():
    """Seçili template'i temizleyen API"""
    try:
        session.pop('selected_template', None)
        session.pop('use_template', None)
        return jsonify({
            'success': True,
            'message': 'Şablon seçimi temizlendi'
        })
    except Exception as e:
        logger.error(f"Template temizleme hatası: {str(e)}")
        return jsonify({'error': f'Template temizleme hatası: {str(e)}'}), 500

@app.route('/api/expand-description', methods=['POST'])
def expand_description():
    data = request.get_json()
    description = data.get('description')
    if not description:
        return jsonify({'success': False, 'error': 'Description is required'}), 400

    provider_name = session.get('selected_provider', config.default_provider)
    _apply_session_api_key(provider_name)
    
    try:
        factory = LLMProviderFactory(config)
        llm_client = factory.create_client(provider_name)
        prompt = f"Expand this short project description into a more detailed version, including key features, goals, and technical aspects: {description}"
        expanded = asyncio.run(llm_client.generate_response(prompt))
        session['expanded_description'] = expanded
        return jsonify({'success': True, 'expanded_description': expanded})
    except Exception as e:
        logger.error(f"Description expansion error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Context processor for template variables
@app.context_processor
def inject_template_vars():
    """Template'lere ortak değişkenleri enjekte et"""
    return {
        'available_providers': get_available_providers(config),
        'current_step_index': get_current_step_index(),
        'progress': get_progress_percentage(),
        'templates': templates,
        'provider_info': get_provider_info(config)
    }

def get_current_step_index():
    """Mevcut adım indeksini döndür"""
    current_step = session.get('current_step', 'project_setup')
    steps = ['project_setup', 'requirements', 'generation', 'results', 'api_keys']
    try:
        return steps.index(current_step) + 1
    except ValueError:
        return 1

def get_progress_percentage():
    """İlerleme yüzdesini döndür"""
    current_step_index = get_current_step_index()
    return (current_step_index / 5) * 100

# Yeni yardımcı: oturum API key'lerini config'e enjekte et
def _apply_session_api_key(provider_name):
    """Session'daki API anahtarını ilgili provider config'ine uygula"""
    # öncelik oturum, sonra db
    api_keys = session.get('api_keys') or load_api_keys()
    key = None
    model = None
    if api_keys and provider_name in api_keys:
        setting = api_keys[provider_name]
        key = setting.get('api_key', '')
        if isinstance(setting, dict):
            model = setting.get('model') if setting.get('model') else None
    if key:
        try:
            config.providers[provider_name].api_key = key
            if model:
                config.providers[provider_name].default_model = model
        except Exception:
            pass

@app.route('/api-keys')
def api_keys_page():
    """API Key ayarları sayfası"""
    session['current_step'] = 'api_keys'
    provider_defaults = {p: getattr(config.providers[p], 'default_model', '') for p in config.providers}
    return render_template('api_keys.html', providers=get_available_providers(config), saved_keys=load_api_keys(), defaults=provider_defaults)

@app.route('/api/save-api-keys', methods=['POST'])
def save_api_keys():
    """API anahtarlarını kaydeder"""
    try:
        data = request.get_json()
        api_keys = data.get('api_keys', {})
        # Basit doğrulama
        if not isinstance(api_keys, dict):
            return jsonify({'error': 'Geçersiz veri'}), 400
        # mevcutları al ve birleştir
        current = load_api_keys()
        merged = current.copy()
        for prov, info in api_keys.items():
            merged[prov] = merged.get(prov, {})
            if info.get('api_key'):
                merged[prov]['api_key'] = info['api_key']
            if info.get('model'):
                merged[prov]['model'] = info['model']
        # oturuma sadece anahtarları koy
        session['api_keys'] = {p: d.get('api_key') for p, d in merged.items() if d.get('api_key')}
        db_save_keys(merged)
        # Kaydetme sonrası config'i güncelle
        _sync_config_api_keys()
        return jsonify({'success': True, 'message': 'API anahtarları kaydedildi'})
    except Exception as e:
        logger.error(f"API anahtarları kaydetme hatası: {str(e)}")
        return jsonify({'error': 'API anahtarları kaydedilemedi'}), 500

if __name__ == '__main__':
    # Templates dizinini oluştur
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    # Eski geçici dosyaları temizle
    cleanup_temp_files()
    
    # Uygulamayı başlat
    app.run(debug=True, host='0.0.0.0', port=5000) 