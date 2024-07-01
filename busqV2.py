from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import download
from collections import Counter
import heapq
import time
from googlesearch import search

# Baixar recursos do NLTK
download('punkt')
download('stopwords')

# Configuração do WebDriver
options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Função para extrair texto da página
def get_page_text(url):
    driver.get(url)
    time.sleep(3)  # Espera a página carregar completamente
    body_text = driver.find_element(By.TAG_NAME, 'body').text
    return body_text

# Função para analisar o texto e encontrar os termos mais relevantes
def find_relevant_terms(text):
    # Exemplo simples: contar frequência das palavras mais comuns
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word.lower() not in stop_words]
    word_counts = Counter(filtered_words)
    return word_counts.most_common(10)  # Retorna as 10 palavras mais comuns

# Função para gerar um resumo do texto usando NLTK
def generate_summary(text, num_sentences=3):
    sentences = sent_tokenize(text)
    clean_sentences = [sentence.lower() for sentence in sentences if sentence.strip() != '']

    stop_words = set(stopwords.words('english'))
    word_freq = {}
    for sentence in clean_sentences:
        words = sentence.split()
        for word in words:
            if word not in stop_words:
                if word not in word_freq.keys():
                    word_freq[word] = 1
                else:
                    word_freq[word] += 1

    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = (word_freq[word] / max_freq)

    sent_strength = {}
    for sentence in clean_sentences:
        for word in sentence.split():
            if word in word_freq.keys():
                if len(sentence.split(' ')) < 30:
                    if sentence not in sent_strength.keys():
                        sent_strength[sentence] = word_freq[word]
                    else:
                        sent_strength[sentence] += word_freq[word]

    summary_sentences = heapq.nlargest(num_sentences, sent_strength, key=sent_strength.get)
    summary = ' '.join(summary_sentences)
    return summary

# Função principal para realizar as buscas e gerar resumos
def main(query):
    results = []
    urls = list(search(query, num_results=5))  # Busca no Google
    for url in urls:
        try:
            text = get_page_text(url)
            summary = generate_summary(text)
            relevant_terms = find_relevant_terms(text)
            results.append((url, summary, relevant_terms))
        except Exception as e:
            print(f"Erro ao processar {url}: {e}")

    return results

# Executa o script
if __name__ == "__main__":
    query = "Product Discovery"  # Palavra-chave de exemplo
    results = main(query)
    for result in results:
        print(f"URL: {result[0]}")
        print("Resumo:")
        print(result[1])
        print("Termos Relevantes:")
        for term, count in result[2]:
            print(f"- {term}: {count}")
        print("\n")

# Fecha o driver
driver.quit()
