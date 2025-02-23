from flask import Flask, jsonify, request
import redis
import json

app = Flask(__name__)

# Redis 连接配置
redis_client = redis.Redis(host='124.223.78.187', port=5200, db=0, password='H4itLSIFYHLBkmBAa6ez')

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
