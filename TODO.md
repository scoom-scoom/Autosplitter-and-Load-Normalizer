# Current LN stuff
- Make the program automate Voll's Size Matters runs if needed?
- Work on rac2 load normalizer.
    1.) Try measure the pixel data of people's runs and see if there is a consistent pattern with the colour of the black screens at different points in the game (e.g. black screen before load 5 is always 50% more black than the black screen before load 11). Then, you could just match the pattern for the splitting and load normalizing.
    2.) If 1.) doesn't work, then try matching against the difference between the frame before the black screen, and the first black frame of the black screen.
    3.) If 2.) don't work, have the user draw a crop around their gameplay screen and match that cropped frame to a generic set of rac2 load screenshots (the user doesn't have to take their own screenshots), where every video resolution is supported, and the program can check each resolution for a match.
    4.) If 3.) doesn't work, then try have the user take their own screenshots.
    5.) if 4.) doesn't work, cry, as you will have to do all the load normalization manually. If doing manually, use a spreadsheet like what I did for size matters. 
- Work on rac2 real-time autosplitter and load normalizer.

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

# Custom made LN by video (OLD):
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