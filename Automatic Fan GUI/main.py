from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQml import *
from PyQt5.QtWidgets import *
from PyQt5.QtQuick import *
import sys
import serial
import threading
import time

# ----------------------------------------------------------------#
# Deklarasi variabel global default
fanSpeed = 0
fanStatusBackground = "#d00000"
fanStatus = "OFF"
temp = 0
tempStatus = "-"
background = "#4a4e69"
tempIcon = "off.png"
button_status = "0"

serial_data = ""

transmit_time = 0
transmit_time_prev = 0

data_send = ""
# ----------------------------------------------------------------#
# Fungsi untuk mendeteksi port serial yang tersedia
def serial_ports():
    import glob

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Platform tidak didukung')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

print("Pilih port Arduino Anda:")
print(serial_ports())

port = input("Masukkan port: ")
try:
    ser = serial.Serial(port, 9600, timeout=3)
except serial.SerialException as e:
    print(f"Gagal membuka port {port}: {e}")
    sys.exit(1)

# ----------------------------------------------------------------#
# Kelas utama untuk menghubungkan PyQt5 dengan QML
class Table(QObject):
    fanSpeedChanged = pyqtSignal(int)
    tempChanged = pyqtSignal(float)
    tempStatusChanged = pyqtSignal(str)
    backgroundChanged = pyqtSignal(str)
    tempIconChanged = pyqtSignal(str)
    fanStatusBackgroundChanged = pyqtSignal(str)
    fanStatusChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.app = QApplication(sys.argv)
        self.engine = QQmlApplicationEngine(self)
        self.engine.rootContext().setContextProperty("backend", self)
        self.engine.load(QUrl("main.qml"))

        self._fanSpeed = 0
        self._temp = 0
        self._tempStatus = "-"
        self._background = "#4a4e69"
        self._tempIcon = "off.png"
        self._fanStatusBackground = "#d00000"
        self._fanStatus = "OFF"  

    @pyqtProperty(int, notify=fanSpeedChanged)
    def fanSpeed(self):
        if not hasattr(self, '_fanSpeed'):
            self._fanSpeed = 0
        return self._fanSpeed

    @fanSpeed.setter
    def fanSpeed(self, value):
        if self._fanSpeed != value:
            self._fanSpeed = value
            self.fanSpeedChanged.emit(self._fanSpeed)

    @pyqtProperty(float, notify=tempChanged)
    def temp(self):
        if not hasattr(self, '_temp'):
            self._temp = 0
        return self._temp

    @temp.setter
    def temp(self, value):
        if self._temp != value:
            self._temp = value
            self.tempChanged.emit(self._temp)

    @pyqtProperty(str, notify=tempStatusChanged)
    def tempStatus(self):
        if not hasattr(self, '_tempStatus'):
            self._tempStatus = "-"
        return self._tempStatus

    @tempStatus.setter
    def tempStatus(self, value):
        if self._tempStatus != value:
            self._tempStatus = value
            self.tempStatusChanged.emit(self._tempStatus)

    @pyqtProperty(str, notify=backgroundChanged)
    def background(self):
        if not hasattr(self, '_background'):
            self._background = "#4a4e69"
        return self._background

    @background.setter
    def background(self, value):
        if self._background != value:
            self._background = value
            self.backgroundChanged.emit(self._background)

    @pyqtProperty(str, notify=tempIconChanged)
    def tempIcon(self):
        if not hasattr(self, '_tempIcon'):
            self._tempIcon = "off.png"
        return self._tempIcon

    @tempIcon.setter
    def tempIcon(self, value):
        if self._tempIcon != value:
            self._tempIcon = value
            self.tempIconChanged.emit(self._tempIcon)

    @pyqtProperty(str, notify=fanStatusBackgroundChanged)
    def fanStatusBackground(self):
        if not hasattr(self, '_fanStatusBackground'):
            self._fanStatusBackground = "#d00000"
        return self._fanStatusBackground

    @fanStatusBackground.setter
    def fanStatusBackground(self, value):
        if self._fanStatusBackground != value:
            self._fanStatusBackground = value
            self.fanStatusBackgroundChanged.emit(self._fanStatusBackground)

    @pyqtProperty(str, notify=fanStatusChanged)
    def fanStatus(self):
        if not hasattr(self, '_fanStatus'):
            self._fanStatus = "OFF" 
        return self._fanStatus

    @fanStatus.setter
    def fanStatus(self, value):
        if self._fanStatus != value:
            self._fanStatus = value
            self.fanStatusChanged.emit(self._fanStatus)
            
    @pyqtSlot(str)
    def button(self, message):
        global button_status
        print(message)
        button_status = message

# ----------------------------------------------------------------#
# Fungsi untuk membaca data serial secara terus-menerus

def serial_read():
    global fanSpeed, temp, tempStatus, background, tempIcon, fanStatusBackground, fanStatus

    while True:
        try:
            if ser.in_waiting > 0:
                ser_bytes = ser.readline().strip()
                serial_data = ser_bytes.decode("utf-8").strip()

                if not serial_data:
                    print("Data kosong diterima. Melewati...")
                    continue
        
                data = serial_data.split(":")
                temp = float(data[1])
                systemStatus = data[0]
                print(systemStatus)
                table.temp = temp

                # Logika untuk menentukan status berdasarkan suhu
                if systemStatus == "ON":
                    if temp <= 0:
                        table.fanSpeed = 0
                        table.tempStatus = "Freezing"
                        table.tempIcon = "freezing.png"
                        table.background = "#48cae4"
                        table.fanStatus = "OFF"
                        table.fanStatusBackground = "#d90429"
                    elif temp < 25:
                        table.fanSpeed = 0
                        table.tempStatus = "Cold"
                        table.tempIcon = "cold.png"
                        table.background = "#caf0f8"
                        table.fanStatus = "OFF"
                        table.fanStatusBackground = "#d90429"
                    elif 25 <= temp <= 30:
                        table.fanSpeed = 40
                        table.tempStatus = "Normal"
                        table.tempIcon = "normal.png"
                        table.background = "#fdf0d5"
                        table.fanStatus = "ON"
                        table.fanStatusBackground = "#70e000"
                    elif 30 < temp <= 35:
                        table.fanSpeed = 60
                        table.tempStatus = "Hot"
                        table.tempIcon = "hot.png"
                        table.background = "#ffd60a"
                        table.fanStatus = "ON"
                        table.fanStatusBackground = "#70e000"
                    else:
                        table.fanSpeed = 100
                        table.tempStatus = "Very Hot"
                        table.tempIcon = "very_hot.png"
                        table.background = "#dc2f02"
                        table.fanStatus = "ON"
                        table.fanStatusBackground = "#70e000"

                    print(f"Temperature: {temp} C, Status: {table.tempStatus}, Fan Speed: {table.fanSpeed}%")
                else:
                    table.fanSpeed = 0
                    table.tempStatus = "-"
                    table.tempIcon = "off.png"
                    table.background = "#4a4e69"
                    table.fanStatus = "OFF"
                    table.fanStatusBackground = "#d90429"
                    
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"Error pada serial_read: {e}")

def serial_write():
    global transmit_time
    global transmit_time_prev
    global data_send
    
    while True:
        transmit_time = time.time() - transmit_time_prev
        data_send = str(button_status)
        if (transmit_time > 0.5):
            #print(data_send)
            ser.write(data_send.encode())
            transmit_time_prev = time.time()
# ----------------------------------------------------------------#
# Main Program
if __name__ == "__main__":
    t1 = threading.Thread(target=serial_read, daemon=True)  # Gunakan daemon agar thread mati saat aplikasi keluar
    t1.start()
    
    t2 = threading.Thread(target=serial_write, daemon=True)
    t2.start()

    table = Table()
    sys.exit(table.app.exec_())
