import sys
import serial
import threading
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtCore import pyqtSignal, QObject, QTimer

# Cambia esto si tu puerto es otro
PUERTO_SERIAL = 'COM5'
BAUDIOS = 9600
UMBRAL = 500

class SerialReader(QObject):
    mensaje = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        try:
            self.serial_port = serial.Serial(PUERTO_SERIAL, BAUDIOS, timeout=1)
            self.running = True
        except serial.SerialException as e:
            print("Error al abrir el puerto serial:", e)
            self.running = False

    def start(self):
        if self.running:
            self.thread = threading.Thread(target=self.read_loop, daemon=True)
            self.thread.start()

    def read_loop(self):
        while self.running:
            try:
                linea = self.serial_port.readline().decode('utf-8').strip()
                if linea.startswith("Valor de luz:"):
                    print(linea)
                    valor = int(linea.split(":")[1].strip())
                    if valor < UMBRAL:
                        self.mensaje.emit("LED ENCENDIDO - Luz baja")
                    else:
                        self.mensaje.emit("LED APAGADO - Luz suficiente")
            except Exception as e:
                print("Error al leer serial:", e)

    def stop(self):
        self.running = False
        if hasattr(self, 'serial_port') and self.serial_port.is_open:
            self.serial_port.close()

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Examen Departamental 3.ui", self)

        # Intentamos encontrar el QTextEdit de forma segura
        self.cuadroTexto: QTextEdit = self.findChild(QTextEdit, "lecturas_txt")
        if not self.cuadroTexto:
            print("Error: No se encontró el QTextEdit llamado 'textEdit'")
            sys.exit(1)

        self.lector_serial = SerialReader()
        self.lector_serial.mensaje.connect(self.mostrar_mensaje)
        self.lector_serial.start()

    def mostrar_mensaje(self, texto):
        self.cuadroTexto.append(texto)

    def closeEvent(self, event):
        self.lector_serial.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
