"""Módulo de utilitários para manipulação de dados com Pandas em projetos RPA"""

import pandas as pd
import os
from pathlib import Path
from datetime import datetime
from typing import Union, List, Dict, Optional, Any


class DataHandler:
    """Gerenciador de dados para projetos RPA com suporte a múltiplos formatos."""
    
    SUPPORTED_FORMATS = ['csv', 'xlsx', 'json', 'parquet', 'html', 'sql']
    DEFAULT_ENCODING = 'utf-8'
    DEFAULT_OUTPUT_DIR = 'dados_exportados'
    
    def __init__(self, output_dir=None, encoding=None):
        """
        Inicializa o gerenciador de dados.

        Args:
            output_dir (str): Diretório para salvar arquivos. 
                            Padrão: 'dados_exportados'
            encoding (str): Codificação padrão dos arquivos. 
                          Padrão: 'utf-8'

        Exemplo:
            >>> handler = DataHandler()
            >>> df = handler.read_csv('dados.csv')
        """
        self.output_dir = output_dir or self.DEFAULT_OUTPUT_DIR
        self.encoding = encoding or self.DEFAULT_ENCODING
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Cria o diretório de saída se não existir."""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    # ==================== LEITURA DE DADOS ====================
    
    def read_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Lê arquivo CSV.

        Args:
            file_path (str): Caminho do arquivo CSV
            **kwargs: Argumentos adicionais para pd.read_csv()

        Returns:
            pd.DataFrame: DataFrame com os dados

        Exemplo:
            >>> df = handler.read_csv('dados.csv', sep=';')
        """
        kwargs.setdefault('encoding', self.encoding)
        return pd.read_csv(file_path, **kwargs)
    
    def read_excel(self, file_path: str, sheet_name=0, **kwargs) -> pd.DataFrame:
        """
        Lê arquivo Excel.

        Args:
            file_path (str): Caminho do arquivo Excel
            sheet_name (str|int): Nome ou índice da aba. Padrão: 0
            **kwargs: Argumentos adicionais para pd.read_excel()

        Returns:
            pd.DataFrame: DataFrame com os dados

        Exemplo:
            >>> df = handler.read_excel('dados.xlsx', sheet_name='Sheet1')
        """
        return pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
    
    def read_json(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Lê arquivo JSON.

        Args:
            file_path (str): Caminho do arquivo JSON
            **kwargs: Argumentos adicionais para pd.read_json()

        Returns:
            pd.DataFrame: DataFrame com os dados
        """
        return pd.read_json(file_path, **kwargs)
    
    def read_parquet(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Lê arquivo Parquet.

        Args:
            file_path (str): Caminho do arquivo Parquet
            **kwargs: Argumentos adicionais para pd.read_parquet()

        Returns:
            pd.DataFrame: DataFrame com os dados
        """
        return pd.read_parquet(file_path, **kwargs)
    
    def read_html(self, html_path: str, match: str = None, **kwargs) -> List[pd.DataFrame]:
        """
        Lê tabelas HTML.

        Args:
            html_path (str): Caminho do arquivo HTML ou URL
            match (str): String para match de tabelas
            **kwargs: Argumentos adicionais para pd.read_html()

        Returns:
            List[pd.DataFrame]: Lista de DataFrames encontrados

        Exemplo:
            >>> dfs = handler.read_html('table.html')
        """
        return pd.read_html(html_path, match=match, **kwargs)
    
    # ==================== ESCRITA DE DADOS ====================
    
    def save_csv(self, df: pd.DataFrame, filename: str, index=False, **kwargs) -> str:
        """
        Salva DataFrame em CSV.

        Args:
            df (pd.DataFrame): DataFrame para salvar
            filename (str): Nome do arquivo (com ou sem extensão)
            index (bool): Salvar índice. Padrão: False
            **kwargs: Argumentos adicionais para df.to_csv()

        Returns:
            str: Caminho do arquivo salvo

        Exemplo:
            >>> path = handler.save_csv(df, 'saida.csv')
        """
        filename = self._add_extension(filename, 'csv')
        file_path = os.path.join(self.output_dir, filename)
        df.to_csv(file_path, index=index, encoding=self.encoding, **kwargs)
        return file_path
    
    def save_excel(self, df: pd.DataFrame, filename: str, 
                   sheet_name='Sheet1', index=False, **kwargs) -> str:
        """
        Salva DataFrame em Excel.

        Args:
            df (pd.DataFrame): DataFrame para salvar
            filename (str): Nome do arquivo
            sheet_name (str): Nome da aba. Padrão: 'Sheet1'
            index (bool): Salvar índice. Padrão: False
            **kwargs: Argumentos adicionais para df.to_excel()

        Returns:
            str: Caminho do arquivo salvo

        Exemplo:
            >>> path = handler.save_excel(df, 'saida.xlsx')
        """
        filename = self._add_extension(filename, 'xlsx')
        file_path = os.path.join(self.output_dir, filename)
        df.to_excel(file_path, sheet_name=sheet_name, index=index, **kwargs)
        return file_path
    
    def save_json(self, df: pd.DataFrame, filename: str, 
                  orient='records', **kwargs) -> str:
        """
        Salva DataFrame em JSON.

        Args:
            df (pd.DataFrame): DataFrame para salvar
            filename (str): Nome do arquivo
            orient (str): Formato JSON. Padrão: 'records'
            **kwargs: Argumentos adicionais para df.to_json()

        Returns:
            str: Caminho do arquivo salvo

        Exemplo:
            >>> path = handler.save_json(df, 'saida.json')
        """
        filename = self._add_extension(filename, 'json')
        file_path = os.path.join(self.output_dir, filename)
        df.to_json(file_path, orient=orient, force_ascii=False, **kwargs)
        return file_path
    
    def save_parquet(self, df: pd.DataFrame, filename: str, **kwargs) -> str:
        """
        Salva DataFrame em Parquet.

        Args:
            df (pd.DataFrame): DataFrame para salvar
            filename (str): Nome do arquivo
            **kwargs: Argumentos adicionais para df.to_parquet()

        Returns:
            str: Caminho do arquivo salvo

        Exemplo:
            >>> path = handler.save_parquet(df, 'saida.parquet')
        """
        filename = self._add_extension(filename, 'parquet')
        file_path = os.path.join(self.output_dir, filename)
        df.to_parquet(file_path, **kwargs)
        return file_path
    
    def save_html(self, df: pd.DataFrame, filename: str, **kwargs) -> str:
        """
        Salva DataFrame em HTML.

        Args:
            df (pd.DataFrame): DataFrame para salvar
            filename (str): Nome do arquivo
            **kwargs: Argumentos adicionais para df.to_html()

        Returns:
            str: Caminho do arquivo salvo
        """
        filename = self._add_extension(filename, 'html')
        file_path = os.path.join(self.output_dir, filename)
        df.to_html(file_path, **kwargs)
        return file_path
    
    # ==================== TRANSFORMAÇÕES ====================
    
    def clean_columns(self, df: pd.DataFrame, lowercase=True, 
                     remove_spaces=True) -> pd.DataFrame:
        """
        Limpa os nomes das colunas.

        Args:
            df (pd.DataFrame): DataFrame para limpar
            lowercase (bool): Converter para minúsculas. Padrão: True
            remove_spaces (bool): Remover espaços. Padrão: True

        Returns:
            pd.DataFrame: DataFrame com colunas limpas

        Exemplo:
            >>> df = handler.clean_columns(df)
        """
        df = df.copy()
        
        if lowercase:
            df.columns = df.columns.str.lower()
        
        if remove_spaces:
            df.columns = df.columns.str.replace(' ', '_')
        
        return df
    
    def remove_duplicates(self, df: pd.DataFrame, subset=None, 
                         keep='first', inplace=False) -> pd.DataFrame:
        """
        Remove linhas duplicadas.

        Args:
            df (pd.DataFrame): DataFrame para processar
            subset (list): Colunas para verificar duplicatas
            keep (str): Qual duplicata manter ('first', 'last', False)
            inplace (bool): Modificar DataFrame original

        Returns:
            pd.DataFrame: DataFrame sem duplicatas

        Exemplo:
            >>> df = handler.remove_duplicates(df, subset=['id'])
        """
        return df.drop_duplicates(subset=subset, keep=keep, inplace=inplace)
    
    def fill_missing(self, df: pd.DataFrame, method='forward', 
                    fill_value=None) -> pd.DataFrame:
        """
        Preenche valores faltantes.

        Args:
            df (pd.DataFrame): DataFrame para processar
            method (str): 'forward', 'backward' ou None
            fill_value (any): Valor para preenchimento

        Returns:
            pd.DataFrame: DataFrame sem NaN

        Exemplo:
            >>> df = handler.fill_missing(df, fill_value=0)
        """
        df = df.copy()
        
        if fill_value is not None:
            df = df.fillna(fill_value)
        elif method == 'forward':
            df = df.fillna(method='ffill')
        elif method == 'backward':
            df = df.fillna(method='bfill')
        
        return df
    
    def rename_columns(self, df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Renomeia colunas usando mapa.

        Args:
            df (pd.DataFrame): DataFrame para processar
            mapping (dict): Dicionário {col_antiga: col_nova}

        Returns:
            pd.DataFrame: DataFrame com colunas renomeadas

        Exemplo:
            >>> df = handler.rename_columns(df, {'id': 'ID', 'name': 'Nome'})
        """
        return df.rename(columns=mapping)
    
    def select_columns(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Seleciona colunas específicas.

        Args:
            df (pd.DataFrame): DataFrame para processar
            columns (list): Lista de colunas para manter

        Returns:
            pd.DataFrame: DataFrame com colunas selecionadas
        """
        return df[columns]
    
    def filter_rows(self, df: pd.DataFrame, column: str, 
                   values: Union[List, Any]) -> pd.DataFrame:
        """
        Filtra linhas por valor em coluna.

        Args:
            df (pd.DataFrame): DataFrame para processar
            column (str): Nome da coluna
            values (list|any): Valor(es) para manter

        Returns:
            pd.DataFrame: DataFrame filtrado

        Example:
            >>> df = handler.filter_rows(df, 'status', ['ativo', 'pendente'])
        """
        if isinstance(values, (list, tuple)):
            return df[df[column].isin(values)]
        return df[df[column] == values]
    
    def convert_dtype(self, df: pd.DataFrame, dtype_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Converte tipos de dados de colunas.

        Args:
            df (pd.DataFrame): DataFrame para processar
            dtype_mapping (dict): Mapa {coluna: tipo}

        Returns:
            pd.DataFrame: DataFrame com tipos convertidos

        Exemplo:
            >>> df = handler.convert_dtype(df, {'idade': 'int', 'data': 'datetime64'})
        """
        df = df.copy()
        
        for column, dtype in dtype_mapping.items():
            if column in df.columns:
                try:
                    df[column] = df[column].astype(dtype)
                except Exception as e:
                    print(f"Erro ao converter {column}: {e}")
        
        return df
    
    # ==================== ANÁLISE ====================
    
    def get_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Retorna informações sobre o DataFrame.

        Args:
            df (pd.DataFrame): DataFrame para analisar

        Returns:
            dict: Dicionário com informações

        Exemplo:
            >>> info = handler.get_info(df)
        """
        return {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'missing': df.isnull().sum().to_dict(),
            'duplicates': df.duplicated().sum(),
            'memory_usage': df.memory_usage(deep=True).sum()
        }
    
    def get_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Retorna resumo estatístico do DataFrame.

        Args:
            df (pd.DataFrame): DataFrame para analisar

        Returns:
            pd.DataFrame: Resumo estatístico
        """
        return df.describe(include='all')
    
    def get_missing_info(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Retorna informações sobre valores faltantes.

        Args:
            df (pd.DataFrame): DataFrame para analisar

        Returns:
            pd.DataFrame: Informações de valores faltantes
        """
        missing = pd.DataFrame({
            'coluna': df.columns,
            'faltantes': df.isnull().sum().values,
            'percentual': (df.isnull().sum().values / len(df) * 100).round(2)
        })
        return missing[missing['faltantes'] > 0].sort_values('percentual', ascending=False)
    
    # ==================== UTILITÁRIOS ====================
    
    def _add_extension(self, filename: str, extension: str) -> str:
        """Adiciona extensão se não existir."""
        if not filename.endswith(f'.{extension}'):
            filename = f'{filename}.{extension}'
        return filename
    
    def merge_dataframes(self, df_list: List[pd.DataFrame], how='inner', 
                        on=None) -> pd.DataFrame:
        """
        Mescla múltiplos DataFrames.

        Args:
            df_list (list): Lista de DataFrames
            how (str): Tipo de merge ('inner', 'outer', 'left', 'right')
            on (str|list): Coluna(s) para merge

        Returns:
            pd.DataFrame: DataFrame mesclado
        """
        result = df_list[0]
        
        for df in df_list[1:]:
            result = pd.merge(result, df, how=how, on=on)
        
        return result
    
    def concat_dataframes(self, df_list: List[pd.DataFrame], 
                         axis=0, ignore_index=True) -> pd.DataFrame:
        """
        Concatena múltiplos DataFrames.

        Args:
            df_list (list): Lista de DataFrames
            axis (int): Eixo (0=linhas, 1=colunas)
            ignore_index (bool): Resetar índice

        Returns:
            pd.DataFrame: DataFrame concatenado
        """
        return pd.concat(df_list, axis=axis, ignore_index=ignore_index)
    
    def save_with_timestamp(self, df: pd.DataFrame, filename: str, 
                           format='csv', **kwargs) -> str:
        """
        Salva arquivo com timestamp.

        Args:
            df (pd.DataFrame): DataFrame para salvar
            filename (str): Nome do arquivo (sem extensão)
            format (str): Formato ('csv', 'xlsx', 'json', 'parquet')
            **kwargs: Argumentos adicionais

        Returns:
            str: Caminho do arquivo salvo

        Exemplo:
            >>> path = handler.save_with_timestamp(df, 'dados', format='csv')
            >>> # Salva como 'dados_20260128_143025.csv'
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename_with_ts = f'{filename}_{timestamp}'
        
        save_method = getattr(self, f'save_{format}')
        return save_method(df, filename_with_ts, **kwargs)
