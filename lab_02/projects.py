from flask import Flask, jsonify, request

app = Flask(__name__)

# Наш список проектов (база данных в памяти)
projects = [
    {"id": 1, "project_name": "Farm", "manager": "Qiqi"},
    {"id": 2, "project_name": "Airport", "manager": "Joe"}
]
next_id = 3

# 1. Получить все проекты
@app.route('/api/projects', methods=['GET'])
def get_projects():
    return jsonify({'projects': projects})

# 2. Создать новый проект
@app.route('/api/projects', methods=['POST'])
def create_project():
    global next_id
    data = request.json
    if not data or 'project_name' not in data:
        return jsonify({'error': 'Project name must be!'}), 400
    
    new_project = {
        'id': next_id,
        'project_name': data['project_name'],
        'manager': data.get('manager', 'No employee')
    }
    projects.append(new_project)
    next_id += 1
    return jsonify(new_project), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
