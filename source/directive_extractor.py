from lxml import etree

class DirectiveExtractor:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.conditional_directives = ['ifdef', 'ifndef', 'elif', 'else', 'endif']

    def extract_conditionals(self, node):
        """Extract the conditional compilation context for a given node."""
        if node is None:
            return "TRUE"

        conditional_path = []
        parent = node.getparent()  # Use lxml's getparent() to traverse up the tree

        # Traverse up the parent hierarchy
        while parent is not None:
            if parent.tag.endswith('ifdef'):
                name = parent.find('name')
                if name is not None:
                    conditional_path.append(f"({name.text})")
            elif parent.tag.endswith('ifndef'):
                name = parent.find('name')
                if name is not None:
                    conditional_path.append(f"!( {name.text} )")
            elif parent.tag.endswith('elif'):
                expr = parent.find('expr')
                if expr is not None:
                    conditional_path.append(f"({expr.text})")
            elif parent.tag.endswith('else'):
                conditional_path.append("else")
            parent = parent.getparent()

        # Reverse the path to get the correct nesting order
        conditional_path.reverse()

        # Return the combined conditionals or "TRUE" if none found
        return " && ".join(conditional_path) if conditional_path else "TRUE"
