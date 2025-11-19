import http.server
import socketserver
import json
import os
import sys
from urllib.parse import urlparse

PORT = 8000
DIRECTORY = "."

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        # Parse URL
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/update-tags':
            self.handle_update_tags()
        else:
            self.send_error(404, "Not Found")

    def handle_update_tags(self):
        # Read content length
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            uuid = data.get('uuid')
            tags = data.get('tags')  # Expected list of tag names ["DSA", "HLD"] etc
            
            if not uuid or tags is None:
                self.send_error(400, "Missing uuid or tags")
                return

            # Update the JSON file
            self.update_json_file(uuid, tags)
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            
        except Exception as e:
            print(f"Error processing request: {e}")
            self.send_error(500, str(e))

    def update_json_file(self, target_uuid, new_tag_names):
        json_path = "all_experience_details.json"
        
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            updated = False
            target_article = None
            
            for article in data.get("articles", []):
                if article.get("uuid") == target_uuid:
                    target_article = article
                    # Get existing non-category tags (like Company names)
                    current_tags = article.get("tags", [])
                    preserved_tags = [
                        t for t in current_tags 
                        if t.get("name") not in ["DSA", "HLD", "LLD"]
                    ]
                    
                    # Create new tag objects
                    for tag_name in new_tag_names:
                        preserved_tags.append({
                            "name": tag_name,
                            "slug": tag_name.lower(),
                            "tagType": "CATEGORY"
                        })
                    
                    article["tags"] = preserved_tags
                    updated = True
                    break
            
            if updated:
                # Write back to JSON
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                
                # Regenerate JS file
                self.regenerate_js_file(data)
                
                # Sync to central file
                self.sync_to_central_file(target_article)
                
                print(f"Updated tags for {target_uuid}: {new_tag_names}")
                
        except Exception as e:
            print(f"Error updating file: {e}")
            raise

    def sync_to_central_file(self, article):
        central_file = "tagged_experiences.json"
        
        try:
            # Load existing data
            if os.path.exists(central_file):
                with open(central_file, "r", encoding="utf-8") as f:
                    try:
                        central_data = json.load(f)
                    except json.JSONDecodeError:
                        central_data = []
            else:
                central_data = []
            
            # Check if article has relevant tags
            relevant_tags = ["DSA", "HLD", "LLD"]
            current_tags = [t.get("name") for t in article.get("tags", [])]
            has_relevant_tag = any(tag in relevant_tags for tag in current_tags)
            
            # Find if article already exists in central file
            existing_index = -1
            for i, item in enumerate(central_data):
                if item.get("uuid") == article.get("uuid"):
                    existing_index = i
                    break
            
            # Update central data
            if has_relevant_tag:
                # Create simplified article object
                simplified_article = {
                    "uuid": article.get("uuid"),
                    "title": article.get("title"),
                    "content": article.get("content")
                }
                
                if existing_index >= 0:
                    central_data[existing_index] = simplified_article
                else:
                    central_data.append(simplified_article)
                print(f"Synced {article.get('uuid')} to {central_file}")
            else:
                if existing_index >= 0:
                    central_data.pop(existing_index)
                    print(f"Removed {article.get('uuid')} from {central_file}")
            
            # Save central file
            with open(central_file, "w", encoding="utf-8") as f:
                json.dump(central_data, f, indent=2)
                
        except Exception as e:
            print(f"Error syncing to central file: {e}")

    def regenerate_js_file(self, data):
        js_content = f"window.EXPERIENCES_DATA = {json.dumps(data, indent=2)};"
        with open("docs/experiences_data.js", "w", encoding="utf-8") as f:
            f.write(js_content)

if __name__ == "__main__":
    print(f"Starting server at http://localhost:{PORT}")
    print(f"Serving files from {os.path.abspath(DIRECTORY)}")
    print("Press Ctrl+C to stop")
    
    # Ensure we can reuse the address
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

