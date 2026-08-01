import os
import subprocess
import sys
from PyQt6.QtCore import Qt
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
)


class OpenModelicaRunnerApp(QWidget):
    """Desktop Application to execute compiled OpenModelica binaries with custom flags."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("FOSSEE OpenModelica GUI Launcher")
        self.setMinimumSize(550, 420)

        main_layout = QVBoxLayout()

        # 1. Executable Field Selection
        app_layout = QHBoxLayout()
        app_label = QLabel("Executable:")
        self.app_input = QLineEdit()
        self.app_input.setPlaceholderText("Select OpenModelica compiled executable (.exe)")
        
        # Pre-fill with current folder's executable if present
        default_exe = os.path.join(os.getcwd(), "TwoConnectedTanks.exe")
        if os.path.exists(default_exe):
            self.app_input.setText(default_exe)

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)

        app_layout.addWidget(app_label)
        app_layout.addWidget(self.app_input)
        app_layout.addWidget(browse_btn)
        main_layout.addLayout(app_layout)

        # 2. Start Time Input
        start_layout = QHBoxLayout()
        start_label = QLabel("Start Time (Integer):")
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("e.g. 0")
        start_layout.addWidget(start_label)
        start_layout.addWidget(self.start_input)
        main_layout.addLayout(start_layout)

        # 3. Stop Time Input
        stop_layout = QHBoxLayout()
        stop_label = QLabel("Stop Time (Integer):")
        self.stop_input = QLineEdit()
        self.stop_input.setPlaceholderText("e.g. 4")
        stop_layout.addWidget(stop_label)
        stop_layout.addWidget(self.stop_input)
        main_layout.addLayout(stop_layout)

        # 4. Action Button
        self.run_btn = QPushButton("Run Simulation")
        self.run_btn.setStyleSheet(
            "font-weight: bold; background-color: #007ACC; color: white; padding: 10px; font-size: 14px;"
        )
        self.run_btn.clicked.connect(self.run_simulation)
        main_layout.addWidget(self.run_btn)

        # 5. Output Console/Log Window
        main_layout.addWidget(QLabel("Execution Logs:"))
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        main_layout.addWidget(self.log_area)

        self.setLayout(main_layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Executable Program",
            "",
            "Executable Files (*.exe);;All Files (*)",
        )
        if file_path:
            self.app_input.setText(file_path)

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

        # Task Constraint: 0 <= start time < stop time < 5
        if not (0 <= start_time < stop_time < 5):
            QMessageBox.critical(
                self,
                "Validation Error",
                "Inputs must satisfy the screening condition:\n\n 0 <= Start Time < Stop Time < 5",
            )
            return None, None, None

        return exe_path, start_time, stop_time

    def run_simulation(self):
        exe_path, start_time, stop_time = self.validate_inputs()
        if exe_path is None:
            return

        # Prepare parameters using OpenModelica flags
        cmd = [
            exe_path,
            f"-override=startTime={start_time},stopTime={stop_time}",
        ]

        self.log_area.clear()
        self.log_area.append(f"Running command:\n{' '.join(cmd)}\n")

        try:
            # Execute simulation binary in working directory of executable
            exe_dir = os.path.dirname(exe_path)
            result = subprocess.run(
                cmd, cwd=exe_dir, capture_output=True, text=True, check=True
            )
            self.log_area.append("--- Output Logs ---")
            self.log_area.append(result.stdout)
            QMessageBox.information(
                self, "Success", "OpenModelica Simulation completed successfully!"
            )
        except subprocess.CalledProcessError as e:
            self.log_area.append("--- Execution Error ---")
            self.log_area.append(e.stderr if e.stderr else str(e))
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