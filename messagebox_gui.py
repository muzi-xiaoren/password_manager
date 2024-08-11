import tkinter as tk
from password_generate import generate_data
from file_stream import save_data, query_data, delete_data


class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, title, message, font, show_entry=False):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)

        self.label = tk.Label(self, text=message, font=font, wraplength=350)
        self.label.pack(pady=20)

        self.result = None

        if show_entry:
            self.entry = tk.Entry(self, font=font, justify="center")
            self.entry.pack(pady=10)
            self.entry.bind("<Return>", self.on_ok)  # 绑定回车键

        self.ok_button = tk.Button(self, text="OK", command=self.on_ok, font=font)
        self.ok_button.pack(pady=10)

        # 将消息框放置在主界面的正中央
        self.center_window(parent)

    def center_window(self, parent):
        self.update_idletasks()  # 更新消息框的尺寸信息
        if parent.winfo_viewable():
            # 获取主窗口的位置和尺寸
            parent_x = parent.winfo_rootx()
            parent_y = parent.winfo_rooty()
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()

            # 获取消息框的宽度和高度
            window_width = self.winfo_width()
            window_height = self.winfo_height()

            # 计算消息框的位置
            x = parent_x + (parent_width - window_width) // 2
            y = parent_y + (parent_height - window_height) // 2
        else:
            # 如果主窗口不可见，则将消息框放在屏幕中央
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            window_width = self.winfo_width()
            window_height = self.winfo_height()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

        # 设置消息框的位置
        self.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def on_ok(self, event=None):
        if hasattr(self, 'entry'):
            self.result = self.entry.get()
        self.destroy()

    def show(self):
        self.grab_set()
        self.wait_window()
        return self.result