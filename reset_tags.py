import json

def reset_tags():
    try:
        with open("all_experience_details.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        count = 0
        for article in data.get("articles", []):
            if "tags" in article:
                # Keep only COMPANY tags or tags that are NOT DSA/HLD/LLD
                original_tags = article["tags"]
                new_tags = [
                    t for t in original_tags 
                    if t["name"] not in ["DSA", "HLD", "LLD"]
                ]
                
                if len(original_tags) != len(new_tags):
                    article["tags"] = new_tags
                    count += 1
        
        with open("all_experience_details.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            
        print(f"Cleared auto-generated tags from {count} articles.")
        
    except FileNotFoundError:
        print("Error: all_experience_details.json not found")

if __name__ == "__main__":
    reset_tags()


