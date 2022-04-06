// ------------------------------------------------ //
// Ratchet and Clank Size Matters - Autosplitter
// ------------------------------------------------ //

state("PPSSPPWindows64") { }

startup {
		vars.scanTarget = new SigScanTarget (0, "48 45 52 4F 53 4B 49 4E 5F 49 6E 69 74 53 69 6E 67 6C 65 50 6C 61 79 65 72");
		
        settings.Add("Yeezy%Split", false, "Yeezy% - Split on wildfire boots collection");
        settings.Add("5TBSplit", false, "5TB - Split on 5th Titanium Bolt");
		settings.Add("GiantClank2Split", true, "Split on Giant Clank 2 (For Wrench only and 100%)");
		settings.Add("Challax2Split", true, "Split on Challax 2 (For Wrench only and 100%)");
		settings.Add("SplitOnBolt", false, "Split on Bolt (see tooltip).");
		settings.SetToolTip("SplitOnBolt", "WARNING: This feature has not been tested in a full run, use at your own risk." + 
		"Set this to true if you want to additionally split on each bolt (the split happens after the bolt collection animation" +
		"is finished, due to current technical limitations).");
		settings.Add("AutoReset", true, "Auto-reset the timer (see tooltip).");
		settings.SetToolTip("AutoReset", "Reset the timer when starting on Pokitaru again (don't use for the 100% category though!).");
		settings.Add("LoadNormalization", false, "Load Normalization (see tooltip).");
		settings.SetToolTip("LoadNormalization", "WARNING: This feature has not been tested in a full run, use at your own risk." +
		"Toggle this to have the timer pause when the load time exceeds the optimal time.");

		vars.loadStartTime = -1;
		vars.isLoading = false;
		vars.checkForLoadNormalization = false;

		// Set to true once we reach Dayni Moon for the first time, so that we know to look for the Dayni Moon 2 split next time we go to Challax.
		vars.dayniMoon1 = false;

		// Set to true if we have reached Dayni Moon 2, so that the load normalization doesn't hit Dayni Moon 1 by accident.
		vars.dayniMoon2 = false;

		// Set to true once we reach Challax for the first time, so that we know to look for the Challax 2 split next time we go to Challax.
		vars.challax1 = false;

		// Set to true if we have reached Challax 2 in Wrench Only or Hundo, so that the load normalization doesn't hit Challax 1 by accident.
		vars.challax2 = false;

		// optimalLoadTime is measured in milliseconds.
		// vars.optimalLoadTimeRyllus = 12783;
		// vars.optimalLoadTimeKalidon = 12809;
		vars.optimalLoadTimeRyllus = 10;
		vars.optimalLoadTimeKalidon = 10;

		// Taken from https://raw.githubusercontent.com/tduva/LiveSplit-ASL/master/AlanWake.asl
		Action<string> LogDebug = (text) => {
			print("[DEBUG] " + text);
		};
		vars.LogDebug = LogDebug;

		Action ResetLoadTimeVars = () => {
			vars.loadStartTime = -1;
			vars.isLoading = false;
			vars.checkForLoadNormalization = false;
		};
		vars.ResetLoadTimeVars = ResetLoadTimeVars;

		Action ResetAllVars = () => {
			vars.ResetLoadTimeVars();
			vars.challax1 = false;
			vars.challax2 = false;
			vars.dayniMoon1 = false;
			vars.dayniMoon2 = false;
		};
		vars.ResetAllVars = ResetAllVars;

		// Takes the optimalLoadTime for this current load and the value (in memory) of the cutscene which plays at the end of the load.
		// This info is used to determine when to pause and resume the timer to normalize the long load.
		Action<int, int> CheckLoadNormalization = (optimalLoadTime, cutsceneVal) => {
			TimeSpan rt = (TimeSpan) timer.CurrentTime.RealTime;
			if ((rt.TotalMilliseconds - vars.loadStartTime) > optimalLoadTime) {
				// Pause the timer to normalize the long load.
				// DEBUGGING
				vars.isLoading = true;
			}
			if (vars.currentCutscene.Current == cutsceneVal) {
				vars.LogDebug("Load time is:" + (rt.TotalMilliseconds - vars.loadStartTime));
				// Resume the timer once the load is done, and the cutscene is playing.
				vars.ResetLoadTimeVars();
			}
		};
		vars.CheckLoadNormalization = CheckLoadNormalization;

		Action<bool> LoadStarted = (isLoadNormalization) => {
			if (isLoadNormalization) {
				// Record the time, as we have entered the load. This will be used for load normalization.
				TimeSpan rt = (TimeSpan) timer.CurrentTime.RealTime;
				vars.loadStartTime = rt.TotalMilliseconds;
				vars.checkForLoadNormalization = true;
			}
		};
		vars.LoadStarted = LoadStarted;
}

init {
	// Run at 30 fps for this 30 fps game. For some weird reason, 60 fps is actually 30 fps (this has been tested). Maybe 
	// it's because the code in this file takes ages to run each frame.
	refreshRate = 60;
	
	var ptr = IntPtr.Zero;

	foreach (var page in game.MemoryPages(true)) {
		var scanner = new SignatureScanner(game, page.BaseAddress, (int)page.RegionSize);
		
		if (ptr == IntPtr.Zero) {
			ptr = scanner.Scan(vars.scanTarget);
		} else {
			break;
		}
	}
	
	vars.currentPlanet = new MemoryWatcher<int>(ptr + 0x190);
	vars.pokiSpawn = new MemoryWatcher<int>(ptr + 0xC7A6F0);
	vars.ottoEntry = new MemoryWatcher<float>(ptr + 0xBAB4F8);
	vars.currentCutscene = new MemoryWatcher<int>(ptr + 0x178CC1D);
    vars.kalidonMoveState = new MemoryWatcher<int>(ptr + 0xBAA8C0);
    vars.titBoltCount = new MemoryWatcher<int>(ptr + 0x80CF8);
	
	vars.watchers = new MemoryWatcherList() {
		vars.currentPlanet,
		vars.pokiSpawn,
		vars.ottoEntry,
		vars.currentCutscene,
        vars.kalidonMoveState,
		vars.titBoltCount
	};
}

update {
	vars.watchers.UpdateAll(game);
}

split {
	// DEBUGGING
	// vars.LogDebug("TEST");
	// vars.LogDebug("Planet: " + vars.currentPlanet.Current);
	// vars.LogDebug("Cutscene " + vars.currentCutscene.Current);

	// NOTE: You cannot use "else if" statements in this "split" function, as there are toggled settings.
	// For example, if one of the settings is true but there is no split, then none of the other
	// "else if" statements will be checked for a split.
	if (settings["SplitOnBolt"]) {
		// For some reason, the memory address value containing the bolt count is multiplied by 256.
		int boltCountOld = (int) (vars.titBoltCount.Old / 256);
		int boltCountCurrent = (int) (vars.titBoltCount.Current / 256);
		// Check to see if our bolt count has gone up by 1. If so, split.
		if ((boltCountCurrent - boltCountOld) == 1) {
			return true;
		}
	}

	// Split on each planet
	bool isLoadNormalization = settings["LoadNormalization"];
	bool planetChanged = false;
	if (vars.currentPlanet.Current != vars.currentPlanet.Old) {
		planetChanged = true;
	}
	// Ryllus
	if (vars.currentPlanet.Current == 2 && planetChanged) {
		vars.LoadStarted(isLoadNormalization);
		return true;
	}
	// Kalidon
	if (vars.currentPlanet.Current == 3 && planetChanged) {
		vars.LoadStarted(isLoadNormalization);
		return true;
	}
	if (settings["Yeezy%Split"]) {
		if (vars.currentPlanet.Current == 3 && vars.kalidonMoveState.Current == 1097126595) {
			return true;
		}
	}
	if (settings["5TBSplit"]) {
		if (vars.currentPlanet.Current == 3 && vars.kalidonMoveState.Current == 1094363991) {
			return true;
		}
	}
	// Metalis
	if (vars.currentPlanet.Current == 4 && planetChanged) {
		vars.LoadStarted(isLoadNormalization);
		return true;
	}
	// Metalis Giant Clank
	if (vars.currentPlanet.Current == 15 && planetChanged) {
		vars.LoadStarted(isLoadNormalization);
		return true;
	}
	// Dreamtime
	if (vars.currentPlanet.Current == 5 && planetChanged) {
		vars.LoadStarted(isLoadNormalization);
		return true;
	}
	// MOO
	if (vars.currentPlanet.Current == 6 && planetChanged) {
		vars.LoadStarted(isLoadNormalization);
		return true;
	}
	// Remains
	if (vars.currentPlanet.Current == 23 && planetChanged) {
		vars.LoadStarted(isLoadNormalization);
		return true;
	}
	// Challax
	if (vars.currentPlanet.Current == 7 && planetChanged && !vars.challax1) {
		vars.LoadStarted(isLoadNormalization);
		vars.challax1 = true;
		return true;
	}
	// Challax Giant Clank 2 (For Wrench Only and 100%)
	if (settings["GiantClank2Split"]) {
		if (vars.currentPlanet.Current == 21 && planetChanged) {
		    vars.LoadStarted(isLoadNormalization);
			return true;
		}
		// Split on Challax 2 (when you return from giant clank section back to Challax)
		else if (vars.currentPlanet.Current == 7 && planetChanged && vars.challax1) {
		    vars.LoadStarted(isLoadNormalization);
			vars.challax2 = true;
			return true;
		}
	}
	// Dayni Moon
	if (vars.currentPlanet.Current == 8 && planetChanged && !vars.dayniMoon1) {
		vars.LoadStarted(isLoadNormalization);
		vars.dayniMoon1 = true;
		return true;
	}
	// Inside Clank
	if (vars.currentPlanet.Current == 9 && planetChanged) {
		vars.LoadStarted(isLoadNormalization);
		return true;
	}
	// Dayni Moon 2
	if (vars.currentPlanet.Current == 8 && planetChanged && vars.dayniMoon1) {
		vars.LoadStarted(isLoadNormalization);
		vars.dayniMoon2 = true;
		return true;
	}
	// Quodrona
	if (vars.currentPlanet.Current == 10 && planetChanged) {
		vars.LoadStarted(isLoadNormalization);
		return true;
	}
	// Otto
	if (vars.currentPlanet.Current == 10) {
		if (vars.ottoEntry.Current == 75000 && vars.ottoEntry.Old <= 0) {
			return true;
		}
	}
	// Split at the end of the run.
	if (vars.currentPlanet.Current == 10 && vars.currentCutscene.Current == 776417329) {
		return true;
	}
}
	
start {
	if (vars.currentPlanet.Current ==  1)
	{
		vars.ResetAllVars();
		return vars.pokiSpawn.Current == 1 && vars.pokiSpawn.Old == 0;
	}
}

reset {
	if (settings["AutoReset"]) {
		if (vars.currentPlanet.Current ==  1)
		{
			vars.ResetAllVars();
			return vars.pokiSpawn.Current == 1 && vars.pokiSpawn.Old == 0;
		}
	}
}

isLoading {
	// NOTE: You cannot use "else if" statements in this block, as there are toggled settings.
	// For example, if one of the settings is true but there is no split, then none of the other
	// "else if" statements will be checked for a split.
	if (vars.checkForLoadNormalization){
		// Ryllus
		if (vars.currentPlanet.Current == 2) {
			vars.CheckLoadNormalization(vars.optimalLoadTimeRyllus, 776024624);
		}
		// Kalidon
		if (vars.currentPlanet.Current == 3) {
			vars.CheckLoadNormalization(vars.optimalLoadTimeKalidon, 776024880);
		}
		// Metalis
		if (vars.currentPlanet.Current == 4) {
			vars.CheckLoadNormalization(vars.optimalLoadTimeKalidon, 776025136);
		}
		// Metalis Giant Clank
		if (vars.currentPlanet.Current == 15) {
			vars.CheckLoadNormalization(vars.optimalLoadTimeKalidon, 654548);
		}
		// Dreamtime
		if (vars.currentPlanet.Current == 5) {
			vars.CheckLoadNormalization(vars.optimalLoadTimeRyllus, 776025392);
		}
		// MOO
		if (vars.currentPlanet.Current == 6) {
			vars.CheckLoadNormalization(vars.optimalLoadTimeRyllus, 776025648);
		}
		// Remains
		if (vars.currentPlanet.Current == 23) {
			vars.CheckLoadNormalization(vars.optimalLoadTimeRyllus, 654548);
		}
		// Challax
		if (vars.currentPlanet.Current == 7 && !vars.challax2) {
			vars.CheckLoadNormalization(vars.optimalLoadTimeRyllus, 776025904);
		}
		// Giant Clank 2 (only for Wrench Only and 100% categories)
		if (settings["GiantClank2Split"]) {
			if (vars.currentPlanet.Current == 21) {
				vars.CheckLoadNormalization(vars.optimalLoadTimeRyllus, 654548);
			}
			// Challax 2 (only for Wrench Only and 100% categories)
			else if (vars.currentPlanet.Current == 7 && vars.challax2) {
				vars.CheckLoadNormalization(vars.optimalLoadTimeRyllus, 776353584);
			}
		}
		// Dayni Moon
		if (vars.currentPlanet.Current == 8 && !vars.dayniMoon2) {
			vars.CheckLoadNormalization(vars.optimalLoadTimeRyllus, 654548);
		}
		// Inside Clank
		if (vars.currentPlanet.Current == 9) {
			vars.CheckLoadNormalization(vars.optimalLoadTimeRyllus, 776026416);
		}
		// Dayni Moon 2
		if (vars.currentPlanet.Current == 8 && vars.dayniMoon2) {
			vars.CheckLoadNormalization(vars.optimalLoadTimeRyllus, 776353840);
		}
		// Quodrona
		if (vars.currentPlanet.Current == 10) {
			vars.CheckLoadNormalization(vars.optimalLoadTimeRyllus, 776024113);
		}
	}
	return vars.isLoading;
}

// ------------------------------------------------ //
// Changelog (used before this project was on github)
// ------------------------------------------------ //
//
// scoom_scoom -> 03/04/2022
// - Man, I hate how long this file is. I wish I could use classes in ASL. I hope I never have to touch ASL again after this project!
//
// Emeralve -> 9/2/2022
// - shhh I was here.
//
// scoom_scoom -> 08/02/2022
// - Added splitting on bolt (splits after the bolt animation is finished). Memory address was found by Emeralve, good job man.
//
// scoom_scoom -> 30/12/2021
// - Added Yeezy% split on wildfire boots collection (the start of the minicutscene)
// - Added 5th titanium bolt split for 5TB category (splits the moment the bolt collection minicutscene triggers)
// - Tidied up if statements
