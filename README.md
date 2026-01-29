# RPA Core Library

Biblioteca Python otimizada para automação web (RPA) com Selenium. Oferece gerenciamento completo de navegador Chrome com segurança contra detecção de bot e utilitários específicos para automação.

## Instalação

### Via pip (a partir do repositório)

```bash
pip install git+https://github.com/broyzz/rpa-core-lib.git
```

### Localmente (desenvolvimento)

```bash
git clone https://github.com/broyzz/rpa-core-lib.git
cd rpa-core-lib
pip install -e .
```

## Requisitos

- Python 3.8+
- Selenium 4.0+
- ChromeDriver (será baixado automaticamente via webdriver-manager)

## Uso

### 1. Usando BrowserManager (Recomendado)

#### Inicialização Básica

```python
from rpa_core_lib.browser import BrowserManager

# Criar gerenciador
manager = BrowserManager(headless=True)

# Obter driver
driver = manager.get_driver()

# Navegar
manager.navigate('https://www.example.com')

# Fechar
manager.close_driver()
```

#### Configuração Avançada

```python
from rpa_core_lib.browser import BrowserManager

manager = BrowserManager(
    headless=True,                    # Modo headless
    window_size=(1920, 1080),         # Tamanho da janela
    wait_time=10,                     # Tempo padrão de espera (segundos)
    additional_args=['--start-maximized'],  # Argumentos customizados
    user_agent='Mozilla/5.0...'       # User Agent customizado
)

driver = manager.get_driver()
```

#### Esperando Elementos

```python
from selenium.webdriver.common.by import By

# Aguardar elemento estar presente no DOM
element = manager.wait_element((By.ID, 'my-element'))

# Aguardar elemento ficar clicável
button = manager.wait_element_clickable((By.CSS_SELECTOR, 'button.submit'))
button.click()

# Com timeout customizado
element = manager.wait_element((By.XPATH, '//div[@class="content"]'), timeout=15)
```

#### Métodos Disponíveis

```python
# Navegação
manager.navigate('https://example.com')
current_url = manager.get_current_url()

# Obter conteúdo
html = manager.get_page_source()

# Obter driver direto (para usar Selenium nativo)
driver = manager.get_driver()
driver.find_element(By.ID, 'element').send_keys('texto')

# Fechar
manager.close_driver()
```

### 2. Usando open_chrome (Legacy/Simples)

```python
from rpa_core_lib.browser import open_chrome

# Abrir Chrome em modo headless
driver = open_chrome(headless=True)

# Usar o driver normalmente
driver.get('https://www.example.com')

# Fechar o navegador
driver.quit()
```

#### Opções

```python
# Com tamanho de janela customizado
driver = open_chrome(
    headless=True, 
    window_size=(1920, 1080)
)

# Com argumentos adicionais
driver = open_chrome(
    headless=False,
    additional_args=['--start-maximized', '--disable-notifications']
)
```

## Exemplos de Casos de Uso

### Exemplo 1: Preenchimento de Formulário

```python
from rpa_core_lib.browser import BrowserManager
from selenium.webdriver.common.by import By

manager = BrowserManager(headless=True, wait_time=10)
driver = manager.get_driver()

manager.navigate('https://example.com/form')

# Preencher campos
name_field = manager.wait_element((By.ID, 'name'))
name_field.send_keys('João Silva')

email_field = driver.find_element(By.ID, 'email')
email_field.send_keys('joao@example.com')

# Clicar botão
submit_btn = manager.wait_element_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
submit_btn.click()

manager.close_driver()
```

### Exemplo 2: Web Scraping com Espera

```python
from rpa_core_lib.browser import BrowserManager
from selenium.webdriver.common.by import By

manager = BrowserManager(headless=True)
driver = manager.get_driver()

manager.navigate('https://example.com/dynamic-content')

# Aguardar conteúdo carregar dinamicamente
items = manager.wait_element((By.CLASS_NAME, 'item-list'))

# Extrair dados
html = manager.get_page_source()
# Processar HTML com BeautifulSoup, etc...

manager.close_driver()
```

### Exemplo 3: Login Automatizado

```python
from rpa_core_lib.browser import BrowserManager
from selenium.webdriver.common.by import By
import time

manager = BrowserManager(headless=False, wait_time=15)
driver = manager.get_driver()

manager.navigate('https://example.com/login')

# Preencher credenciais
username = manager.wait_element((By.ID, 'username'))
username.send_keys('seu_usuario')

password = driver.find_element(By.ID, 'password')
password.send_keys('sua_senha')

# Fazer login
login_btn = manager.wait_element_clickable((By.XPATH, '//button[@type="submit"]'))
login_btn.click()

# Aguardar redirecionamento
time.sleep(2)

# Verificar sucesso
logged_in = driver.find_elements(By.CLASS_NAME, 'user-profile')
if logged_in:
    print("Login realizado com sucesso!")

manager.close_driver()
```

### Exemplo 4: Múltiplas Abas

```python
from rpa_core_lib.browser import BrowserManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

manager = BrowserManager(headless=True)
driver = manager.get_driver()

manager.navigate('https://example.com')

# Abrir nova aba
driver.execute_script("window.open('');")

# Alternar para nova aba
driver.switch_to.window(driver.window_handles[-1])
manager.navigate('https://example2.com')

# Voltar para primeira aba
driver.switch_to.window(driver.window_handles[0])

manager.close_driver()
```

## Recursos e Destaques

✅ **BrowserManager**: Gerenciador completo com métodos auxiliares  
✅ **Detecção de Bot**: Argumentos otimizados para evitar bloqueios  
✅ **User-Agent Customizado**: Padrão legítimo para parecer navegador real  
✅ **Esperas Inteligentes**: `wait_element()` e `wait_element_clickable()`  
✅ **Logging**: Rastreamento de ações para debugging  
✅ **Compatibilidade**: Acesso ao driver Selenium nativo  
✅ **Argumentos RPA**: Pré-configurados para automação robusta  

## Argumentos do Chrome Pré-configurados

```
--no-sandbox                          # Desabilitar sandbox do Chrome
--disable-dev-shm-usage               # Melhor performance em Docker
--disable-blink-features=AutomationControlled  # Evitar detecção de bot
--disable-gpu                         # Desabilitar GPU
--no-first-run                        # Skip first-run dialogs
--no-default-browser-check            # Skip default browser check
--disable-popup-blocking              # Desabilitar bloqueio de popups
```

## Desenvolvimento

```bash
# Clonar repositório
git clone https://github.com/broyzz/rpa-core-lib.git
cd rpa-core-lib

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Ativar ambiente (Linux/Mac)
source venv/bin/activate

# Instalar em modo desenvolvimento
pip install -e .

# Instalar dependências de desenvolvimento
pip install -r requirements.txt
```

## Troubleshooting

### Chrome não encontrado
```bash
pip install --upgrade webdriver-manager
```

### Timeout em elementos
- Aumentar `wait_time` no BrowserManager
- Verificar seletor do elemento
- Considerar delays explícitos com `time.sleep()`

### Detecção de bot
- Use `BrowserManager` (já otimizado)
- Adicione delays entre ações
- Customize `user_agent` se necessário

## Licença

MIT
