import threading
from flask import Flask, jsonify, render_template, request
import json

import keyboard
from action import Action


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/config")
def get_config():
    config = {}
    with open("./config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    return config


@app.route("/api/save-config", methods=["POST"])
def save_config():
    try:
        received_data = request.get_json()
        print("收到的数据：", received_data)

        # 将数据写入本地文件保存
        with open("./config.json", "w", encoding="utf-8") as f:
            json.dump(received_data, f, ensure_ascii=False, indent=4)

        return jsonify({"code": "1", "msg": "配置已保存", "data": ""})

    except Exception as e:
        print("保存失败:", str(e))
        return jsonify({"code": "0", "msg": "保存失败：" + str(e), "data": ""}), 500


@app.route("/api/start")
def start():
    config={}
    with open('config.json','r',encoding='utf-8') as f:
        config=json.load(f)
    action=Action(config=config)
    def on_esc():
        print("尝试停止任务...")
        if action:
            action.stop()

    # 添加热键监听
    keyboard.add_hotkey('ctrl+1', on_esc)
    thread = threading.Thread(
        target=action.main, daemon=True
    )
    thread.start()
    return jsonify({"code": "1", "msg": "开始执行", "data": ""})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
