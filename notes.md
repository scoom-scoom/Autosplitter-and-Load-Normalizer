## Load screens in the categories:

### Any% (13 loads in total) - taken from Alemusa WR vid 2021-02-04 on speedrun.com
- Pokitaru ship (not counted towards the load time though)
- Ryllus ship
- Kalidon ship
- Metallis ratchet floating (this still does black entrance and black fade out visually, not sure about exact values though)
- Giant Clank 1 (this still does black entrance and black fade out visually, not sure about exact values though)
- Dreamtime (fades into white screen visually, then one black screen, then the load, and then fades into black, not sure about exact values though)
- Moo ship
- Remains ship
- Challax ship before giant clank 2
- Giant Clank 2
- Challax ship after giant clank 2
- Dayni ship
- IC ratchet using shrink ray (this still does black entrance and black fade out visually, not sure about exact values though)
- Dayni 2 ratchet floating (this still does black entrance and black fade out visually, not sure about exact values though)
- Quodrona ship

## (OLD)
Video autosplitter just fuckin died on me. >:( Live capture just shows a black screen. Fuck this, I'm making my own.

## How to measure a load - start and end frames
We start at the first ship frame, and end on the first black frame after the ship fade (measured using a learned threshold value which is consistent for many tested videos). Here is why we measure by these frames:
- One time, I had ratchet freeze on poki for a second before going to a black screen, and loading. This is unfortunate, as there is no way to know what that exact frame looks like, so there is no way to measure that time in frames. After ratchet froze, the black screen didn't last as long as it usually does. Therefore, we should start measuring the load from when the first ship frame appears.
- The black screen after poki is mostly consisten, so it should be fine if we start measuring the load from the first ship frame.
- From the first black frame after the Ryllus load ship fade to the last black frame before the gameplay vs. cutscene, the frames were 29 for skipping the cutscene, and 52 for not skipping the cutscene. That's over half a second of variation! Therefore, we should not time these frames, and stick strictly to the frames where the ship is visible.

## (OLD) Video autosplitting
- Because the black screen load before the ship cutscene varies, its impossible to know what the exact image at the end of the optimal load time will be. Therefore, we need to hack into the Toufool autosplitter code to have an option to hit the split button after the optimal load time, specified in the split image filename.
- People will need to provide their own screenshots, as everyone has a different stream/recording setup, and some people have splits on their screen, ect. Once people create their own screenshots, they should be able to (with a consistent streaming/recording setup):
    - LLR offline
    - LLR in real-time
LLR offline:
    - It might be possible to use black screen split images on all pre-recorded runs, as the black pixels won't change. Then, only the other split images will have to change. DO NOT watch the whole video, have the code start the livesplit timer to display the LLR only by pausing and unpausing. Then, you can skip through the vid.
    - Otherwise, could write a quick Python script where you only need to write in the frame numbers, and the LLR is calculated for you. Just record my voice saying the frame numbers, and then write them to a file.