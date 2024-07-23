from flask import Flask, render_template, request, jsonify
from data import data_set
from data import website_data_get
from data import get_processed_data
import json
app = Flask(__name__)


@app.route('/')
def index():
    # 调用处理 JSON 数据的函数
    top_five, total_duration, total_visits = data_set()
    website_names = list(website_data_get())

    # 将数据传递到 HTML 模板中
    return render_template('index.html', top_five=top_five, total_duration=total_duration, total_visits=total_visits,
                           website_names=website_names)

@app.route('/process_input', methods=['POST'])
def process_input():
    # 获取从前端发送的数据
    data = request.json

    # 检查数据是否有效
    if data is None or 'inputData' not in data:
        return jsonify({'error': 'Invalid request or missing data'}), 400

    # 处理数据
    input_data = data['inputData']
    site_name, total_visit, total_durations, active_days, max_duration, max_visits, last_7_days = get_processed_data(input_data)

    last_7_days_json = json.dumps(last_7_days, indent=4)

    print(site_name, total_visit, total_durations, active_days, max_duration, max_visits,last_7_days_json)

    # 返回JSON格式的响应
    return jsonify({
        'site_name': site_name,
        'total_visit': total_visit,
        'total_durations': total_durations,
        'active_days': active_days,
        'max_duration': max_duration,
        'max_visits': max_visits,
        'daily_data': last_7_days
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # 使用端口号5001
