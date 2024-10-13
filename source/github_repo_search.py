
import os
import requests
from directory_manager import REPOSITORIES
from get_github_token import get_github_token

def get_repos(language="C", stars=">10000", sort="updated", per_page=30, page=1):
    url = "https://api.github.com/search/repositories"
    headers = {"Authorization": f"token {get_github_token()}"}
    
    # Query parameters to filter repositories
    params = {
        "q": f"language:{language} stars:{stars}",
        "sort": sort,
        "order": "desc",
        "per_page": per_page,
        "page": page
    }
    
    print(f"Fetching page {page} of repositories with language '{language}' and stars '{stars}'...")
    
    # Sending request to the GitHub API
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"Successfully retrieved {len(data['items'])} repositories from page {page}.")
        
        return data['items']  # Returns the list of repositories on the current page
    else:
        print(f"Request error: {response.status_code}. Unable to fetch repositories.")
        return []

def save_links_to_file(filename=REPOSITORIES):
    # Get the current directory where the script is running
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the script directory
    file_path = os.path.join(current_dir, filename)  # Concatenates the full path to the file

    page = 1
    repos_per_page = 30  # Maximum number of repositories per page
    all_repos = set() # Using a set to avoid duplicates

    # If the file already exists, load the existing repository links to avoid duplicates
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            all_repos.update([line.strip() for line in file.readlines()])
        print(f"Loaded {len(all_repos)} existing repository links from {file_path}.")

    # Open the file for writing (append mode, to avoid overwriting if it already exists)
    with open(file_path, "a") as file:
        while True:
            repos = get_repos(page=page, per_page=repos_per_page)
            if not repos:
                print(f"No more repositories to fetch. Stopping at page {page}.")
                break  # Exit if there are no more repositories to retrieve

            new_links_count = 0
            # Writing the links to the file
            for repo in repos:

                repo_url = repo['html_url']
                if repo_url not in all_repos:  # Avoid duplicating links
                    file.write(repo_url + "\n")
                    all_repos.add(repo_url)
                    new_links_count += 1

            print(f"Saved {new_links_count} new repository links from page {page}.")

            # If no new repositories were added, the program can stop early
            if new_links_count == 0:
                print("No new repositories found. Stopping early.")
                break
            
            page += 1  # Fetch the next page

    print(f"Total of {len(all_repos)} unique repository links saved to {file_path}.")
