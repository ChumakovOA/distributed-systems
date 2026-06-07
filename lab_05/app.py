import time
import redis
from flask import Flask

app = Flask(__name__)

# Подключаемся к Redis по имени сервиса
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    current_count = get_hit_count()
    squared_count = current_count * current_count
    
    return f'''
    <h1 style="color: green; font-family: sans-serif;">Бизнес-стенд "Инновации"</h1>
    <p style="font-size: 1.2em;">
        Текущее число посетителей: <strong>{current_count}</strong><br>
        <span style="color: blue; font-size: 1.5em;">
            Результат (число²): {squared_count}
        </span>
    </p>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
EOF