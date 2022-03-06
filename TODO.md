All the contents required for the autosplitter and load normalizer used for speedrunning the game Ratchet and Clank Size Matters.
$73mkMCMpqRN8o
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
https://github.com/mindfulmonk600/ASL-RAC-SM.git
mindful monk: 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

# Current LLR stuff
- Make new github which doesn't have my full name on it, and transfer this project.
- Rename frame scanner to image scanner.
- Test the program on various videos (video and screen scanning) to see:
    - If I can just use exactly 0. Is the ship fade exactly 0 after a certain number of frames everytime?
    - If the differences between black and the almost black image are consistent, or can at least be bounded.
- AFTER more measurements, change the threshold to be the difference between prev and curr frame, based on the 7th and 8th pb measurements I did.
    - OR use both difference and curr value below threshold, as the value differences seem to be very inconsistent.
    - COULD try to match exact ship frame, but this would fail when having different offsets after cropping.
- IF NEEDED Have a number of frames during the load where the program isn't scanning for anything. It should be optimal number of game frames minus 15 (half a second).

# Custom made llr by video:
- 1.) Give video file to program, and it will scan frame by frame and output LLR time of the speed-run based on the category.
    - Measure the optimal load time in frames for the ASL by having a counter in an action that runs every frame (maybe split) (Test that it actually prints every frame by recording it).
    - Get it working for only the ship cutscenes, then see if any runs have cutscenes not skipped, and make program detect if the cuscene is shorter than the ship cutscene, and if so, discard and start the time again on the ship cutscene.
    - Maybe adjust the ASL file to split as soon as the cutscene value changes, rather than to a constant value, so that the split is close to when the ship cutscene ends.
        - Take 60FPS samples to measure how effective this is, and offset llr-programs frames if necessary.
- 2.) (Good for speedrun.com vids) Record the screen and measure the total load time, then have the program do math with stored LLR times and the total speed-run time to output LLR speed-run time.
- Use SM textures for the program's GUI, and maybe a meme image in the background.

# Message at end of LLR video:
- Thank the rac community for being nice and funny people.
- Thank sm people for being patient with my progress.
- Talk about applying this to rac2.
- Ask if anyone wants LLR or autosplitting in their rac game. Say that Isaki has alread implemented a lot of cool stuff in rac1 and uya.

# Maybe later:
- Could also apply this program to other rac llr (I think rac2 would work, as it has black screens for the loads).
    - Look at getting ALL rac2 and rac3 runs converted to llr time.

# Making a video autosplitter:
- 1.) Isaki suggested to have the video-autosplitter program write to a memory-mapped file. Then, have the Livesplit ASL file read the memory mapped file to decide when to split.
- 2.) Look at how Toufol hooked up the video-autosplitter to livesplit, and copy that to make a video autosplitter that is highly performant, doesn't stop working, and doesn't have the annoying glitch where you save a screenshot and leave the video on the screenshot frame, so it splits infinitely.
    - It woud be a hassle for people to provide their own screenshots and have to update whenever they change layouts though. Maybe they could scale and translate an image and overlay it on the new layout. Then, the program could adjust all split images as necessary. It wouldn't be a perfect overlay, but you would only need 95% pixel matches. If this isn't matching at all, then you could try shifting the images pixels to the left or right to match the images.

# ASL:
- IMPORTANT Check that cutscene values for when the load starts and ends line up with the llr by video.
- Might have to change when the split starts, as you want it to be as soon as you get a black screen, not when the ship cutscene loads.
- Measure all load variations using output from the autosplitter, NOT video!
- Also measure the non-planet loads that I'm not sure about.
- Make a graph of all the loads using Python.
- See if I can get LiveSplit to auto detect the ASL, rather than from a local file.
- Issue warnings:
    - To name Yeezy% and 5TB splits with Kalidon suffix, or else the autosplitter will give lower times for other categories.
    - ALSO issue warning to name Wrench Only and Hundo Challax with suffix.
    - ALSO issue warning about using autosplitter and going to wrong planet accidentally, then returning to the planet you came from accidentally, as it will split due to checking for "current planet == && planetChanged".

# (Old) Toufol image scanning:
- Use image scanning LLR to do LLR on recorded runs
    - Check that the image scanner splits at the right images at the start and end of each load.
    - Check that I actually can program the ASL to split at the right times, lining up with the image scanner. If its consistent, you could have the image scanner wait a number of milliseconds after the black screen, so that it lines up with the ASL file.
- Use image scanning to do LLR on console runs in real time
- See if you can trust Toufool app after enough testing.
    - Test on stream vids too, as the image quality changes. Probably don't want to use screenshots from streams, as the quality will be variable.
- Measure CPU usage
- Have a link in my github to the releases page of Toufool.
- Maybe publish LLR changes to actual repo?