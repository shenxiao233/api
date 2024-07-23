import argparse
from flask import Flask, jsonify, request
from utils.start import main


app = Flask(__name__)


@app.route('/api/crawl', methods=['GET'])
def crawl():
    uid = request.args.get('uid')
    page_num = request.args.get('page_num')  # 获取请求参数中的 page_num
    if not uid:
        return jsonify({'error': 'Missing uid parameter'}), 400
    args = {
        'uid': uid,
        'page_number': int(page_num) if page_num else 1,  # 将请求参数中的 page_num 转换为整数，默认为 1
        'save_dir': 'json',
        'save_by_page': False,
        'time': 1,
        'detailed': False,
    }

    args_namespace = argparse.Namespace(**args)

    json_data = main(args_namespace)  # 调用 main 函数
    # 返回爬取结果
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True)
