import os
import subprocess
import tkinter as tk
from tkinter import font as tkfont
from password_generate import generate_data
from file_stream import save_data, query_data, delete_data
from messagebox_gui import CustomMessageBox

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")

        # 计算屏幕中心位置
        self.center_window(820, 530)
        self.root.withdraw()  # 先隐藏主窗口

        font = tkfont.Font(family="Comic Sans MS", size=13)
        custom_message_box = CustomMessageBox(self.root, "Master Key", "Enter your master Key:", font, show_entry=True)
        self.master_password = custom_message_box.show()
        # self.master_password = simpledialog.askstring("Master Key", "Enter your master Key:")

        if not self.master_password:
            self.master_password = ' '  # 默认使用空格作为 Master Key

        if self.master_password is None:
            self.root.destroy()
            return

        self.create_widgets()
        self.root.deiconify()  # 显示主窗口

        self.new_window = None   # 用于存储新窗口的引用

    def center_window(self, width, height):
        # 获取屏幕宽度和高度
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 计算窗口的 x 和 y 位置
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # 设置窗口的位置
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def show_message(self, title, message, font):
        CustomMessageBox(self.root, title, message, font).show()

    def create_widgets(self):
        # 设置主窗口的字体
        # self.default_font = tkfont.Font(size=15)
        # self.bold_font = tkfont.Font(size=18, weight="bold")
        # self.root.option_add('*Font', self.default_font)
        self.default_font = tkfont.Font(family="Comic Sans MS", size=13)
        self.bold_font = tkfont.Font(family="Comic Sans MS", size=16, weight="bold")
        self.root.option_add('*Font', self.default_font)

        # 展示密钥和打开文件的界面，"Generate Password Master"
        self.generate_master = tk.LabelFrame(self.root, font=self.bold_font)
        self.generate_master.grid(row=0, column=0, padx=10, pady=2)

        # 在主界面的最上方显示输入的 Master Key
        if self.master_password == ' ':
            self.master_key_label = tk.Label(self.generate_master, text="Master Key: default a space -> ", font=self.bold_font)
        else:
            self.master_key_label = tk.Label(self.generate_master, text=f"Master Key: {self.master_password}", font=self.bold_font)
        self.master_key_label.grid(row=0, column=0, padx=10, pady=2, rowspan=2)

        # 展示密钥和打开文件的界面，"Generate Password Frame"
        self.generate_button = tk.LabelFrame(self.root, font=self.bold_font)
        self.generate_button.grid(row=0, column=1, padx=10, pady=2)

        # 添加按钮来打开 md 和 txt 文件
        self.open_md_button = tk.Button(self.generate_button, text="md", command=self.open_md_file)
        self.open_md_button.grid(row=0, column=0, padx=10, pady=2)
        self.open_txt_button = tk.Button(self.generate_button, text="txt", command=self.open_txt_file)
        self.open_txt_button.grid(row=0, column=1, padx=10, pady=2)

        # 生成密码的界面，"Generate Password Frame"
        self.generate_frame = tk.LabelFrame(self.root, text="Generate Password", font=self.bold_font)
        self.generate_frame.grid(row=1, column=0, padx=10, pady=8)

        self.length_label = tk.Label(self.generate_frame, text="Password Length: ")
        self.length_label.grid(row=0, column=0, padx=20, pady=8)
        self.length_entry = tk.Entry(self.generate_frame, width=10, justify="center")
        self.length_entry.grid(row=0, column=1, padx=36, pady=8)

        self.upper_var = tk.IntVar()
        self.lower_var = tk.IntVar()
        self.digits_var = tk.IntVar()
        self.special_var = tk.IntVar()

        self.upper_check = tk.Checkbutton(self.generate_frame, text="Uppercase", variable=self.upper_var)
        self.upper_check.grid(row=1, column=0, pady=8)
        self.lower_check = tk.Checkbutton(self.generate_frame, text="Lowercase", variable=self.lower_var)
        self.lower_check.grid(row=1, column=1, pady=8)
        self.digits_check = tk.Checkbutton(self.generate_frame, text="Digits", variable=self.digits_var)
        self.digits_check.grid(row=2, column=0, pady=8)
        self.special_check = tk.Checkbutton(self.generate_frame, text="Special", variable=self.special_var)
        self.special_check.grid(row=2, column=1, pady=8)

        self.generate_button = tk.Button(self.generate_frame, text="Generate", command=self.generate_password)
        self.generate_button.grid(row=3, column=0, padx=1, pady=5)

        self.default1_button = tk.Button(self.generate_frame, text="Default", command=self.deflaut_password)
        self.default1_button.grid(row=3, column=1, padx=1, pady=5)

        # 存储密码部分 "Store Password Frame"
        self.store_frame = tk.LabelFrame(self.root, text="Store Password", font=self.bold_font)
        self.store_frame.grid(row=2, column=0, padx=10, pady=2)

        self.website_label = tk.Label(self.store_frame, text="Website:")
        self.website_label.grid(row=0, column=0, pady=5)
        self.website_entry = tk.Entry(self.store_frame, width=23, justify="center")
        self.website_entry.grid(row=0, column=1, pady=5)
        # self.website_entry.bind("<Return>", self.store_password)

        self.username_label = tk.Label(self.store_frame, text="Name(optional):")
        self.username_label.grid(row=1, column=0, pady=5)
        self.username_entry = tk.Entry(self.store_frame, width=23, justify="center")
        self.username_entry.grid(row=1, column=1, pady=5)
        self.username_entry.bind("<Return>", self.store_password)

        self.password_label = tk.Label(self.store_frame, text="Password:")
        self.password_label.grid(row=2, column=0, pady=5)
        self.password_entry = tk.Entry(self.store_frame, width=23, justify="center")
        self.password_entry.grid(row=2, column=1, pady=5)
        self.password_entry.bind("<Return>", self.store_password)

        self.store_button = tk.Button(self.store_frame, text="Store", command=self.store_password)
        self.store_button.grid(row=3, column=0, columnspan=2, pady=3)

        # 查询密码界面 "Query Password Frame"
        self.query_frame = tk.LabelFrame(self.root, text="Query Password", font=self.bold_font)
        self.query_frame.grid(row=1, column=1, padx=10, pady=2)

        self.query_website_label = tk.Label(self.query_frame, text="Website:")
        self.query_website_label.grid(row=0, column=0)
        self.query_website_entry = tk.Entry(self.query_frame, width=30, justify="center")
        self.query_website_entry.grid(row=0, column=1)
        self.query_website_entry.bind("<Return>", self.query_password)  # 绑定回车键

        self.query_button = tk.Button(self.query_frame, text="Query", command=self.query_password)
        self.query_button.grid(row=1, column=1, padx=65, pady=3, sticky="w")
        self.open_button = tk.Button(self.query_frame, text="Open", command=self.open_newpassword)
        self.open_button.grid(row=1, column=1, padx=65, pady=3, sticky="e")
    
        self.result_label = tk.Label(self.query_frame, text="Result:")
        self.result_label.grid(row=2, column=0)
        self.result_text = tk.Text(self.query_frame, height=5, width=30)
        self.result_text.grid(row=2, column=1)

        # 删除密码界面 "Delete Password Frame"
        self.delete_frame = tk.LabelFrame(self.root, text="Delete Password", font=self.bold_font)
        self.delete_frame.grid(row=2, column=1, padx=10, pady=2)

        self.delete_website_label = tk.Label(self.delete_frame, text="Website:")
        self.delete_website_label.grid(row=0, column=0)
        self.delete_website_entry = tk.Entry(self.delete_frame, width=30, justify="center")
        self.delete_website_entry.grid(row=0, column=1)
        self.delete_website_entry.bind("<Return>", self.delete_password)  # 绑定回车键

        self.delete_button = tk.Button(self.delete_frame, text="Delete", command=self.delete_password)
        self.delete_button.grid(row=1, column=1, pady=5)

        self.delete_result_label = tk.Label(self.delete_frame, text="Result:")
        self.delete_result_label.grid(row=2, column=0, pady=5)
        self.delete_result_text = tk.Text(self.delete_frame, height=3, width=30)
        self.delete_result_text.grid(row=2, column=1, pady=5)

        # 使窗口自适应大小
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

    def open_newpassword(self):
        # 获取查询结果框中的内容
        result_content = self.result_text.get(1.0, tk.END).strip()

        if not result_content or result_content in ["Invalid master key", "No data found.", "Please get some data first."]:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please get some data first.")
            return

        # 关闭之前的窗口（如果存在）
        if self.new_window is not None:
            self.new_window.destroy()
            self.new_window = None
            
        # 创建一个新的Tkinter窗口
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Query Result")

        # 获取主窗口的位置和大小
        main_window_geometry = self.root.geometry().split('+')
        main_window_size = main_window_geometry[0].split('x')
        main_window_x = int(main_window_geometry[1])
        main_window_y = int(main_window_geometry[2])
        main_window_width = int(main_window_size[0])
        main_window_height = int(main_window_size[1])

        max_line_length = max(len(line) for line in result_content.split('\n'))
        new_window_width = max_line_length * 10  # 每个字符宽度约为10像素
        new_window_height = main_window_height
        # 设置新窗口的位置和大小，使其在主窗口的右边
        self.new_window.geometry(f'{new_window_width}x{new_window_height}+{main_window_x + main_window_width}+{main_window_y}')

        # 创建一个框架来包含文本框和滚动条
        frame = tk.Frame(self.new_window)
        frame.grid(row=0, column=0, sticky="nsew")
        self.new_window.grid_rowconfigure(0, weight=1)
        self.new_window.grid_columnconfigure(0, weight=1)

        # 创建一个文本框并将查询结果显示在新的窗口中
        result_text = tk.Text(frame, wrap=tk.WORD)
        result_text.insert(tk.END, result_content)
        result_text.config(state=tk.NORMAL)

        # 创建一个滚动条
        scrollbar = tk.Scrollbar(frame, command=result_text.yview)
        result_text.config(yscrollcommand=scrollbar.set)

        # 布局
        result_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)


    def generate_password(self):
        length = int(self.length_entry.get())
        use_upper = self.upper_var.get()
        use_lower = self.lower_var.get()
        use_digits = self.digits_var.get()
        use_special = self.special_var.get()
        password = generate_data(length, use_upper, use_lower, use_digits, use_special)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def deflaut_password(self):
        self.length_entry.delete(0, tk.END)
        self.length_entry.insert(0,'20')
        self.use_upper = self.upper_var.set(1)
        self.use_lower = self.lower_var.set(1)
        self.use_digits = self.digits_var.set(1)
        self.use_special = self.special_var.set(1)
        
        self.generate_password()
    
    def store_password(self, event=None):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not website or not password:
            self.show_message("Error", "Website and password cannot be empty.", self.bold_font)
            return
        if save_data(self.master_password, website, username, password):
            self.show_message("Success", "Password stored successfully.", self.bold_font)
        else:
            self.show_message("Error", "The same information already exists.", self.bold_font)

    def query_password(self, event=None):
        website = self.query_website_entry.get()
        results = query_data(self.master_password, website)

        self.result_text.delete(1.0, tk.END)
        if results == "Invalid master key":
            self.result_text.insert(tk.END, f"Invalid master key with '{self.master_password}'")
        elif results is None:
            self.result_text.insert(tk.END, f"No data found for website '{website}'")
        else:
            for stored_website, username, password in results:
                self.result_text.insert(tk.END, f"Website: {stored_website}\nUsername: {username}\nPassword: {password}\n\n")

    def delete_password(self, event=None):
        website = self.delete_website_entry.get()
        result = delete_data(self.master_password, website)
        self.delete_result_text.delete(1.0, tk.END)

        if result == "Invalid master key":
            self.delete_result_text.insert(tk.END, f"Invalid master key with '{self.master_password}'")
        elif result:
            self.delete_result_text.insert(tk.END, "Password deleted successfully.")
        else:
            self.delete_result_text.insert(tk.END, f"No data found for website '{website}', please enter whole website.")

    
    def open_md_file(self):
        md_path = os.path.join(os.path.expanduser('~'), 'password_person', 'passwords.md')
        if os.path.exists(md_path):
            subprocess.Popen(['start', md_path], shell=True)
        else:
            self.show_message("Error", "MD file not found. Please store your password first", self.bold_font)

    def open_txt_file(self):
        txt_path = os.path.join(os.path.expanduser('~'), 'password_person', 'passwords.txt')
        if os.path.exists(txt_path):
            subprocess.Popen(['start', txt_path], shell=True)
        else:
            self.show_message("Error", "TXT file not found. Please store your password first", self.bold_font)
