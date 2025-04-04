import os
import json

def main():
    folder = "Rules"
    combined = {}  
    if not os.path.exists(folder):
        print(f"No folder named '{folder}' found. Nothing to combine.")
        return

    # Gather all .json files in the 'Rules' folder
    files = [f for f in os.listdir(folder) if f.endswith(".json")]

    if not files:
        print(f"No JSON files found in '{folder}'. Nothing to combine.")
        return

    for file_name in files:
        file_path = os.path.join(folder, file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error reading '{file_name}': {e}")
                continue

        if "subreddit" in data:
            sub_name = data["subreddit"]
            if sub_name not in combined:
                combined[sub_name] = []
            
            if "rules" in data:
                # 'rules' is a list of rule objects with short_name, description, kind
                combined[sub_name].extend(data["rules"])
            else:
                # Possibly a malformed file
                combined[sub_name].append({"error": "No 'rules' key found"})
        
        elif "error" in data:
            # This might be a file with just an error, but no "subreddit" name
            combined.setdefault("unknown", []).append({"error": data["error"]})
        else:
            # Some other structure
            combined.setdefault("unknown", []).append(data)

    # Finally, write the combined data to a single JSON file
    output_file = "Rules/combined_rules.json"
    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(combined, out, indent=4, ensure_ascii=False)

    print(f"\nAll done! Combined rules are in '{output_file}'.")

if __name__ == "__main__":
    main()