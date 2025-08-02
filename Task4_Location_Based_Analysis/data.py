# data_loader.py
import pandas as pd
import chardet
import ftfy
import unicodedata

def fix_words(text):
    return (
        text
        .replace('Bras _lia', 'Brasília')
        .replace('S  o Paulo', 'São Paulo')
        .replace('  stanbul', 'İstanbul')
        .replace(' ', '')
    )

def load_data(file_path="Dataset .csv"):
    # Detect encoding
    with open(file_path, 'rb') as f:
        encoding = chardet.detect(f.read())['encoding'] or 'utf-8'

    df = pd.read_csv(file_path, encoding=encoding)
    df = df.dropna(subset=['Latitude', 'Longitude'])

    # Fix encoding issues
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).apply(ftfy.fix_encoding)
        df[col] = df[col].apply(lambda x: unicodedata.normalize('NFKC', x).strip())
        df[col] = df[col].apply(fix_words)

    df['Latitude'] = df['Latitude'].astype(float)
    df['Longitude'] = df['Longitude'].astype(float)
    df['Cuisines'] = df['Cuisines'].str.lower().str.strip()

    return df
