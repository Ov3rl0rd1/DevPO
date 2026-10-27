import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window

    width: 560
    height: 640
    minimumWidth: 460
    minimumHeight: 600
    visible: true
    title: "Карточка объекта учёта: Оборудование"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12

        GridLayout {
            Layout.fillWidth: true
            columns: 2
            columnSpacing: 12
            rowSpacing: 8

            Label {
                text: "Название объекта*:"
            }

            TextField {
                id: nameField
                Layout.fillWidth: true
                placeholderText: "Например, Токарный станок ТС-16"
                text: cardViewModel.name
                onTextEdited: cardViewModel.name = text
            }

            Label {
                text: "Инвентарный номер:"
            }

            TextField {
                Layout.fillWidth: true
                placeholderText: "Например, INV-00123"
                text: cardViewModel.inventory
                onTextEdited: cardViewModel.inventory = text
            }

            Label {
                text: "Тип оборудования:"
            }

            ComboBox {
                Layout.fillWidth: true
                model: cardViewModel.equipmentTypes
                currentIndex: cardViewModel.typeIndex
                onActivated: cardViewModel.typeIndex = currentIndex
            }

            Label {
                text: "Количество:"
            }

            RowLayout {
                spacing: 8

                SpinBox {
                    from: 0
                    to: 1000
                    editable: true
                    value: cardViewModel.quantity
                    onValueModified: cardViewModel.quantity = value
                }

                Label {
                    text: "шт."
                }
            }

            Label {
                text: "Статус:"
            }

            CheckBox {
                text: "В эксплуатации"
                checked: cardViewModel.active
                onToggled: cardViewModel.active = checked
            }

            Label {
                text: "Степень износа:"
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 8

                Slider {
                    Layout.fillWidth: true
                    from: 0
                    to: 100
                    stepSize: 1
                    snapMode: Slider.SnapAlways
                    value: cardViewModel.wear
                    onMoved: cardViewModel.wear = value
                }

                Label {
                    Layout.minimumWidth: 40
                    text: `${cardViewModel.wear}%`
                }
            }

            Label {
                Layout.alignment: Qt.AlignTop
                Layout.topMargin: 6
                text: "Примечания:"
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.preferredHeight: 80

                TextArea {
                    placeholderText: "Дополнительные сведения об объекте"
                    wrapMode: TextArea.Wrap
                    text: cardViewModel.notes
                    onTextChanged: cardViewModel.notes = text
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 8

            Button {
                Layout.fillWidth: true
                text: "Сохранить"
                enabled: cardViewModel.canSave
                onClicked: cardViewModel.save()
            }

            Button {
                Layout.fillWidth: true
                text: "Очистить"
                onClicked: {
                    cardViewModel.clear()
                    nameField.forceActiveFocus()
                }
            }
        }

        Label {
            text: "Предпросмотр карточки:"
        }

        Frame {
            Layout.fillWidth: true

            Label {
                width: parent.width
                wrapMode: Text.Wrap
                text: cardViewModel.preview
            }
        }

        Item {
            Layout.fillHeight: true
        }
    }

    footer: ToolBar {
        Label {
            anchors.fill: parent
            leftPadding: 12
            verticalAlignment: Text.AlignVCenter
            text: cardViewModel.statusMessage
        }
    }

    Dialog {
        id: savedDialog

        anchors.centerIn: Overlay.overlay
        modal: true
        title: "Сохранено"
        standardButtons: Dialog.Ok

        Label {
            text: "Карточка объекта успешно сохранена."
        }
    }

    Connections {
        target: cardViewModel

        function onSaved() {
            savedDialog.open()
        }
    }
}
