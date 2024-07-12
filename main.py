import numpy as np
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class ImpedanceCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.width_label = None
        self.width_entry = None
        self.height_label = None
        self.height_entry = None
        self.isolation_label = None
        self.isolation_entry = None
        self.er_label = None
        self.er_entry = None
        self.calc_button = None
        self.result_label = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.width_label = QLabel("Trace Width (mm):")
        self.width_entry = QLineEdit()
        layout.addWidget(self.width_label)
        layout.addWidget(self.width_entry)

        self.height_label = QLabel("Trace Height (mm):")
        self.height_entry = QLineEdit()
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_entry)

        self.isolation_label = QLabel("Isolation Height (mm):")
        self.isolation_entry = QLineEdit()
        layout.addWidget(self.isolation_label)
        layout.addWidget(self.isolation_entry)

        self.er_label = QLabel("Dielectric Constant:")
        self.er_entry = QLineEdit()
        layout.addWidget(self.er_label)
        layout.addWidget(self.er_entry)

        self.calc_button = QPushButton("Calculate Impedance")
        self.calc_button.clicked.connect(self.calculate_impedance)
        layout.addWidget(self.calc_button)

        self.result_label = QLabel("Impedance: ")
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.setWindowTitle("PCB Trace Impedance Calculator")

    def calculate_impedance(self):
        try:
            w = float(self.width_entry.text()) / 1000
            t = float(self.height_entry.text()) / 1000
            h = float(self.isolation_entry.text()) / 1000
            er = float(self.er_entry.text())

            print(f"track_width = {w}, track_height = {t}, isolation_height = {h}, er = {er}")

            w_eff = w + (1.25 * t / np.pi) * (1 + np.log(4 * np.pi * w / t))

            u = w_eff / h
            a = 1 + (1 / 49) * np.log((u ** 4 + (u / 52) ** 2) / (u ** 4 + 0.432)) + (1 / 18.7) * np.log(
                1 + (u / 18.1) ** 3)
            b = 0.564 * ((er - 0.9) / (er + 3)) ** 0.053
            e_eff = ((er + 1) / 2) + ((er - 1) / 2) * (1 + 10 / u) ** (-a * b)

            print(f"Effective width = {w_eff}, Effective dielectric constant = {e_eff}")

            if u <= 1:
                z0 = (60 / np.sqrt(e_eff)) * np.log(8 / u + 0.25 * u)
            else:
                z0 = (120 * np.pi) / (np.sqrt(e_eff) * (u + 1.393 + 0.667 * np.log(u + 1.444)))

            print(f"z0 = {z0}")
            self.result_label.setText(f"Impedance: {z0:.2f} Ω")
        except ValueError:
            self.result_label.setText("Error: Enter numerical values")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            self.result_label.setText(f"Error: {str(e)}")


if __name__ == "__main__":
    app = QApplication([])
    window = ImpedanceCalculator()
    window.show()
    app.exec()
