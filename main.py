import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from ssh_logic import SSHLogic

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ssh_logic = SSHLogic()
    engine.rootContext().setContextProperty("sshLogic", ssh_logic)
    engine.load("./qml/main.qml")
    if not engine.rootObjects(): sys.exit(-1)
    sys.exit(app.exec())