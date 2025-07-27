import sys
import markdown
import datetime
import qtawesome as qta
import google.generativeai as genai

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLineEdit, QLabel,
    QMessageBox, QInputDialog, QScrollArea, QFrame, QTextBrowser
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QTextOption

from all_apis import route_all_apis

# Configure Gemini
genai.configure(api_key="AIzaSyCM10Ct_FKnlz37MRazEhEOEDkjywU8_cQ")
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=genai.GenerationConfig(temperature=0.5, max_output_tokens=2500)
)

_sessions = []

def get_sessions():
    return _sessions

def start_session(name):
    session = {
        "name": name,
        "messages": [],
        "chat": model.start_chat()
    }
    _sessions.append(session)
    return session

def get_session_by_name(name):
    for session in _sessions:
        if session["name"] == name:
            return session
    return None

def delete_session_by_name(name):
    global _sessions
    _sessions = [s for s in _sessions if s["name"] != name]

class ChatBubble(QTextBrowser):
    def __init__(self, text, is_user):
        super().__init__()
        self.setOpenExternalLinks(True)
        self.setReadOnly(True)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setMaximumWidth(600)

        self.setStyleSheet(f'''
            QTextBrowser {{
                background-color: {'#3f3f46' if is_user else '#27272a'};
                color: {'#f4f4f5' if is_user else '#e4e4e7'};
                border-radius: 12px;
                padding: 8px 12px;
                font-size: 14px;
            }}
        ''')

        html_content = markdown.markdown(text, extensions=['extra'])
        self.setHtml(html_content)
        self.adjustSize()
        self.setMinimumHeight(int(self.document().size().height()) + 10)

        self.setWindowOpacity(0.0)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(250)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.start()

class ChatHome(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fred")
        self.resize(1000, 640)
        self.session = None
        self.typing_label = QLabel("Fred is typing...")
        self.typing_label.setStyleSheet("color: #a1a1aa; font-style: italic;")
        self.typing_label.hide()
        self.is_dark_mode = True
        self.init_ui()
        self.set_styles()

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        left_layout = QVBoxLayout()
        self.session_list = QListWidget()
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon("fa5s.history").pixmap(16, 16))
        text_label = QLabel("  Sessions")

        row_layout = QHBoxLayout()
        row_layout.addWidget(icon_label)
        row_layout.addWidget(text_label)
        row_layout.addStretch()

        row_widget = QWidget()
        row_widget.setLayout(row_layout)

        left_layout.addWidget(row_widget)
        left_layout.addWidget(self.session_list)

        btn_new = QPushButton(qta.icon('fa5s.plus'), "  New")
        btn_new.clicked.connect(self.new_session)
        btn_continue = QPushButton(qta.icon('fa5s.play'), "  Continue")
        btn_continue.clicked.connect(self.continue_session)
        btn_delete = QPushButton(qta.icon('fa5s.trash'), "  Delete")
        btn_delete.clicked.connect(self.delete_session)

        btn_toggle_theme = QPushButton("Toggle Light/Dark Mode")
        btn_toggle_theme.clicked.connect(self.toggle_theme)

        for btn in [btn_new, btn_continue, btn_delete, btn_toggle_theme]:
            btn.setIconSize(btn.sizeHint())
            left_layout.addWidget(btn)

        right_layout = QVBoxLayout()
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_container = QVBoxLayout()
        chat_widget = QWidget()
        chat_widget.setLayout(self.chat_container)
        self.chat_scroll.setWidget(chat_widget)

        input_layout = QHBoxLayout()
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Type a message...")

        btn_send = QPushButton(qta.icon('fa5s.paper-plane'), "")
        btn_send.clicked.connect(self.send_message)

        input_layout.addWidget(self.entry)
        input_layout.addWidget(btn_send)

        right_layout.addWidget(QLabel("Chat"))
        right_layout.addWidget(self.chat_scroll)
        right_layout.addWidget(self.typing_label)
        right_layout.addLayout(input_layout)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 3)

        self.refresh_session_list()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.set_styles()

    def set_styles(self):
        if self.is_dark_mode:
            self.setStyleSheet("""QWidget {
                background-color: #1e1e20;
                color: #f4f4f5;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QListWidget {
                background-color: #2a2a2e;
                border: 1px solid #3a3a3e;
                color: #e4e4e7;
            }
            QPushButton {
                background-color: #3f3f46;
                color: #ffffff;
                border-radius: 5px;
                padding: 6px 10px;
            }
            QPushButton:hover {
                background-color: #52525b;
            }
            QLineEdit {
                background-color: #27272a;
                color: #f4f4f5;
                border: 1px solid #3f3f46;
                padding: 8px;
                border-radius: 5px;
            }
            QLabel {
                font-weight: bold;
                margin-bottom: 6px;
            }""")
        else:
            self.setStyleSheet("""QWidget {
                background-color: #ffffff;
                color: #000000;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QListWidget {
                background-color: #f5f5f5;
                border: 1px solid #cccccc;
                color: #000000;
            }
            QPushButton {
                background-color: #e0e0e0;
                color: #000000;
                border-radius: 5px;
                padding: 6px 10px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QLineEdit {
                background-color: #f0f0f0;
                color: #000000;
                border: 1px solid #cccccc;
                padding: 8px;
                border-radius: 5px;
            }
            QLabel {
                font-weight: bold;
                margin-bottom: 6px;
            }""")

    def refresh_session_list(self):
        self.session_list.clear()
        for session in get_sessions():
            self.session_list.addItem(session["name"])

    def new_session(self):
        name, ok = QInputDialog.getText(self, "New Session", "Enter a name:")
        if ok and name:
            self.session = start_session(name)
            self.clear_chat()
            self.refresh_session_list()

    def continue_session(self):
        selected = self.session_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Error", "Select a session first.")
            return
        name = selected.text()
        session_data = get_session_by_name(name)
        if not session_data:
            QMessageBox.warning(self, "Error", f"Session '{name}' not found.")
            return
        self.session = session_data
        self.load_messages()

    def delete_session(self):
        selected = self.session_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Error", "Select a session to delete.")
            return
        name = selected.text()
        confirm = QMessageBox.question(self, "Confirm", f"Delete session '{name}'?")
        if confirm == QMessageBox.StandardButton.Yes:
            delete_session_by_name(name)
            self.clear_chat()
            self.refresh_session_list()

    def clear_chat(self):
        while self.chat_container.count():
            child = self.chat_container.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.typing_label.hide()

    def load_messages(self):
        self.clear_chat()
        messages = self.session.get("messages", [])
        for msg in messages:
            self.add_chat_bubble(msg["user_message"], is_user=True)
            self.add_chat_bubble(msg["bot_response"], is_user=False)

    def add_chat_bubble(self, text, is_user):
        bubble = ChatBubble(text, is_user)
        wrapper = QHBoxLayout()
        if is_user:
            wrapper.addStretch()
            wrapper.addWidget(bubble)
        else:
            wrapper.addWidget(bubble)
            wrapper.addStretch()
        container = QWidget()
        container.setLayout(wrapper)
        self.chat_container.addWidget(container)
        QTimer.singleShot(0, lambda: self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()))

    def send_message(self):
        if not self.session:
            QMessageBox.warning(self, "No Session", "Start or continue a session first.")
            return
        user_text = self.entry.text().strip()
        if not user_text:
            return
        self.add_chat_bubble(user_text, is_user=True)
        self.entry.clear()
        self.typing_label.show()
        QTimer.singleShot(500, lambda: self.fake_typing(user_text))

    def fake_typing(self, user_text):
        response = route_all_apis(self.session, user_text)
        self.typing_label.hide()
        self.add_chat_bubble(response, is_user=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatHome()
    window.show()
    sys.exit(app.exec())