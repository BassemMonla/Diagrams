from plantuml import PlantUML
import os

def render_diagram(file_path):
    print(f"Rendering {file_path}...")
    # Use the public PlantUML server to generate the image
    # This avoids asking the user to install Java and Graphviz locally
    pl = PlantUML(url='http://www.plantuml.com/plantuml/img/')
    
    try:
        # processes_file writes the output to the same directory with .png extension
        pl.processes_file(file_path)
        print("Successfully rendered model.png")
    except Exception as e:
        print(f"Error rendering diagram: {e}")

if __name__ == "__main__":
    render_diagram('c:/Users/basse/diagrams/model.puml')
