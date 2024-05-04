import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog
import rsa

class CipherDecrypter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RSA Cipher Decrypter")
        self.setGeometry(100, 100, 500, 300)

        layout = QVBoxLayout()

        self.private_key_button = QPushButton("Select Private Key File")
        self.private_key_button.clicked.connect(self.select_private_key)
        layout.addWidget(self.private_key_button)

        self.clear_private_key_button = QPushButton("CLEAR Private Key File")
        self.clear_private_key_button.clicked.connect(self.clear_private_key)
        layout.addWidget(self.clear_private_key_button)

        self.private_key_label = QLabel()
        self.private_key_label.setWordWrap(True)
        self.private_key_label.setText("No private key file selected.")
        layout.addWidget(self.private_key_label)

        self.clear_cipher_button = QPushButton("Select Cipher File(s)")
        self.clear_cipher_button.clicked.connect(self.select_cipher_files)
        layout.addWidget(self.clear_cipher_button)

        self.clear_private_key_button = QPushButton("CLEAR Cipher File(s)")
        self.clear_private_key_button.clicked.connect(self.clear_cipher_files)
        layout.addWidget(self.clear_private_key_button)

        self.cipher_queue_label = QLabel()
        self.cipher_queue_label.setWordWrap(True)
        self.cipher_queue_label.setText("No cipher file(s) selected.")
        layout.addWidget(self.cipher_queue_label)

        self.decrypt_button = QPushButton("Decrypt")
        self.decrypt_button.clicked.connect(self.decrypt_ciphers)
        layout.addWidget(self.decrypt_button)

        self.clear_all_button = QPushButton("CLEAR All File(s)")
        self.clear_all_button.clicked.connect(self.clear_all_selections)
        layout.addWidget(self.clear_all_button)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.private_key = None
        self.cipher_files = []

    def select_private_key(self):
        options = QFileDialog.Options()
        # singlular file selection
        self.private_key, _ = QFileDialog.getOpenFileName(self, "Select Private Key File", "", "All Files (*)", options=options)
        if self.private_key:
            self.private_key_label.setText(f"Private key file selected: {self.private_key}")

    def select_cipher_files(self):
        options = QFileDialog.Options()
        # plural file selection
        new_ciphers = QFileDialog.getOpenFileNames(self, "Select Cipher File(s)", "", "All Files (*)", options=options)[0]
        for path in new_ciphers:
            if path not in self.cipher_files:
                self.cipher_files.append(path)

        if len(new_ciphers) > 0:
            self.cipher_queue_label.setText(f"{len(self.cipher_files)} cipher file(s) selected: {self.cipher_files}")

    def clear_private_key(self):
        # If the private key is not empty meaning there is a private key file selected
        if self.private_key:
            self.private_key = None
            self.private_key_label.setText("No private key file selected.")
            self.status_label.setText("Please select your private key file.")

    def clear_cipher_files(self):
        # If the list is not empty meaning there are cipher file(s) selected
        if self.cipher_files:
            self.cipher_files = []
            self.cipher_queue_label.setText("No cipher file(s) selected.")
            self.status_label.setText("Please select your binary cipher file(s).")

    def clear_all_selections(self):
        self.clear_private_key()
        self.clear_cipher_files()
        self.status_label.setText("")

    def decrypt_ciphers(self):
        if not self.private_key:
            self.status_label.setText("Please select your private key file.")
            QMessageBox.critical(self, "Error", "No private key file selected.")
            return
        elif not self.cipher_files:
            self.status_label.setText("Please select your binary cipher file(s).")
            QMessageBox.critical(self, "Error", "No binary cipher file(s) selected.")
            return

        with open(self.private_key, "rb") as key:
            privatekeydata = rsa.PrivateKey.load_pkcs1(key.read())

        for index, filename in enumerate(self.cipher_files, 1):
            with open(filename, "rb") as cipherfile, open(f'decrypted_text_{index}.txt', 'w') as output_file:
                current_cipher = rsa.decrypt(crypto=cipherfile.read(), priv_key=privatekeydata).decode()
                output_file.write(current_cipher)

        self.status_label.setText(f"{index} ciphers decrypted successfully.")

def gui_start():
    app = QApplication(sys.argv)
    window = CipherDecrypter()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    gui_start()
