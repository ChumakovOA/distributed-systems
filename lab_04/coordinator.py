from flask import Flask, request, jsonify
import requests
import urllib3

app = Flask(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

servers = [
    "https://127.0.0.1:5001",
    "https://127.0.0.1:5002"
]

@app.route('/', defaults={'path': ''}, methods=['POST', 'GET', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def proxy(path):
    """Проксирует все запросы на backend серверы"""
    
    # Получаем данные и ЗАГОЛОВКИ (важно!)
    data = request.get_data()
    
    # Передаем ВСЕ заголовки, включая Authorization
    headers = {}
    for key, value in request.headers.items():
        if key.lower() != 'host':  # исключаем Host, чтобы не было конфликта
            headers[key] = value
    
    print(f" Проксируем {request.method} /{path}")
    print(f"   Заголовки: {headers}")
    
    for server in servers:
        try:
            response = requests.request(
                method=request.method,
                url=f"{server}/{path}",
                data=data,
                headers=headers,  # Передаем заголовки дальше
                cert=("client_cert.pem", "client_key.pem"),
                verify=False,
                timeout=5
            )
            
            print(f" {server} ответил с кодом {response.status_code}")
            return response.content, response.status_code
            
        except Exception as e:
            print(f" {server} failed: {e}")
            continue
    
    return jsonify({"error": "All servers down"}), 503

if __name__ == "__main__":
    print("Coordinator on port 8000")
    app.run(host='0.0.0.0', port=8000, debug=True)