cd /home/pi/Desktop/robot

chmod 755 install.sh
chmod 755 keyboard_mouse_test.sh
chmod 755 launcher.sh
chmod 755 startup_disable.sh
chmod 755 startup_enable.sh
chmod 755 stuff/setup_i2c.sh

sudo apt-get install -y xboxdrv

sudo apt-get install -y xterm

sudo python3 -m pip install pynput

sudo python3 -m pip install adafruit-circuitpython-pca9685

sudo sh stuff/setup_i2c.sh

sh startup_enable.sh

sudo reboot