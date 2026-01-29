# RPA Core Library

Biblioteca Python otimizada para automação web (RPA) com Selenium. Oferece gerenciamento completo de navegador Chrome, logging avançado e manipulação de dados com Pandas.

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
- Pandas 1.3.0+
- ChromeDriver (será baixado automaticamente via webdriver-manager)

## Módulos Disponíveis

A biblioteca contém 3 módulos principais:

1. **BrowserManager** - Gerenciamento de navegador Chrome
2. **RPALogger** - Sistema de logging avançado
3. **DataHandler** - Manipulação de dados com Pandas

---

## 1️⃣ Módulo: BrowserManager

Gerenciador completo do navegador Chrome com otimizações para RPA.

### Inicialização Básica

```python
from rpa_core_lib import BrowserManager

manager = BrowserManager(headless=True)
driver = manager.get_driver()
manager.navigate('https://www.example.com')
manager.close_driver()
```

### Configuração Completa

```python
from rpa_core_lib import BrowserManager

manager = BrowserManager(
    headless=True,
    window_size=(1920, 1080),
    wait_time=10,
    additional_args=['--start-maximized'],
    user_agent='Mozilla/5.0...'
)
driver = manager.get_driver()
```

### Esperando Elementos

```python
from selenium.webdriver.common.by import By

# Aguardar elemento estar presente
element = manager.wait_element((By.ID, 'my-element'))

# Aguardar elemento ficar clicável
button = manager.wait_element_clickable((By.CSS_SELECTOR, 'button.submit'))
button.click()

# Com timeout customizado
element = manager.wait_element((By.XPATH, '//div[@class="content"]'), timeout=15)
```

### Navegação e Conteúdo

```python
# Navegar
manager.navigate('https://example.com')

# Obter URL atual
current_url = manager.get_current_url()

# Obter HTML da página
html_content = manager.get_page_source()

# Acessar driver nativo do Selenium
driver = manager.get_driver()
driver.find_element(By.ID, 'element').send_keys('texto')

# Fechar
manager.close_driver()
```

### Exemplo Completo: Scraping com Espera

```python
from rpa_core_lib import BrowserManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

manager = BrowserManager(headless=True, wait_time=10)
driver = manager.get_driver()

# Navegar e aguardar conteúdo
manager.navigate('https://example.com/products')
products = manager.wait_element((By.CLASS_NAME, 'product-list'))

# Extrair dados
html = manager.get_page_source()
soup = BeautifulSoup(html, 'html.parser')
product_names = [p.text for p in soup.find_all(class_='product-name')]

print(product_names)
manager.close_driver()
```

---

## 2️⃣ Módulo: RPALogger

Sistema de logging avançado com rotação de arquivos e múltiplos formatos.

### Uso Rápido

```python
from rpa_core_lib import get_rpa_logger

logger = get_rpa_logger('MyBot')
logger.info('Iniciando automação')
logger.warning('Algo aconteceu')
logger.error('Erro encontrado')
logger.critical('Erro crítico!')
```

### Configuração Customizada

```python
from rpa_core_lib import RPALogger
import logging

logger = RPALogger(
    name='RPA_Bot',
    log_dir='meus_logs',
    level=logging.DEBUG,
    format_type='detailed',  # 'simple' ou 'detailed'
    max_bytes=5 * 1024 * 1024,  # 5 MB
    backup_count=10
)

logger.debug('Informação de debug')
logger.info('Processo iniciado')
```

### Usar Factory com Cache

```python
from rpa_core_lib import LoggerFactory

# Primeira chamada cria o logger
logger1 = LoggerFactory.get_logger('MyApp', context='browser')

# Segunda chamada reutiliza a mesma instância
logger2 = LoggerFactory.get_logger('MyApp', context='browser')

logger1.info('Mesmo logger')
```

### Alterar Nível de Log

```python
import logging
from rpa_core_lib import get_rpa_logger

logger = get_rpa_logger('MyBot')

# Aumentar verbosidade
logger.set_level(logging.DEBUG)
logger.debug('Agora mostra messages de debug')

# Reduzir verbosidade
logger.set_level(logging.ERROR)
logger.warning('Isso não será exibido')
```

### Log de Exceções

```python
from rpa_core_lib import get_rpa_logger

logger = get_rpa_logger('MyBot')

try:
    result = 10 / 0
except Exception as e:
    # Registra a exceção com traceback
    logger.exception('Erro ao executar cálculo')
```

### Exemplo Completo: Automação com Logging

```python
from rpa_core_lib import BrowserManager, get_rpa_logger
from selenium.webdriver.common.by import By

logger = get_rpa_logger('LoginBot', log_dir='logs')
manager = BrowserManager(headless=True)

try:
    logger.info('Abrindo navegador')
    driver = manager.get_driver()
    
    logger.info('Navegando para login')
    manager.navigate('https://example.com/login')
    
    logger.info('Preenchendo credenciais')
    username = manager.wait_element((By.ID, 'username'))
    username.send_keys('user@example.com')
    
    password = driver.find_element(By.ID, 'password')
    password.send_keys('senha123')
    
    logger.info('Enviando formulário')
    submit = manager.wait_element_clickable((By.XPATH, '//button[@type="submit"]'))
    submit.click()
    
    logger.info('Login realizado com sucesso!')
    
except Exception as e:
    logger.exception('Erro durante login')
    
finally:
    logger.info('Encerrando navegador')
    manager.close_driver()
```

---

## 3️⃣ Módulo: DataHandler

Gerenciador de dados com Pandas para leitura, escrita e transformação de dados.

### Leitura de Dados

```python
from rpa_core_lib import DataHandler

handler = DataHandler(output_dir='dados')

# Ler CSV
df = handler.read_csv('entrada.csv')

# Ler Excel
df = handler.read_excel('dados.xlsx', sheet_name='Sheet1')

# Ler JSON
df = handler.read_json('dados.json')

# Ler Parquet
df = handler.read_parquet('dados.parquet')

# Ler HTML
dfs = handler.read_html('tabela.html')
```

### Escrita de Dados

```python
from rpa_core_lib import DataHandler
import pandas as pd

handler = DataHandler(output_dir='dados')
df = pd.DataFrame({'nome': ['João', 'Maria'], 'idade': [30, 25]})

# Salvar em diferentes formatos
handler.save_csv(df, 'saida.csv')
handler.save_excel(df, 'saida.xlsx')
handler.save_json(df, 'saida.json')
handler.save_parquet(df, 'saida.parquet')
handler.save_html(df, 'saida.html')

# Salvar com timestamp automático
path = handler.save_with_timestamp(df, 'backup', format='csv')
# Resultado: dados/backup_20260128_143025.csv
```

### Limpeza de Dados

```python
# Limpar nomes de colunas
df = handler.clean_columns(df)  # minúsculas e sem espaços
# "User Name" -> "user_name"

# Remover duplicatas
df = handler.remove_duplicates(df, subset=['id'])

# Preencher valores faltantes
df = handler.fill_missing(df, fill_value=0)
df = handler.fill_missing(df, method='forward')

# Renomear colunas
df = handler.rename_columns(df, {'id': 'ID', 'name': 'Nome'})
```

### Seleção e Filtro

```python
# Selecionar colunas específicas
df = handler.select_columns(df, ['id', 'nome', 'email'])

# Filtrar por valor único
df = handler.filter_rows(df, 'status', 'ativo')

# Filtrar por múltiplos valores
df = handler.filter_rows(df, 'status', ['ativo', 'pendente'])

# Filtrar por condição customizada
df_filtered = df[df['idade'] > 25]
```

### Conversão de Tipos

```python
# Converter tipos de dados
df = handler.convert_dtype(df, {
    'idade': 'int',
    'data': 'datetime64',
    'ativo': 'bool',
    'preço': 'float'
})
```

### Análise de Dados

```python
# Informações gerais
info = handler.get_info(df)
# {'shape': (100, 5), 'columns': [...], 'dtypes': {...}, ...}

# Resumo estatístico
summary = handler.get_summary(df)

# Valores faltantes
missing = handler.get_missing_info(df)
# DataFrame com coluna, quantidade e percentual de valores faltantes
```

### Merge e Concatenação

```python
# Mesclar DataFrames
df_merged = handler.merge_dataframes([df1, df2], how='inner', on='id')

# Concatenar DataFrames
df_concat = handler.concat_dataframes([df1, df2, df3])
```

### Exemplo Completo: ETL com DataHandler

```python
from rpa_core_lib import DataHandler, BrowserManager, get_rpa_logger
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

logger = get_rpa_logger('ETLBot')
handler = DataHandler(output_dir='dados')
manager = BrowserManager(headless=True)

try:
    # EXTRACT - Coletar dados da web
    logger.info('Coletando dados da web')
    driver = manager.get_driver()
    manager.navigate('https://example.com/products')
    products = manager.wait_element((By.CLASS_NAME, 'product-list'))
    html = manager.get_page_source()
    
    # TRANSFORM - Processar dados
    logger.info('Processando dados')
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    
    for product in soup.find_all(class_='product'):
        data.append({
            'nome': product.find(class_='name').text,
            'preço': float(product.find(class_='price').text.replace('R$', '').strip()),
            'disponível': 'estoque' in product.get('class', [])
        })
    
    import pandas as pd
    df = pd.DataFrame(data)
    
    # TRANSFORM - Limpar dados
    logger.info('Limpando dados')
    df = handler.clean_columns(df)
    df = handler.remove_duplicates(df, subset=['nome'])
    df = df[df['preço'] > 0]  # Remover produtos inválidos
    
    # LOAD - Salvar dados
    logger.info('Salvando dados')
    handler.save_csv(df, 'produtos.csv')
    handler.save_excel(df, 'produtos.xlsx')
    handler.save_with_timestamp(df, 'backup', format='parquet')
    
    # ANALYZE - Analisar
    logger.info('Resumo dos dados:')
    logger.info(f'Total de produtos: {len(df)}')
    logger.info(f'Preço médio: R$ {df["preço"].mean():.2f}')
    
    logger.info('ETL concluído com sucesso!')
    
except Exception as e:
    logger.exception('Erro durante ETL')
    
finally:
    manager.close_driver()
```

---

## 📋 Resumo de Funcionalidades

### BrowserManager
| Método | Descrição |
|--------|-----------|
| `get_driver()` | Obtém instância do driver Chrome |
| `navigate(url)` | Navega para uma URL |
| `wait_element(locator)` | Aguarda elemento estar presente |
| `wait_element_clickable(locator)` | Aguarda elemento ficar clicável |
| `get_current_url()` | Retorna URL atual |
| `get_page_source()` | Retorna HTML da página |
| `close_driver()` | Fecha o navegador |

### RPALogger
| Método | Descrição |
|--------|-----------|
| `debug(msg)` | Log de debug |
| `info(msg)` | Log de informação |
| `warning(msg)` | Log de aviso |
| `error(msg)` | Log de erro |
| `critical(msg)` | Log crítico |
| `exception(msg)` | Log com traceback |
| `set_level(level)` | Altera nível de log |

### DataHandler
| Método | Descrição |
|--------|-----------|
| `read_csv()` | Lê arquivo CSV |
| `read_excel()` | Lê arquivo Excel |
| `read_json()` | Lê arquivo JSON |
| `read_parquet()` | Lê arquivo Parquet |
| `save_csv()` | Salva em CSV |
| `save_excel()` | Salva em Excel |
| `clean_columns()` | Limpa nomes de colunas |
| `remove_duplicates()` | Remove duplicatas |
| `fill_missing()` | Preenche valores faltantes |
| `filter_rows()` | Filtra linhas |
| `get_info()` | Informações do DataFrame |
| `get_summary()` | Resumo estatístico |
| `merge_dataframes()` | Mescla DataFrames |
| `concat_dataframes()` | Concatena DataFrames |

---

## 🔧 Desenvolvimento

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

# Instalar dependências
pip install -r requirements.txt
```

---

## 🐛 Troubleshooting

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

### Erro ao ler/escrever arquivos
- Verificar se o caminho do arquivo está correto
- Para Excel, instalar `openpyxl`: `pip install openpyxl`
- Para Parquet, instalar `pyarrow`: `pip install pyarrow`

---

## 📄 Licença

MIT
