# Current LN stuff
- Normalize all of the speedrun.com runs.
- When releasing, see if you can run 2 instances of livesplit at the same time, having one time with the autospliter, and one without.

# ASL:
- IMPORTANT Check that cutscene values for when the load starts and ends line up with manual LN.
- Make a graph of all the loads using Python.
- Issue warnings:
    - To name Yeezy% and 5TB splits with Kalidon suffix, or else the autosplitter will give lower times for other categories.
    - ALSO issue warning to name Wrench Only and Hundo Challax with suffix.

# Message at end of LN:
- Thank sm people for being patient with my progress.
- Thank the rac community for being nice and funny people, and always shit posting.
- Talk about applying this to rac2.

# Maybe later:
- Could also apply this program to other rac LN (I think rac2 would work, as it has black screens for the loads).
    - Look at getting ALL rac2 and rac3 runs converted to LN time.

# Making a video autosplitter:
- 1.) Isaki suggested to have the video-autosplitter program write to a memory-mapped file. Then, have the Livesplit ASL file read the memory mapped file to decide when to split.
- 2.) Look at how Toufol hooked up the video-autosplitter to livesplit, and copy that to make a video autosplitter that is highly performant, doesn't stop working, and doesn't have the annoying glitch where you save a screenshot and leave the video on the screenshot frame, so it splits infinitely.
    - It woud be a hassle for people to provide their own screenshots and have to update whenever they change layouts though. Maybe they could scale and translate an image and overlay it on the new layout. Then, the program could adjust all split images as necessary. It wouldn't be a perfect overlay, but you would only need 95% pixel matches. If this isn't matching at all, then you could try shifting the images pixels to the left or right to match the images.

# LN stuff (OLD)
- Check if there is a common threshold value that works for all 360p vids.
- Start by only measuring the middle 2x2 patch of pixels.
    - DON'T FORGET to change the times for OG PSP hardware, which is longer than emulator.
    - If there are still false detections:
        - Ask Isaki if he has any ideas.
        - Could check to see if the pixels are close to the cutscene pixels (e.g. blue pixels for the ship cutscene). This could be dodgy though due to gameplay triggering this, but you can still use this as a last resort after the previous 2 checks.
        - Make the program wait a number of seconds before detecting the ship cutscene. This will need to be updated according to the comgold sheet (have the program download the comgold sheet when it starts and use these values to make sure that the program doesn't wait too long and miss an actual load.)
            - BE CAREFUL as this depends on what WR time is. If someone does a run with a new strat where the time is significantly lower, then this program could break.
- GREAT IDEA you could change the patch size after each load, so that the next load will be detected correctly.
- GREAT IDEA, have the program try to scan through with the smallest crop patch size, and if there is an incorrect number of loads, it can scan through again with a greater patch size.
    - If this also fails, it can override the patch scaling and go up in pixel steps until it gets the correct number of loads.

# Custom made LN by video:
- 1.) Give video file to program, and it will scan frame by frame and output LN time of the speed-run based on the category.
    - Measure the optimal load time in frames for the ASL by having a counter in an action that runs every frame (maybe split) (Test that it actually prints every frame by recording it).
    - Get it working for only the ship cutscenes, then see if any runs have cutscenes not skipped, and make program detect if the cuscene is shorter than the ship cutscene, and if so, discard and start the time again on the ship cutscene.
    - Maybe adjust the ASL file to split as soon as the cutscene value changes, rather than to a constant value, so that the split is close to when the ship cutscene ends.
        - Take 60FPS samples to measure how effective this is, and offset LN-programs frames if necessary.
- 2.) (Good for speedrun.com vids) Record the screen and measure the total load time, then have the program do math with stored LN times and the total speed-run time to output LN speed-run time.
- Use SM textures for the program's GUI, and maybe a meme image in the background.

# (Old) Toufol image scanning:
- Use image scanning LN to do LN on recorded runs
    - Check that the image scanner splits at the right images at the start and end of each load.
    - Check that I actually can program the ASL to split at the right times, lining up with the image scanner. If its consistent, you could have the image scanner wait a number of milliseconds after the black screen, so that it lines up with the ASL file.
- Use image scanning to do LN on console runs in real time
- See if you can trust Toufool app after enough testing.
    - Test on stream vids too, as the image quality changes. Probably don't want to use screenshots from streams, as the quality will be variable.
- Measure CPU usage
- Have a link in my github to the releases page of Toufool.
- Maybe publish LN changes to actual repo?

Tested the program on various videos. It seems to only work on EMU runs, and there isn't much I can do about that for now (I could run the program over the vid many times with different settings until the final load normalized time is valid).