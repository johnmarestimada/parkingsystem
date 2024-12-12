from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QApplication
from PyQt5.QtCore import QThread, pyqtSignal
import sys
from DataBaseOperation import DBOperation
from HomeWindow import HomeScreen


class LoginWorker(QThread):
    login_result = pyqtSignal(bool)

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def run(self):
        try:
            dboperation = DBOperation()
            result = dboperation.doAdminLogin(self.username, self.password)
            self.login_result.emit(result)
        except Exception as e:
            print(f"Error during login: {e}")
            self.login_result.emit(False)


class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Login")
        self.resize(300, 100)
        layout = QVBoxLayout()

        label_username = QLabel("Username : ")
        label_username.setStyleSheet("color:#000;padding:8px 0px;font-size:18px;")
        self.input_username = QLineEdit()
        self.input_username.setStyleSheet("padding:5px;font-size:17px")
        label_password = QLabel("Password : ")
        label_password.setStyleSheet("color:#000;padding:8px 0px;font-size:18px;")
        self.error_msg = QLabel()
        self.error_msg.setStyleSheet("color:red;padding:8px 0px;font-size:18px;text-align:center")
        self.input_password = QLineEdit()
        self.input_password.setStyleSheet("padding:5px;font-size:17px")
        self.input_password.setEchoMode(QLineEdit.Password)  # Hide password input

        self.btn_login = QPushButton("Login")
        self.btn_login.setStyleSheet("padding:5px;font-size:20px;background:green;color:#fff")
        layout.addWidget(label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.error_msg)
        layout.addStretch()
        self.btn_login.clicked.connect(self.showHome)
        self.setLayout(layout)

    def showLoginScreen(self):
        self.show()

    def showHome(self):
        if self.input_username.text() == "":
            self.error_msg.setText("Please Enter Username")
            return

        if self.input_password.text() == "":
            self.error_msg.setText("Please Enter Password")
            return

        self.error_msg.setText("Logging in...")  # Immediate feedback to the user
        self.btn_login.setEnabled(False)  # Disable login button

        # Create and start the worker thread
        self.worker = LoginWorker(self.input_username.text(), self.input_password.text())
        self.worker.login_result.connect(self.handleLoginResult)
        self.worker.finished.connect(lambda: self.btn_login.setEnabled(True))  # Re-enable button after login process
        self.worker.start()

    def handleLoginResult(self, success):
        if success:
            self.error_msg.setText("Login Successful")
            self.close()
            self.home = HomeScreen()
            self.home.show()
        else:
            self.error_msg.setText("Invalid Login Details")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginScreen()
    login.showLoginScreen()
    sys.exit(app.exec_())
