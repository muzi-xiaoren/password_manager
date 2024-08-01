import tkinter as tk
import tkinter.font as tkfont

# 查看系统字体和样式
class FontViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Font Viewer")

        # 创建一个滚动条和一个文本框来显示字体列表
        self.scrollbar = tk.Scrollbar(root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text = tk.Text(root, wrap=tk.NONE, yscrollcommand=self.scrollbar.set)
        self.text.pack(expand=1, fill=tk.BOTH)

        self.scrollbar.config(command=self.text.yview)

        # 获取所有可用的字体
        self.font_families = tkfont.families()
        self.display_fonts()

    def display_fonts(self):
        for family in self.font_families:
            # 创建一个字体对象
            font = tkfont.Font(family=family, size=12)
            # 在文本框中显示字体名称和示例文本
            self.text.insert(tk.END, f"Font: {family}\n")
            self.text.insert(tk.END, f"Example: The quick brown fox jumps over the lazy dog\n", (family,))
            self.text.insert(tk.END, "\n\n")
            # 为每种字体样式设置标签
            self.text.tag_configure(family, font=font)

if __name__ == "__main__":
    root = tk.Tk()
    app = FontViewerApp(root)
    root.mainloop()

