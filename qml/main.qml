import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    width: 800
    height: 600
    visible: true
    title: "SSH客户端"

    TextArea{
        id: contentDisplay
        anchors.top:statusContainer.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 10
        readOnly: true
        placeholderText:"SSH连接成功后，可通过[操作]菜单栏查看远程主机信息···"
        font.pixelSize: 12
        background:Rectangle{
        color: "#f5f5f5"
        border.color: "#ddd"
        }
    }
    Button{
        id:clearBtn
        text: "清空输出"
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 10
        onClicked:sshLogic.clear_output()
        font.pixelSize: 12
        padding: 4
    }
    // 连接状态和断开按钮容器（垂直排列）
    Column {
        id: statusContainer
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.margins: 10
        spacing: 8

    Row {
        id: statusIndicator
        spacing: 5

        Text {
            text: "连接状态"
            font.bold: true
            color: "#333"
        }

        Rectangle {
            id: statusIcon
            width: 12
            height: 12
            radius: 6
            color: "red"
            Connections {
                target: sshLogic
                function onConnectionStatus(status) {
                    statusIcon.color = (status === "connected") ? "green" : "red";
                    // 连接成功时显示断开按钮，否则隐藏
                    disconnectBtn.visible = (status === "connected");
                    operationMenu.enabled = (status === "connected");
                }
            }
        }
    }

    // 断开连接按钮（默认隐藏，连接成功后显示）
    Button {
            id: disconnectBtn
            text: "断开连接"
            visible: false  // 初始隐藏
            onClicked: sshLogic.disconnect_ssh()
            padding: 4
            font.pixelSize: 12
        }
    }

    Dialog{
        id:sshDialog
        title: "SSH连接设置"
        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel
        

        ColumnLayout { 
            anchors.fill: parent
            spacing: 12
            Layout.margins: 15

            RowLayout{
                Label{text:"主机名:";Layout.alignment: Qt.AlignVCenter}
                TextField{
                    id:hostInput
                    placeholderText: "例如192.168.1.1"
                    Layout.fillWidth: true
                }
            }
            RowLayout{
                Label{text:"端口:";Layout.alignment: Qt.AlignVCenter}
                TextField{
                    id:portInput
                    text: "22"
                    placeholderText: "默认22"
                    Layout.fillWidth: true
                    validator: IntValidator{
                        bottom: 1
                        top: 65535
                    }
                }
            }
            RowLayout{
                Label{text:"用户名:";Layout.alignment: Qt.AlignVCenter}
                TextField{
                    id:userInput
                    placeholderText: "例如：root"
                    Layout.fillWidth: true
                }
            }
            RowLayout{
                Label{text:"密码:";Layout.alignment: Qt.AlignVCenter}
                TextField{
                    id:passInput
                    echoMode: TextField.Password
                    placeholderText: "请输入密码"
                    Layout.fillWidth: true
                }
            }
        }
        onAccepted: {
            const port=portInput.text ? parseInt(portInput.text) : 22;
            sshLogic.connect_ssh(
                hostInput.text,
                port,
                userInput.text,
                passInput.text
            )
        }
    }
    menuBar: MenuBar {
        Menu {
            title: "连接主机"
            MenuItem {
                text: "SSH连接"
                onTriggered: sshDialog.open()
            }
            MenuItem {
                text: "退出"
                onTriggered: sshLogic.exit_app()
            }
        }
        Menu{
            id:operationMenu
            title: "操作"
            enabled: false
            MenuItem{
                text:"显示远程当前路径"
                onTriggered: sshLogic.get_remote_current_path()
            }
            MenuItem{
            text:"显示远程目录文件"
            onTriggered: sshLogic.get_remote_dir_files()
            }
        }
    }
    Connections {
        target: sshLogic
        function onShowContentSignal(content){
            contentDisplay.text =content;
        }
        function onClearContentSignal(){
            contentDisplay.text = "";
        }
    }
}