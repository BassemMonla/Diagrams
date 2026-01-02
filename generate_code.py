import re
import os

def parse_puml(file_path):
    """
    Parses a simple PlantUML class diagram file.
    Returns a dictionary of classes, their attributes, and methods.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    classes = {}
    current_class = None

    for line in lines:
        line = line.strip()
        
        # Match class definition: class ClassName {
        class_match = re.match(r'class\s+(\w+)\s*\{?', line)
        if class_match:
            current_class = class_match.group(1)
            classes[current_class] = {'attributes': [], 'methods': []}
            continue

        # Match end of class
        if line == '}':
            current_class = None
            continue

        if current_class:
            # Match method: +method_name(args)
            method_match = re.match(r'\+(\w+)\((.*)\)', line)
            if method_match:
                classes[current_class]['methods'].append({
                    'name': method_match.group(1),
                    'args': method_match.group(2)
                })
                continue

            # Match attribute: +type name or +name
            # simplified regex for demo
            attr_match = re.match(r'\+(\w+)\s+(\w+)', line) # +type name
            if attr_match:
                classes[current_class]['attributes'].append({
                    'type': attr_match.group(1),
                    'name': attr_match.group(2)
                })
                continue

    return classes

def generate_python_code(classes, output_dir):
    """
    Generates Python files from the parsed class structure.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for class_name, details in classes.items():
        filename = f"{class_name.lower()}.py"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(f"# Auto-generated code for class {class_name}\n\n")
            f.write(f"class {class_name}:\n")
            
            # __init__
            f.write("    def __init__(self")
            for attr in details['attributes']:
                f.write(f", {attr['name']}: {attr['type']}")
            f.write("):\n")
            
            if not details['attributes']:
                f.write("        pass\n")
            else:
                for attr in details['attributes']:
                    f.write(f"        self.{attr['name']} = {attr['name']}\n")
            f.write("\n")

            # Methods
            for method in details['methods']:
                args = method['args']
                f.write(f"    def {method['name']}(self")
                if args:
                    f.write(f", {args}")
                f.write("):\n")
                f.write(f"        # TODO: Implement {method['name']}\n")
                f.write("        pass\n\n")

        print(f"Generated {filepath}")

if __name__ == "__main__":
    puml_file = "c:/Users/basse/diagrams/model.puml"
    classes = parse_puml(puml_file)
    generate_python_code(classes, "c:/Users/basse/diagrams/generated")
