import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234

# Colors and fonts
DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 14)
BUTTON_FONT = ("Helvetica", 12)
SMALL_FONT = ("Helvetica", 11)

# Create socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)
    message_box.see(tk.END)  # auto-scroll to latest

def connect():
    try:
        client.connect((HOST, PORT))
        add_message("[SERVER] Connected to server")
    except Exception as e:
        messagebox.showerror("Connection Error", f"Cannot connect: {e}")
        return

    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Invalid Username", "Please enter a username.")
        return

    client.sendall(username.encode('utf-8'))

    threading.Thread(target=listen_for_messages_from_server, args=(client, ), daemon=True).start()

    username_entry.config(state=tk.DISABLED)
    join_button.config(state=tk.DISABLED)

def send_message():
    message = message_entry.get().strip()
    if not message:
        messagebox.showerror("Empty Message", "Please enter a message before sending.")
        return
    try:
        client.sendall(message.encode('utf-8'))
        add_message(f"[You] {message}")
        message_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Send Error", f"Failed to send message: {e}")

def send_video():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
    if not file_path:
        return

    try:
        filename = file_path.split("/")[-1]
        with open(file_path, "rb") as f:
            file_data = f.read()

        filesize = len(file_data)
        header = f"VIDEO~{filename}~{filesize}"
        client.sendall(header.encode('utf-8'))
        client.sendall(file_data)

        add_message(f"[You] Sent video: {filename}")
    except Exception as e:
        messagebox.showerror("Send Video Error", f"Could not send video: {e}")

def listen_for_messages_from_server(client):
    while True:
        try:
            header = client.recv(1024).decode('utf-8')
            if header.startswith("VIDEO~"):
                # Format: VIDEO~sender~filename~filesize
                _, sender, filename, filesize = header.split("~")
                filesize = int(filesize)

                video_data = b''
                while len(video_data) < filesize:
                    packet = client.recv(min(4096, filesize - len(video_data)))
                    if not packet:
                        break
                    video_data += packet

                save_path = f"received_{filename}"
                with open(save_path, "wb") as f:
                    f.write(video_data)

                add_message(f"[{sender}] sent a video: {save_path}")

            else:
                username, content = header.split("~", 1)
                add_message(f"[{username}] {content}")

        except Exception as e:
            add_message("[SERVER] Disconnected or error occurred.")
            break


# --- Build UI ---
root = tk.Tk()
root.title("Messenger Client")
root.geometry("600x600")
root.configure(bg=DARK_GREY)

# Configure grid weights
root.grid_rowconfigure(0, weight=0)  # username row
root.grid_rowconfigure(1, weight=1)  # messages row (expand)
root.grid_rowconfigure(2, weight=0)  # input row
root.grid_columnconfigure(0, weight=1)

# Top frame - username input
top_frame = tk.Frame(root, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

username_label = tk.Label(top_frame, text="Username:", bg=DARK_GREY, fg=WHITE, font=FONT)
username_label.pack(side=tk.LEFT)

username_entry = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
username_entry.pack(side=tk.LEFT, padx=10)

join_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
join_button.pack(side=tk.LEFT)

# Middle frame - message box
middle_frame = tk.Frame(root, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky="nsew", padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, state=tk.DISABLED)
message_box.pack(fill=tk.BOTH, expand=True)

# Bottom frame - message entry and buttons
bottom_frame = tk.Frame(root, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

message_entry = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE)
message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

send_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
send_button.pack(side=tk.LEFT, padx=(10, 5))

video_button = tk.Button(bottom_frame, text="Send Video", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_video)
video_button.pack(side=tk.LEFT)

# main function
def main():

    root.mainloop()
    
if __name__ == '__main__':
    main()