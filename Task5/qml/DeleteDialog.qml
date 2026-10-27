import QtQuick
import QtQuick.Controls

Dialog {
    id: dialog

    property int equipmentId
    property string equipmentName

    function ask(targetId, targetName) {
        equipmentId = targetId
        equipmentName = targetName
        open()
    }

    anchors.centerIn: Overlay.overlay
    modal: true
    title: "Удаление техники"

    Label {
        text: `Удалить «${dialog.equipmentName}»?`
    }

    footer: DialogButtonBox {
        Button {
            text: "Отмена"
            DialogButtonBox.buttonRole: DialogButtonBox.RejectRole
        }

        Button {
            text: "Удалить"
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
        }
    }
}
