const int ldrPin = A0;      // Pin analógico donde está conectada la LDR
const int ledPin = 9;       // Pin digital donde está conectado el LED

int umbral = 500;           // Umbral de luz (ajusta este valor según tus pruebas)

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);       // Iniciar comunicación serial para monitoreo
}

void loop() {
  int valorLuz = analogRead(ldrPin);   // Leer valor de luz desde el pin A0

  // Mostrar el valor en el monitor serial
  Serial.print("Valor de luz: ");
  Serial.println(valorLuz);

  // Comparar el valor leído con el umbral
  if (valorLuz < umbral) {
    digitalWrite(ledPin, HIGH);  // Si hay poca luz, encender el LED
  } else {
    digitalWrite(ledPin, LOW);   // Si hay suficiente luz, apagar el LED
  }

  delay(200);  // Pequeña pausa para estabilidad de lectura
}
