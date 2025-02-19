import os
import json

def scan_directory(directory):
    index_file = directory + "/index.json"
    index = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json") and file != "index.json":
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        id = os.path.splitext(file)[0]
                        
                        relative_path = os.path.relpath(root, directory)
                        path = relative_path if relative_path != "." else None
                        path += '/' + id + ".json"

                        data = json.load(f)
                        
                        name = data.get("name", "")
                        if len(name) == 0:
                            manufacturer = data.get("manufacturer")
                            model = data.get("model")
                            name = manufacturer
                            if len(model) > 0:
                                name += ' ' + model

                        display_name = data.get("display_name", "")
                        if len(display_name) == 0:
                            display_name = manufacturer + " " + data.get("target")

                        item = {"id": id, "name": name, "display_name": display_name, "path": path}
                        index.append(item)
                except (json.JSONDecodeError, OSError) as e:
                    print(f"Error processing {file_path}: {e}")
    
    index_path = os.path.join(directory, index_file)
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4, ensure_ascii=False)
    print(f"Index file generated: {index_path}")

scan_directory(os.getcwd() + "/codes")

