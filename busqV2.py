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

# Função para configurar o WebDriver
def setup_driver():
    options = Options()
    options.headless = True
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Função para extrair texto da página
def get_page_text(driver, url):
    try:
        driver.get(url)
        time.sleep(3)  # Espera a página carregar completamente
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        return body_text
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return ""

# Função para analisar o texto e encontrar os termos mais relevantes
def find_relevant_terms(text):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word.lower() not in stop_words]
    word_counts = Counter(filtered_words)
    return word_counts.most_common(10)

# Função para gerar um resumo do texto usando NLTK
def generate_summary(text, num_sentences=3):
    sentences = sent_tokenize(text)
    clean_sentences = [sentence.lower() for sentence in sentences if sentence.strip() != '']

    stop_words = set(stopwords.words('english'))
    word_freq = Counter(word for sentence in clean_sentences for word in sentence.split() if word not in stop_words)

    max_freq = max(word_freq.values(), default=1)
    for word in word_freq:
        word_freq[word] /= max_freq

    sent_strength = {sentence: sum(word_freq.get(word, 0) for word in sentence.split()) / len(sentence.split()) for sentence in clean_sentences}

    summary_sentences = heapq.nlargest(num_sentences, sent_strength, key=sent_strength.get)
    summary = ' '.join(summary_sentences)
    return summary

# Função principal para realizar as buscas e gerar resumos
def main(query):
    driver = setup_driver()
    try:
        results = []
        urls = list(search(query, num_results=5))  # Busca no Google
        for url in urls:
            text = get_page_text(driver, url)
            if text:
                summary = generate_summary(text)
                relevant_terms = find_relevant_terms(text)
                results.append((url, summary, relevant_terms))
        return results
    finally:
        driver.quit()

# Executa o script
if __name__ == "__main__":
    query = "Product Discovery"
    results = main(query)
    for result in results:
        print(f"URL: {result[0]}\nResumo:\n{result[1]}\nTermos Relevantes:")
        for term, count in result[2]:
            print(f"- {term}: {count}")
        print("\n")