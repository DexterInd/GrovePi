using System;
using System.Threading.Tasks;

namespace GrovePi.Common
{
    public static class Delay
    {
        public static async void Milliseconds(int milliseconds)
        {
            await Task.Delay(TimeSpan.FromMilliseconds(milliseconds));
        }
    }
}
