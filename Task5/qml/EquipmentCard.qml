import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ItemDelegate {
    id: card

    property string equipmentName
    property string category
    property string inventoryNumber
    property string status
    property string location
    property string responsible
    property int year
    property int hours
    property int condition
    property bool active

    readonly property color statusColor: ({
        "Исправна": "#2e7d32",
        "Требует обслуживания": "#e65100",
        "В ремонте": "#c62828",
        "Списана": "#616161"
    })[status] ?? "#616161"

    signal editRequested()
    signal deleteRequested()

    padding: 14
    leftPadding: 26

    background: Rectangle {
        radius: 8
        color: card.hovered ? card.palette.alternateBase : card.palette.base
        border.width: card.highlighted ? 2 : 1
        border.color: card.highlighted ? card.palette.highlight : card.palette.mid

        Rectangle {
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.margins: 10
            width: 5
            radius: 2
            color: card.statusColor
        }
    }

    contentItem: RowLayout {
        spacing: 16

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 4

            Label {
                Layout.fillWidth: true
                text: card.equipmentName
                font.pixelSize: 16
                font.bold: true
                elide: Text.ElideRight
            }

            Label {
                Layout.fillWidth: true
                text: `${card.category} · инв. № ${card.inventoryNumber} · ${card.year} г.`
                elide: Text.ElideRight
            }

            Label {
                Layout.fillWidth: true
                text: `${card.location || "—"} · ${card.responsible || "—"} · наработка ${card.hours} м/ч`
                elide: Text.ElideRight
                opacity: 0.7
            }
        }

        ColumnLayout {
            Layout.fillWidth: false
            Layout.preferredWidth: 200
            spacing: 6

            Label {
                text: card.status
                color: "white"
                font.bold: true
                leftPadding: 10
                rightPadding: 10
                topPadding: 3
                bottomPadding: 3

                background: Rectangle {
                    radius: height / 2
                    color: card.statusColor
                }
            }

            ProgressBar {
                Layout.fillWidth: true
                from: 0
                to: 100
                value: card.condition
            }

            Label {
                text: `Состояние ${card.condition}% · ${card.active ? "в эксплуатации" : "не эксплуатируется"}`
                font.pixelSize: 12
                opacity: 0.7
            }
        }

        Button {
            text: "Редактировать"
            onClicked: card.editRequested()
        }

        Button {
            text: "Удалить"
            onClicked: card.deleteRequested()
        }
    }
}
