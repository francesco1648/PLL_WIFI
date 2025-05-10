#include "WebTelemetry.h"

void WebTelemetry::begin(const char* ssid, const char* pass,
           IPAddress localIP, IPAddress gateway,
           IPAddress subnet, IPAddress dns,
           uint16_t port) {
  WiFi.config(localIP, gateway, subnet, dns);
  WiFi.begin(ssid, pass);

  Serial.print("Connessione a ");
  Serial.println(ssid);

  unsigned long startAttemptTime = millis();
  const unsigned long timeout = 10000; // 10 secondi

  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - startAttemptTime > timeout) {
      Serial.println("Timeout nella connessione WiFi.");
      return;
    }
    delay(200);
    Serial.print(".");
  }

  Serial.println("\nConnesso!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  _server = new WiFiServer(port);
  _server->begin();

}

void WebTelemetry::setUdpTarget(IPAddress pcIp, uint16_t pcPort) {
    _udpTargetIP   = pcIp;
    _udpTargetPort = pcPort;
    _udp.begin(0);  // porta locale libera
}

void WebTelemetry::updateData(float currentSpeed, float targetSpeed, float pidOutput, float OutputPcalculate, float OutputIcalculate, float OutputDcalculate) {
    // salva nel buffer circolare
    _history[_head] = { currentSpeed, targetSpeed, pidOutput, OutputPcalculate, OutputIcalculate, OutputDcalculate, millis() };
    _head = (_head + 1);
    if (_head >= TELEMETRY_HISTORY_SIZE) {
        _head = 0;
        _bufferFull = true;
    }
    // invia subito l’ultimo campione via UDP
    sendLatestUdp();
}

void WebTelemetry::sendLatestUdp() {
    if (_udpTargetPort == 0) return;

    int lastIdx = (_head - 1 + TELEMETRY_HISTORY_SIZE) % TELEMETRY_HISTORY_SIZE;
    TelemetrySample& s = _history[lastIdx];

    // preparo un record CSV
    char buf[128];
     int len = snprintf(buf, sizeof(buf), "%lu,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n",
                       s.timestamp, s.currentSpeed, s.targetSpeed,
                       s.pidOutput, s.OutputPcalculate, s.OutputIcalculate, s.OutputDcalculate);

    _udp.beginPacket(_udpTargetIP, _udpTargetPort);
    _udp.write((uint8_t*)buf, len);
    _udp.endPacket();
}


void WebTelemetry::handleClient() {
    static unsigned long lastWebUpdate = 0;
    unsigned long now = millis();

    // Mostra la pagina solo ogni 3 secondi
    if (now - lastWebUpdate < 3000) return;
    lastWebUpdate = now;

    WiFiClient client = _server->accept();
    if (!client) return;

    while (client.available()) client.read(); // pulizia non bloccante

    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println();
    client.println("<!DOCTYPE html><html><head>");
    client.println("<meta http-equiv='refresh' content='3'>"); // aggiornamento ogni 3s
    client.println("</head><body>");
    client.printf("<p>Velocità Attuale: %.2f RPM</p>\n", _showCurrentSpeed);
    client.printf("<p>Velocità Target: %.2f RPM</p>\n", _showTargetSpeed);
    client.printf("<p>PID Output: %.2f</p>\n", _showPIDOutput);
    client.printf("<p>Output P: %.2f</p>\n", _showOutputPcalculate);
    client.printf("<p>Output I: %.2f</p>\n", _showOutputIcalculate);
    client.printf("<p>Output D: %.2f</p>\n", _showOutputDcalculate);

    client.println("</body></html>");
    client.stop();
}



void WebTelemetry::currentData( float currentSpeed, float targetSpeed, float pidOutput, float OutputPcalculate, float OutputIcalculate, float OutputDcalculate) {
    _showCurrentSpeed = currentSpeed;
    _showTargetSpeed  = targetSpeed;
    _showPIDOutput    = pidOutput;
    _showOutputPcalculate = OutputPcalculate;
    _showOutputIcalculate = OutputIcalculate;
    _showOutputDcalculate = OutputDcalculate;
 }

void WebTelemetry::sendCsv(WiFiClient&){ /* … */ }
void WebTelemetry::sendHtml(WiFiClient&){ /* … */ }
