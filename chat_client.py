import socket
import threading
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle, Rectangle
from datetime import datetime

HOST = '127.0.0.1'
PORT = 3456

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
is_connected = False

class ChatApp(App):
    def build(self):
        self.username = ""
        self.current_theme = "Light Blue"
        self.themes = {
            "Light Blue": {
                'main_bg': (0.85, 0.92, 1, 1),
                'input_bg': (0.95, 0.95, 0.95, 1),
                'button_bg': (0.6, 0.8, 0.9, 1),
                'send_button_bg': (0.2, 0.4, 0.6, 1),
                'message_bg': (0.9, 0.9, 0.9, 1),
                'server_message_bg': (0.98, 0.98, 0.85, 1),  # Light yellow for server
                'own_message_bg': (0.9, 0.98, 0.9, 1),       # Light green for user
                'other_message_bg': (0.98, 0.92, 0.95, 1),   # Light pink for others
                'text_color': (0, 0, 0, 1),
                'button_text_color': (1, 1, 1, 1),
            },
            "Soft Gray": {
                'main_bg': (0.9, 0.9, 0.9, 1),
                'input_bg': (0.95, 0.95, 0.95, 1),
                'button_bg': (0.7, 0.7, 0.7, 1),
                'send_button_bg': (0.5, 0.5, 0.5, 1),
                'message_bg': (0.85, 0.85, 0.85, 1),
                'server_message_bg': (0.97, 0.97, 0.90, 1),  # Light yellow
                'own_message_bg': (0.92, 0.97, 0.92, 1),     # Light green
                'other_message_bg': (0.97, 0.94, 0.96, 1),   # Light pink
                'text_color': (0, 0, 0, 1),
                'button_text_color': (1, 1, 1, 1),
            },
            "Mint Green": {
                'main_bg': (0.878, 0.961, 0.929, 1),
                'input_bg': (0.95, 0.98, 0.95, 1),
                'button_bg': (0.6, 0.9, 0.7, 1),
                'send_button_bg': (0.3, 0.7, 0.5, 1),
                'message_bg': (0.9, 0.95, 0.9, 1),
                'server_message_bg': (0.97, 0.98, 0.92, 1),  # Light yellow
                'own_message_bg': (0.92, 0.98, 0.92, 1),     # Light green
                'other_message_bg': (0.96, 0.96, 0.94, 1),   # Light pink
                'text_color': (0, 0, 0, 1),
                'button_text_color': (1, 1, 1, 1),
            },
            "Peach": {
                'main_bg': (0.992, 0.914, 0.894, 1),
                'input_bg': (0.98, 0.95, 0.95, 1),
                'button_bg': (0.9, 0.7, 0.7, 1),
                'send_button_bg': (0.8, 0.5, 0.5, 1),
                'message_bg': (0.95, 0.9, 0.9, 1),
                'server_message_bg': (0.99, 0.97, 0.90, 1),  # Light yellow
                'own_message_bg': (0.95, 0.98, 0.95, 1),     # Light green
                'other_message_bg': (0.98, 0.95, 0.96, 1),   # Light pink
                'text_color': (0, 0, 0, 1),
                'button_text_color': (1, 1, 1, 1),
            },
            "Lavender": {
                'main_bg': (0.925, 0.906, 0.961, 1),
                'input_bg': (0.95, 0.95, 0.98, 1),
                'button_bg': (0.7, 0.6, 0.9, 1),
                'send_button_bg': (0.5, 0.4, 0.7, 1),
                'message_bg': (0.9, 0.9, 0.95, 1),
                'server_message_bg': (0.97, 0.97, 0.93, 1),  # Light yellow
                'own_message_bg': (0.93, 0.97, 0.93, 1),     # Light green
                'other_message_bg': (0.96, 0.94, 0.97, 1),   # Light pink
                'text_color': (0, 0, 0, 1),
                'button_text_color': (1, 1, 1, 1),
            },
            "Turkish Red": {
                'main_bg': (0.9, 0.1, 0.1, 1),
                'input_bg': (1, 0.95, 0.95, 1),
                'button_bg': (0.8, 0.2, 0.2, 1),
                'send_button_bg': (0.7, 0.1, 0.1, 1),
                'message_bg': (1, 0.9, 0.9, 1),
                'server_message_bg': (0.99, 0.98, 0.92, 1),  # Light yellow
                'own_message_bg': (0.95, 0.98, 0.95, 1),     # Light green
                'other_message_bg': (0.98, 0.95, 0.96, 1),   # Light pink
                'text_color': (1, 1, 1, 1),
                'button_text_color': (1, 1, 1, 1),
            },
            "Midnight Blue": {
                'main_bg': (0.1, 0.1, 0.3, 1),
                'input_bg': (0.2, 0.2, 0.4, 1),
                'button_bg': (0.2, 0.3, 0.5, 1),
                'send_button_bg': (0.1, 0.2, 0.4, 1),
                'message_bg': (0.3, 0.3, 0.5, 1),
                'server_message_bg': (0.97, 0.97, 0.93, 1),  # Light yellow
                'own_message_bg': (0.93, 0.97, 0.93, 1),     # Light green
                'other_message_bg': (0.96, 0.94, 0.97, 1),   # Light pink
                'text_color': (1, 1, 1, 1),
                'button_text_color': (1, 1, 1, 1),
            },
            "Sunset Orange": {
                'main_bg': (1, 0.6, 0.3, 1),
                'input_bg': (1, 0.9, 0.8, 1),
                'button_bg': (0.9, 0.5, 0.2, 1),
                'send_button_bg': (0.8, 0.4, 0.1, 1),
                'message_bg': (1, 0.8, 0.7, 1),
                'server_message_bg': (0.99, 0.98, 0.92, 1),  # Light yellow
                'own_message_bg': (0.95, 0.98, 0.95, 1),     # Light green
                'other_message_bg': (0.98, 0.95, 0.96, 1),   # Light pink
                'text_color': (0, 0, 0, 1),
                'button_text_color': (1, 1, 1, 1),
            },
            "Forest Green": {
                'main_bg': (0.2, 0.5, 0.3, 1),
                'input_bg': (0.9, 0.95, 0.9, 1),
                'button_bg': (0.3, 0.6, 0.4, 1),
                'send_button_bg': (0.2, 0.5, 0.3, 1),
                'message_bg': (0.85, 0.9, 0.85, 1),
                'server_message_bg': (0.97, 0.98, 0.92, 1),  # Light yellow
                'own_message_bg': (0.92, 0.98, 0.92, 1),     # Light green
                'other_message_bg': (0.96, 0.96, 0.94, 1),   # Light pink
                'text_color': (0, 0, 0, 1),
                'button_text_color': (1, 1, 1, 1),
            },
            "Amethyst": {
                'main_bg': (0.6, 0.4, 0.8, 1),
                'input_bg': (0.95, 0.9, 0.95, 1),
                'button_bg': (0.5, 0.3, 0.7, 1),
                'send_button_bg': (0.4, 0.2, 0.6, 1),
                'message_bg': (0.9, 0.85, 0.95, 1),
                'server_message_bg': (0.97, 0.97, 0.93, 1),  # Light yellow
                'own_message_bg': (0.93, 0.97, 0.93, 1),     # Light green
                'other_message_bg': (0.96, 0.94, 0.97, 1),   # Light pink
                'text_color': (0, 0, 0, 1),
                'button_text_color': (1, 1, 1, 1),
            }
        }
        Window.bind(on_key_down=self._on_key_down)
        Builder.unload_file("chat.kv")
        kv = Builder.load_file("chat.kv")
        print("KV file reloaded successfully")
        return kv

    def _on_key_down(self, window, key, *args):
        if key == 13 and is_connected and self.root.ids.message_input.focus:
            self.send_message()

    def connect_to_server(self):
        global is_connected
        self.username = self.root.ids.username_input.text.strip()
        if self.username:
            try:
                client_socket.connect((HOST, PORT))
                client_socket.sendall(self.username.encode('utf-8'))
                response = client_socket.recv(2048).decode('utf-8')
                if "Connected to server" in response:
                    is_connected = True
                    Clock.schedule_once(lambda dt: self.display_message("SERVER", "Connected to server"), 0)
                    threading.Thread(target=self.listen_for_messages, daemon=True).start()
                    self.root.ids.username_input.disabled = True
                    self.root.ids.join_button.disabled = True
                    self.root.ids.disconnect_button.disabled = False
                    self.root.ids.reconnect_button.disabled = True
            except Exception as e:
                self.display_message("ERROR", f"Connection failed: {e}")
        else:
            self.display_message("SYSTEM", "Username cannot be empty.")

    def disconnect_from_server(self):
        global is_connected
        if is_connected:
            try:
                client_socket.sendall("DISCONNECT".encode('utf-8'))
                client_socket.close()
                is_connected = False
                self.root.ids.disconnect_button.disabled = True
                self.root.ids.reconnect_button.disabled = False
                self.root.ids.join_button.disabled = False
                self.root.ids.username_input.disabled = False
                self.display_message("SYSTEM", "Disconnected from server.")
            except Exception as e:
                self.display_message("ERROR", f"Disconnection failed: {e}")

    def reconnect_to_server(self):
        global is_connected, client_socket
        if not is_connected and self.username:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((HOST, PORT))
                client_socket.sendall(self.username.encode('utf-8'))
                response = client_socket.recv(2048).decode('utf-8')
                if "Connected to server" in response:
                    is_connected = True
                    Clock.schedule_once(lambda dt: self.display_message("SERVER", "Reconnected to server"), 0)
                    threading.Thread(target=self.listen_for_messages, daemon=True).start()
                    self.root.ids.reconnect_button.disabled = True
                    self.root.ids.disconnect_button.disabled = False
                    self.root.ids.join_button.disabled = True
                    self.root.ids.username_input.disabled = True
            except Exception as e:
                self.display_message("ERROR", f"Reconnection failed: {e}")

    def send_message(self):
        message = self.root.ids.message_input.text.strip()
        if message and is_connected:
            try:
                client_socket.sendall(message.encode('utf-8'))
                self.display_message(self.username, message)
                self.root.ids.message_input.text = ""
            except Exception as e:
                self.display_message("ERROR", f"Send failed: {e}")

    def listen_for_messages(self):
        while is_connected:
            try:
                message = client_socket.recv(2048).decode('utf-8')
                if message:
                    sender, content = message.split("~", 1)
                    Clock.schedule_once(lambda dt: self.display_message(sender, content), 0)
                else:
                    break
            except:
                break

    def display_message(self, sender, message):
        is_own_message = sender == self.username
        theme = self.themes[self.current_theme]

        box = BoxLayout(
            size_hint_y=None,
            height=0,
            padding=(10, 5, 10, 5),
            spacing=10,
            orientation='vertical',
        )

        bg_color = theme['server_message_bg'] if sender == "SERVER" else theme['own_message_bg'] if is_own_message else theme['other_message_bg']
        text_color = theme['text_color']

        label = Label(
            text=f"[b]{sender}:[/b] {message}",
            markup=True,
            font_size=16,
            size_hint_x=None,
            text_size=(self.root.ids.chat_log.width * 0.75, None),
            halign="right" if is_own_message else "left",
            valign="middle",
            color=text_color
        )

        label.bind(texture_size=lambda inst, val: setattr(label, 'size', val))

        timestamp = datetime.now().strftime("%d %B %Y %H:%M")
        time_label = Label(
            text=f"[size=12][color={('ffffff' if sender == 'SERVER' else '000000' if is_own_message else '000000')}]{timestamp}[/color][/size]",
            markup=True,
            font_size=12,
            size_hint=(1, None),
            text_size=(self.root.ids.chat_log.width * 0.75, None),
            halign="right" if is_own_message else "left",
            valign="top"
        )
        time_label.bind(texture_size=lambda inst, val: setattr(time_label, 'size', val))

        with label.canvas.before:
            Color(*bg_color)
            label.rect = RoundedRectangle(radius=[10])
            label.bind(pos=lambda inst, val: setattr(label.rect, 'pos', val))
            label.bind(size=lambda inst, val: setattr(label.rect, 'size', val))

        box.add_widget(label)
        box.add_widget(time_label)

        box.bind(minimum_height=lambda inst, val: setattr(box, 'height', label.height + time_label.height + 10))
        self.root.ids.chat_log.add_widget(box)

        with open("chat_log.txt", "a", encoding="utf-8") as file:
            file.write(f"{timestamp} - {sender}: {message}\n")

    def show_theme_picker(self):
        popup = Popup(title="Select a Theme", size_hint=(0.8, 0.6))
        grid = GridLayout(cols=3, spacing=5, padding=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        for theme_name in self.themes.keys():
            btn = Button(
                text=theme_name,
                font_size=16,
                size_hint_y=None,
                height=50,
                background_color=self.themes[theme_name]['button_bg'],
                color=self.themes[theme_name]['button_text_color']
            )
            btn.bind(on_release=lambda instance, t=theme_name: self.change_theme(t, popup))
            grid.add_widget(btn)
        popup.content = grid
        popup.open()

    def change_theme(self, theme_name, popup):
        self.current_theme = theme_name
        theme = self.themes[theme_name]

        self.root.canvas.before.clear()
        with self.root.canvas.before:
            Color(*theme['main_bg'])
            Rectangle(pos=self.root.pos, size=self.root.size)

        self.root.ids.username_input.background_color = theme['input_bg']
        self.root.ids.username_input.foreground_color = theme['text_color']
        self.root.ids.message_input.background_color = theme['input_bg']
        self.root.ids.message_input.foreground_color = theme['text_color']

        self.root.ids.join_button.background_color = theme['button_bg']
        self.root.ids.join_button.color = theme['button_text_color']
        self.root.ids.theme_button.background_color = theme['button_bg']
        self.root.ids.theme_button.color = theme['button_text_color']
        self.root.ids.disconnect_button.background_color = theme['button_bg']
        self.root.ids.disconnect_button.color = theme['button_text_color']
        self.root.ids.reconnect_button.background_color = theme['button_bg']
        self.root.ids.reconnect_button.color = theme['button_text_color']
        self.root.ids.send_button.background_color = theme['send_button_bg']
        self.root.ids.send_button.color = theme['button_text_color']
        self.root.ids.clear_button.background_color = theme['button_bg']
        self.root.ids.clear_button.color = theme['button_text_color']

        for child in self.root.ids.chat_log.children:
            if isinstance(child, BoxLayout):
                is_own_message = "right" in child.children[0].halign
                child.children[0].canvas.before.clear()
                with child.children[0].canvas.before:
                    Color(*(theme['server_message_bg'] if child.children[0].text.startswith("[b]SERVER:[/b]") else theme['own_message_bg'] if is_own_message else theme['other_message_bg']))
                    RoundedRectangle(pos=child.children[0].pos, size=child.children[0].size, radius=[10])
                child.children[0].color = theme['text_color']

        popup.dismiss()

    def clear_chat(self):
        self.root.ids.chat_log.clear_widgets()
        with open("chat_log.txt", "w", encoding="utf-8") as file:
            file.write("")

if __name__ == "__main__":
    ChatApp().run()