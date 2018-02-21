#!/usr/bin/env ruby

require '../grove_pi'

firmware_version_bytes = GrovePi.read_firmware_version

print "Firmware: #{firmware_version_bytes[0]}.\
#{firmware_version_bytes[1]}.\
#{firmware_version_bytes[2]}
Test    : Read analog value from port A0
========================================

"

while true
	analog_value = GrovePi.read_analog GrovePi::A0
	print "[+] Analog Value (Port A0) = #{analog_value}\n"
	sleep 0.5
end
