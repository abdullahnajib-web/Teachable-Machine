# MIT License
# 
# Copyright (c) 2020 Tony Smith (@smittytone)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
class HT16K33:
    """
    A simple, generic driver for the I2C-connected Holtek HT16K33 controller chip.
    This release supports MicroPython and CircuitPython
    Version:    3.0.2
    Bus:        I2C
    Author:     Tony Smith (@smittytone)
    License:    MIT
    Copyright:  2020
    """

    # *********** CONSTANTS **********

    HT16K33_GENERIC_DISPLAY_ON = 0x81
    HT16K33_GENERIC_DISPLAY_OFF = 0x80
    HT16K33_GENERIC_SYSTEM_ON = 0x21
    HT16K33_GENERIC_SYSTEM_OFF = 0x20
    HT16K33_GENERIC_DISPLAY_ADDRESS = 0x00
    HT16K33_GENERIC_CMD_BRIGHTNESS = 0xE0
    HT16K33_GENERIC_CMD_BLINK = 0x81

    # *********** PRIVATE PROPERTIES **********

    i2c = None
    address = 0
    brightness = 15
    flash_rate = 0

    # *********** CONSTRUCTOR **********

    def __init__(self, i2c, i2c_address):
        assert 0x00 <= i2c_address < 0x80, "ERROR - Invalid I2C address in HT16K33()"
        self.i2c = i2c
        self.address = i2c_address
        self.power_on()

    # *********** PUBLIC METHODS **********

    def set_blink_rate(self, rate=0):
        """
        Set the display's flash rate.
        Only four values (in Hz) are permitted: 0, 2, 1, and 0,5.
        Args:
            rate (int): The chosen flash rate. Default: 0Hz (no flash).
        """
        assert rate in (0, 0.5, 1, 2), "ERROR - Invalid blink rate set in set_blink_rate()"
        self.blink_rate = rate & 0x03
        self._write_cmd(self.HT16K33_GENERIC_CMD_BLINK | rate << 1)

    def set_brightness(self, brightness=15):
        """
        Set the display's brightness (ie. duty cycle).
        Brightness values range from 0 (dim, but not off) to 15 (max. brightness).
        Args:
            brightness (int): The chosen flash rate. Default: 15 (100%).
        """
        if brightness < 0 or brightness > 15: brightness = 15
        self.brightness = brightness
        self._write_cmd(self.HT16K33_GENERIC_CMD_BRIGHTNESS | brightness)

    def draw(self):
        """
        Writes the current display buffer to the display itself.
        Call this method after updating the buffer to update
        the LED itself.
        """
        self._render()

    def update(self):
        """
        Alternative for draw() for backwards compatibility
        """
        self._render()

    def clear(self):
        """
        Clear the buffer.
        Returns:
            The instance (self)
        """
        for i in range(0, len(self.buffer)): self.buffer[i] = 0x00
        return self

    def power_on(self):
        """
        Power on the controller and display.
        """
        self._write_cmd(self.HT16K33_GENERIC_SYSTEM_ON)
        self._write_cmd(self.HT16K33_GENERIC_DISPLAY_ON)

    def power_off(self):
        """
        Power on the controller and display.
        """
        self._write_cmd(self.HT16K33_GENERIC_DISPLAY_OFF)
        self._write_cmd(self.HT16K33_GENERIC_SYSTEM_OFF)

    # ********** PRIVATE METHODS **********

    def _render(self):
        """
        Write the display buffer out to I2C
        """
        buffer = bytearray(len(self.buffer) + 1)
        buffer[1:] = self.buffer
        buffer[0] = 0x00
        self.i2c.writeto(self.address, bytes(buffer))

    def _write_cmd(self, byte):
        """
        Writes a single command to the HT16K33. A private method.
        """
        self.i2c.writeto(self.address, bytes([byte]))