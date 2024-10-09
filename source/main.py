from clone_repositories import download_repositories
from directory_manager import get_project_dirs_and_output
from github_repo_search import save_links_to_file
from program import JoernAnalyzer

def main():
    save_links_to_file()
    download_repositories()
    project_dirs, output_csv = get_project_dirs_and_output()
    analyzer = JoernAnalyzer(project_dirs, output_csv)
    analyzer.process_projects()  # Process all projects and generate call graphs in a single CSV file

if __name__ == "__main__":
    main()