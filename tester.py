import customtkinter as ctk
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import tkinter.messagebox as messagebox

# Set appearance mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# App window
app = ctk.CTk()
app.title("MongoDB URI Tester")
app.geometry("500x300")

# Function to test MongoDB connection
def test_mongo_connection():
    uri = uri_entry.get()
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        client.server_info()  # Forces a call to the server
        result_label.configure(text="✅ Connection Successful", text_color="green")
    except ConnectionFailure:
        result_label.configure(text="❌ Connection Failed", text_color="red")
    except Exception as e:
        result_label.configure(text=f"❌ Error: {str(e)}", text_color="orange")

# UI Elements
title_label = ctk.CTkLabel(app, text="MongoDB URI Tester", font=ctk.CTkFont(size=20, weight="bold"))
title_label.pack(pady=20)

uri_entry = ctk.CTkEntry(app, placeholder_text="Enter your MongoDB URI here...", width=400)
uri_entry.pack(pady=10)

test_button = ctk.CTkButton(app, text="Test Connection", command=test_mongo_connection)
test_button.pack(pady=10)

# ✅ Define result_label here
result_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=14))
result_label.pack(pady=20)

# Run the app
app.mainloop()
