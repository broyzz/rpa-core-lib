# RPA Core Library

Biblioteca Python para automação web com Selenium.

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

## Uso

```python
from rpa_core_lib.browser import open_chrome

# Abrir Chrome em modo headless
driver = open_chrome(headless=True)

# Usar o driver
driver.get('https://www.example.com')

# Fechar o navegador
driver.quit()
```

## Recursos

- `open_chrome()`: Abre uma instância do Chrome com Selenium

## Requisitos

- Python 3.8+
- Selenium 4.0+
- ChromeDriver (será baixado automaticamente via webdriver-manager)

## Desenvolvimento

```bash
# Clonar repositório
git clone https://github.com/broyzz/rpa-core-lib.git
cd rpa-core-lib

# Instalar em modo desenvolvimento
pip install -e .

# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt
```

## Licença

MIT
