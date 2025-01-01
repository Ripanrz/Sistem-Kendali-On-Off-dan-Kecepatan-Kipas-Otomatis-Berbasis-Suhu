import QtQuick 2.12 
import QtQuick.Window 2.13 
import QtQuick.Controls 2.0 
import QtQuick.Controls.Styles 1.4 
import QtQuick.Extras 1.4 
import QtQuick.Extras.Private 1.0 

Window 
{
    id: root
    width: 1200
    height: 800
    title: "Temperature Monitoring"
    color: "#023047"
    visible: true
    flags: Qt.Window

    Rectangle 
    {
        x: 0
        y: 0
        width: 1200
        height: 200
        color: "#ffb703"

        Rectangle 
        {
            anchors.centerIn: parent
            width: 600
            height: 100
            color: "#fb8500"
            radius: 40

            Text 
            {
                anchors.centerIn: parent
                text: "Temperature Monitoring"
                font.pixelSize: 30
                font.family: "Comic Sans MS"
                font.bold: true
                color: "#023047"
            }
        }
    }

    Image
    {
        x: 50
        y: 50
        width: 100
        height: 100
        source: "arduino.png"
    }

    Image 
    {
        x: 1050
        y: 50
        width: 100
        height: 100
        source: "pyqt.png"
    }

    Rectangle 
    {
        x: 133.333
        y: 400
        width: 400
        height: 350
        color: "#ffba08"
        radius: 40

        Text 
        {
            anchors.horizontalCenter: parent.horizontalCenter
            y: 10
            text: "FAN SPEED (%)"
            font.pixelSize: 20
            font.family: "Comic Sans MS"
            font.bold: true
            color: "#023047"
        }

        Rectangle 
        {
            anchors.centerIn: parent
            width: 200
            height: 200
            radius: width / 2
            color: "#233d4d"

            CircularGauge 
            {
                anchors.centerIn: parent
                id: gauge1
                height: 200
                width: 200
                value: backend.fanSpeed
                minimumValue: 0
                maximumValue: 100

                style: CircularGaugeStyle 
                {
                    labelStepSize: 10

                    needle: Rectangle 
                    {
                        y: outerRadius * 0.15
                        implicitWidth: outerRadius * 0.03
                        implicitHeight: outerRadius * 0.9
                        antialiasing: true
                        color: "#ffbc0a"
                    }
                }

                Behavior on value 
                {
                    NumberAnimation 
                    {
                        duration: 1000
                        easing.type: Easing.InOutQuad
                    }
                }
            }
        }
    }

    Rectangle 
    {
        x: 666.666
        y: 400
        width: 400
        height: 350
        color: "#fe7f2d"
        radius: 40

        Text 
        {
            anchors.horizontalCenter: parent.horizontalCenter
            y: 10
            text: "TEMPERATURE"
            font.pixelSize: 20
            font.family: "Comic Sans MS"
            font.bold: true
            color: "#023047"
        }

        Rectangle 
        {
            anchors.horizontalCenter: parent.horizontalCenter
            y: 50
            width: 300
            height: 100
            color: backend.background // Bind background color to backend
            radius: 20

            Rectangle 
            {
                x: 50
                y: 10
                width: 100
                height: 80
                radius: 20

                Text 
                {
                    anchors.centerIn: parent
                    text: String(backend.temp) // Bind temperature value to backend
                    font.pixelSize: 40
                    font.family: "Comic Sans MS"
                    font.bold: true
                    color: "#023047"
                }

                Image 
                {
                    x: 120
                    y: 0
                    width: 80
                    height: 80
                    source: "thermometer.png"
                }
            }
        }

        Rectangle 
        {
            anchors.horizontalCenter: parent.horizontalCenter
            y: 170
            width: 300
            height: 100
            color: backend.background// Bind background color to backend
            radius: 20

            Rectangle 
            {
                x: 50
                y: 10
                width: 100
                height: 80
                radius: 20

                Text 
                {
                    anchors.centerIn: parent
                    text: backend.tempStatus// Bind status to backend
                    font.pixelSize: 20
                    font.family: "Comic Sans MS"
                    font.bold: true
                    color: "#023047"
                }

                Image 
                {
                    x: 120
                    y: 0
                    width: 80
                    height: 80
                    source: backend.tempIcon // Bind icon to backend
                }
            }
        }
    }

    Rectangle
    {
        x: 50
        y: 250
        width: 250
        height: 50
        color: backend.fanStatusBackground // Bind fan status background to backend
        radius: 20

        Text 
        {
            x: 20
            y: 10
            text: "FAN Status: "
            font.pixelSize: 20
            font.family: "Comic Sans MS"
            font.bold: true
            color: "#023047"
        }

        Text 
        {
            x: 170
            y: 10
            text: backend.fanStatus // Bind fan status to backend
            font.pixelSize: 20
            font.family: "Comic Sans MS"
            font.bold: true
            color: "#023047"
        }
    }

    Button
    {
        id : button
        x : 350
        y : 250
        width : 100
        height : 50

        background : Rectangle
        {
            id: buttonBackground
            color : "#d90429"
            radius : 20
        }

        Text
        {
            id: fanStatusText
            anchors.centerIn : parent
            text : "OFF"
            font.pixelSize : 20
            font.family : "Comic Sans MS"
            font.bold : true
            color : "#023047"
        }

        onClicked :
        {
            if (fanStatusText.text == "ON")
            {
                fanStatusText.text = "OFF"
                buttonBackground.color = "#d90429"
                backend.button("0")
            }
            else if (fanStatusText.text == "OFF")
            {
                fanStatusText.text = "ON"
                buttonBackground.color = "#70e000"
                backend.button("1")
            }
        }
    }
}
