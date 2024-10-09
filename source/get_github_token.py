import os

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