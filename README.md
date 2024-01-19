# Redwood
weather station w/ solar panel tracking
Using an UDOO.key device [ESP-32 & RP2040] ; programmed with MicroPython

    .  send temperature from a sensor
    .  send a light value from a sensor
    .  keep a basic RTC [RP2040]; set/updated via command
    .  measure a battery [Li-type] that is solar panel charged
    .  move solar panel to track local sun's Azimuth via a motor/servo
    .    (using a programmed time from a simple Python data element)

The RP2040 sends data streams to the ESP32 via internal serial port
for transmission by the ESP-32; using the ESP-Now protocol.

Software is a collobaration from various Internet snippets,
modified and assembled by Olzeke51.  The command structure is
intended to be ASCII terminal based of my own design.
