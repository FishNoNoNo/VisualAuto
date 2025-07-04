import time
import pyautogui as pg
import pyperclip

""" 
TYPE
鼠标移动 1
# 获取鼠标位置 2
鼠标拖拽 2
鼠标点击 3
输入字符 4
粘贴中文 5
按键操作 6
热键操作 7
截屏操作 8
 """


class Action:
    def __init__(self, config=None):
        self.config = config
        self.stop_flag=False

    def stop(self):
        self.stop_flag = True

    def ac(self,actions,pause):
        pg.PAUSE=pause
        for action in actions:
            if self.stop_flag:
                return
            acType = action["type"]
            params = action["params"]
            x = params.get("x")
            y = params.get("y")
            duration = params.get("duration") if params.get("duration") else 0
            interval = params.get("interval") if params.get("interval") else 0
            clicks = params.get("clicks") if params.get("clicks") else 1
            keys = params.get("keys")
            key = params.get("key")
            button = params.get("button") if params.get("button") else 'LEFT'
            text = params.get("text")
            msg = params.get("msg")
            presses = params.get("presses") if params.get("presses") else 1
            path = params.get("path")

            if acType == 1:
                pg.moveTo(x=x, y=y, duration=duration)
            elif acType == 2:
                pg.dragTo(x=x, y=y, duration=duration, button=button)
            elif acType == 3:
                pg.click(x=x, y=y, clicks=clicks, interval=interval, button=button, duration=duration)
            elif acType == 4:
                pg.write(message=text, interval=interval)
            elif acType == 5:
                pyperclip.copy(msg)
                pg.hotkey("ctrl", "v", interval=interval)
            elif acType == 6:
                pg.press(keys=key, presses=presses, interval=interval)
            elif acType == 7:
                keys = keys.split(",")
                pg.hotkey(*keys, interval=interval)
            elif acType == 8:
                pg.screenshot(imageFilename=path)
            else:
                raise Exception("未知操作")

    def main(self):
        config = self.config

        actions = config["actions"]

        cycle = config["cycle"]

        ifCycle = cycle.get("ifCycle")

        interval=cycle.get('interval')

        pause=config.get('pause')

        while True:
            try:
                self.ac(actions=actions,pause=pause)
            except Exception as e:
                print(e)
            if not ifCycle or self.stop_flag:
                break
            else:
                time.sleep(interval)
