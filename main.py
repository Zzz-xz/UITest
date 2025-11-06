import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from ssh_logic import SSHLogic

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ssh_logic = SSHLogic()
    engine.rootContext().setContextProperty("sshLogic", ssh_logic)
    # 获取 QML 文件的正确路径（适配打包后的单文件模式）
    qml_path = os.path.join(os.path.dirname(sys.executable), "qml", "main.qml")
    # 若打包为单文件，sys.executable 是临时目录的路径，需确保 qml 目录存在
    if not os.path.exists(qml_path):
        # 回退到开发环境的相对路径（调试用）
        qml_path = os.path.join(os.path.dirname(__file__), "qml", "main.qml")
    
    engine.load(qml_path)
    if not engine.rootObjects(): sys.exit(-1)
    sys.exit(app.exec())