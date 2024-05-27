import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import re
from io import StringIO
from dateutil.parser import parse
from pathlib import Path

def fetch_wikipedia_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_table(html_content):
    """
    Args:
        html_content: html contents extract from the url

    Returns:
       table_html: html lines that contains the table class
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table', {'class': 'wikitable'})
    
    if not tables:
        raise ValueError("No tables found on the page.")
    
    for table in tables:
        for row in table.find_all('tr'):
            for cell in row.find_all(['td', 'th']):
                for sup in cell.find_all('sup'):
                    sup.decompose()
    
    return tables

def parse_table(table):
    table_html = str(table)
    df = pd.read_html(StringIO(table_html))[0]
    return df

def is_date(list_val : pd.core.series.Series):
    """
    Args:
        list_val (pd.core.series.Series): pandas column to be checked if this column contains date value or not

    Returns:
        boolean: True / False
    """
    for i in range(len(list_val)):
        try:
            parse(list_val[i])
            return True
        except (ValueError, TypeError):
            return False
        
def convert_to_numeric(value):
    match = re.search(r'(\d+(\.\d+)?)', value)
    if match:
        return float(match.group(1))
    return None

def identify_numeric_column(df):
    numeric_columns = []
    for column in df.columns:
        try:
            if not is_date(df[column]):
                df[column] = df[column].apply(convert_to_numeric)
                if df[column].dropna().apply(lambda x: isinstance(x, (int, float))).all() and not df[column].isnull().all():
                    numeric_columns.append(column)
        except Exception as e:
            continue
    
    if not numeric_columns:
        raise ValueError("No numeric columns found in the table.")
    
    return numeric_columns

def plot_numeric_column(df, numeric_column):
    plt.figure(figsize=(10, 5))
    rootpath = f"{Path(__file__).parent}\output"
    for col in numeric_column:
        df[col].plot(kind='line', marker='o')
        plt.title(f"Plot of {col}")
        plt.xlabel('Index')
        plt.ylabel(col)
        plt.grid(True)
        plt.savefig(f'{rootpath}\output_plot_{col}.png')

def main(url):
    html_content = fetch_wikipedia_page(url)
    tables = extract_table(html_content)
    for i in range(len(tables)):
        table = tables[i]
        df = parse_table(table)
        numeric_column = identify_numeric_column(df)
        plot_numeric_column(df, numeric_column)
    
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Women%27s_high_jump_world_record_progression"
    main(url)