import os

# Constant to represent the directory name where cloned projects will be stored
BASE_DIR = os.path.abspath("..")
PROJECTS_DIR = "projects"
CLONED_PROJECTS_DIR = os.path.join(BASE_DIR, PROJECTS_DIR)
OUTPUT_DIR = "output"
OUTPUT_CSV_FILE_NAME = "function_call_graph.csv"
REPOSITORIES = "repositories.txt"

def extract_relative_path(path):
    """Extracts the path that comes after 'projects/' in the given path."""
    try:
        relative_path = path.split(PROJECTS_DIR + '/')[1]
        return relative_path
    except IndexError:
        return "The specified directory 'projects/' was not found in the path."

def get_projects_names():
    if not os.path.exists(CLONED_PROJECTS_DIR):
        print(f"Directory {CLONED_PROJECTS_DIR} does not exist.")
        return []
    folders = [f for f in os.listdir(CLONED_PROJECTS_DIR) if os.path.isdir(os.path.join(CLONED_PROJECTS_DIR, f))]
    return folders

def get_project_dirs_and_output():
    """Set up the project directories and the output CSV file path."""
    current_path = os.getcwd()

    # Get the list of project names
    project_lists = get_projects_names()

    if not project_lists:
        print("No projects found.")
        return [], None
    
    # Get the full paths for each project directory
    projects_dir = os.path.join(current_path, CLONED_PROJECTS_DIR)
    project_dirs = [os.path.join(projects_dir, project) for project in project_lists]

    # Define the output CSV file path
    output_csv = os.path.join(current_path, BASE_DIR, OUTPUT_DIR, OUTPUT_CSV_FILE_NAME)

    return project_dirs, output_csv
