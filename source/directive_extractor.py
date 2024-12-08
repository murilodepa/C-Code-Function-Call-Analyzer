import os
import json
from bs4 import BeautifulSoup


class DirectiveExtractor:
    def __init__(self, file_path):
        """Initialize with file path."""
        self.file_path = file_path
        self.all_directives = []
        self.all_conditionals = {}

    def initialize(self):
        """Reset all internal state."""
        self.all_directives = []
        self.all_conditionals = {}

    def parse_file(self):
        """Parse the XML file and initialize BeautifulSoup."""
        try:
            with open(self.file_path, 'r') as f:
                data = f.read()
            return BeautifulSoup(data, 'xml')
        except FileNotFoundError:
            raise Exception(f"File not found: {self.file_path}")
        except Exception as e:
            raise Exception(f"Error reading file {self.file_path}: {e}")

    def extract_directives(self, bs_data):
        """Extract all directives and their indices."""
        return [
            (i, element)
            for i, element in enumerate(bs_data.find_all())
            if element.name == "directive" and element.next in ['if', 'ifdef', 'ifndef', 'elif', 'else', 'endif']
        ]

    def parse_conditional_blocks(self, bs_data, index, parent_condition=""):
        """Parse conditional blocks recursively and associate code with conditions."""
        current_condition = parent_condition
        i = index

        while i < len(self.all_directives):
            directive_index, directive = self.all_directives[i]

            if directive.next in ['ifdef', 'ifndef']:
                condition_name = directive.find_next("name").text
                condition = f"!{condition_name}" if directive.next == 'ifndef' else condition_name
                nested_condition = f"({parent_condition}) && ({condition})" if parent_condition else condition
                i = self.parse_conditional_blocks(bs_data, i + 1, nested_condition)
            elif directive.next == 'elif':
                condition_name = directive.find_next("name").text
                current_condition = f"!({parent_condition}) && ({condition_name})"
            elif directive.next == 'else':
                current_condition = f"!({parent_condition})"
            elif directive.next == 'endif':
                return i + 1

            # Extract associated code block
            code_block = self.extract_code_block(bs_data, directive_index)
            if current_condition:
                self.all_conditionals.setdefault(current_condition, []).extend(code_block)

            i += 1

        return i

    def extract_code_block(self, bs_data, start_index):
        """Extract the code block associated with a directive."""
        code_block = []
        elements = bs_data.find_all()

        for i in range(start_index + 1, len(elements)):
            element = elements[i]
            if element.name == "directive":
                break
            if element.name in ['expr_stmt', 'decl_stmt', 'call', 'macro']:
                code_block.append(element.text.strip())

        return code_block

    def process(self):
        """Process the XML file and extract directives and code."""
        self.initialize()
        bs_data = self.parse_file()
        self.all_directives = self.extract_directives(bs_data)
        self.parse_conditional_blocks(bs_data, 0)

    def save_to_json(self, output_dir, data, suffix):
        """Save extracted data to a JSON file."""
        output_file = os.path.basename(self.file_path).replace(".xml", f"_{suffix}.json")
        os.makedirs(output_dir, exist_ok=True)
        output_file_path = os.path.join(output_dir, output_file)

        try:
            with open(output_file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            raise Exception(f"Error saving file {output_file_path}: {e}")

        return output_file_path

    def create_list(self, output_dir):
        """Generate a JSON file with the list of directives."""
        self.process()
        directive_list = {"List of Directives": list(self.all_conditionals.keys())}
        return self.save_to_json(output_dir, directive_list, "directives_list")

    def get_code_instructions(self, output_dir):
        """Generate a JSON file with code instructions for directives."""
        self.process()
        return self.save_to_json(output_dir, self.all_conditionals, "instructions_code")


# Example Usage:
# extractor = DirectiveExtractor("path_to_xml_file.xml")
# directives_list_path = extractor.create_list("output_directory_path")
# instructions_path = extractor.get_code_instructions("output_directory_path")