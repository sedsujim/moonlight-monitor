#!/usr/bin/env python3

import sys
import os
import json
import psutil
import subprocess
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QProgressBar, QFrame, QPushButton, QComboBox, QColorDialog
)
from PySide6.QtGui import QFont, QColor, QAction
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve

CONFIG_PATH = os.path.expanduser("~/.config/moonlight/config.json")

DEFAULT_CONFIG = {
    "theme": "dark",
    "primary_color": "#4fc3f7",
    "refresh_interval": 1000,
    "streaming_mode": False,
    "autostart": False
}


def load_config():
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=4)


class MetricCard(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setObjectName("card")
        self.title = QLabel(title)
        self.value = QLabel("--")
        self.bar = QProgressBar()

        self.title.setFont(QFont("Inter", 10))
        self.value.setFont(QFont("Inter", 22, QFont.Bold))
        self.bar.setFixedHeight(6)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.value)
        layout.addWidget(self.bar)

    def update(self, text, percent):
        self.value.setText(text)
        self.bar.setValue(int(percent))


class Moonlight(QWidget):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.setWindowTitle("Moonlight Monitor")
        self.setFixedSize(520, 440)

        self.cpu = MetricCard("CPU")
        self.ram = MetricCard("RAM")
        self.gpu = MetricCard("GPU")
        self.disk = MetricCard("Disk")

        self.settings_button = QPushButton("⚙")
        self.settings_button.setFixedWidth(32)
        self.settings_button.clicked.connect(self.open_settings)

        header = QHBoxLayout()
        header.addWidget(QLabel("Moonlight Monitor"))
        header.addStretch()
        header.addWidget(self.settings_button)

        grid = QVBoxLayout()
        grid.addWidget(self.cpu)
        grid.addWidget(self.ram)
        grid.addWidget(self.gpu)
        grid.addWidget(self.disk)

        main = QVBoxLayout(self)
        main.addLayout(header)
        main.addLayout(grid)

        self.apply_theme()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(self.config["refresh_interval"])

    def apply_theme(self):
        dark = self.config["theme"] == "dark"
        primary = self.config["primary_color"]

        self.setStyleSheet(f"""
        QWidget {{
            background-color: {"#1e1e2e" if dark else "#f5f5f5"};
            color: {"#ffffff" if dark else "#000000"};
            font-family: Inter;
        }}
        QFrame#card {{
            background-color: {"#2d2d44" if dark else "#ffffff"};
            border-radius: 10px;
            padding: 8px;
        }}
        QProgressBar {{
            background-color: #444;
            border-radius: 3px;
        }}
        QProgressBar::chunk {{
            background-color: {primary};
            border-radius: 3px;
        }}
        QPushButton {{
            background: transparent;
            border: none;
            font-size: 16px;
        }}
        """)

    def update_metrics(self):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        self.cpu.update(f"{cpu:.1f}%", cpu)
        self.ram.update(f"{mem.percent:.1f}%", mem.percent)
        self.disk.update(f"{disk.percent:.1f}%", disk.percent)

        gpu_usage = 0
        try:
            out = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
                timeout=1
            )
            gpu_usage = float(out.decode().strip())
        except:
            pass

        if gpu_usage > 0:
            self.gpu.update(f"{gpu_usage:.1f}%", gpu_usage)
        else:
            self.gpu.update("N/A", 0)

    def open_settings(self):
        self.settings = SettingsWindow(self)
        self.settings.show()


class SettingsWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.config = parent.config
        self.setWindowTitle("Settings")
        self.setFixedSize(300, 260)

        self.theme = QComboBox()
        self.theme.addItems(["dark", "light"])
        self.theme.setCurrentText(self.config["theme"])

        self.color = QPushButton("Primary Color")
        self.color.clicked.connect(self.pick_color)

        self.streaming = QComboBox()
        self.streaming.addItems(["off", "on"])
        self.streaming.setCurrentIndex(1 if self.config["streaming_mode"] else 0)

        self.save = QPushButton("Save")
        self.save.clicked.connect(self.apply)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Theme"))
        layout.addWidget(self.theme)
        layout.addWidget(self.color)
        layout.addWidget(QLabel("Streaming mode"))
        layout.addWidget(self.streaming)
        layout.addStretch()
        layout.addWidget(self.save)

    def pick_color(self):
        color = QColorDialog.getColor(QColor(self.config["primary_color"]), self)
        if color.isValid():
            self.config["primary_color"] = color.name()

    def apply(self):
        self.config["theme"] = self.theme.currentText()
        self.config["streaming_mode"] = self.streaming.currentText() == "on"
        self.config["refresh_interval"] = 2000 if self.config["streaming_mode"] else 1000
        save_config(self.config)
        self.parent.config = self.config
        self.parent.timer.setInterval(self.config["refresh_interval"])
        self.parent.apply_theme()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Moonlight()
    w.show()
    sys.exit(app.exec())
