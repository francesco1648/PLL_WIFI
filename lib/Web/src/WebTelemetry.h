#ifndef WEB_TELEMETRY_H
#define WEB_TELEMETRY_H

#include <WiFi.h>
#include <WiFiUdp.h>

#define TELEMETRY_HISTORY_SIZE 1000

struct TelemetrySample {
    float currentSpeed;
    float targetSpeed;
    float pidOutput;
    float OutputPcalculate;
    float OutputIcalculate;
    float OutputDcalculate;
    unsigned long timestamp;
};


class WebTelemetry {
public:
    void begin(const char* ssid, const char* password,
               IPAddress localIP, IPAddress gateway,
               IPAddress subnet, IPAddress dns,
               uint16_t port);

    void setUdpTarget(IPAddress pcIp, uint16_t pcPort);
    void updateData(float currentSpeed, float targetSpeed, float pidOutput,float OutputPcalculate, float OutputIcalculate, float OutputDcalculate);
    void handleClient();  // puoi tenere il web server, o toglierlo se non serve
    void currentData( float currentSpeed, float targetSpeed, float pidOutput, float OutputPcalculate, float OutputIcalculate, float OutputDcalculate);
private:
    WiFiServer* _server = nullptr;
    WiFiUDP    _udp;
    IPAddress  _udpTargetIP;
    uint16_t   _udpTargetPort = 0;
    float _showCurrentSpeed = 0;
    float _showTargetSpeed = 0;
     float _showPIDOutput = 0;
    float _showOutputPcalculate = 0;
    float _showOutputIcalculate = 0;
    float _showOutputDcalculate = 0;

    TelemetrySample _history[TELEMETRY_HISTORY_SIZE];
    int _head = 0;
    bool _bufferFull = false;

    void sendCsv( WiFiClient& client );
    void sendHtml( WiFiClient& client );
    void sendLatestUdp();
};

#endif // WEB_TELEMETRY_H
