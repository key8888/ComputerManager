import tkinter as tk
import client
import threading

from tkinter import ttk, messagebox
from ttkthemes import ThemedTk


class DynamicButtonApp:
    from typing import Optional

    def __init__(self, master, devices: Optional[dict] = None):
        self.master = master
        self.devices = devices if devices is not None else {}
        # ThemedTk を使用してテーマを適用
        # 'adapta', 'arc', 'elegance', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative' などがあります
        self.master.set_theme("adapta")
        master.title("Lab manager")

        # --- フォントの設定 ---
        # Microsoft YaHei が利用可能であることを前提
        # macOS/Linux の場合は 'Yu Gothic UI', 'Hiragino Sans', 'Noto Sans CJK JP' などに調整
        self.style = ttk.Style()
        self.style.configure('.', font=('BIZ UDPMincho Medium', 12))
        self.style.configure('TButton', font=(
            'Microsoft YaHei', 12), padding=10)  # ボタンにパディングを追加

        # ボタンの背景色とテキスト色を設定する例（テーマによっては上書きされる可能性あり）
        # self.style.map('TButton',
        #                background=[('active', '#e0e0e0'), ('!disabled', '#f0f0f0')],
        #                foreground=[('active', 'black'), ('!disabled', 'black')])

        self.button_count = tk.IntVar(value=9)  # デフォルトのボタン数
        self.buttons = []  # ボタンオブジェクトを保持するリスト
        self.button_reset_timers = {}  # ボタンのリセットタイマーIDを格納する辞書

        self.create_widgets()
        self.update_buttons()  # 初期ボタンの表示

        # ウィンドウの初期サイズを設定
        self.master.geometry("260x380")  # 幅x高さ
        # ウィンドウを中央に配置する（任意）
        self.master.update_idletasks()  # ウィジェットの実際のサイズを計算させる
        x = (self.master.winfo_screenwidth() // 2) - \
            (self.master.winfo_width() // 2)
        y = (self.master.winfo_screenheight() // 2) - \
            (self.master.winfo_height() // 2)
        self.master.geometry(f"+{x}+{y}")

    def create_widgets(self):
        # --- ボタン数を設定するUI ---
        # outer_padding でフレーム全体の余白を設定
        control_frame = ttk.Frame(self.master, padding="15 10")  # 左右15、上下10
        control_frame.pack(pady=10, fill=tk.X)  # 上下の余白と横方向の引き伸ばし

        # ttk.Label(control_frame, text="ボタンの数:").pack(
        #     side=tk.LEFT, padx=(0, 10))  # ラベルとエントリーの間に余白

        # self.count_entry = ttk.Entry(
        #     control_frame, textvariable=self.button_count, width=15, justify='center')  # 中央揃え
        # self.count_entry.pack(side=tk.LEFT, padx=5)
        # self.count_entry.bind("<Return>", self.on_enter_pressed)

        # update_button = ttk.Button(
        #     control_frame, text="更新", command=self.update_buttons)
        # update_button.pack(side=tk.LEFT, padx=(10, 0))  # エントリーとボタンの間に余白

        # control_frame 内の要素を中央に寄せるための調整
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)
        control_frame.grid_columnconfigure(2, weight=1)
        control_frame.grid_columnconfigure(3, weight=1)

        # --- ボタンを配置するフレーム ---
        self.button_frame = ttk.Frame(self.master, padding="10")  # 内側のパディング
        self.button_frame.pack(expand=True, fill=tk.BOTH,
                               padx=10, pady=5)  # 外側のパディング

    def on_button_click(self, original_text, button_widget):
        """ボタンがクリックされたときに実行されるハンドラ"""


        print(f"{original_text} がクリックされました。")
        
        # lock命令を送信
        # self.devices[original_text] は IP アドレスを指す
        threading.Thread(target=client.start_client,
                         kwargs={"server_ip": self.devices[original_text], "msg": "lock"}
                         ).start()


        # 既にタイマーがセットされている場合はキャンセル
        if button_widget in self.button_reset_timers:
            self.master.after_cancel(self.button_reset_timers[button_widget])

        # ボタンのテキストを「ロックに成功」に変更し、一時的に無効化
        button_widget.config(text="ロックに成功", state=tk.DISABLED)  # 無効化

        # 5秒後に元のテキストに戻す処理をスケジュール
        timer_id = self.master.after(
            5000, lambda: self.reset_button_text(button_widget, original_text))
        self.button_reset_timers[button_widget] = timer_id

    def reset_button_text(self, button_widget, original_text):
        """ボタンのテキストを元の状態に戻す"""
        if button_widget.winfo_exists():  # ウィジェットが存在するか確認
            button_widget.config(text=original_text, state=tk.NORMAL)  # 有効化
        if button_widget in self.button_reset_timers:
            del self.button_reset_timers[button_widget]

    def update_buttons(self, event=None):
        """エントリーの値に基づいてボタンを更新する"""
        try:
            # new_count = self.button_count.get()
            new_count = len(self.devices)  # devices の数を取得
            if not isinstance(new_count, int) or new_count < 0:
                raise ValueError("無効な数値です。0以上の整数を入力してください。")
        except tk.TclError:
            messagebox.showerror(
                "入力エラー", "有効な整数を入力してください。", parent=self.master)
            self.button_count.set(len(self.buttons))
            return
        except ValueError as e:
            messagebox.showerror("入力エラー", str(e), parent=self.master)
            self.button_count.set(len(self.buttons))
            return

        # 既存のボタンとタイマーを全て削除・キャンセル
        for button in self.buttons:
            if button in self.button_reset_timers:
                self.master.after_cancel(self.button_reset_timers[button])
                del self.button_reset_timers[button]
            button.destroy()
        self.buttons.clear()

        # 新しい数のボタンを作成し配置
        # for i in range(new_count):
        for i, device_name in enumerate(self.devices):
            button = ttk.Button(self.button_frame, text=device_name,
                                width=20, padding=5)  # ボタンの幅とパディング
            button.config(command=lambda id=i+1,
                          btn=button: self.on_button_click(device_name, btn))

            # グリッドレイアウトで配置
            row = i // 3
            col = i % 3
            # padx, pady でボタン間の間隔を確保
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.buttons.append(button)

        # グリッドの重み付けを設定
        for i in range(3):  # 最大3列なので3列分設定
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range((new_count + 2) // 3):  # 必要な行数分設定
            self.button_frame.grid_rowconfigure(i, weight=1)

    def on_enter_pressed(self, event):
        """エントリーでEnterキーが押されたときにボタンを更新する"""
        self.update_buttons()


def start_gui(devices: dict) -> None:
    root = ThemedTk()  # ThemedTk を使用してテーマを適用
    app = DynamicButtonApp(root, devices)
    root.mainloop()

