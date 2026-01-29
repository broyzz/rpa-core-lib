"""RPA Core Library - Ferramentas para automação web com Selenium"""

__version__ = '0.1.0'
__author__ = 'Bruno Oliveira Marques'

from .browser import open_chrome, BrowserManager
from .logger import RPALogger, LoggerFactory, get_rpa_logger

__all__ = [
    'open_chrome',
    'BrowserManager',
    'RPALogger',
    'LoggerFactory',
    'get_rpa_logger',
]
