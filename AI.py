# -*- coding: utf-8 -*-
import datetime
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window

# ========== 原有对话逻辑（完全保留，无需修改） ==========
jokes = [
    "为什么数学书总是很忧郁？——因为它有太多问题。",
    "鱼为什么不会打篮球？——因为怕被裁判吹“走步”。",
    "什么东西越洗越脏？——水。",
]
riddles = [
    ("什么东西越削越大？", "坑"),
    ("什么路最窄？", "冤家路窄"),
    ("什么东西晚上才出生？", "月亮"),
]
facts = [
    "海豚睡觉时只有一半大脑休息。",
    "香蕉其实是浆果。",
    "章鱼有三个心脏。",
]

def respond(ui):
    # 原有规则
    if '你' in ui and '是' in ui:
        if '你妈' in ui:
            return '我妈也是机器人'
        else:
            return '我是机器人'
    if '真的' in ui or '假的' in ui:
        return '真的'
    if all(word in ui for word in ['你','只','会','几','句','话','吗']) or \
       all(word in ui for word in ['你','只','会','一','句','话','吗']):
        return "不是的哦，系统还在不断完善中"

    # 1. 问候与告别
    if any(greet in ui for greet in ['你好','嗨','hi','hello','hey']):
        return '你好呀！很高兴见到你。'
    if any(bye in ui for bye in ['再见','拜拜','bye','88','下次见']):
        return '再见，期待下次聊天！'
    if '退出' in ui or '结束' in ui:
        return '__EXIT__'

    # 2. 自我介绍
    if any(q in ui for q in ['你是谁','你叫什么','你的名字']):
        return '我叫元宝，是腾讯开发的AI助手。'
    if '谁创造' in ui or '谁开发' in ui or '谁做的' in ui:
        return '我是由腾讯公司创造的。'
    if '你能做什么' in ui or '你有什么功能' in ui:
        return '我可以陪你聊天、讲笑话、猜谜语、算算术，还能告诉你时间和日期。'

    # 3. 感谢与道歉
    if any(t in ui for t in ['谢谢','多谢','感谢']):
        return '不客气，能帮到你我很开心！'
    if any(s in ui for s in ['对不起','抱歉','不好意思']):
        return '没关系，不用放在心上。'

    # 4. 情感与状态
    if any(mood in ui for mood in ['开心','高兴','快乐','兴奋']):
        return '哇，真为你开心！继续保持好心情！'
    if any(mood in ui for mood in ['难过','伤心','悲伤','郁闷','沮丧']):
        return '别难过，生活总有起伏，明天会更好。需要我讲个笑话吗？'
    if '无聊' in ui:
        return '那我陪你聊聊天吧，或者我给你讲个笑话？'
    if '累' in ui:
        return '辛苦了，记得适当休息哦。'

    # 5. 家庭与朋友
    if '爸爸' in ui or '父亲' in ui:
        return '爸爸是家里的顶梁柱，你要多孝顺他哦。'
    if '妈妈' in ui or '母亲' in ui:
        return '妈妈是最温柔的人，记得常对她说爱。'
    if '兄弟' in ui or '姐妹' in ui or '兄妹' in ui:
        return '手足之情很珍贵，好好珍惜。'
    if '朋友' in ui:
        return '朋友是一生的财富，真诚相待最重要。'

    # 6. 工作与学习
    if any(w in ui for w in ['工作','上班','加班','职业']):
        return '工作固然重要，但也要平衡生活，别太拼了。'
    if any(s in ui for s in ['学习','考试','作业','上课']):
        return '加油！学习是一个积累的过程，每天进步一点点。'
    if '压力' in ui or '焦虑' in ui:
        return '压力大的时候可以深呼吸，听听音乐放松一下。'

    # 7. 兴趣爱好
    if any(h in ui for h in ['音乐','唱歌','歌曲']):
        return '音乐是治愈心灵的良药，你喜欢哪种风格？'
    if any(m in ui for m in ['电影','电视剧','追剧']):
        return '最近有什么好看的片子吗？给我推荐一下吧。'
    if any(s in ui for s in ['运动','健身','跑步','打球']):
        return '运动有益健康，坚持就是胜利！'
    if any(b in ui for b in ['书','阅读','小说','读书']):
        return '书籍是人类进步的阶梯，你最近在读什么？'

    # 8. 饮食
    if any(f in ui for f in ['吃','美食','好吃','饿']):
        return '民以食为天，你最喜欢吃什么？'
    if '推荐' in ui and ('菜' in ui or '饭' in ui or '餐厅' in ui):
        return '我推荐试试番茄炒蛋，简单又美味！'
    if '水果' in ui:
        return '多吃水果对身体好，我喜欢苹果和香蕉。'

    # 9. 时间与日期
    if '时间' in ui or '几点' in ui:
        now = datetime.datetime.now()
        return f'现在是 {now.hour:02d}:{now.minute:02d}'
    if '日期' in ui or '今天几号' in ui or '年月日' in ui:
        today = datetime.date.today()
        return f'今天是 {today.year}年{today.month}月{today.day}日'
    if '星期' in ui:
        weekdays = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
        return f'今天是 {weekdays[datetime.datetime.today().weekday()]}'

    # 10. 天气（模拟）
    if '天气' in ui:
        return '我目前无法获取实时天气，建议你打开手机天气应用查看。'

    # 11. 笑话与谜语
    if '笑话' in ui:
        return random.choice(jokes)
    if '谜语' in ui or '猜谜' in ui:
        riddle, answer = random.choice(riddles)
        return f'谜题：{riddle}\n（提示：输入“答案”查看谜底）'
    if '答案' in ui and '谜语' in ui:
        return '谜底是：坑（或其他，请重新猜一个谜语吧）'

    # 12. 小知识
    if '冷知识' in ui or '知识' in ui or '科普' in ui:
        return random.choice(facts)

    # 13. 鼓励与哲学
    if '人生' in ui or '意义' in ui:
        return '人生的意义在于寻找属于自己的幸福和热爱。'
    if '加油' in ui or '努力' in ui:
        return '加油！你的努力终会有回报。'
    if '梦想' in ui:
        return '有梦想谁都了不起，坚持追逐吧！'

    # 14. 数字游戏（简单）
    if '数字' in ui or '数数' in ui:
        return '我会从1数到10：1 2 3 4 5 6 7 8 9 10！'
    if '最大' in ui and '数字' in ui:
        return '理论上没有最大的数字，但计算机里常用的是2^31-1。'

    # 15. 复读机模式（趣味）
    if '复读' in ui or 'echo' in ui:
        return ui

    # 16. 默认回应
    return '嗯…这个话题我还不太懂，换个话题聊聊吧？'


# ========== Kivy GUI 部分 ==========
class ChatScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=[10, 20, 10, 10], **kwargs)

        # 聊天记录显示区域（使用 ScrollView + Label）
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.chat_label = Label(
            text='',
            size_hint_y=None,
            halign='left',
            valign='top',
            markup=True,
            font_size='16sp',
            text_size=(Window.width - 40, None),
            color=(0.95, 0.92, 0.85, 1)  # 浅米色背景
        )
        self.chat_label.bind(texture_size=self._update_chat_height)
        self.scroll_view.add_widget(self.chat_label)
        self.add_widget(self.scroll_view)

        # 底部输入区域
        input_box = BoxLayout(size_hint_y=None, height='48dp', spacing=5)
        self.text_input = TextInput(
            hint_text='请输入消息...',
            multiline=False,
            font_size='16sp',
            background_color=(1,1,1,0.9),
            foreground_color=(0.1,0.1,0.1,1)
        )
        self.text_input.bind(on_text_validate=self.send_message)
        send_button = Button(
            text='发送',
            size_hint_x=None,
            width='70dp',
            font_size='16sp',
            background_normal='',
            background_color=(0.3, 0.65, 0.35, 1),
            color=(1,1,1,1)
        )
        send_button.bind(on_release=self.send_message)
        input_box.add_widget(self.text_input)
        input_box.add_widget(send_button)
        self.add_widget(input_box)

        # 显示欢迎信息
        self._append_message('系统', '我是聊天机器人（增强版）\n你可以和我聊：问候、名字、心情、家庭、工作、学习、爱好、食物、时间、笑话、谜语等等。\n输入“退出”或“结束”可以离开。')

    def _update_chat_height(self, instance, value):
        instance.height = max(value[1], self.scroll_view.height)

    def _append_message(self, sender, msg):
        """在聊天标签后追加一行消息（支持颜色标记）"""
        current_text = self.chat_label.text
        if sender == '你':
            line = f'[color=3399ff][b]你[/b] > [/color]{msg}\n\n'
        elif sender == '系统':
            line = f'[color=666666]{msg}[/color]\n\n'
        else:
            line = f'[color=33aa33][b]元宝[/b] > [/color]{msg}\n\n'
        self.chat_label.text = current_text + line
        # 自动滚动到底部
        Clock.schedule_once(lambda dt: setattr(self.scroll_view, 'scroll_y', 0), 0.01)

    def send_message(self, *args):
        user_input = self.text_input.text.strip()
        if not user_input:
            return
        self.text_input.text = ''
        # 显示用户消息
        self._append_message('你', user_input)
        # 获取回复
        reply = respond(user_input)
        if reply == '__EXIT__':
            self._append_message('系统', '再见！期待下次聊天。')
            Clock.schedule_once(lambda dt: App.get_running_app().stop(), 1.5)
            return
        self._append_message('元宝', reply)


class ChatBotApp(App):
    def build(self):
        Window.size = (400, 700)  # 模拟手机尺寸，实际运行时会被忽略
        self.title = 'AI 聊天机器人'
        return ChatScreen()


if __name__ == '__main__':
    ChatBotApp().run()