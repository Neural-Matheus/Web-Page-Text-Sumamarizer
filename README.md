# Web Page Text Summarizer and Analyzer

Este projeto utiliza Selenium e NLTK para extrair, resumir e analisar texto de páginas web. Ele acessa uma lista de URLs, extrai o conteúdo de cada página, gera um resumo e identifica os termos mais relevantes.

## Pré-requisitos

- Python 3.6 ou superior
- Bibliotecas Python: `selenium`, `nltk`, `webdriver_manager`, `collections`, `heapq`, `time`

## Instalação

1. **Clone o repositório**:
    ```sh
    https://github.com/Neural-Matheus/Web-Page-Text-Sumamarizer
    cd Web-Page-Text-Sumamarizer
    ```

2. **Instale as dependências**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Baixe os recursos do NLTK**:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    ```

## Uso

1. **Configure o WebDriver**:
    - O script usa o ChromeDriver em modo headless. Certifique-se de que o ChromeDriver está instalado e configurado corretamente.

2. **Adicione as URLs**:
    - Adicione as URLs das páginas web que você deseja processar na lista `urls` no script.

3. **Execute o script**:
    ```sh
    python main.py
    ```

4. **Verifique os resultados**:
    - Os resultados serão exibidos no console. Cada resultado inclui o URL da página, um resumo do texto e uma lista dos termos mais relevantes.

## Estrutura do Código

- `get_page_text(url)`: Extrai o texto do corpo de uma página web.
- `find_relevant_terms(text)`: Encontra os termos mais relevantes no texto, excluindo stopwords.
- `generate_summary(text, num_sentences)`: Gera um resumo do texto, baseado na frequência das palavras.
- `main()`: Função principal que realiza a extração de texto, geração de resumo e identificação de termos relevantes para cada URL na lista `urls`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT.
