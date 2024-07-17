import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import font as tkfont
from password_utils import generate_password
from file_utils import save_data, query_data, delete_data

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")

        # 计算屏幕中心位置
        self.center_window(450, 850)

        self.root.withdraw()  # 先隐藏主窗口

        self.master_password = simpledialog.askstring("Master Key", "Enter your master Key:")

        if not self.master_password:
            self.master_password = ' '  # 默认使用空格作为 Master Key

        self.create_widgets()
        self.root.deiconify()  # 显示主窗口

    def center_window(self, width, height):
        # 获取屏幕宽度和高度
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 计算窗口的 x 和 y 位置
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # 设置窗口的位置
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        # 设置主窗口的字体
        self.default_font = tkfont.Font(size=15)
        self.bold_font = tkfont.Font(size=18, weight="bold")
        self.root.option_add('*Font', self.default_font)

        # 在主界面的最上方显示输入的 Master Key
        self.master_key_label = tk.Label(self.root, text=f"Master Key: {self.master_password}", font=self.bold_font)
        self.master_key_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.generate_frame = tk.LabelFrame(self.root, text="Generate Password", font=self.bold_font)
        self.generate_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.length_label = tk.Label(self.generate_frame, text="Length:")
        self.length_label.grid(row=0, column=0)
        self.length_entry = tk.Entry(self.generate_frame)
        self.length_entry.grid(row=0, column=1)

        self.upper_var = tk.IntVar()
        self.lower_var = tk.IntVar()
        self.digits_var = tk.IntVar()
        self.special_var = tk.IntVar()

        self.upper_check = tk.Checkbutton(self.generate_frame, text="Uppercase", variable=self.upper_var)
        self.upper_check.grid(row=1, column=0)
        self.lower_check = tk.Checkbutton(self.generate_frame, text="Lowercase", variable=self.lower_var)
        self.lower_check.grid(row=1, column=1)
        self.digits_check = tk.Checkbutton(self.generate_frame, text="Digits", variable=self.digits_var)
        self.digits_check.grid(row=2, column=0)
        self.special_check = tk.Checkbutton(self.generate_frame, text="Special", variable=self.special_var)
        self.special_check.grid(row=2, column=1)

        self.generate_button = tk.Button(self.generate_frame, text="Generate", command=self.generate_password)
        self.generate_button.grid(row=3, column=0, columnspan=2)

        self.generated_password_label = tk.Label(self.generate_frame, text="Generated Password:")
        self.generated_password_label.grid(row=4, column=0)
        self.generated_password_entry = tk.Entry(self.generate_frame)
        self.generated_password_entry.grid(row=4, column=1)

        self.store_frame = tk.LabelFrame(self.root, text="Store Password", font=self.bold_font)
        self.store_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.website_label = tk.Label(self.store_frame, text="Website:")
        self.website_label.grid(row=0, column=0)
        self.website_entry = tk.Entry(self.store_frame)
        self.website_entry.grid(row=0, column=1)

        self.username_label = tk.Label(self.store_frame, text="Username (optional):")
        self.username_label.grid(row=1, column=0)
        self.username_entry = tk.Entry(self.store_frame)
        self.username_entry.grid(row=1, column=1)

        self.password_label = tk.Label(self.store_frame, text="Password:")
        self.password_label.grid(row=2, column=0)
        self.password_entry = tk.Entry(self.store_frame, state='readonly')  # 设置为只读
        self.password_entry.grid(row=2, column=1)

        self.store_button = tk.Button(self.store_frame, text="Store", command=self.store_password)
        self.store_button.grid(row=3, column=0, columnspan=2)

        self.query_frame = tk.LabelFrame(self.root, text="Query Password", font=self.bold_font)
        self.query_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.query_website_label = tk.Label(self.query_frame, text="Website:")
        self.query_website_label.grid(row=0, column=0)
        self.query_website_entry = tk.Entry(self.query_frame, width=30)
        self.query_website_entry.grid(row=0, column=1)

        self.query_button = tk.Button(self.query_frame, text="Query", command=self.query_password)
        self.query_button.grid(row=1, column=0, columnspan=2)

        self.result_label = tk.Label(self.query_frame, text="Result:")
        self.result_label.grid(row=2, column=0)
        self.result_text = tk.Text(self.query_frame, height=5, width=30)
        self.result_text.grid(row=2, column=1)

        self.delete_frame = tk.LabelFrame(self.root, text="Delete Password", font=self.bold_font)
        self.delete_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.delete_website_label = tk.Label(self.delete_frame, text="Website:")
        self.delete_website_label.grid(row=0, column=0)
        self.delete_website_entry = tk.Entry(self.delete_frame, width=30)
        self.delete_website_entry.grid(row=0, column=1)

        self.delete_button = tk.Button(self.delete_frame, text="Delete", command=self.delete_password)
        self.delete_button.grid(row=1, column=0, columnspan=2)

        self.delete_result_label = tk.Label(self.delete_frame, text="Result:")
        self.delete_result_label.grid(row=2, column=0)
        self.delete_result_text = tk.Text(self.delete_frame, height=4, width=30)
        self.delete_result_text.grid(row=2, column=1)

        # 使窗口自适应大小
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)

    def generate_password(self):
        length = int(self.length_entry.get())
        use_upper = self.upper_var.get()
        use_lower = self.lower_var.get()
        use_digits = self.digits_var.get()
        use_special = self.special_var.get()

        password = generate_password(length, use_upper, use_lower, use_digits, use_special)
        self.generated_password_entry.delete(0, tk.END)
        self.generated_password_entry.insert(0, password)
        self.password_entry.config(state='normal')  # 解除只读状态
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.password_entry.config(state='readonly')  # 设置为只读状态

    def store_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.generated_password_entry.get()

        if not website or not password:
            messagebox.showerror("Error", "Website and password fields cannot be empty.")
            return

        save_data(self.master_password, website, username, password)
        messagebox.showinfo("Success", "Password stored successfully.")

    def query_password(self):
        website = self.query_website_entry.get()
        results = query_data(self.master_password, website)

        self.result_text.delete(1.0, tk.END)
        if results == "Invalid master key":
            self.result_text.insert(tk.END, "Invalid master key")
        elif results is None:
            self.result_text.insert(tk.END, "No data found.")
        else:
            for username, password in results:
                self.result_text.insert(tk.END, f"Website: {website}\nUsername: {username}\nPassword: {password}\n\n")


    def delete_password(self):
        website = self.delete_website_entry.get()
        success = delete_data(self.master_password, website)
        self.delete_result_text.delete(1.0, tk.END)
        if success:
            self.delete_result_text.insert(tk.END, "Password deleted successfully.")
        else:
            self.delete_result_text.insert(tk.END, "No data found for the specified website.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
