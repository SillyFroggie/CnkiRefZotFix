import tkinter as tk
from tkinter import filedialog, messagebox
import os

# 文本处理函数
def process_text(input_text):
    lines = input_text.splitlines()
    processed_lines = []

    for line in lines:
        # Step 1: 去除每段开头的空格
        line = line.lstrip()

        # Step 2: 如果开头前2个字符为"vo"，替换为"VO"
        if line.startswith("vo"):
            line = "VO" + line[2:]

        # Step 3: 锁定开头前2个字符为"A1"的段
        if line.startswith("A1"):
            # 去除所有空格
            line_no_spaces = line.replace(" ", "")
            # 在A1后添加" ;"
            line_no_spaces = line_no_spaces[:2] + " ;" + line_no_spaces[2:]
            # 在最后一个字符后添加";"
            line_no_spaces += ";"

            # Step 4: 记录每两个";"中出现的字段
            segments = line_no_spaces.split(";")[1:-1]  # 去掉首尾的空字段

            # Step 5: 删除原A1段，改为新的段
            for segment in segments:
                processed_lines.append(f"A1 {segment}")
        else:
            # Step 6: 其他文本完整保留
            processed_lines.append(line)

    # 将处理后的段落重新组合为文本
    processed_text = "\n".join(processed_lines)
    return processed_text

# 运行按钮：处理输入框中的文本并显示在输出框
def run():
    input_text = input_text_area.get("1.0", tk.END).strip()  # 获取输入框内容并去除首尾空格
    if not input_text:
        messagebox.showwarning("警告", "输入框为空，请输入文本或上传文件！")
        return

    output_text = process_text(input_text)
    output_text_area.delete("1.0", tk.END)  # 清空输出框
    output_text_area.insert("1.0", output_text)  # 将处理后的文本显示在输出框
    output_text_area.config(state=tk.NORMAL)  # 确保输出框可编辑
    status_label.config(text="状态：处理完成，结果已显示在输出框。")
    save_txt_button.config(state=tk.NORMAL)  # 启用“保存为txt”按钮

# 上传按钮：加载txt文件内容到输入框
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            input_text = file.read()
            input_text_area.delete("1.0", tk.END)
            input_text_area.insert("1.0", input_text)
        # 设置默认保存路径
        save_path.set(os.path.dirname(file_path))
        uploaded_file_name.set(os.path.splitext(os.path.basename(file_path))[0])
        status_label.config(text=f"状态：已加载文件 {os.path.basename(file_path)}")
        save_txt_button.config(state=tk.DISABLED)  # 禁用“保存为txt”按钮

# 保存为txt按钮：选择保存路径并保存输出框内容为txt文件
def save_as_txt():
    output_text = output_text_area.get("1.0", tk.END).strip()
    if not output_text:
        messagebox.showwarning("警告", "输出框为空，无内容可保存！")
        return

    if not save_path.get():
        # 如果未设置保存路径，提示用户选择路径
        path = filedialog.askdirectory()
        if not path:
            messagebox.showwarning("警告", "未选择保存路径，操作已取消！")
            return
        save_path.set(path)

    # 生成文件名
    if uploaded_file_name.get():
        file_name = f"{uploaded_file_name.get()}-new.txt"
    else:
        file_name = "output-new.txt"
    file_path = os.path.join(save_path.get(), file_name)

    # 保存文件
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(output_text)
    messagebox.showinfo("成功", f"文件已保存到：{file_path}")
    status_label.config(text=f"状态：文件已保存到 {file_path}")

# 清空按钮：清空输入框和输出框的内容
def clear():
    input_text_area.delete("1.0", tk.END)
    output_text_area.delete("1.0", tk.END)
    save_path.set("")
    uploaded_file_name.set("")
    status_label.config(text="状态：已清空内容。")
    save_txt_button.config(state=tk.DISABLED)  # 禁用“保存为txt”按钮

# 创建主窗口
root = tk.Tk()
root.title("Text Processor")

# 输入框
input_frame = tk.LabelFrame(root, text="输入文本")
input_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
input_text_area = tk.Text(input_frame, height=10, width=50)
input_text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# 输出框
output_frame = tk.LabelFrame(root, text="输出文本")
output_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
output_text_area = tk.Text(output_frame, height=10, width=50)
output_text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
output_text_area.config(state=tk.NORMAL)  # 确保输出框可编辑

# 保存路径变量
save_path = tk.StringVar()
uploaded_file_name = tk.StringVar()

# 状态提示标签
status_label = tk.Label(root, text="状态：等待输入或上传文件。")
status_label.pack(pady=5)

# 按钮
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

run_button = tk.Button(button_frame, text="运行", command=run)
run_button.pack(side=tk.LEFT, padx=10)

upload_button = tk.Button(button_frame, text="上传", command=upload_file)
upload_button.pack(side=tk.LEFT, padx=10)

save_txt_button = tk.Button(button_frame, text="保存为txt", command=save_as_txt, state=tk.DISABLED)
save_txt_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(button_frame, text="清空", command=clear)
clear_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
