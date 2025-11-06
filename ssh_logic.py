import sys
import paramiko
from PySide6.QtCore import QObject, Slot,Signal
from PySide6.QtWidgets import QApplication,QMessageBox
import cmds

class SSHLogic(QObject):
    connectionStatus=Signal(str)
    showContentSignal=Signal(str)
    clearContentSignal=Signal()
    _ssh_connection = None


    @Slot(str, int,str, str)
    def connect_ssh(self,hostname,port, username, password):
        # 先断开可能存在的旧连接
        if self._ssh_connection:
            self.disconnect_ssh()

        if not hostname or not username:
            self.show_error("输入错误", "主机名和用户名不能为空!")
            self.connectionStatus.emit("disconnected")
            return
        if not (1 <= port <= 65535):
            self.show_error("端口错误", "端口号必须在1-65535之间！")
            self.connectionStatus.emit("disconnected")
            return
        try: 
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname, port=port, username=username, password=password, timeout=10)
            # 保存连接实例
            self._ssh_connection = ssh
            self.show_info("连接成功", f"成功连接到{hostname} 用户名为{username}!")
            self.connectionStatus.emit("connected")
        except Exception as e:
            self._ssh_connection = None  # 连接失败时清空实例
            # 所有异常分支都发送未连接状态
            self.connectionStatus.emit("disconnected")  # 新增：发送未连接状态
            if isinstance(e, paramiko.AuthenticationException):
                self.show_error("认证失败", "用户名或密码错误!")
            elif isinstance(e, paramiko.SSHException):
                self.show_error("SSH协议错误", f"无法建立SSH连接: {e}")
            elif isinstance(e, TimeoutError):
                self.show_error("连接超时", "连接超时!")
            else:
                self.show_error("连接错误", f"无法连接到{hostname}: {e}")
    @Slot()
    def disconnect_ssh(self):
        if self._ssh_connection:
            try:
                self._ssh_connection.close()  # 关闭SSH连接
                self._ssh_connection = None  # 清空连接实例
                self.show_info("断开成功", "已断开与SSH主机的连接")
                self.connectionStatus.emit("disconnected")  # 更新状态
            except Exception as e:
                self.show_error("断开失败", f"断开连接时出错: {e}")
        else:
            self.show_info("未连接", "当前没有活跃的SSH连接")
    @Slot()
    def exit_app(self):
        print("退出应用程序...")
        if self._ssh_connection:
            self._ssh_connection.close()
        QApplication.quit()
    def show_error(self, title, message):
        QMessageBox.critical(None, title, message)

    def show_info(self, title, message):
        QMessageBox.information(None, title, message)
    @Slot()
    def get_remote_current_path(self):
        if not self._ssh_connection:
            self.show_error("未连接", "请先连接到SSH主机!")
            return
        remote_path = cmds.get_remote_current_path(self._ssh_connection)
        self.showContentSignal.emit(f"远程主机当前路径:\n{remote_path}")
    @Slot()
    def get_remote_dir_files(self):
        if not self._ssh_connection:
            self.show_error("未连接", "请先连接到SSH主机!")
            return
        remote_files = cmds.get_remote_dir_files(self._ssh_connection)
        self.showContentSignal.emit(f"远程主机文件列表:\n{remote_files}")
    @Slot()
    def clear_output(self):
        self.clearContentSignal.emit()