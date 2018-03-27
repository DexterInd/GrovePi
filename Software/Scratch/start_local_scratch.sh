
echo "ensuring only one instance of GoPiGo3 Scratch Communicator"
sudo pkill -f GrovePiScratch.py
sudo python /home/pi/Dexter/GrovePi/Software/Scratch/GrovePiScratch.py &

echo "starting Scratch"
scratch /home/pi/Dexter/lib/Dexter/Scratch_GUI/new.sb

echo "killing background process"
sudo pkill -f GrovePiScratch.py
echo "background process killed"
