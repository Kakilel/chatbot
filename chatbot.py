from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLineEdit,
    QMessageBox, QInputDialog, QLabel, QScrollArea, QFrame, QTextBrowser
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QTextOption
import qtawesome as qta
import markdown
import sys
import api

class ChatBubble(QTextBrowser):
    def __init__(self, text, is_user):
        super().__init__()
        self.setOpenExternalLinks(True)
        self.setOpenLinks(True)
        self.setReadOnly(True)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setMaximumWidth(400)
        self.setStyleSheet(f'''
            QTextBrowser {{
                background-color: {'#3D5A80' if is_user else '#98C1D9'};
                color: {'#ffffff' if is_user else '#000000'};
                border-radius: 15px;
                padding: 8px 12px;
            }}
        ''')

        html_content = markdown.markdown(text, extensions=['extra'])
        self.setHtml(html_content)
        self.adjustSize()
        self.setMinimumHeight(int(self.document().size().height()) + 10)

        # Animation
        self.setGraphicsEffect(None)
        self.setWindowOpacity(0.0)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(300)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.start()

class ChatHome(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fred (PyQt6)")
        self.resize(950, 620)
        self.session = None
        self.typing_timer = None
        self.typing_label = QLabel("Bot is typing...")
        self.typing_label.setStyleSheet("color: #cccccc; font-style: italic;")
        self.typing_label.hide()
        self.init_ui()
        self.set_styles()

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Sidebar
        left_layout = QVBoxLayout()
        self.session_list = QListWidget()
        left_layout.addWidget(QLabel("\U0001F4D1 Sessions"))
        left_layout.addWidget(self.session_list)

        btn_new = QPushButton(qta.icon('fa5s.plus'), "  New")
        btn_new.clicked.connect(self.new_session)
        btn_continue = QPushButton(qta.icon('fa5s.play'), "  Continue")
        btn_continue.clicked.connect(self.continue_session)
        btn_delete = QPushButton(qta.icon('fa5s.trash'), "  Delete")
        btn_delete.clicked.connect(self.delete_session)

        for btn in [btn_new, btn_continue, btn_delete]:
            btn.setIconSize(btn.sizeHint())
            left_layout.addWidget(btn)

        # Right layout
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

        right_layout.addWidget(QLabel("\U0001F4AC Chat"))
        right_layout.addWidget(self.chat_scroll)
        right_layout.addWidget(self.typing_label)
        right_layout.addLayout(input_layout)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 3)

        self.refresh_session_list()

    def set_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0F1C2E;
                color: #FFFFFF;
                font-family: Arial;
                font-size: 14px;
            }
            QListWidget {
                background-color: #1F2B3E;
                border: 1px solid #374357;
                color: #e0e0e0;
            }
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #3D5A80, stop:1 #1F2B3E);
                color: #FFFFFF;
                border-radius: 5px;
                padding: 8px 10px;
            }
            QPushButton:hover {
                background-color: #4D648D;
            }
            QLineEdit {
                background-color: #2B3A50;
                color: #FFFFFF;
                border: 1px solid #374357;
                padding: 6px;
            }
            QLabel {
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)

    def refresh_session_list(self):
        self.session_list.clear()
        for session in api.get_sessions():
            self.session_list.addItem(session['name'])

    def new_session(self):
        name, ok = QInputDialog.getText(self, "New Session", "Enter a name:")
        if ok and name:
            self.session = api.start_session(name)
            self.clear_chat()
            self.refresh_session_list()

    def continue_session(self):
        selected = self.session_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Error", "Select a session first.")
            return
        name = selected.text()
        session_data = api.get_session_by_name(name)
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
            api.delete_session_by_name(name)
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
        
        messages = self.session.get('messages') or []
        for msg in messages:

            self.add_chat_bubble(msg['user_message'], is_user=True)
            self.add_chat_bubble(msg['bot_response'], is_user=False)

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

        QTimer.singleShot(1000, lambda: self.fake_typing(user_text))

    def fake_typing(self, user_text):
        response = api.send_to_session(self.session, user_text)
        self.typing_label.hide()
        self.add_chat_bubble(response, is_user=False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatHome()
    window.show()
    sys.exit(app.exec())
