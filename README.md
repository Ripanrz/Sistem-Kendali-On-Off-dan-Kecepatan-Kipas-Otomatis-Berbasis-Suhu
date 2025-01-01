# Sistem Kendali On/Off dan Kecepatan Kipas Otomatis Berbasis Suhu
Proyek ini bertujuan untuk mengembangkan prototipe kipas otomatis yang mampu mengatur kecepatan dan status on/off berdasarkan suhu ruangan. Sistem ini mengintegrasikan teknologi mikrokontroler, sensor suhu, dan antarmuka pengguna grafis (GUI) untuk menciptakan perangkat pendingin yang efisien dan ramah pengguna.

## Fitur Utama
1. Pengaturan Kecepatan Otomatis
Kipas akan menyesuaikan kecepatan dalam 4 tingkat berdasarkan suhu:
- Mati (Suhu < 25°C)
- Kecepatan Rendah (25°C–30°C)
- Kecepatan Sedang (30°C–35°C)
- Kecepatan Tinggi (> 35°C)

2. Sistem Kendali On/Off Otomatis
Kipas akan menyala atau mati sesuai kebutuhan suhu ruangan.

3. Antarmuka Pengguna (GUI)
GUI berbasis QML dan Python untuk memantau suhu dan mengontrol on/off kipas secara manual.

4. Efisiensi Energi
Hanya mengoperasikan kipas sesuai kebutuhan, mengurangi konsumsi daya.

## Komponen Utama
1. Hardware:
- Mikrokontroler: Arduino Uno R3
- Sensor Suhu: DHT11
- Transistor: MOSFET 2N7000
- Kipas DC: Panamatic DC 9225
- Sumber Daya: Baterai 12V

2. Software:
- Arduino IDE untuk pemrograman mikrokontroler
- Thonny (Python) untuk backend GUI
- Visual Studio Code (QML) untuk frontend GUI
