# Autosplitter and Load Normalizer for Ratchet and Clank - Size Matters

This repository contains the contents required for the autosplitter and load normalizer used for speed running the game Ratchet and Clank Size Matters.

There is also an unfinished project which is a video based load normalizer. It was supposed to be used on the Size Matters runs, but some people have different colored black screens on their run videos for some reason (so the pixels are not all [0, 0, 0]). See "TODO.txt" for some ideas for next steps. This video based load normalizer could very easily be adapted and used for rac2.

This is how I download run videos to look at frame by frame by the way:
https://en.y2mate.is/55/youtube-to-mp4.html
https://github.com/Franiac/TwitchLeecher/releases
https://darbyjohnston.github.io/DJV/

The autosplitter file (.asl file) is written in ASL (Auto splitting language - https://github.com/LiveSplit/LiveSplit.AutoSplitters/blob/master/README.md), which uses C# with some special syntax. The autosplitter also supports long load removal.

## How to use:

https://youtu.be/GHNmgyuaKh0