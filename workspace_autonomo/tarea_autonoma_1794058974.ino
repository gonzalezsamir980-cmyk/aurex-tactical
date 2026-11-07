void setup() {
  Serial.begin(115200);  // Inicializar la comunicación serial a 115200 baudios

  // Configurar el ADC
  adc = machine.ADC(0);  // Usar el ADC0
  adc.atten(machine.ADC.ATTN_11DB);  // Configurar la atenuación a 11dB para un rango de 0V a 3.3V
  adc.width(machine.ADC.WIDTH_10BIT);  // Configurar la resolución a 10 bits
}

void loop() {
  // Leer 5 muestras y calcular el voltaje correspondiente
  for (int i = 0; i < 5; i++) {
    adc_value = adc.read();  // Leer el valor del ADC
    voltage = (adc_value * 3.3) / 1023;  // Calcular el voltaje correspondiente
    Serial.print("Muestra ");
    Serial.print(i + 1);
    Serial.print(": Valor ADC = ");
    Serial.print(adc_value);
    Serial.print(", Voltaje = ");
    Serial.print(voltage, 2);
    Serial.println("V");
    delay(1000);  // Esperar 1 segundo antes de la siguiente lectura
  }
}