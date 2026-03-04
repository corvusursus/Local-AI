import requests
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8000
WEB_FOLDER = Path(__file__).parent / "web"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.1:8b"
SYSTEM_PROMPT = "Ты дружелюбный помощник. Отвечай простыми словами."

class ChatHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_FOLDER), **kwargs)
        
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        request_data = json.loads(self.rfile.read(content_length))
        question = request_data["question"]
        answer = ask_ollama(question)
        self.send_json({"answer": answer})
        
    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
        self.wfile.write(json.dumps(data).encode())
    
def ask_ollama(question):
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "stream": False           
    }
    
    response = requests.post(OLLAMA_URL, json=payload)
    
    return response.json()["message"]["content"]

if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), ChatHandler)
    print(f"http://{HOST}:{PORT}")
    server.serve_forever()






response = requests.post(
    "http://localhost:11434/api/chat",
    
    json= {
        "model": "llama3.1:8b",
        "messages": [
            {
                "role": "system",
                "content": "Ты дружелюбный помощник. Отвечай простыми словами."
            },
            {
                "role": "user",
                "content": "Объясни, что такое API, простыми словами в 4 предложениях."
            }
        ],
        "stream": False         
    }
)

print(response.json()["message"]["content"])