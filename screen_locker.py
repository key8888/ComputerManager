import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont

def locker(PASSWORD:str):
    root = tk.Tk()
    root.title("パスワードで閉じるウィンドウ")

    # フルスクリーン & 最前面
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.configure(bg="black")

    # コンテナフレームを中央に配置
    frame = tk.Frame(root, bg="black")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # メッセージラベル
    label = tk.Label(frame, text="パソコンはもうすぐ爆発します, 直ちに勉強に戻ってください", 
                     font=("BIZ UDPMincho Medium", 24), fg="white", bg="black")
    label.pack(pady=20)
    label = tk.Label(frame, text="ウィンドウを閉じるにはパスワードを入力してください", 
                     font=("BIZ UDPMincho Medium", 24), fg="white", bg="black")
    label.pack(pady=40)

    # パスワード入力
    password_var = tk.StringVar()
    entry = tk.Entry(frame, textvariable=password_var, show="*", font=("Arial", 20), width=30)
    entry.pack(pady=10)
    entry.focus_set()

    # チェック関数
    def check_password():
        if password_var.get() == PASSWORD:
            root.destroy()
        else:
            messagebox.showerror("エラー", "パスワードが間違っています")
            password_var.set("")

    # 閉じるボタン
    button = tk.Button(frame, text="閉じる", command=check_password, font=("Arial", 18))
    button.pack(pady=10)

    # Enterキー対応
    root.bind("<Return>", lambda event: check_password())

    root.mainloop()



