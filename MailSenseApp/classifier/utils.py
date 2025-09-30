import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.stem import RSLPStemmer
import os
from pypdf import PdfReader
from django.core.files.uploadedfile import UploadedFile

# Funções utilitárias para o classificador

# Definindo stopwords com a lib NLTK configurada para PT-BR
stop_words = list(nltk.corpus.stopwords.words('portuguese'))
stemmer = RSLPStemmer()

def pre_process_text(text: str) -> str:
    """
    Aplica técnicas de NLP clássico (lower, pontuação, tokenização, 
    remoção de stopwords e stemming) ao texto.
    """
    # 1. Lowercase e remoção da pontuação
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    
    # 2. Tokenização
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    
    # 3. Filtragem e Stemming
    tokens_processados = [
        stemmer.stem(word) 
        for word in tokens 
        if word not in stop_words 
        and len(word) > 1 
        and not word[0].isdigit()
    ]
    
    # 4. Reconstruindo texto (que será enviado para a IA)
    return ' '.join(tokens_processados)

def extract_text_from_file(file: UploadedFile) -> str:
    """
    Extrai o conteúdo de um arquivo UploadedFile do Django, 
    suportando .txt e .pdf.
    """
    filename, file_extension = os.path.splitext(file.name)
    file_extension = file_extension.lower()
    
    # Reinicia o ponteiro do arquivo para garantir a leitura do início
    file.seek(0) 

    if file_extension == '.txt':
        # Para TXT, basta ler e decodificar
        return file.read().decode('utf-8', errors='ignore')
    
    elif file_extension == '.pdf':
        try:
            # Para PDF, usa o pypdf
            reader = PdfReader(file)
            text = ""
            # Loop por todas as páginas do PDF
            for page in reader.pages:
                text += page.extract_text() or "" # Usa string vazia se falhar a extração
            return text
        except Exception as e:
            # Em caso de PDF corrompido ou criptografado
            return f"ERRO_LEITURA_PDF: Falha ao extrair texto do PDF: {e}"
            
    else:
        # Caso o formulário falhe na validação, ou tipo inesperado
        return "Formato de arquivo não suportado."