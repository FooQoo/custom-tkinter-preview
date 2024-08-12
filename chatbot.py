import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

# 初期設定
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# ウィンドウ作成
app = ctk.CTk()
app.geometry("1000x600")  # 幅を1000ピクセルに拡大
app.title("ChatBot App")

# グリッドレイアウトの設定
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=0)
app.grid_columnconfigure(0, weight=1)

# チャット表示エリア (CTkScrollableFrame)
chat_frame = ctk.CTkScrollableFrame(app)
chat_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# ユーザー入力エリア (CTkTextbox、ファイルボタン、送信ボタン)
input_frame = ctk.CTkFrame(app)
input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
input_frame.grid_columnconfigure(1, weight=1)  # テキストエリアの列を拡張可能に設定

# ファイル入力ボタン
file_button = ctk.CTkButton(input_frame, text="File", command=lambda: open_file())
file_button.grid(row=0, column=0, padx=(0, 10))

# テキスト入力エリア
entry = ctk.CTkTextbox(input_frame, height=50)
entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))

# 送信ボタン
send_button = ctk.CTkButton(input_frame, text="Send", command=lambda: send_message())
send_button.grid(row=0, column=2)

# アイコン画像の読み込み
you_icon_image = Image.open("you.png")
you_icon = ctk.CTkImage(you_icon_image, size=(60, 60))

bot_icon_image = Image.open("bot.png")
bot_icon = ctk.CTkImage(bot_icon_image, size=(60, 60))

# ファイル選択処理
def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        add_message_to_chat("You", f"File selected: {file_path}", user=True)
        # ファイルの内容を処理する場合は、ここに処理を追加します

# メッセージ送信とボット応答処理
def send_message(event=None):
    user_message = entry.get("1.0", "end-1c")  # テキストボックスの全テキストを取得
    if user_message.strip():
        # ユーザーのメッセージを表示
        add_message_to_chat("You", user_message, user=True)
        entry.delete("1.0", "end")  # テキストボックスをクリア
        entry.configure(height=50)  # メッセージ送信後、エリアの高さをリセット

        # ボットの応答
        bot_response = get_bot_response(user_message)
        add_message_to_chat("Bot", bot_response, user=False)

def get_bot_response(user_message):
    # 簡単な応答ロジック（ここをカスタマイズ可能）
    if "hello" in user_message.lower():
        return "Hello! How can I assist you today?"
    elif "how are you" in user_message.lower():
        return "I'm just a bot, but I'm here to help!"
    else:
        return "I'm sorry, I didn't understand that. Can you rephrase?"

def add_message_to_chat(sender, message, user=True):
    # メッセージ全体のフレーム
    frame = ctk.CTkFrame(chat_frame, corner_radius=10)
    frame.grid(sticky="ew", padx=10, pady=5)  # 幅いっぱいに広げる

    # アイコンの表示
    icon_label = ctk.CTkLabel(frame, image=you_icon if user else bot_icon, text="")
    icon_label.grid(row=0, column=0, padx=5, pady=5)

    # メッセージ内容の表示
    message_label = ctk.CTkLabel(frame, text=message, justify="left", wraplength=800)
    message_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # チャットエリアをスクロールする
    chat_frame._parent_canvas.yview_moveto(1.0)  # 一番下までスクロール

# Shift + Enterで改行し、Enterで送信する処理
def handle_return(event):
    if event.keysym == "Return" and event.state == 0:
        send_message()
        return "break"  # デフォルトの動作を無効化
    elif event.keysym == "Return" and event.state == 1:
        entry.insert(ctk.END, "\n")
        auto_resize_text_area()
        return "break"  # デフォルトの動作を無効化

# テキストエリアの高さを自動調整する
def auto_resize_text_area(event=None):
    # テキストの行数に応じて高さを変更
    lines = int(entry.index('end-1c').split('.')[0])  # 現在の行数を取得
    entry.configure(height=50 + lines * 20)  # 行数に応じて高さを調整

# キーのバインド
entry.bind("<KeyPress-Return>", handle_return)
entry.bind("<KeyRelease>", auto_resize_text_area)  # キー入力のたびに高さを調整

# メインループ開始
app.mainloop()
