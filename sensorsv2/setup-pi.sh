#!/bin/bash

curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
sudo mv bin/arduino-cli /usr/local/bin/
rm -r bin

arduino-cli core install arduino:avr

arduino-cli config init
arduino-cli config set library.enable_unsafe_install true

arduino-cli lib install --git-url https://github.com/PaulStoffregen/OneWire.git
arduino-cli lib install --git-url https://github.com/milesburton/Arduino-Temperature-Control-Library.git
arduino-cli lib install --git-url https://github.com/DFRobot/DFRobot_EC.git
arduino-cli lib install --git-url https://github.com/DFRobot/DFRobot_EC10.git
arduino-cli lib install --git-url https://github.com/Sensirion/arduino-i2c-scd4x.git
arduino-cli lib install --git-url https://github.com/Sensirion/arduino-core.git
arduino-cli lib install VernierLib