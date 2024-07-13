import tkinter as tk
from tkinter import scrolledtext
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

def setup_driver():
    options = Options()
    options.headless = True
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_page_text(driver, url):
    try:
        driver.get(url)
        time.sleep(3)  # Espera a página carregar completamente
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        return body_text
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return ""

def find_relevant_terms(text):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word.lower() not in stop_words]
    word_counts = Counter(filtered_words)
    return word_counts.most_common(10)

def generate_summary(text, num_sentences):
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

def format_summary(summary):
    return f"Resumo:\n{summary}\n"

def format_terms(terms):
    formatted_terms = "Termos Relevantes:\n" + "\n".join(f"- {term}: {count}" for term, count in terms)
    return formatted_terms + "\n"

def format_output(url, summary, terms):
    separator = "=" * 80
    return f"{separator}\nURL: {url}\n\n{format_summary(summary)}\n{format_terms(terms)}{separator}\n"

def main(query, num_results, summary_length):
    driver = setup_driver()
    results = []
    try:
        urls = list(search(query, num_results=num_results))
        for url in urls:
            text = get_page_text(driver, url)
            if text:
                summary = generate_summary(text, summary_length)
                relevant_terms = find_relevant_terms(text)
                results.append((url, summary, relevant_terms))
    finally:
        driver.quit()

    return "\n".join(format_output(url, summary, terms) for url, summary, terms in results)

def run_search():
    query = query_entry.get()
    num_results = int(num_results_entry.get())
    summary_length = int(summary_length_entry.get())
    results = main(query, num_results, summary_length)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, results)

root = tk.Tk()
root.title("Web Text Summarizer")

tk.Label(root, text="Consulta:").pack()
query_entry = tk.Entry(root, width=50)
query_entry.pack()

tk.Label(root, text="Número de Resultados:").pack()
num_results_entry = tk.Entry(root, width=5)
num_results_entry.pack()

tk.Label(root, text="Comprimento do Resumo (sentenças):").pack()
summary_length_entry = tk.Entry(root, width=5)
summary_length_entry.pack()

search_button = tk.Button(root, text="Pesquisar e Sumarizar", command=run_search)
search_button.pack()

output_text = scrolledtext.ScrolledText(root, width=100, height=20)
output_text.pack()

root.mainloop()
