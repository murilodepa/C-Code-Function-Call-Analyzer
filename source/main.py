from github_repo_search import save_links_to_file
from clone_repositories import download_repositories
from directory_manager import get_project_dirs_and_output
from program import JoernAnalyzer

def main():
    #print("Starting the process of saving GitHub repository links to a .txt file...")
    #save_links_to_file()     # Save GitHub repository links to a file
    
    print("Starting the process of downloading repositories...")
    download_repositories()     # Download repositories from GitHub

    print("Getting project directories and output CSV file path...")
    project_dirs, output_csv = get_project_dirs_and_output()     # Get project directories and CSV output path
    
    print(f"Found project directories: {project_dirs}")
    print(f"Output CSV file will be saved at: {output_csv}")
    
    print("Initializing JoernAnalyzer with the project directories...")
    analyzer = JoernAnalyzer(project_dirs, output_csv)      # Create an instance of JoernAnalyzer 
    
    print("Processing projects to generate call graphs...")
    analyzer.process_projects()     # Process all projects and generate call graphs in a single CSV file

    print("Process completed successfully!")

if __name__ == "__main__":
    main()