"""
Logging Sistemi
===============

Bu modül, uygulamanın logging altyapısını sağlar.
Structured logging, log levels ve file/console output yönetimini içerir.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
import json
import os

class StructuredFormatter(logging.Formatter):
    """Structured JSON logging formatter"""
    
    def format(self, record):
        """Log kaydını JSON formatında formatla"""
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Exception bilgilerini ekle
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Extra fields'ları ekle
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
        
        return json.dumps(log_entry, ensure_ascii=False)

class ColoredConsoleFormatter(logging.Formatter):
    """Renkli console formatter"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        """Renkli log formatla"""
        
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Level with color
        level = f"{color}{record.levelname:<8}{reset}"
        
        # Module info
        module_info = f"{record.module}:{record.funcName}:{record.lineno}"
        
        # Message
        message = record.getMessage()
        
        return f"{timestamp} | {level} | {module_info:<30} | {message}"

def setup_logger(
    name: str = "context_engineering",
    level: str = "INFO",
    log_file: Optional[str] = None,
    enable_console: bool = True,
    enable_structured: bool = False
) -> logging.Logger:
    """
    Logger'ı yapılandır ve döndür
    
    Args:
        name: Logger adı
        level: Log seviyesi (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Log dosyası yolu (None ise dosyaya yazılmaz)
        enable_console: Console'a log yazılsın mı
        enable_structured: JSON formatında structured logging kullanılsın mı
    
    Returns:
        Yapılandırılmış logger instance
    """
    
    # Environment'tan ayarları al
    level = os.getenv("LOG_LEVEL", level).upper()
    log_file = os.getenv("LOG_FILE", log_file)
    enable_structured = os.getenv("ENABLE_DETAILED_LOGGING", "false").lower() == "true"
    
    # Logger'ı oluştur
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    # Mevcut handler'ları temizle
    logger.handlers.clear()
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        
        if enable_structured:
            console_handler.setFormatter(StructuredFormatter())
        else:
            console_handler.setFormatter(ColoredConsoleFormatter())
        
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        # Log dizinini oluştur
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        
        if enable_structured:
            file_handler.setFormatter(StructuredFormatter())
        else:
            # File için basit format
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s'
            )
            file_handler.setFormatter(file_formatter)
        
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str = None) -> logging.Logger:
    """
    Mevcut logger'ı al veya yeni bir tane oluştur
    
    Args:
        name: Logger adı (None ise root logger)
    
    Returns:
        Logger instance
    """
    
    if name is None:
        name = "context_engineering"
    
    logger = logging.getLogger(name)
    
    # Eğer logger henüz yapılandırılmamışsa, default setup'ı yap
    if not logger.handlers:
        return setup_logger(name)
    
    return logger

class LoggerMixin:
    """Logger mixin class - diğer class'lara logging capability ekler"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = get_logger(self.__class__.__name__)
    
    def log_info(self, message: str, **extra):
        """Info level log"""
        self.logger.info(message, extra={"extra_fields": extra} if extra else None)
    
    def log_warning(self, message: str, **extra):
        """Warning level log"""
        self.logger.warning(message, extra={"extra_fields": extra} if extra else None)
    
    def log_error(self, message: str, **extra):
        """Error level log"""
        self.logger.error(message, extra={"extra_fields": extra} if extra else None)
    
    def log_debug(self, message: str, **extra):
        """Debug level log"""
        self.logger.debug(message, extra={"extra_fields": extra} if extra else None)

def log_function_call(func):
    """Decorator - fonksiyon çağrılarını logla"""
    
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        # Function call'u logla
        logger.debug(
            f"Calling {func.__name__}",
            extra={
                "extra_fields": {
                    "function": func.__name__,
                    "args_count": len(args),
                    "kwargs_count": len(kwargs)
                }
            }
        )
        
        try:
            result = func(*args, **kwargs)
            
            # Success'i logla
            logger.debug(
                f"Successfully completed {func.__name__}",
                extra={
                    "extra_fields": {
                        "function": func.__name__,
                        "status": "success"
                    }
                }
            )
            
            return result
            
        except Exception as e:
            # Error'u logla
            logger.error(
                f"Error in {func.__name__}: {str(e)}",
                extra={
                    "extra_fields": {
                        "function": func.__name__,
                        "status": "error",
                        "error_type": type(e).__name__,
                        "error_message": str(e)
                    }
                },
                exc_info=True
            )
            raise
    
    return wrapper

def log_async_function_call(func):
    """Decorator - async fonksiyon çağrılarını logla"""
    
    async def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        # Function call'u logla
        logger.debug(
            f"Calling async {func.__name__}",
            extra={
                "extra_fields": {
                    "function": func.__name__,
                    "type": "async",
                    "args_count": len(args),
                    "kwargs_count": len(kwargs)
                }
            }
        )
        
        try:
            result = await func(*args, **kwargs)
            
            # Success'i logla
            logger.debug(
                f"Successfully completed async {func.__name__}",
                extra={
                    "extra_fields": {
                        "function": func.__name__,
                        "type": "async",
                        "status": "success"
                    }
                }
            )
            
            return result
            
        except Exception as e:
            # Error'u logla
            logger.error(
                f"Error in async {func.__name__}: {str(e)}",
                extra={
                    "extra_fields": {
                        "function": func.__name__,
                        "type": "async",
                        "status": "error",
                        "error_type": type(e).__name__,
                        "error_message": str(e)
                    }
                },
                exc_info=True
            )
            raise
    
    return wrapper 