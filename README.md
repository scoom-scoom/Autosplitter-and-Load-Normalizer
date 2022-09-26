# Autosplitter and Load Normalizer for Ratchet and Clank - Size Matters (but could be adapted for Rac2)
This repository contains the contents required for the autosplitter and load normalizer (an Auto Splitting Language file) used for speed running the game Ratchet and Clank Size Matters. The autosplitter file (.asl file) is written in ASL (Auto Splitting Language - https://github.com/LiveSplit/LiveSplit.AutoSplitters/blob/master/README.md), which uses C# with some special syntax. The autosplitter also supports long load removal.

## How to use the autosplitter for Size Matters:
https://youtu.be/GHNmgyuaKh0

## Image-based autosplitting and load normalization:
There is also an unfinished project which is a video based load normalizer. It was supposed to be used on the Size Matters runs, but some people have different colored black screens on their run videos for some reason (so the pixels are not all [0, 0, 0]). See "TODO.txt" for some ideas for next steps. This video based load normalizer could very easily be adapted and used for rac2.

**Explanation of the motivation behind the image-based autosplitter program for rac2:**

**Memory scanning:**\
So, you want to load normalize rac2 run videos and runs in real time because the loads vary. The best way to do this is in real-time by looking at the memory addresses of the game, and using that to split and do load normalization. Because rac2 is optimal on ps2 for many categories, ps2 is hard to use for memory addresses, so that option is ruled out.

**Image-based scanning:**\
The next best option is to scan the video frame by frame, offline or in real-time, to determine when the loads start and end. There exists software that does this image-based scanning where screenshots of where you want to split are provided, and the program compares each frame to the split screenshots until a match of around 95% or greater in the pixel data is achieved, then a split is performed. This means that you will have to provide a set of rac2 load screenshots to match against (preferably for each video resolution, to support people's different resolutions), or else have the user take their own screenshots. Another downside to this method is that the user will have to draw a crop around their game so that only the game pixel data is being captured. Also, for the toufool autosplitter, you need to have the game window un-minimized. I'm pretty sure this program works for windows only as well, but you could adapt the code to run on Mac or Linux because it's open source (toufool). 
This is the only program that does that in real time, and could be used offline as well if you adapt the code:
https://github.com/Toufool/Auto-Split

**My image-based scanning improvement:**\
So, my idea is that, because size matters and rac2 have black screens before and after the loads, instead of having to have a user take screenshots, just compare the current frame to the black screen frame (every pixel is [0, 0, 0]). This also has the benefit that you are less likely to miss a comparison, because you're not relying on that 95% match. Some other benefits is that the user doesn't need to crop their game feed, as you can just compare the centre 20 pixels or so to black. 

**The problem with my idea:**\
The problem with my idea is that for some reason, different people's run videos have different pixel values for the black screens. These values are close to black, but not exactly [0, 0, 0]. 

**My proposed solutions to my idea:**\
1.) Try measure the pixel data of people's runs and see if there is a consistent pattern with the colour of the black screens at different points in the game (e.g. black screen before load 5 is always 50% more black than the black screen before load 11). Then, you could just match the pattern for the splitting and load normalizing.\
2.) If 1.) doesn't work, then try matching against the difference between the frame before the black screen, and the first black frame of the black screen.\
3.) If 2.) don't work, have the user draw a crop around their gameplay screen and match that cropped frame to a generic set of rac2 load screenshots (the user doesn't have to take their own screenshots), where every video resolution is supported, and the program can check each resolution for a match.\
4.) If 3.) doesn't work, then try have the user take their own screenshots.\
5.) if 4.) doesn't work, cry, as you will have to do all the load normalization manually. If doing manually, use a spreadsheet like what I did for size matters. 

## How I download run videos and view them frame by frame:
https://en.y2mate.is/55/youtube-to-mp4.html
https://github.com/Franiac/TwitchLeecher/releases
https://darbyjohnston.github.io/DJV/



