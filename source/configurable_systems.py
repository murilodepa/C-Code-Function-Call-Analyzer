import os
import subprocess
import csv
import sys
from pathlib import Path
from lxml import etree
from directive_extractor import DirectiveExtractor
from directory_manager import CLONED_PROJECTS_DIR, extract_relative_path

# Define a variable that stores the name of the "output" folder
OUTPUT_DIR = "output"

class SrcMLAnalyzer:
    def __init__(self, project_dirs, output_csv):
        self.project_dirs = project_dirs
        self.output_csv = output_csv

        # Ensure that the output CSV directory exists
        output_dir = os.path.dirname(self.output_csv)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        print(f"Initialized SrcMLAnalyzer with output CSV: {self.output_csv}")

    def process_projects(self):
        print(f"Processing projects and writing to {self.output_csv}")

        try:
            with open(self.output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Project", "File", "Caller", "Callee", "Conditional_Compilation"])
                print(f"CSV file initialized: {self.output_csv}")

                for project_dir in self.project_dirs:
                    project_name = os.path.basename(project_dir)
                    try:
                        self.process_project(project_dir, project_name, writer)
                    except Exception as e:
                        print(f"Error processing {project_dir}: {e}")
                        sys.exit(1)
        except IOError as e:
            print(f"Error opening/creating CSV file: {e}")
            sys.exit(1)

    def process_project(self, project_dir, project_name, writer):
        c_files = list(Path(project_dir).rglob("*.c"))
        if not c_files:
            print(f"No .c files found in project: {project_dir}")
            return

        print(f"Found {len(c_files)} .c files in project: {project_name}")

        for c_file in c_files:
            xml_output_path = os.path.join(project_dir, f"{os.path.basename(c_file)}.xml")
            self.generate_srcml(c_file, xml_output_path)
            self.extract_call_graph(xml_output_path, project_name, c_file, writer)

    def generate_srcml(self, c_file_path, xml_output_path):
        """Convert .c file to XML using srcML."""
        result = subprocess.run(['srcml', c_file_path, '-o', xml_output_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error generating XML for {c_file_path}: {result.stderr}")
            sys.exit(1)

    def extract_call_graph(self, xml_output_path, project_name, c_file, writer):
        """Extract caller-callee pairs from the srcML XML."""
        try:
            # Parse the XML with lxml
            tree = etree.parse(xml_output_path)
            root = tree.getroot()

            # Initialize DirectiveExtractor with the lxml tree
            directive_extractor = DirectiveExtractor(tree)

            namespaces = {'src': 'http://www.srcML.org/srcML/src', 'cpp': 'http://www.srcML.org/srcML/cpp'}

            for function in root.findall('.//src:function', namespaces):
                caller = function.find('src:name', namespaces).text

                for call in function.findall('.//src:call/src:name', namespaces):
                    callee = call.text

                    # Extract conditional compilation context for the call
                    conditional_info = directive_extractor.extract_conditionals(call)

                    # Write to CSV
                    writer.writerow([project_name, extract_relative_path(str(c_file)), caller, callee, conditional_info])
        except Exception as e:
            print(f"Error extracting call graph: {e}")
            sys.exit(1)



# Example usage
if __name__ == "__main__":
    # Define the directories containing C projects and the output CSV file path
    project_dirs = ['/home/lucas/Documents/call_graph_extractor/C-Code-Function-Call-Analyzer/projects/']  # Replace with actual project directory paths
    output_csv = '/home/lucas/Documents/call_graph_extractor/C-Code-Function-Call-Analyzer/output/caller_callee.csv'  # Update the path if needed

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_csv)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Initializing SrcMLAnalyzer with the specified project directories and output CSV...")
    analyzer = SrcMLAnalyzer(project_dirs, output_csv)

    print("Starting the process of analyzing projects and generating the call graph...")
    analyzer.process_projects()

    print(f"Call graph successfully generated and saved to: {output_csv}")
