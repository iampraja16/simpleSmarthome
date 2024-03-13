import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtQuick.Extras.Private 1.0

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: qsTr("Smarthome GUI")

    GridLayout {
        anchors.fill: parent
        columns: 2
        rowSpacing: 10
        columnSpacing: 10

        Label {
            text: qsTr("LDR Set Point")
            font.pixelSize: 20
        }
        
        Slider {
            id: ldrSlider
            from: 0
            to: 1023
            stepSize: 10
            onValueChanged: {
                ldrGauge.value = value;
                communicator.receive_ldr_set_point(value);
            }
        }
        
        Gauge {
            id: ldrGauge
            value: ldrSlider.value
            minimumValue: 0
            maximumValue: 1023
            tickmarkStepSize: 100
            onValueChanged: communicator.receive_ldr_set_point(value)
        }

        Label {
            text: qsTr("DHT11 Set Point")
            font.pixelSize: 20
        }
        
        Slider {
            id: dht11Slider
            from: 0
            to: 50
            stepSize: 1
            onValueChanged: {
                dht11Gauge.value = value;
                communicator.receive_LM35_set_point(value);
            }
        }
        Gauge {
            id: dht11Gauge
            value: dht11Slider.value
            minimumValue: 0
            maximumValue: 50
            tickmarkStepSize: 5
            onValueChanged: communicator.receive_LM35_set_point(value)
        }

        Label {
            text: qsTr("LED 1")
            font.pixelSize: 20
        }
        Button {
            id: led1Button
            text: qsTr("ON")
            checkable: true
            checked: true
            onClicked: {
                if (checked) {
                    text = qsTr("ON");
                    communicator.receive_led1_status(true); 
                } else {
                    text = qsTr("OFF");
                    communicator.receive_led1_status(false); 
                }
            }
        }

        Label {
            text: qsTr("LED 2")
            font.pixelSize: 20
        }
        Button {
            id: led2Button
            text: qsTr("ON")
            checkable: true
            checked: true
            onClicked: {
                if (checked) {
                    text = qsTr("ON");
                    communicator.receive_led2_status(true); 
                } else {
                    text = qsTr("OFF");
                    communicator.receive_led2_status(false); 
                }
            }
        }
        Label {
            text: qsTr("LED 3")
            font.pixelSize: 20
        }
        Button {
            id: led3Button
            text: qsTr("ON")
            checkable: true
            checked: true
            onClicked: {
                if (checked) {
                    text = qsTr("ON");
                    communicator.receive_led4_status(true); 
                } else {
                    text = qsTr("OFF");
                    communicator.receive_led4_status(false); 
                }
            }
        }
        
        Label {
            text: qsTr("LED 4")
            font.pixelSize: 20
        }
        Button {
            id: led4Button
            text: qsTr("ON")
            checkable: true
            checked: true
            onClicked: {
                if (checked) {
                    text = qsTr("ON");
                    communicator.receive_led5_status(true); 
                } else {
                    text = qsTr("OFF");
                    communicator.receive_led5_status(false);
                }
            }
        }

        Label {
            text: qsTr("Servo Clockwise")
            font.pixelSize: 20
        }
        Button {
            id: servoCWButton
            text: qsTr("Rotate")
            onClicked: {
                communicator.receive_servo_command("clockwise");
            }
        }

        Label {
            text: qsTr("Servo Counter Clockwise")
            font.pixelSize: 20
        }
        Button {
            id: servoCCWButton
            text: qsTr("Rotate")
            onClicked: {
                communicator.receive_servo_command("counterclockwise");
            }
        }
    }
}
