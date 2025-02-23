from flask import Flask, jsonify, request
from flask_cors import CORS
import redis
import json
import os

app = Flask(__name__)
# 只允许特定域名访问
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173",  # 开发环境
            "http://ebike.littleking.site"  # 生产环境
        ]
    }
})

# Redis 连接配置，从环境变量中读取密码
redis_password = os.getenv('REDIS_PASSWORD')
if not redis_password:
    raise ValueError("REDIS_PASSWORD environment variable is not set")

redis_client = redis.Redis(host='localhost', port=5200, db=0, password=redis_password)

# 查询指定日期的数据
@app.route('/api/get_vehicle_data', methods=['GET'])
def get_vehicle_data():
    date = request.args.get('date')  # 通过URL参数获取日期
    if not date:
        return jsonify({"error": "Missing date parameter"}), 400

    redis_key = f"tq_{date}"

    # 获取该日期所有的时间戳字段
    vehicle_data = redis_client.hgetall(redis_key)

    # 将数据从字节转换为 JSON 格式
    data = []
    for timestamp, value in vehicle_data.items():
        timestamp = timestamp.decode('utf-8')  # 时间戳
        value = json.loads(value.decode('utf-8'))  # 将存储的JSON字符串转换回字典
        value['timestamp'] = timestamp
        data.append(value)
    
    # 按timestamp排序
    data.sort(key=lambda x: x['timestamp'])

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
