
import os
import requests
from directory_manager import REPOSITORIES
from get_github_token import get_github_token

def get_repos(language="C", stars=">10000", sort="updated", per_page=30, page=1):
    url = "https://api.github.com/search/repositories"
    headers = {"Authorization": f"token {get_github_token()}"}
    
    # Query parameters
    params = {
        "q": f"language:{language} stars:{stars}",
        "sort": sort,
        "order": "desc",
        "per_page": per_page,
        "page": page
    }
    
    # Sending request to the GitHub API
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data['items']  # Returns the list of repositories on the current page
    else:
        print(f"Request error: {response.status_code}")
        return []

def save_links_to_file(filename=REPOSITORIES):
    # Ensures the file is saved in the directory where the script is running
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the script directory
    file_path = os.path.join(current_dir, filename)  # Concatenates the full path to the file

    page = 1
    repos_per_page = 30  # Maximum number of repositories per page
    all_repos = []

    # Open the file for writing (append mode, to avoid overwriting if it already exists)
    with open(file_path, "a") as file:
        while True:
            repos = get_repos(page=page, per_page=repos_per_page)
            if not repos:
                break  # Exit if there are no more repositories to retrieve

            # Writing the links to the file
            for repo in repos:
                file.write(repo['html_url'] + "\n")
                all_repos.append(repo['html_url'])
            
            page += 1  # Next page

    print(f"Total of {len(all_repos)} repository links saved to {file_path}")
