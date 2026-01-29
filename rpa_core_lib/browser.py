"""Módulo de gerenciamento de navegador Chrome com Selenium"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configurar logging
logger = logging.getLogger(__name__)


class BrowserManager:
    """Gerenciador de navegador Chrome para automação RPA."""
    
    DEFAULT_WAIT_TIME = 10  # segundos
    DEFAULT_WINDOW_SIZE = (1920, 1080)
    
    # Argumentos recomendados para RPA
    RPA_ARGS = [
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-blink-features=AutomationControlled',
        '--disable-gpu',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-popup-blocking',
    ]
    
    def __init__(self, headless=True, window_size=None, additional_args=None, 
                 wait_time=DEFAULT_WAIT_TIME, user_agent=None):
        """
        Inicializa o gerenciador de navegador Chrome.

        Args:
            headless (bool): Se True, executa em modo headless. Padrão: True
            window_size (tuple): Tamanho da janela (largura, altura). 
                               Padrão: (1920, 1080)
            additional_args (list): Argumentos adicionais para o Chrome
            wait_time (int): Tempo padrão de espera para elementos (segundos)
            user_agent (str): User Agent customizado para evitar detecção de bot

        Exemplo:
            >>> manager = BrowserManager(headless=True)
            >>> driver = manager.get_driver()
            >>> manager.close_driver()
        """
        self.headless = headless
        self.window_size = window_size or self.DEFAULT_WINDOW_SIZE
        self.wait_time = wait_time
        self.additional_args = additional_args or []
        self.user_agent = user_agent
        self.driver = None
        self.wait = None
    
    def _configure_options(self):
        """Configura as opções do Chrome."""
        chrome_options = Options()
        
        # Modo headless
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Tamanho da janela
        chrome_options.add_argument(
            f'--window-size={self.window_size[0]},{self.window_size[1]}'
        )
        
        # User Agent customizado para evitar detecção de bot
        if self.user_agent:
            chrome_options.add_argument(f'user-agent={self.user_agent}')
        else:
            # User Agent padrão que parece mais legítimo
            default_ua = (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            )
            chrome_options.add_argument(f'user-agent={default_ua}')
        
        # Adicionar argumentos recomendados para RPA
        for arg in self.RPA_ARGS:
            chrome_options.add_argument(arg)
        
        # Argumentos adicionais do usuário
        for arg in self.additional_args:
            chrome_options.add_argument(arg)
        
        return chrome_options
    
    def get_driver(self):
        """
        Obtém ou cria uma instância do driver Chrome.

        Returns:
            selenium.webdriver.Chrome: Instância do driver
        """
        if self.driver is None:
            chrome_options = self._configure_options()
            
            try:
                self.driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    options=chrome_options
                )
                self.wait = WebDriverWait(self.driver, self.wait_time)
                logger.info("Driver Chrome inicializado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao inicializar driver Chrome: {str(e)}")
                raise
        
        return self.driver
    
    def close_driver(self):
        """Fecha o driver Chrome."""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                self.wait = None
                logger.info("Driver Chrome fechado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao fechar driver: {str(e)}")
    
    def wait_element(self, locator, timeout=None):
        """
        Aguarda um elemento estar presente no DOM.

        Args:
            locator (tuple): Tupla (By.*, valor) do elemento
            timeout (int): Tempo máximo de espera em segundos. 
                          Se None, usa wait_time padrão

        Returns:
            WebElement: O elemento quando encontrado

        Exemplo:
            >>> element = manager.wait_element((By.ID, 'myElement'))
        """
        timeout = timeout or self.wait_time
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def wait_element_clickable(self, locator, timeout=None):
        """
        Aguarda um elemento estar clicável.

        Args:
            locator (tuple): Tupla (By.*, valor) do elemento
            timeout (int): Tempo máximo de espera em segundos

        Returns:
            WebElement: O elemento quando clicável
        """
        timeout = timeout or self.wait_time
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def navigate(self, url):
        """
        Navega para uma URL.

        Args:
            url (str): URL para navegar
        """
        try:
            self.driver.get(url)
            logger.info(f"Navegado para {url}")
        except Exception as e:
            logger.error(f"Erro ao navegar para {url}: {str(e)}")
            raise
    
    def get_current_url(self):
        """Retorna a URL atual."""
        return self.driver.current_url
    
    def get_page_source(self):
        """Retorna o HTML da página."""
        return self.driver.page_source


# Função legacy para compatibilidade
def open_chrome(headless=True, window_size=None, additional_args=None):
    """
    Abre uma instância do Chrome utilizando Selenium.
    
    DEPRECATED: Use BrowserManager em vez desta função.

    Args:
        headless (bool): Se True, executa em modo headless. Padrão: True
        window_size (tuple): Tamanho da janela como (largura, altura). Padrão: None
        additional_args (list): Lista de argumentos adicionais. Padrão: None

    Returns:
        selenium.webdriver.Chrome: Instância do driver Chrome

    Exemplo:
        >>> driver = open_chrome(headless=True, window_size=(1920, 1080))
        >>> driver.quit()
    """
    manager = BrowserManager(
        headless=headless,
        window_size=window_size,
        additional_args=additional_args
    )
    return manager.get_driver()
