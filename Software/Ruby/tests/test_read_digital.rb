#!/usr/bin/env ruby

require '../grove_pi'

firmware_version_bytes = GrovePi.read_firmware_version

print "Firmware: #{firmware_version_bytes[0]}.\
#{firmware_version_bytes[1]}.\
#{firmware_version_bytes[2]}
Test    : Read digital value from port D4
=========================================

"

while true
	digital_value = GrovePi.read_digital GrovePi::D4
	print "[+] Digital input from port D4 = #{digital_value}\n"
	sleep 0.5
end
