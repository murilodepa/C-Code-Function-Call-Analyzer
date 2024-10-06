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
        self.project_dirs = project_dirs           # List of project directories
        self.output_csv = output_csv               # Single CSV file to store all call graphs

        # Ensure that the output CSV directory exists
        output_dir = os.path.dirname(self.output_csv)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def process_projects(self):
        """Process all projects and their .c files."""
        # Ensure the output directory exists before opening the CSV file
        output_dir = os.path.dirname(self.output_csv)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            # Open the CSV file for writing
            with open(self.output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Project", "File", "Caller", "Callee"])  # CSV headers

                for project_dir in self.project_dirs:
                    print(f"Processing project: {project_dir}")
                    self.process_project(project_dir, writer)  # Pass the writer to save directly in the CSV
        except IOError as e:
            print(f"Error opening/creating CSV file: {e}")
            sys.exit(1)

    def process_project(self, project_dir, writer):
        """Process a single project (directory) and its .c files."""
        # Find all .c files in the project's directory
        #c_files = [os.path.join(project_dir, f) for f in os.listdir(project_dir) if f.endswith(".c")]
        c_files = list(Path(project_dir).rglob("*.c"))
        if not c_files:
            print(f"No .c files found in project: {project_dir}")
            return

        project_name = os.path.basename(project_dir)

        # Process each .c file in the project
        for c_file in c_files:
            cpg_output_path = os.path.join(project_dir, f"{os.path.basename(c_file)}.cpg.bin")

            print(f"Generating CPG for {c_file}")
            self.generate_cpg(c_file, cpg_output_path)
            print(f"Extracting call graph for {c_file}")
            self.extract_call_graph(cpg_output_path, project_name, c_file, writer)

    def generate_cpg(self, c_file_path, cpg_output_path):
        """Generate the CPG file using joern-parse."""
        result = subprocess.run(
            ["joern-parse", c_file_path, "--output", cpg_output_path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error generating CPG for {c_file_path}: {result.stderr}")
            sys.exit(1)
        print(f"CPG successfully generated at: {cpg_output_path}")

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
                f.write(query_script)
        except IOError as e:
            print(f"Error writing the Scala query file: {e}")
            sys.exit(1)

        # Execute Joern via Joern-CLI
        print(f"Running the query in Joern to extract the call graph for {cpg_output_path}...")
        result = subprocess.run(
            ["joern", "--script", query_file],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error running the query for {cpg_output_path}: {result.stderr}")
            return  # Continue with the next file instead of exiting the script

        # Save the result directly in the CSV
        self._save_csv(result.stdout, project_name, c_file, writer)

    def _save_csv(self, data, project_name, c_file, writer):
        """Save the extracted call graph to the shared CSV file."""
        try:
            for line in data.splitlines():
                if "Caller:" in line:
                    caller, callee = line.replace("Caller: ", "").replace(" -> Callee: ", ",").split(",")
                    
                    print("c_file: ", c_file)
                    print("c_file type: ", type(c_file))
                    c_file_str = str(c_file)
                    
                    file = extract_relative_path(c_file_str);
                    
                    writer.writerow([project_name, file, caller, callee])
            print(f"Call graph for {c_file} saved in {self.output_csv}")
        except IOError as e:
            print(f"Error writing to CSV file: {e}")

#if __name__ == "__main__":
#    project_dirs, output_csv = get_project_dirs_and_output()
#    analyzer = JoernAnalyzer(project_dirs, output_csv)
#    analyzer.process_projects()  # Process all projects and generate call graphs in a single CSV file
