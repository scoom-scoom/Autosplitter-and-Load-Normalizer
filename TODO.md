# Current LLR stuff
- Great idea, have the program try to scan through with the smallest crop patch size, and if there is an incorrect number of loads, it can scan through again with +1 on the patch size scale.
If this also fails, it can override the patch scaling and go up in pixel steps until it gets the correct number of loads.
- IF HAVING ISSUES WITH BLACK SCREEN NOT BEING 0 DIFFERENCE, LLR think about stopping the time when the load screen changes to the last load screen (big pixel change). Will need to make sure last load time is consistent.
- Test the program on various videos (video and screen scanning) to see:
    - If I can just use exactly 0. Is the ship fade exactly 0 after a certain number of frames everytime?
    - If the differences between black and the almost black image are consistent, or can at least be bounded.
- AFTER more measurements, could change the threshold to be the difference between prev and curr frame, based on the 7th and 8th pb measurements I did.
    - OR use both difference and curr value below threshold, as the value differences seem to be very inconsistent.
    - Maybe the treshold can just be scaled for a particular video based on what the measurement is for the Ryllus load.
    - COULD try to match exact ship frame, but this would fail when having different offsets after cropping.
- Make sure autosplitter file is consistently timing loads.
- [LAST RESORT OPTIMIZATION] IF NEEDED Have a number of frames during the load where the program isn't scanning for anything.
    - BE CAREFUL as this depends on what WR time is. If someone does a run with a new strat where the time is significantly lower, then this program could break.

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