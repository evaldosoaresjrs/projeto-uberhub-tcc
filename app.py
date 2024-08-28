from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def home():
    # Aqui você chama a função de scraping e passa os dados para o template
    vagas = scrape_gupy()
    return render_template('index.html', vagas=vagas)

@app.route("/test")
def teste():
    return render_template("teste.html")

def scrape_gupy():
    empresas = ["sankhya", "tribanco"]
    vagas = []
    for empresa in empresas:
        url = f'https://{empresa}.gupy.io/'
        print(empresa)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            itens = soup.find_all(attrs={"data-testid": "job-list__listitem"})


            for item in itens:
                link = item.find('a', {'data-testid': 'job-list__listitem-href'})['href']
                divs = item.find_all('div')

                if len(divs) >= 3:
                    nome_empresa = empresa.capitalize()
                    cargo_div = divs[-3].get_text(strip=True)
                    local_div = divs[-2].get_text(strip=True)
                    tipo_div = divs[-1].get_text(strip=True)

                    if 'remoto' in local_div.lower() or 'uberlândia' in local_div.lower():
                        vaga = {
                            'cargo': cargo_div,
                            'local': local_div,
                            'tipo': tipo_div,
                            'link': f'{url}{link}',
                            'nome_empresa': nome_empresa
                        }
                        vagas.append(vaga)
    return vagas

if __name__ == '__main__':
    app.run(debug=True)
