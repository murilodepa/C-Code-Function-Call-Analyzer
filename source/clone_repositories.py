import requests
import os
from urllib.parse import urlparse
from directory_manager import CLONED_PROJECTS_DIR, REPOSITORIES
from get_github_token import get_github_token

def extract_repo_info(repo_link):
    parsed_url = urlparse(repo_link)
    path = parsed_url.path.strip('/')
    parts = path.split('/')
    if len(parts) == 2:
        repo_owner = parts[0]  # First element is the owner
        repo_name = parts[1]    # Second element is the repository name
        print(f"Extracted repository info - Owner: {repo_owner}, Repository: {repo_name}")
        return repo_owner, repo_name
    else:
        raise ValueError("The URL is not in the expected format.")

def get_files_from_github(repo_owner, repo_name, path="", base_path=""):
    print(f"Fetching files from GitHub repository: {repo_owner}/{repo_name}, Path: {path}")
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    github_token = get_github_token()
    
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
        print(f"Error to access {api_url}. Status code: {response.status_code}")

def download_file(file_url, base_path, original_path):
    local_file_path = os.path.join(base_path, os.path.basename(original_path))
    os.makedirs(base_path, exist_ok=True)

    try:
        response = requests.get(file_url)
        
        if response.status_code == 200:
            with open(local_file_path, 'w') as f:
                f.write(response.text)
        else:
            print(f"Error to download the file: {file_url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error to download the file: {file_url}: {e}")

def download_repositories():
  
    # Reads the links from the txt file
    with open(REPOSITORIES, "r") as file:
        repos = file.readlines()

    for repo_link in repos:
        repo_link = repo_link.strip()
        try:
            repo_owner, repo_name = extract_repo_info(repo_link)

            # Creates a subdirectory for each repository
            repo_directory = os.path.join(CLONED_PROJECTS_DIR, repo_name)
            
            # Checks if the repository already exists
            if os.path.exists(repo_directory):
                print(f"The repository {repo_name} already exists in {repo_directory}. Skipping cloning.")
                continue
            
            print(f"Creating directory for repository {repo_name} at {repo_directory}")
            get_files_from_github(repo_owner, repo_name, base_path=repo_directory)
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"Error: {e}")

#if __name__ == "__main__":
#    download_repositories()
