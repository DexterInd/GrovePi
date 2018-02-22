#!/usr/bin/env ruby

require '../grove_pi'

firmware_version_bytes = GrovePi.read_firmware_version

print "Firmware: #{firmware_version_bytes[0]}.\
#{firmware_version_bytes[1]}.\
#{firmware_version_bytes[2]}
Test    : Write analog value (with PWM) to port D5
==================================================

"

while true
  puts '[+] Starting analog write sequence on port D5'

  i = 0

  while i <= 255
    puts i
    GrovePi.write_analog GrovePi::D5, i
    i += 4
    sleep 0.02
  end

  i = 255

  while i >= 1
    puts i
    GrovePi.write_analog GrovePi::D5, i
    i -= 4
    sleep 0.02
  end
end
