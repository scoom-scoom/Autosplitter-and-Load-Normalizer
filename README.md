# Autosplitter and Load Normalizer for Ratchet and Clank - Size Matters

This repository contains the contents required for the autosplitter and load normalizer used for speed running the game Ratchet and Clank Size Matters.

The autosplitter file (.asl file) is written in ASL (Auto splitting language - https://github.com/LiveSplit/LiveSplit.AutoSplitters/blob/master/README.md), which uses C# with some special syntax. The autosplitter also supports long load removal.

## How to use:

We need to select the autosplitter, and then switch all of the timing methods to "Game Time", as long load removal can only be done in terms of "Game Time".
- Right click on your LiveSplits, click on "Edit Layout -> Control -> Scriptable autosplitter".
- Double click on the scriptable autosplitter, and click browse.
- Open the downloaded autosplitter file, and select the checkboxes that you want.
- Double click on "Splits".
- Scroll down to the bottom and set the two "Timing method" boxes to "Game Time".
- Click on the "Timer" tab, and set the "Timing method" to "Game Time".
- Click "Ok". Click "Ok" again.
- Right click on your LiveSplits, click on "Edit Splits".
- Copy your "Real Time" split times over to the "Game Time" split times.
- Click "Ok".
- Right click on your LiveSplits, click on "Compare against", and select "Game Time".
- You are good to go fam!

TODO: Add photo's of what the category splits should look like for the autosplitter.