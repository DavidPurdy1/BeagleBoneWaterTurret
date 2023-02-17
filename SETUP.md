# BeagleBone Ai-64 Setup instructions
Here are some instructions for how I set up the beaglebone ai-64

Install a graphical OS, makes it easier to debug later imo.

I installed the [Bullseye XFCE (with graphical desktop) for BeagleBone AI-64](https://beagleboard.org/latest-images)

There are probably more up to date ones now

Once flashed on, to get the display port working you are going to want an ACTIVE micro display port adapter. Trust me there is a difference, the active ones have a thick block like [so]().

Once you get this and boot you should see a desktop boot up on the display.

Now you probably want some internet right?
 
So I setup the wifi dongle and used this for downloading everything. I used [](https://github.com/kelebek333/rtl8188fu) instructions for setting up the wifi drivers on the bone.

I will add for installation of the wifi drivers. Let it go though while you have something else to do because it will take a min to compile.
