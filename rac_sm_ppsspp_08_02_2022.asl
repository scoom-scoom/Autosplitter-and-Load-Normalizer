// ------------------------------------------------ //
// Ratchet and Clank Size Matters - Autosplitter
// ------------------------------------------------ //

state("PPSSPPWindows64") { }

startup {
		vars.scanTarget = new SigScanTarget (0, "48 45 52 4F 53 4B 49 4E 5F 49 6E 69 74 53 69 6E 67 6C 65 50 6C 61 79 65 72");
		
        settings.Add("Yeezy%Split", false, "Yeezy% - Split on wildfire boots collection");
        settings.Add("5TBSplit", false, "5TB - Split on 5th Titanium Bolt");
		settings.Add("RemainsSplit", true, "Split on Remains");
		settings.Add("SplitOtto", true, "Split on Otto entry");
		settings.Add("ChallaxSplit", true, "Split on Challax");
		settings.Add("GiantClank2Split", true, "Split on Giant Clank 2 (For Wrench only and 100%)");
		settings.Add("IClankSplit", true, "Split after Inside Clank");
		settings.Add("QuodronaSplit", true, "Split on Quodrona");
		settings.Add("AutoReset", true, "Toggle this to auto-reset (NG+)");
		settings.Add("LongLoadRemoval", false, "Long Load Removal (see tooltip).");
		settings.SetToolTip("LongLoadRemoval", "WARNING: This feature has not been tested in a full run, use at your own risk. Toggle this to have the timer pause when the load time exceeds the optimal time.");
		settings.Add("SplitOnBolt", false, "Split on Bolt (see tooltip).");
		settings.SetToolTip("SplitOnBolt", "WARNING: This feature has not been tested in a full run, use at your own risk. Set this to true if you want to additionally split on each bolt (the split happens after the bolt collection animation is finished, due to current technical limitations).");

		vars.loadStartTime = -1;
		vars.isLoading = false;
		vars.checkForLoadRemoval = false;

		// Set to true if we have reached Dayni Moon 2, so that the long load removal doesn't hit Dayni Moon 1 by accident.
		vars.dayniMoon2 = false;

		// Set to true if we have reached Challax 2 in Wrench Only or Hundo, so that the long load removal doesn't hit Challax 1 by accident.
		vars.challax2 = false;

		// optimalLoadTime is measured in milliseconds.
		vars.optimalLoadTimeRyllus = 12783;
		vars.optimalLoadTimeKalidon = 12809;

		// Taken from https://raw.githubusercontent.com/tduva/LiveSplit-ASL/master/AlanWake.asl
		Action<string> LogDebug = (text) => {
			print("[DEBUG] " + text);
		};
		vars.LogDebug = LogDebug;

		Action ResetLoadTimeVars = () => {
			vars.loadStartTime = -1;
			vars.isLoading = false;
			vars.checkForLoadRemoval = false;
			vars.dayniMoon2 = false;
			vars.challax2 = false;
		};
		vars.ResetLoadTimeVars = ResetLoadTimeVars;

		// Takes the optimalLoadTime for this current load and the value (in memory) of the cutscene which plays at the end of the load.
		// This info is used to determine when to pause and resume the timer to remove the long load.
		Action<int, int> CheckLoadRemoval = (optimalLoadTime, cutsceneVal) => {
			TimeSpan rt = (TimeSpan) timer.CurrentTime.RealTime;
			if ((rt.TotalMilliseconds - vars.loadStartTime) > optimalLoadTime) {
				// Pause the timer to remove the long load.
				vars.isLoading = true;
			}
			if (vars.currentCutscene.Current == cutsceneVal) {
				// Resume the timer once the load is done, and the cutscene is playing.
				vars.ResetLoadTimeVars();
				vars.LogDebug("Load resumed");
			}
		};
		vars.CheckLoadRemoval = CheckLoadRemoval;

		Action LoadStarted = () => {
			// Record the time, as we have entered the load. This will be used for long load removal.
			TimeSpan rt = (TimeSpan) timer.CurrentTime.RealTime;
			vars.loadStartTime = rt.TotalMilliseconds;
			vars.checkForLoadRemoval = true;
		};
		vars.LoadStarted = LoadStarted;
}

init {
	refreshRate = 1000/30;
	
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
	// vars.LogDebug("Planet: " + vars.currentPlanet.Current);
	// vars.LogDebug("Cutscene " + vars.currentCutscene.Current);
	// vars.LogDebug("Tit bolt count " + vars.titBoltCount.Current);

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
	bool planetChanged = false;
	if (vars.currentPlanet.Current != vars.currentPlanet.Old) {
		planetChanged = true;
	}
	// Ryllus
	if (vars.currentPlanet.Current == 2 && planetChanged) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
		return true;
	}
	// Kalidon
	if (vars.currentPlanet.Current == 3 && planetChanged) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
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
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
		return true;
	}
	// Metalis Giant Clank
	if (vars.currentPlanet.Current == 15 && planetChanged) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
		return true;
	}
	// Dreamtime
	if (vars.currentPlanet.Current == 5 && planetChanged) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
		return true;
	}
	// MOO
	if (vars.currentPlanet.Current == 6 && planetChanged) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
		return true;
	}
	if (settings["RemainsSplit"]) {
		if (vars.currentPlanet.Current == 23 && planetChanged) {
			if (settings["LongLoadRemoval"]) {
				vars.LoadStarted();
			}
			return true;
		}
	}
	if (settings["ChallaxSplit"]) {
		if (vars.currentPlanet.Current == 7 && planetChanged) {
			if (settings["LongLoadRemoval"]) {
				vars.LoadStarted();
			}
			return true;
		}
	}
	// Challax Giant Clank 2 (For Wrench Only and 100%)
	if (settings["GiantClank2Split"]) {
		if (vars.currentPlanet.Current == 21 && planetChanged) {
			if (settings["LongLoadRemoval"]) {
				vars.LoadStarted();
			}
			return true;
		}
		// Split on Challax 2 (when you return from giant clank section back to Challax)
		if (vars.currentPlanet.Current == 7 && planetChanged) {
			if (settings["LongLoadRemoval"]) {
				vars.LoadStarted();
			}
			vars.challax2 = true;
			return true;
		}
	}
	// Dayni Moon
	if (vars.currentPlanet.Current == 8 && planetChanged) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
		return true;
	}
	if (settings["IClankSplit"]) {
		if (vars.currentPlanet.Current == 9 && planetChanged) {
			if (settings["LongLoadRemoval"]) {
				vars.LoadStarted();
			}
			return true;
		}
	}
	// Dayni Moon 2
	if (vars.currentPlanet.Current == 8 && planetChanged) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
		vars.dayniMoon2 = true;
		return true;
	}
	if (settings["QuodronaSplit"]) {
		if (vars.currentPlanet.Current == 10 && planetChanged) {
			if (settings["LongLoadRemoval"]) {
				vars.LoadStarted();
			}
			return true;
		}
	}
	if (settings["SplitOtto"]) {
		if (vars.currentPlanet.Current == 10) {
			if (vars.ottoEntry.Current == 75000 && vars.ottoEntry.Old <= 0) {
				return true;
			}
		}
	}
	// Split on end of run
	if (vars.currentPlanet.Current == 10 && vars.currentCutscene.Current == 776417329) {
		return true;
	}
}
	

start {
	if (vars.currentPlanet.Current ==  1)
	{
		vars.ResetLoadTimeVars();
		return vars.pokiSpawn.Current == 1 && vars.pokiSpawn.Old == 0;
	}
}

reset {
	if (settings["AutoReset"]) {
		if (vars.currentPlanet.Current ==  1)
		{
			vars.ResetLoadTimeVars();
			return vars.pokiSpawn.Current == 1 && vars.pokiSpawn.Old == 0;
		}
	}
}

isLoading {
	// Long load removal
	if (vars.checkForLoadRemoval){
		// Ryllus
		if (vars.currentPlanet.Current == 2) {
			vars.CheckLoadRemoval(vars.optimalLoadTimeRyllus, 776024624);
		}
		// Kalidon
		else if (vars.currentPlanet.Current == 3) {
			vars.CheckLoadRemoval(vars.optimalLoadTimeKalidon, 776024880);
		}
		// Metalis
		else if (vars.currentPlanet.Current == 4) {
			vars.CheckLoadRemoval(vars.optimalLoadTimeKalidon, 776025136);
		}
		// Metalis Giant Clank
		if (vars.currentPlanet.Current == 15) {
			vars.CheckLoadRemoval(vars.optimalLoadTimeKalidon, 654548);
		}
		// Dreamtime
		if (vars.currentPlanet.Current == 5) {
			vars.CheckLoadRemoval(vars.optimalLoadTimeRyllus, 776025392);
		}
		// MOO
		if (vars.currentPlanet.Current == 6) {
			vars.CheckLoadRemoval(vars.optimalLoadTimeRyllus, 776025648);
		}
		if (settings["RemainsSplit"]) {
			if (vars.currentPlanet.Current == 23) {
				vars.CheckLoadRemoval(vars.optimalLoadTimeRyllus, 654548);
			}
		}
		if (settings["ChallaxSplit"]) {
			if (vars.currentPlanet.Current == 7 && !vars.challax2) {
				vars.CheckLoadRemoval(vars.optimalLoadTimeRyllus, 776025904);
			}
		}
		// Challax Giant Clank 2
		if (settings["GiantClank2Split"]) {
			if (vars.currentPlanet.Current == 21) {
				vars.CheckLoadRemoval(vars.optimalLoadTimeRyllus, 654548);
			}
			if (vars.currentPlanet.Current == 7 && vars.challax2) {
				vars.CheckLoadRemoval(vars.optimalLoadTimeRyllus, 776353584);
			} 
		}
		// Dayni Moon
		if (vars.currentPlanet.Current == 8 && !vars.dayniMoon2) {
			vars.CheckLoadRemoval(vars.optimalLoadTimeRyllus, 654548);
		}
		if (settings["IClankSplit"]) {
			if (vars.currentPlanet.Current == 9) {
				vars.CheckLoadRemoval(vars.optimalLoadTimeRyllus, 776026416);
			}
		}
		// Dayni Moon 2
		if (vars.currentPlanet.Current == 8 && vars.dayniMoon2) {
			vars.CheckLoadRemoval(vars.optimalLoadTimeRyllus, 776353840);
		}
		if (settings["QuodronaSplit"]) {
			if (vars.currentPlanet.Current == 10) {
				vars.CheckLoadRemoval(vars.optimalLoadTimeRyllus, 776024113);
			}
		}
	}
	return vars.isLoading;
}

// ------------------------------------------------ //
// Changelog
// ------------------------------------------------ //
//
// Emeralve -> 9/2/2022
// - shhh I was here.
//
// scoom_scoom -> 08/02/2022
// - Added splitting on bolt (after the bolt animation is finished). Memory address was found by Emeralve.
//
// scoom_scoom -> 30/12/2021
// - Added Yeezy% split on wildfire boots collection (the start of the minicutscene)
// - Added 5th titanium bolt split for 5TB category (splits the moment the bolt collection minicutscene triggers)
// - Tidied up if statements
