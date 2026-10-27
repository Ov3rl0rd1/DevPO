import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: form

    property int equipmentId: 0
    property string errorText: ""

    readonly property bool canSave: nameField.text.trim() !== "" && inventoryField.text.trim() !== ""

    function openForCreate() {
        equipmentId = 0
        fill(equipmentController.defaults)
        open()
    }

    function openForEdit(equipment) {
        equipmentId = equipment.id
        fill(equipment)
        open()
    }

    function fill(equipment) {
        nameField.text = equipment.name
        categoryBox.currentIndex = categoryBox.find(equipment.category)
        inventoryField.text = equipment.inventory_number
        yearBox.value = equipment.year
        statusBox.currentIndex = statusBox.find(equipment.status)
        locationField.text = equipment.location
        responsibleField.text = equipment.responsible
        hoursBox.value = equipment.hours
        activeSwitch.checked = equipment.active
        conditionSlider.value = equipment.condition
        errorText = ""
    }

    function submit() {
        errorText = equipmentController.save({
            id: equipmentId,
            name: nameField.text,
            category: categoryBox.currentText,
            inventory_number: inventoryField.text,
            year: yearBox.value,
            status: statusBox.currentText,
            location: locationField.text,
            responsible: responsibleField.text,
            hours: hoursBox.value,
            active: activeSwitch.checked,
            condition: conditionSlider.value
        })
        if (!errorText)
            close()
    }

    anchors.centerIn: Overlay.overlay
    width: Math.min(560, parent.width - 40)
    modal: true
    title: equipmentId ? "Редактирование техники" : "Новая техника"

    onOpened: nameField.forceActiveFocus()
    onApplied: submit()
    onReset: fill(equipmentController.defaults)

    GridLayout {
        anchors.fill: parent
        columns: 2
        columnSpacing: 12
        rowSpacing: 8

        Label {
            text: "Название / модель*"
        }

        TextField {
            id: nameField
            Layout.fillWidth: true
            placeholderText: "Например, Кировец К-744Р4"
        }

        Label {
            text: "Тип техники"
        }

        ComboBox {
            id: categoryBox
            Layout.fillWidth: true
            model: equipmentController.categories
        }

        Label {
            text: "Инвентарный номер*"
        }

        TextField {
            id: inventoryField
            Layout.fillWidth: true
            placeholderText: "Например, TR-001"
        }

        Label {
            text: "Год выпуска"
        }

        SpinBox {
            id: yearBox
            from: equipmentController.minYear
            to: equipmentController.maxYear
            editable: true
            textFromValue: value => value.toString()
            valueFromText: text => parseInt(text)
        }

        Label {
            text: "Состояние"
        }

        ComboBox {
            id: statusBox
            Layout.fillWidth: true
            model: equipmentController.statuses
        }

        Label {
            text: "Место эксплуатации"
        }

        TextField {
            id: locationField
            Layout.fillWidth: true
            placeholderText: "Например, поле № 3"
        }

        Label {
            text: "Ответственный"
        }

        TextField {
            id: responsibleField
            Layout.fillWidth: true
            placeholderText: "Например, Иванов И.И."
        }

        Label {
            text: "Наработка, м/ч"
        }

        SpinBox {
            id: hoursBox
            from: 0
            to: 1000000
            stepSize: 10
            editable: true
            textFromValue: value => value.toString()
            valueFromText: text => parseInt(text)
        }

        Label {
            text: "Эксплуатация"
        }

        Switch {
            id: activeSwitch
            text: "Активна в эксплуатации"
        }

        Label {
            text: "Техническое состояние"
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 8

            Slider {
                id: conditionSlider
                Layout.fillWidth: true
                from: 0
                to: 100
                stepSize: 1
                snapMode: Slider.SnapAlways
            }

            Label {
                Layout.minimumWidth: 40
                text: `${conditionSlider.value}%`
            }
        }

        Label {
            Layout.columnSpan: 2
            Layout.fillWidth: true
            visible: form.errorText !== ""
            text: form.errorText
            color: "#c62828"
            wrapMode: Text.Wrap
        }
    }

    footer: DialogButtonBox {
        Button {
            text: "Сохранить"
            enabled: form.canSave
            DialogButtonBox.buttonRole: DialogButtonBox.ApplyRole
        }

        Button {
            text: "Очистить"
            DialogButtonBox.buttonRole: DialogButtonBox.ResetRole
        }

        Button {
            text: "Отмена"
            DialogButtonBox.buttonRole: DialogButtonBox.RejectRole
        }
    }
}
