from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout, QWidget


class CombatPanel(QFrame):
    def __init__(self, title=None, parent=None):
        super().__init__(parent)
        self.setObjectName("combat_panel")
        self.setStyleSheet(
            """
            QFrame#combat_panel {
                background: #1d2229;
                border: 1px solid #4d5865;
                border-radius: 10px;
                color: #edf3f8;
            }
            """
        )

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(14, 12, 14, 12)
        self.layout.setSpacing(10)

        if title:
            self.title = QLabel(title)
            self.title.setStyleSheet(
                "font-weight: 700; letter-spacing: 1px; color: #dfeaf6; font-size: 13px;"
            )
            self.title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.layout.addWidget(self.title)

        self.content = QWidget()
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.layout.addWidget(self.content)
