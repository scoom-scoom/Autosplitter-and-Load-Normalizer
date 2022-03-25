# Current LLR stuff
- Have the program save the image at the start and end of the measured load, so that you can quickly check if something is wrong.
- Measure poki load times.
- Check many different runs work with the load bounds for the first 3 loads.
- Continue measuring load times (only 10 samples per load at first) and check that different runs work.
- Start by only measuring the middle 2x2 patch of pixels.
    - Make sure each load is within the load time threshold. This will get rid of most false detections. DON'T FORGET to change the times for OG PSP hardware, which is longer than emulator.
    - Make sure each black screen lasts for a time within the black screen threshold. Not sure how much this will help, but it's definitely worth a shot.
    - If there are still false detections:
        - Ask Isaki if he has any ideas.
        - Could check to see if the pixels are close to the cutscene pixels (e.g. blue pixels for the ship cutscene). This could be dodgy though due to gameplay triggering this, but you can still use this as a last resort after the previous 2 checks.
        - Make the program wait a number of seconds before detecting the ship cutscene. This will need to be updated according to the comgold sheet (have the program download the comgold sheet when it starts and use these values to make sure that the program doesn't wait too long and miss an actual load.)
            - BE CAREFUL as this depends on what WR time is. If someone does a run with a new strat where the time is significantly lower, then this program could break.
- GREAT IDEA you could change the patch size after each load, so that the next load will be detected correctly.
- GREAT IDEA, have the program try to scan through with the smallest crop patch size, and if there is an incorrect number of loads, it can scan through again with +1 on the patch size scale.
    - If this also fails, it can override the patch scaling and go up in pixel steps until it gets the correct number of loads.
- Make sure autosplitter file is consistently timing loads.    

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