import os
import glob
import subprocess
import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QFrame,
    QGraphicsDropShadowEffect
)


class OpenModelicaRunnerApp(QWidget):
    """Modern Desktop Application to execute compiled OpenModelica binaries with custom flags."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("OpenModelica GUI Launcher | FOSSEE Submission")
        self.resize(750, 600)
        self.setMinimumSize(650, 520)

        # Global Dark Neutral Theme Stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                color: #F8FAFC;
                font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            }
            QFrame#card {
                background-color: #1E293B;
                border-radius: 12px;
                border: 1px solid #334155;
            }
            QLabel {
                font-size: 13px;
                color: #94A3B8;
            }
            QLabel#headerTitle {
                font-size: 20px;
                font-weight: bold;
                color: #38BDF8;
            }
            QLabel#headerSubtitle {
                font-size: 12px;
                color: #64748B;
            }
            QLabel#fieldLabel {
                font-size: 13px;
                font-weight: 600;
                color: #E2E8F0;
            }
            QLineEdit {
                background-color: #0F172A;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px 14px;
                color: #F8FAFC;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #38BDF8;
                background-color: #0F172A;
            }
            QPushButton#browseBtn {
                background-color: #334155;
                color: #F8FAFC;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: 600;
            }
            QPushButton#browseBtn:hover {
                background-color: #475569;
            }
            QPushButton#runBtn {
                background-color: #0284C7;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 14px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton#runBtn:hover {
                background-color: #0369A1;
            }
            QPushButton#runBtn:pressed {
                background-color: #075985;
            }
            QTextEdit {
                background-color: #020617;
                border: 1px solid #1E293B;
                border-radius: 8px;
                color: #38BDF8;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                padding: 10px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        # 1. Header Section
        header_frame = QFrame()
        header_frame.setObjectName("card")
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(20, 16, 20, 16)
        
        title = QLabel("⚙️ OpenModelica Interactive Launcher")
        title.setObjectName("headerTitle")
        subtitle = QLabel("Simulate physical models dynamically with instant parameter configuration")
        subtitle.setObjectName("headerSubtitle")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)

        # 2. Main Config Card
        config_card = QFrame()
        config_card.setObjectName("card")
        config_layout = QVBoxLayout()
        config_layout.setContentsMargins(20, 20, 20, 20)
        config_layout.setSpacing(14)

        # Executable Path Field
        config_layout.addWidget(QLabel("Executable Program Path:", objectName="fieldLabel"))
        exe_layout = QHBoxLayout()
        self.app_input = QLineEdit()
        self.app_input.setPlaceholderText("Select OpenModelica executable (.exe)")
        
        default_exe = os.path.join(os.getcwd(), "TwoConnectedTanks.exe")
        if os.path.exists(default_exe):
            self.app_input.setText(default_exe)

        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("browseBtn")
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.clicked.connect(self.browse_file)

        exe_layout.addWidget(self.app_input)
        exe_layout.addWidget(browse_btn)
        config_layout.addLayout(exe_layout)

        # Time Inputs Layout
        time_layout = QHBoxLayout()
        time_layout.setSpacing(12)

        start_col = QVBoxLayout()
        start_col.addWidget(QLabel("Start Time (sec):", objectName="fieldLabel"))
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("e.g. 0")
        start_col.addWidget(self.start_input)

        stop_col = QVBoxLayout()
        stop_col.addWidget(QLabel("Stop Time (sec):", objectName="fieldLabel"))
        self.stop_input = QLineEdit()
        self.stop_input.setPlaceholderText("e.g. 4")
        stop_col.addWidget(self.stop_input)

        time_layout.addLayout(start_col)
        time_layout.addLayout(stop_col)
        config_layout.addLayout(time_layout)

        # Requirement Hint Badge
        hint_label = QLabel("⚡ Constraint: 0 ≤ Start Time < Stop Time < 5")
        hint_label.setStyleSheet("color: #F59E0B; font-size: 11px; font-weight: 500;")
        config_layout.addWidget(hint_label)

        # Run Button
        self.run_btn = QPushButton("🚀 Launch Simulation")
        self.run_btn.setObjectName("runBtn")
        self.run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_btn.clicked.connect(self.run_simulation)
        config_layout.addWidget(self.run_btn)

        config_card.setLayout(config_layout)
        layout.addWidget(config_card)

        # 3. Execution Console Output Card
        console_card = QFrame()
        console_card.setObjectName("card")
        console_layout = QVBoxLayout()
        console_layout.setContentsMargins(20, 16, 20, 16)
        
        console_title = QLabel("Execution Output Console", objectName="fieldLabel")
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("Simulation run outputs and execution logs will appear here...")

        console_layout.addWidget(console_title)
        console_layout.addWidget(self.log_area)
        console_card.setLayout(console_layout)
        
        layout.addWidget(console_card)

        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Executable Program",
            "",
            "Executable Files (*.exe);;All Files (*)",
        )
        if file_path:
            self.app_input.setText(file_path)

    def find_om_bin(self):
        om_home = os.environ.get("OPENMODELICAHOME")
        if om_home and os.path.exists(os.path.join(om_home, "bin")):
            return os.path.join(om_home, "bin")

        possible_dirs = glob.glob(r"C:\Program Files*\OpenModelica*\bin")
        if possible_dirs:
            return possible_dirs[0]

        om_bin = os.environ.get("OPENMODELICABIN")
        if om_bin and os.path.exists(om_bin):
            return om_bin

        return None

    def validate_inputs(self):
        exe_path = self.app_input.text().strip()
        start_str = self.start_input.text().strip()
        stop_str = self.stop_input.text().strip()

        if not exe_path or not os.path.exists(exe_path):
            QMessageBox.warning(
                self, "Input Error", "Please select a valid OpenModelica executable file."
            )
            return None, None, None

        try:
            start_time = int(start_str)
            stop_time = int(stop_str)
        except ValueError:
            QMessageBox.warning(
                self, "Input Error", "Start time and Stop time must be valid integers."
            )
            return None, None, None

        if not (0 <= start_time < stop_time < 5):
            QMessageBox.critical(
                self,
                "Validation Error",
                "Inputs must satisfy condition:\n\n 0 <= Start Time < Stop Time < 5",
            )
            return None, None, None

        return exe_path, start_time, stop_time

    def run_simulation(self):
        exe_path, start_time, stop_time = self.validate_inputs()
        if exe_path is None:
            return

        cmd = [
            exe_path,
            f"-startTime={start_time}",
            f"-stopTime={stop_time}",
        ]

        self.log_area.clear()
        self.log_area.append(f"► Running command:\n{' '.join(cmd)}\n")

        env = os.environ.copy()
        om_bin = self.find_om_bin()
        if om_bin:
            env["PATH"] = om_bin + os.pathsep + env.get("PATH", "")
            self.log_area.append(f"► Using OpenModelica Bin Path: {om_bin}\n")

        try:
            exe_dir = os.path.dirname(exe_path)
            result = subprocess.run(
                cmd, cwd=exe_dir, env=env, capture_output=True, text=True, check=True
            )
            self.log_area.append("--- Output Logs ---")
            self.log_area.append(result.stdout if result.stdout else "Simulation completed without console stdout.")
            QMessageBox.information(
                self, "Success", "OpenModelica Simulation completed successfully!"
            )
        except subprocess.CalledProcessError as e:
            self.log_area.append("--- Execution Error ---")
            if e.stdout:
                self.log_area.append(e.stdout)
            if e.stderr:
                self.log_area.append(e.stderr)
            else:
                self.log_area.append(str(e))
            QMessageBox.critical(
                self, "Execution Failed", "The executable exited with an error."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to run simulation: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenModelicaRunnerApp()
    window.show()
    sys.exit(app.exec())