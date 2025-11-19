import os
import json

def scan_directory(path):
    structure = []
    # Sort to ensure consistent order
    try:
        items = sorted(os.listdir(path))
    except FileNotFoundError:
        return []

    for item in items:
        if item.startswith('.'): continue
        
        full_path = os.path.join(path, item)
        
        if os.path.isdir(full_path):
            # Recursively scan subdirectories
            children = scan_directory(full_path)
            if children:
                structure.append({
                    "type": "directory",
                    "name": item,
                    "children": children
                })
        elif item.endswith('.md'):
            # Read markdown content
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            structure.append({
                "type": "file",
                "name": item,
                "content": content
            })
            
    return structure

def generate_site():
    base_dir = "Interview_Preparation"
    data = scan_directory(base_dir)
    
    # Create the JS file
    js_content = f"window.CONTENT_DATA = {json.dumps(data, indent=2)};"
    
    with open("docs/content_data.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    
    print("Successfully generated docs/content_data.js")

    # Process all_experience_details.json
    try:
        with open("all_experience_details.json", "r", encoding="utf-8") as f:
            experiences = json.load(f)
        
        exp_js_content = f"window.EXPERIENCES_DATA = {json.dumps(experiences, indent=2)};"
        
        with open("docs/experiences_data.js", "w", encoding="utf-8") as f:
            f.write(exp_js_content)
            
        print("Successfully generated docs/experiences_data.js")
    except FileNotFoundError:
        print("Warning: all_experience_details.json not found")

if __name__ == "__main__":
    generate_site()

