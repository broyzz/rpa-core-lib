"""Módulo de gerenciamento de navegador Chrome com Selenium"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def open_chrome(headless=True, window_size=None, additional_args=None):
    """
    Abre uma instância do Chrome utilizando Selenium.

    Args:
        headless (bool): Se True, executa em modo headless (sem interface gráfica).
                         Padrão: True
        window_size (tuple): Tamanho da janela como (largura, altura).
                            Exemplo: (1920, 1080)
                            Padrão: None
        additional_args (list): Lista de argumentos adicionais para o Chrome.
                               Exemplo: ['--no-sandbox', '--disable-dev-shm-usage']
                               Padrão: None

    Returns:
        selenium.webdriver.Chrome: Instância do driver Chrome configurado

    Exemplo:
        >>> driver = open_chrome(headless=True, window_size=(1920, 1080))
        >>> driver.get('https://www.example.com')
        >>> driver.quit()
    """
    
    # Configurar opções do Chrome
    chrome_options = Options()
    
    # Modo headless
    if headless:
        # Executar em modo headless (sem interface gráfica)
        chrome_options.add_argument('--headless')

    # Tamanho da janela
    if window_size:
        # Definir tamanho da janela (exemplo: 1920x1080)
        chrome_options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')

    # Argumentos adicionais
    if additional_args:
        # Adicionar argumentos adicionais para o Chrome
        for arg in additional_args:
            chrome_options.add_argument(arg)

    # Criar instância do driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    return driver
