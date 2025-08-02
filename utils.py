import pandas as pd
import ftfy
import chardet
import unicodedata

def load_and_clean_data(file_path):
    #Detect encoding
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding'] if result['encoding'] else 'utf-8'

    # Read CSV file
    try:
        df = pd.read_csv(file_path, encoding=encoding)
    except Exception:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            df = pd.read_csv(f)

    # Fix text encoding and normalize
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).apply(ftfy.fix_encoding)
        df[col] = df[col].apply(lambda x: unicodedata.normalize('NFKC', x).strip())

    # Manual fix: known garbled words
    def fix_words(text):
        return (
            text.replace('b _rek', 'börek')
                .replace('d _ner', 'döner')
                .replace('caf ', 'café')
                .replace('na ve', 'naïve')
                .replace('Bras _lia', 'Brasília')
                .replace('S  o Paulo', 'São Paulo')
                .replace('ï¿½', '')
                .replace(' ', '')
        )

    df['Cuisines'] = df['Cuisines'].apply(fix_words)
    df['Restaurant Name'] = df['Restaurant Name'].apply(fix_words)

    # Clean up
    df.dropna(subset=['Cuisines'], inplace=True)
    df['Cuisines'] = df['Cuisines'].str.lower().str.strip()

    return df
