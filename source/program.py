import os
import subprocess
import csv
import sys
from pathlib import Path
from lxml import etree
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
        tree = etree.parse(xml_output_path)
        root = tree.getroot()

        namespaces = {'src': 'http://www.srcML.org/srcML/src', 'cpp': 'http://www.srcML.org/srcML/cpp'}
        
        for function in root.findall('.//src:function', namespaces):
            caller = function.find('src:name', namespaces).text
            for call in function.findall('.//src:call/src:name', namespaces):
                callee = call.text
                conditional_info = self.conditional_compilation(call, namespaces)
                writer.writerow([project_name, extract_relative_path(str(c_file)), caller, callee, conditional_info])

    def conditional_compilation(self, call_node, namespaces):
        """Check if a callee is within a conditional compilation block using XPath."""
        # Using XPath to check if a call is within a conditional block
        directives = call_node.xpath("ancestor::cpp:ifdef | ancestor::cpp:ifndef | ancestor::cpp:if | ancestor::cpp:elif", namespaces=namespaces)
        
        if directives:
            # Collecting conditional directive names and values
            conditions = [directive.text for directive in directives if directive.text is not None]
            return ', '.join(conditions)
        else:
            return "TRUE"

# Example usage
# if __name__ == "__main__":
#     project_dirs = ['/home/lucas/Documents/call_graph_extractor/C-Code-Function-Call-Analyzer/source/projects/']  # Replace with actual project directory paths
#     output_csv = '/home/lucas/Documents/call_graph_extractor/C-Code-Function-Call-Analyzer/output/caller_callee.csv'
#     analyzer = SrcMLAnalyzer(project_dirs, output_csv)
#     analyzer.process_projects()
