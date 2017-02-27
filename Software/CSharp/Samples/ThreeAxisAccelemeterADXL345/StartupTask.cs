using System;
using Windows.ApplicationModel.Background;

using GrovePi;
using GrovePi.Sensors;
using GrovePi.I2CDevices;
using Windows.System.Threading;
using System.Diagnostics;


// The Background Application template is documented at http://go.microsoft.com/fwlink/?LinkID=533884&clcid=0x409

namespace ThreeAxisAccelemeterADXL345
{
    public sealed class StartupTask : IBackgroundTask
    {
        IThreeAxisAccelerometerADXL345 acc;
        ThreadPoolTimer timer;
        BackgroundTaskDeferral deferral;

        public void Run(IBackgroundTaskInstance taskInstance)
        {
            deferral = taskInstance.GetDeferral();
            acc = DeviceFactory.Build.ThreeAxisAccelerometerADXL345();
            acc.Initialize();
            timer = ThreadPoolTimer.CreatePeriodicTimer(this.Timer_Tick, TimeSpan.FromSeconds(.5));
        }

        private void Timer_Tick(ThreadPoolTimer timer)
        {
            try
            {
                double[] AccXYZ = new double[3];
                AccXYZ = acc.GetAcclXYZ();
                Debug.WriteLine("Acc: " + AccXYZ[0] + " " + AccXYZ[1] + " " + AccXYZ[2] + " ");
            }
            catch (Exception e)
            {

            }
        }
    }
}
