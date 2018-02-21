#!/usr/bin/env ruby

require '../grove_pi'

firmware_version_bytes = GrovePi.read_firmware_version

print "Firmware: #{firmware_version_bytes[0]}.\
#{firmware_version_bytes[1]}.\
#{firmware_version_bytes[2]}
Test    : Write digital value to port D3
========================================

"

while true
  GrovePi.write_digital GrovePi::D3, 1
  puts '[+] Tick: ON'
  sleep 1

  GrovePi.write_digital GrovePi::D3, 0
  puts '[+] Tock: OFF'
  sleep 1

  puts '[+] End of cycle'
  puts
end
