"""Módulo de gerenciamento de logs para automação RPA"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path


class RPALogger:
    """Gerenciador de logs para projetos RPA com rotação e formatação customizada."""
    
    # Formatos de log
    SIMPLE_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    DETAILED_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s'
    
    # Níveis padrão
    DEFAULT_LEVEL = logging.INFO
    DEFAULT_LOG_DIR = 'logs'
    DEFAULT_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
    DEFAULT_BACKUP_COUNT = 5
    
    def __init__(self, name='RPA', log_dir=None, level=None, 
                 format_type='detailed', enable_file=True, enable_console=True,
                 max_bytes=DEFAULT_MAX_BYTES, backup_count=DEFAULT_BACKUP_COUNT):
        """
        Inicializa o gerenciador de logs RPA.

        Args:
            name (str): Nome do logger. Padrão: 'RPA'
            log_dir (str): Diretório para arquivos de log. Padrão: 'logs'
            level (int): Nível de log (logging.DEBUG, INFO, WARNING, ERROR, CRITICAL)
                        Padrão: logging.INFO
            format_type (str): Tipo de formato ('simple' ou 'detailed'). Padrão: 'detailed'
            enable_file (bool): Se True, salva logs em arquivo. Padrão: True
            enable_console (bool): Se True, exibe logs no console. Padrão: True
            max_bytes (int): Tamanho máximo do arquivo de log antes de rotacionar. 
                           Padrão: 10 MB
            backup_count (int): Quantidade de arquivos de backup a manter. 
                              Padrão: 5

        Exemplo:
            >>> logger = RPALogger(name='MyBot')
            >>> logger.info('Iniciando automação')
            >>> logger.error('Erro encontrado')
        """
        self.name = name
        self.log_dir = log_dir or self.DEFAULT_LOG_DIR
        self.level = level or self.DEFAULT_LEVEL
        self.format_type = format_type
        self.enable_file = enable_file
        self.enable_console = enable_console
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        
        # Criar logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        
        # Evitar handlers duplicados
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Configurar formato
        self._formatter = self._get_formatter()
        
        # Adicionar handlers
        if enable_console:
            self._add_console_handler()
        
        if enable_file:
            self._add_file_handler()
    
    def _get_formatter(self):
        """Retorna o formatter baseado no tipo configurado."""
        if self.format_type == 'simple':
            format_str = self.SIMPLE_FORMAT
        else:
            format_str = self.DETAILED_FORMAT
        
        return logging.Formatter(
            format_str,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    def _ensure_log_dir(self):
        """Cria o diretório de logs se não existir."""
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)
    
    def _add_console_handler(self):
        """Adiciona handler para exibição no console."""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(self._formatter)
        self.logger.addHandler(console_handler)
    
    def _add_file_handler(self):
        """Adiciona handler com rotação de arquivos."""
        self._ensure_log_dir()
        
        # Nome do arquivo com timestamp
        timestamp = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(
            self.log_dir,
            f'{self.name.lower()}_{timestamp}.log'
        )
        
        # Handler com rotação por tamanho
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(self.level)
        file_handler.setFormatter(self._formatter)
        self.logger.addHandler(file_handler)
    
    def set_level(self, level):
        """
        Altera o nível de log.

        Args:
            level (int): Nível de log (logging.DEBUG, INFO, WARNING, ERROR, CRITICAL)

        Exemplo:
            >>> logger.set_level(logging.DEBUG)
        """
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
    
    def debug(self, message, *args, **kwargs):
        """Log de nível DEBUG."""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message, *args, **kwargs):
        """Log de nível INFO."""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        """Log de nível WARNING."""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        """Log de nível ERROR."""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message, *args, **kwargs):
        """Log de nível CRITICAL."""
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message, *args, **kwargs):
        """Log de exceção com traceback."""
        self.logger.exception(message, *args, **kwargs)
    
    def get_logger(self):
        """
        Retorna a instância do logger Python.
        
        Útil para integração com outras bibliotecas.

        Returns:
            logging.Logger: Instância do logger Python
        """
        return self.logger


class LoggerFactory:
    """Factory para criar loggers pré-configurados para diferentes contextos."""
    
    _loggers = {}
    
    @staticmethod
    def get_logger(name='RPA', context=None, **kwargs):
        """
        Obtém ou cria um logger com cache.

        Args:
            name (str): Nome do logger
            context (str): Contexto de uso ('browser', 'scraping', 'automation', etc)
            **kwargs: Argumentos adicionais para RPALogger

        Returns:
            RPALogger: Instância do logger

        Exemplo:
            >>> logger = LoggerFactory.get_logger('MyBot', context='browser')
            >>> logger.info('Abrindo navegador')
        """
        logger_key = f"{name}_{context}" if context else name
        
        if logger_key not in LoggerFactory._loggers:
            LoggerFactory._loggers[logger_key] = RPALogger(name, **kwargs)
        
        return LoggerFactory._loggers[logger_key]
    
    @staticmethod
    def clear_cache():
        """Limpa o cache de loggers."""
        LoggerFactory._loggers.clear()


# Função helper para uso rápido
def get_rpa_logger(name='RPA', **kwargs):
    """
    Cria rapidamente um logger RPA.

    Args:
        name (str): Nome do logger
        **kwargs: Argumentos para RPALogger

    Returns:
        RPALogger: Instância do logger

    Exemplo:
        >>> logger = get_rpa_logger('MyProject')
        >>> logger.info('Iniciando')
    """
    return RPALogger(name, **kwargs)
