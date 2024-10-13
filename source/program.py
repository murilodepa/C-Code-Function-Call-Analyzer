import os
import subprocess
import csv
import sys
from pathlib import Path
from directory_manager import CLONED_PROJECTS_DIR, extract_relative_path

# Define a variable that stores the name of the "output" folder
OUTPUT_DIR = "output"

class JoernAnalyzer:
    def __init__(self, project_dirs, output_csv):
        # Initialize the class with the list of project directories and the output CSV file path
        self.project_dirs = project_dirs           # List of project directories
        self.output_csv = output_csv               # Single CSV file to store all call graphs

        # Ensure that the output CSV directory exists
        output_dir = os.path.dirname(self.output_csv)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        print(f"Initialized JoernAnalyzer with output CSV: {self.output_csv}")

    def process_projects(self):
        """Process all projects and their .c files."""
        # Ensure the output directory exists before opening the CSV file
        output_dir = os.path.dirname(self.output_csv)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        print(f"Processing projects. Output CSV directory: {output_dir}")

        try:
            # Open the CSV file for writing
            with open(self.output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                # Write the CSV headers for the call graph
                writer.writerow(["Project", "File", "Caller", "Callee"])  # CSV headers
                print(f"CSV file initialized: {self.output_csv}")

                # Process each project directory provided
                for project_dir in self.project_dirs:
                    try:
                        self.process_project(project_dir, writer)  # Pass the writer to save directly in the CSV
                    except MemoryError as e:
                        print(f"MemoryError encountered while processing {project_dir}: {e}")
                        sys.exit(1)  # Exit the program if there's a memory error
                    except Exception as e:
                        print(f"An unexpected error occurred while processing {project_dir}: {e}")
                        sys.exit(1)  # Exit the program for other errors
        except IOError as e:
            print(f"Error opening/creating CSV file: {e}")
            sys.exit(1) # Exit the program if the CSV can't be opened

    def process_project(self, project_dir, writer):
        """Process a single project (directory) and its .c files."""
        # Find all .c files in the project directory (including subdirectories)
        c_files = list(Path(project_dir).rglob("*.c"))
        if not c_files:
            print(f"No .c files found in project: {project_dir}")
            return

        project_name = os.path.basename(project_dir)
        print(f"Found {len(c_files)} .c files in project: {project_name}")
        print(f"Processing project: '{project_dir}'...")

        total_files = len(c_files)  # Total number of .c files
        twenty_five_percent = total_files * 25 // 100  # 25% of total files
        fifty_percent = total_files * 50 // 100        # 50% of total files
        seventy_five_percent = total_files * 75 // 100  # 75% of total files
        ninety_percent = total_files * 90 // 100        # 90% of total files

        processed_files = 0  # Initialize a counter for processed files

        # Process each .c file in the project
        for c_file in c_files:
            # Generate output path for the CPG (Code Property Graph) file
            cpg_output_path = os.path.join(project_dir, f"{os.path.basename(c_file)}.cpg.bin")

            # Generate the CPG file and extract the call graph
            self.generate_cpg(c_file, cpg_output_path)
            self.extract_call_graph(cpg_output_path, project_name, c_file, writer)

            # Increment the processed files counter
            processed_files += 1

            # Check for processing milestones
            if processed_files == twenty_five_percent:
                print(f"Processed 25% of the .c files in project: {project_name}")
            elif processed_files == fifty_percent:
                print(f"Processed 50% of the .c files in project: {project_name}")
            elif processed_files == seventy_five_percent:
                print(f"Processed 75% of the .c files in project: {project_name}")
            elif processed_files == ninety_percent:
                print(f"Processed 90% of the .c files in project: {project_name}")

    def generate_cpg(self, c_file_path, cpg_output_path):
        """Generate the CPG file using joern-parse."""
        # Set the heap size using JAVA_OPTS environment variable
        env = os.environ.copy()  # Copiar o ambiente atual
        env['JOERN_HEAP_SIZE'] = "8G"  # Configurar o tamanho da heap do Joern para 4G
        env['JAVA_OPTS'] = "-Xmx8g -Xms4g"  # Configurar a heap inicial e máxima para o Java

        # Run the 'joern-parse' command to create the CPG file for the .c file
        result = subprocess.run(
            ["joern-parse", c_file_path, "--output", cpg_output_path],
            capture_output=True, text=True, env=env
        )
        if result.returncode != 0:
            print(f"Error generating CPG for {c_file_path}: {result.stderr}")
            sys.exit(1)

    def extract_call_graph(self, cpg_output_path, project_name, c_file, writer):
        """Extract the call graph and save it directly to the CSV."""
        # Scala query script to extract the call graph
        query_script = f"""
        importCpg("{cpg_output_path}")
        val edges = cpg.call
        .filterNot(_.name.startsWith("<operator>")) // Ignore operators if necessary
        .map {{ call =>
        val caller = call.method.fullName       // Full name of the calling function
        val callee = call.name                  // Name of the called function
        (caller, callee)                        // Return the tuple (caller, callee)
        }}.l

        // Print each edge in the call graph
        edges.foreach {{ case (caller, callee) =>
        println(s"Caller: $caller -> Callee: $callee")  
        }}
        """

        # Save the Scala query to a temporary file
        query_file = "call_graph_query.sc"
        try:
            with open(query_file, "w", encoding="utf-8") as f:
                # Write the query to a file
                f.write(query_script)
        except IOError as e:
            print(f"Error writing the Scala query file: {e}")
            sys.exit(1)

        # Execute Joern via Joern-CLI
        result = subprocess.run(
            ["joern", "--script", query_file],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error running the query for {cpg_output_path}: {result.stderr}")
            return  # Continue with the next file instead of exiting the script

        # Save the result of the call graph extraction directly in the CSV
        self._save_csv(result.stdout, project_name, c_file, writer)

    def _save_csv(self, data, project_name, c_file, writer):
        """Save the extracted call graph to the shared CSV file."""
        try:
            # Parse each line of the output and extract caller and callee functions
            for line in data.splitlines():
                if "Caller:" in line:
                    # Replace "Caller:" and " -> Callee:" to get the caller and callee functions
                    caller, callee = line.replace("Caller: ", "").replace(" -> Callee: ", ",").split(",")
                    c_file_str = str(c_file)
                    
                    # Get the relative path for the file
                    file = extract_relative_path(c_file_str);
                    
                    # Write the project, file, caller, and callee to the CSV file
                    writer.writerow([project_name, file, caller, callee])
        except IOError as e:
            print(f"Error writing to CSV file: {e}") # Handle potential errors during CSV writing

#if __name__ == "__main__":
#    project_dirs, output_csv = get_project_dirs_and_output()
#    analyzer = JoernAnalyzer(project_dirs, output_csv)
#    analyzer.process_projects()  # Process all projects and generate call graphs in a single CSV file
