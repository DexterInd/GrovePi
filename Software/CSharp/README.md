# GrovePi for C#

Multiple implantationss of GrovePi exist for C#:

- Universal Windows Platform for Windows IoT Core. You will find all details [here](./README-UWP.md)
- .NET Core IoT for Linux or Windows. You will find all details [here](https://github.com/dotnet/iot/tree/master/src/devices/GrovePi)

Universal Windows Platform for Windows IoT Core is a specific implementation of Windows IoT Core running on boards like Raspberry Pi. It's best if you love XAML and traditional Universal Windows Platform and if you need a UI.

.NET Core is open source. .NET Core is best thought of as 'agile .NET'. Generally speaking it is the same as the Desktop .NET Framework distributed as part of the Windows operating system, but it is a cross platform (Windows, Linux, macOS) and cross architecture (x86, x64, ARM) subset that can be deployed as part of the application (if desired), and thus can be updated quickly to fix bugs or add features. It is a perfect fit for boards like Raspberry running Raspbian. Check the [.NET Core IoT documentation](https://github.com/dotnet/iot/tree/master/Documentation) if you are not familiar with .NET Core.
