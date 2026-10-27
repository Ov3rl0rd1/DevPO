import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window

    function editEquipment(equipmentId) {
        equipmentForm.openForEdit(equipmentController.find(equipmentId))
    }

    width: 1040
    height: 760
    minimumWidth: 820
    minimumHeight: 680
    visible: true
    title: "Учёт сельскохозяйственной техники"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 16

        RowLayout {
            Layout.fillWidth: true
            spacing: 12

            ColumnLayout {
                Layout.fillWidth: true
                spacing: 2

                Label {
                    Layout.fillWidth: true
                    text: window.title
                    font.pixelSize: 24
                    font.bold: true
                }

                Label {
                    text: "Реестр машин и оборудования предприятия"
                    opacity: 0.7
                }
            }

            Button {
                text: "Добавить технику"
                highlighted: true
                onClicked: equipmentForm.openForCreate()
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 12

            Repeater {
                model: equipmentModel.statistics

                delegate: Frame {
                    required property var modelData

                    Layout.fillWidth: true
                    Layout.preferredWidth: 1

                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 2

                        Label {
                            text: modelData.value
                            font.pixelSize: 22
                            font.bold: true
                        }

                        Label {
                            Layout.fillWidth: true
                            text: modelData.title
                            elide: Text.ElideRight
                            opacity: 0.7
                        }
                    }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 8

            TextField {
                Layout.fillWidth: true
                placeholderText: "Поиск по названию или инвентарному номеру"
                onTextChanged: equipmentFilter.searchText = text
            }

            ComboBox {
                Layout.preferredWidth: 200
                model: ["Все типы"].concat(equipmentController.categories)
                onActivated: equipmentFilter.category = currentIndex > 0 ? currentText : ""
            }

            ComboBox {
                Layout.preferredWidth: 200
                model: ["Все состояния"].concat(equipmentController.statuses)
                onActivated: equipmentFilter.status = currentIndex > 0 ? currentText : ""
            }

            ComboBox {
                Layout.preferredWidth: 170
                model: equipmentFilter.sortOptions
                currentIndex: equipmentFilter.sortIndex
                onActivated: equipmentFilter.sortIndex = currentIndex
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true

            ListView {
                id: equipmentList

                anchors.fill: parent
                clip: true
                spacing: 8
                currentIndex: -1
                model: equipmentFilter

                ScrollBar.vertical: ScrollBar {}

                delegate: EquipmentCard {
                    width: equipmentList.width - 16
                    highlighted: ListView.isCurrentItem
                    equipmentName: model.name
                    category: model.category
                    inventoryNumber: model.inventoryNumber
                    status: model.status
                    location: model.location
                    responsible: model.responsible
                    year: model.year
                    hours: model.hours
                    condition: model.condition
                    active: model.active

                    onClicked: equipmentList.currentIndex = index
                    onDoubleClicked: window.editEquipment(model.equipmentId)
                    onEditRequested: window.editEquipment(model.equipmentId)
                    onDeleteRequested: deleteDialog.ask(model.equipmentId, model.name)
                }
            }

            Label {
                anchors.centerIn: parent
                width: parent.width - 40
                visible: equipmentList.count === 0
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.Wrap
                font.pixelSize: 16
                opacity: 0.7
                text: equipmentModel.count === 0
                    ? "Техника пока не зарегистрирована.\nНажмите «Добавить технику», чтобы создать первую запись."
                    : "По заданным условиям ничего не найдено.\nИзмените строку поиска или фильтры."
            }
        }
    }

    EquipmentForm {
        id: equipmentForm
    }

    DeleteDialog {
        id: deleteDialog

        onAccepted: equipmentController.remove(equipmentId)
    }

    Dialog {
        id: errorDialog

        anchors.centerIn: Overlay.overlay
        modal: true
        title: "Ошибка"
        standardButtons: Dialog.Ok

        Label {
            id: errorLabel
            wrapMode: Text.Wrap
        }
    }

    Connections {
        target: equipmentController

        function onErrorOccurred(message) {
            errorLabel.text = message
            errorDialog.open()
        }
    }
}
