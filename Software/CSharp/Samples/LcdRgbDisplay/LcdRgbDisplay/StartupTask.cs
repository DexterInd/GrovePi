using System;
using System.Text;
using Windows.ApplicationModel.Background;

using Windows.System.Threading;
using GrovePi;
using GrovePi.I2CDevices;

namespace LcdRgbDisplay
{
    public sealed class StartupTask : IBackgroundTask
    {
        ThreadPoolTimer timer;
        BackgroundTaskDeferral deferral;
        IRgbLcdDisplay display;
        DateTime now;
        string ampm;


        public void Run(IBackgroundTaskInstance taskInstance)
        {
            deferral = taskInstance.GetDeferral();

            // Connect the RGB display to one of the I2C ports
            display = DeviceFactory.Build.RgbLcdDisplay();

            // Create a timer that will 'tick' every half-second (500ms)
            timer = ThreadPoolTimer.CreatePeriodicTimer(this.Timer_Tick, TimeSpan.FromSeconds(1));
        }

        private void Timer_Tick(ThreadPoolTimer timer)
        {
            try
            {
                // Get the current time
                now = DateTime.Now;

                // Use a StringBuilder to assemble the display text
                StringBuilder timeString = new StringBuilder();

                if (now.Hour > 12)
                {
                    // Set the RGB backlight to a light blue-ish color
                    display.SetBacklightRgb(0, 255, 255);

                    timeString.Append("Good evening.\n");
                    ampm = " PM";
                    timeString.Append(now.Hour - 12);
                }
                else
                {
                    // Set the RGB backlight to a light yellow-ish color
                    display.SetBacklightRgb(255, 255, 0);

                    timeString.Append("Good morning.\n");
                    ampm = " AM";
                    timeString.Append(now.Hour);
                }

                timeString.Append(":");
                timeString.Append(now.Minute.ToString("D2"));
                timeString.Append(":");
                timeString.Append(now.Second.ToString("D2"));
                timeString.Append(ampm);

                // Display the time
                display.SetText(timeString.ToString());
            }
            catch (Exception ex)
            {

            }
        }
    }
}
