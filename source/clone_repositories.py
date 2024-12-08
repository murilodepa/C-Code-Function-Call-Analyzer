import requests
import os
import time
from datetime import datetime, timezone  # Ensure timezone is imported
from urllib.parse import urlparse
from directory_manager import CLONED_PROJECTS_DIR, REPOSITORIES
from get_github_token import get_github_token
from email_notifier import send_email  # Import the email notifier
import math

BASE_API_URL = "https://api.github.com/repos"

def check_rate_limit():
    """Check the remaining GitHub API rate limit and pause if necessary."""
    github_token = get_github_token()
    headers = {"Authorization": f"token {github_token}"}
    api_url = "https://api.github.com/rate_limit"
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            rate_limit = response.json()
            remaining = rate_limit['rate']['remaining']
            reset_time = rate_limit['rate']['reset']
            
            if remaining == 0:
                current_time = int(time.time())
                wait_time = max(0, reset_time - current_time)  # Ensure non-negative wait time
                wait_minutes = math.ceil(wait_time / 60)  # Convert to minutes for readability
                reset_timestamp = datetime.fromtimestamp(reset_time, tz=timezone.utc)
                
                print(
                    f"[Rate Limit] GitHub API limit reached. "
                    f"Reset expected at {reset_timestamp} "
                    f"(in {wait_minutes} minute(s), {wait_time} second(s))."
                )

                time.sleep(wait_time)  # Wait for the calculated time
        else:
            print(f"[Error] Failed to check rate limit. Status code: {response.status_code}. Retrying after 60 seconds.")
            time.sleep(60)  # Safe fallback wait
    except requests.RequestException as e:
        print(f"[Critical] Network error while checking rate limit: {e}. Retrying after 120 seconds.")
        time.sleep(120)  # Safe fallback wait

def extract_repo_info(repo_link):
    """Extract repository owner and name from the repository URL."""
    parsed_url = urlparse(repo_link)
    path = parsed_url.path.strip('/')
    parts = path.split('/')
    if len(parts) == 2:
        repo_owner, repo_name = parts[0], parts[1]
        print(f"Extracted repository info - Owner: {repo_owner}, Repository: {repo_name}")
        return repo_owner, repo_name
    else:
        raise ValueError("The URL is not in the expected format.")

def get_files_from_github(repo_owner, repo_name, path="", base_path=""):
    """Fetch and download files from a GitHub repository."""
    print(f"Fetching files from GitHub repository: {repo_owner}/{repo_name}, Path: {path}")
    api_url = f"{BASE_API_URL}/{repo_owner}/{repo_name}/contents/{path}"
    github_token = get_github_token()
    
    headers = {"Authorization": f"token {github_token}"}
    check_rate_limit()  # Check and handle rate limits before making the API call

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item['type'] == 'file' and item['name'].endswith('.c'):
                download_file(item['download_url'], base_path, item['path'])
            elif item['type'] == 'dir':
                new_path = os.path.join(base_path, item['name'])
                get_files_from_github(repo_owner, repo_name, path=item['path'], base_path=new_path)
    elif response.status_code == 403:
        print("Rate limit exceeded. Pausing and retrying...")
        check_rate_limit()  # Handle rate limit and retry
        get_files_from_github(repo_owner, repo_name, path, base_path)
    else:
        print(f"Error accessing {api_url}. Status code: {response.status_code}")

def download_file(file_url, base_path, original_path):
    """Download a single file from a GitHub repository."""
    local_file_path = os.path.join(base_path, os.path.basename(original_path))
    os.makedirs(base_path, exist_ok=True)

    if os.path.exists(local_file_path):
        print(f"File {local_file_path} already exists. Skipping download.")
        return

    try:
        response = requests.get(file_url)
        check_rate_limit()  # Check rate limits before downloading
        if response.status_code == 200:
            with open(local_file_path, 'w') as f:
                f.write(response.text)
            print(f"File downloaded: {local_file_path}")
        else:
            print(f"Error downloading file: {file_url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading file: {file_url}: {e}")

def download_repositories():
    """Download all repositories listed in the text file."""
    errors = []  # Track errors to include in email notifications
    with open(REPOSITORIES, "r") as file:
        repos = file.readlines()

    for repo_link in repos:
        repo_link = repo_link.strip()
        try:
            repo_owner, repo_name = extract_repo_info(repo_link)

            # Create a directory for the repository
            repo_directory = os.path.join(CLONED_PROJECTS_DIR, repo_name)
            if os.path.exists(repo_directory):
                print(f"The repository {repo_name} already exists in {repo_directory}. Skipping cloning.")
                continue

            print(f"Creating directory for repository {repo_name} at {repo_directory}")
            os.makedirs(repo_directory, exist_ok=True)

            # Fetch repository files
            get_files_from_github(repo_owner, repo_name, base_path=repo_directory)
        except ValueError as ve:
            errors.append(f"Error: {ve}")
            print(f"Error: {ve}")
        except Exception as e:
            errors.append(f"Unexpected error: {e}")
            print(f"Unexpected error: {e}")

    # Send email notification
    if errors:
        send_email("Repository Cloning Errors", "\n".join(errors))
    else:
        send_email("Repository Cloning Completed", "All repositories were successfully cloned.")

# if __name__ == "__main__":
#     download_repositories()
