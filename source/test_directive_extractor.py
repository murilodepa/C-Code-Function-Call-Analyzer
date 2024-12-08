import os
from directive_extractor import DirectiveExtractor

PROJECTS_PATH = "/home/lucas/Documents/call_graph_extractor/C-Code-Function-Call-Analyzer/projects"
OUTPUT_PATH = "/home/lucas/Documents/call_graph_extractor/C-Code-Function-Call-Analyzer/output_json"
TEST_FILE_NAME = "test2.c.xml"

def run_tests():
    test_file_path = os.path.join(PROJECTS_PATH, TEST_FILE_NAME)
    if not os.path.exists(test_file_path):
        raise FileNotFoundError(f"Test file not found: {test_file_path}")

    print("Running tests...")
    extractor = DirectiveExtractor(test_file_path)

    print("Generating directives list...")
    directives_path = extractor.create_list(OUTPUT_PATH)
    print(f"Directives list saved to: {directives_path}")

    print("Generating code instructions...")
    instructions_path = extractor.get_code_instructions(OUTPUT_PATH)
    print(f"Code instructions saved to: {instructions_path}")

if __name__ == "__main__":
    run_tests()
