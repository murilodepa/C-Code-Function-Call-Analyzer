import os

def get_github_token():
    """
    Reads the GitHub token from a file.
    Make sure that this file is not tracked by Git.
    """
    token_file = "github_token.txt"
    
    # Check if the token file exists
    if os.path.exists(token_file):
        try:
            with open(token_file, "r") as file:
                token = file.read().strip()
                if not token:
                    raise ValueError(f"{token_file} is empty. Please add your GitHub token inside the file.")
                return token
        except (IOError, OSError) as e:
            raise IOError(f"Error reading {token_file}: {e}")
    else:
        raise FileNotFoundError(f"{token_file} not found. Please make sure it contains your GitHub token.")