import requests
import os
from urllib.parse import urlparse
from directory_manager import CLONED_PROJECTS_DIR

def get_github_token():
    """
    Reads the GitHub token from a file.
    Make sure that this file is not tracked by Git.
    """
    token_file = "github_token.txt"
    
    # Check if the token file exists
    if os.path.exists(token_file):
        with open(token_file, "r") as file:
            token = file.read().strip()
            return token
    else:
        raise FileNotFoundError(f"{token_file} not found. Please make sure it contains your GitHub token.")

def extract_repo_info(repo_link):
    parsed_url = urlparse(repo_link)
    path = parsed_url.path.strip('/')
    parts = path.split('/')
    if len(parts) == 2:
        repo_owner = parts[0]  # First element is the owner
        repo_name = parts[1]    # Second element is the repository name
        return repo_owner, repo_name
    else:
        raise ValueError("The URL is not in the expected format.")

def get_files_from_github(repo_owner, repo_name, path="", base_path=""):
    
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    github_token = get_github_token()
    print("github_token" + github_token)
    
    headers = {
        "Authorization": f"token {github_token}"
    }
    
    response = requests.get(api_url, headers=headers)
    #response = requests.get(api_url)
    
    if response.status_code == 200:
        contents = response.json()
        
        for item in contents:
            if item['type'] == 'file' and item['name'].endswith('.c'):
                download_file(item['download_url'], base_path, item['path'])
            elif item['type'] == 'dir':
                new_path = os.path.join(base_path, item['name'])
                get_files_from_github(repo_owner, repo_name, path=item['path'], base_path=new_path)
    else:
        print(f"Erro ao acessar {api_url}. Código de status: {response.status_code}")

def download_file(file_url, base_path, original_path):
    local_file_path = os.path.join(base_path, os.path.basename(original_path))
    os.makedirs(base_path, exist_ok=True)

    try:
        response = requests.get(file_url)
        
        if response.status_code == 200:
            with open(local_file_path, 'w') as f:
                f.write(response.text)
            print(f"Arquivo {local_file_path} criado.")
        else:
            print(f"Erro ao baixar arquivo {file_url}. Código de status: {response.status_code}")
    except Exception as e:
        print(f"Ocorreu um erro ao baixar o arquivo {file_url}: {e}")

def download_repositories():
  
    # Reads the links from the txt file
    with open("repositories.txt", "r") as file:
        repos = file.readlines()

    for repo_link in repos:
        repo_link = repo_link.strip()
        try:
            repo_owner, repo_name = extract_repo_info(repo_link)
            print("repo_link: " + repo_link)
            print("repo_owner: " + repo_owner)
            print("repo_name: " + repo_name)

            # Creates a subdirectory for each repository
            repo_directory = os.path.join(CLONED_PROJECTS_DIR, repo_name)
            
            # Checks if the repository already exists
            if os.path.exists(repo_directory):
                print(f"The repository {repo_name} already exists in {repo_directory}. Skipping cloning.")
                continue
            
            get_files_from_github(repo_owner, repo_name, base_path=repo_directory)
        except ValueError as ve:
            print(f"Erro: {ve}")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

#if __name__ == "__main__":
#    download_repositories()
