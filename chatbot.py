import customtkinter as ctk
from PIL import Image

# 初期設定
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# ウィンドウ作成
app = ctk.CTk()
app.geometry("1000x600")  # 幅を1000ピクセルに拡大
app.title("ChatBot App")

# チャット表示エリア
chat_frame = ctk.CTkScrollableFrame(app)
chat_frame.pack(fill="both", expand=True, padx=10, pady=10)  # 幅と高さをウィンドウに合わせる

# ユーザー入力エリア (CTkTextboxを使用)
input_frame = ctk.CTkFrame(app)
input_frame.pack(fill="x", padx=10, pady=10)

entry = ctk.CTkTextbox(input_frame, height=50)
entry.pack(side="left", fill="both", expand=True, padx=10)

# アイコン画像の読み込み
you_icon_image = Image.open("you.png")
you_icon = ctk.CTkImage(you_icon_image, size=(60, 60))

bot_icon_image = Image.open("bot.png")
bot_icon = ctk.CTkImage(bot_icon_image, size=(60, 60))

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
    frame.pack(fill="x", pady=5, padx=10, anchor="e" if user else "w")  # ユーザーは右寄せ、ボットは左寄せ

    if user:
        # ユーザーのメッセージ（アイコンが左、メッセージが右）
        icon_label = ctk.CTkLabel(frame, image=you_icon, text="")
        icon_label.pack(side="left", padx=5, pady=5)

        message_label = ctk.CTkLabel(frame, text=message, justify="right", wraplength=800)
        message_label.pack(side="left", fill="both", expand=True, padx=10, pady=5)

    else:
        # ボットのメッセージ（アイコンが左、メッセージが右）
        icon_label = ctk.CTkLabel(frame, image=bot_icon, text="")
        icon_label.pack(side="left", padx=5, pady=5)

        message_label = ctk.CTkLabel(frame, text=message, justify="left", wraplength=800)
        message_label.pack(side="left", fill="both", expand=True, padx=10, pady=5)

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

# 送信ボタン
send_button = ctk.CTkButton(input_frame, text="Send", command=send_message)
send_button.pack(side="right", padx=10)  # 送信ボタンもテキストボックスと同じ行に配置

# キーのバインド
entry.bind("<KeyPress-Return>", handle_return)
entry.bind("<KeyRelease>", auto_resize_text_area)  # キー入力のたびに高さを調整

# メインループ開始
app.mainloop()
