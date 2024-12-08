import os
import requests
from directory_manager import REPOSITORIES
from get_github_token import get_github_token
from advanced_github_repository_search import params2

def get_repos(page=1):
    url = "https://api.github.com/search/repositories"
    headers = {"Authorization": f"token {get_github_token()}"}

    # Ajustando os parâmetros para remover filtros inválidos, como 'code_lines'
    params = params2.copy()
    params["page"] = page  # Adicionando o número da página dinamicamente

    print(f"Params: {params}")  # Log para depuração

    # Enviando a requisição para a API do GitHub
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"Successfully retrieved {len(data['items'])} repositories from page {page}.")
        return data['items']  # Retorna a lista de repositórios da página atual
    else:
        print(f"Request error: {response.status_code}. Response content: {response.text}")
        return []

def save_links_to_file(filename=REPOSITORIES):
    # Diretório atual do script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)

    page = 1
    all_repos = set()  # Conjunto para evitar duplicatas

    # Carregar links existentes para evitar duplicados
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            all_repos.update([line.strip() for line in file.readlines()])
        print(f"Loaded {len(all_repos)} existing repository links from {file_path}.")

    # Abrir o arquivo para escrita no modo de append
    with open(file_path, "a") as file:
        while True:
            repos = get_repos(page=page)
            if not repos:
                print(f"No more repositories to fetch. Stopping at page {page}.")
                break  # Saída se não houver mais repositórios

            new_links_count = 0
            for repo in repos:
                repo_url = repo['html_url']
                if repo_url not in all_repos:  # Evitar duplicação
                    file.write(repo_url + "\n")
                    all_repos.add(repo_url)
                    new_links_count += 1

            print(f"Saved {new_links_count} new repository links from page {page}.")

            if new_links_count == 0:  # Parar se não houver novos links
                print("No new repositories found. Stopping early.")
                break
            
            page += 1  # Próxima página

    print(f"Total of {len(all_repos)} unique repository links saved to {file_path}.")
