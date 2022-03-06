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
		settings.Add("LongLoadRemoval", false, "LongLoadRemoval - Toggle this to have the timer pause when the load time exceeds the optimal time (Layout settings -> Timer settings -> Timing method MUST be set to GameTime)");

		vars.loadStartTime = -1;
		vars.isLoading = false;
		vars.checkForLoadRemoval = false;

		vars.loadStartRealTime = -1;

		// Set to true if we have reached Dayni Moon 2, so that the long load removal doesn't hit Dayni Moon 1 by accident.
		vars.dayniMoon2 = false;

		// Set to true if we have reached Challax 2 in Wrench Only or Hundo, so that the long load removal doesn't hit Challax 1 by accident.
		vars.challax2 = false;

		// optimalLoadTime is measured in milliseconds.
		vars.optimalLoadTimeRyllus = 500;
		vars.optimalLoadTimeKalidon = 500;

		// Taken from https://raw.githubusercontent.com/tduva/LiveSplit-ASL/master/AlanWake.asl
		Action<string> LogDebug = (text) => {
			//print("[DEBUG] " + text);

			// DEBUGGING
			print(text);
		};
		vars.LogDebug = LogDebug;

		Action ResetLoadTimeVars = () => {
			vars.loadStartTime = -1;
			vars.isLoading = false;
			vars.checkForLoadRemoval = false;
			vars.dayniMoon2 = false;
			vars.challax2 = false;

			vars.loadStartRealTime = -1;
		};
		vars.ResetLoadTimeVars = ResetLoadTimeVars;

		// Takes the optimalLoadTime for this current load and the value (in memory) of the cutscene which plays at the end of the load.
		// This info is used to determine when to pause and resume the timer to remove the long load.
		Action<int, int> CheckLoadRemoval = (optimalLoadTime, cutsceneVal) => {
			TimeSpan gt = (TimeSpan) timer.CurrentTime.GameTime;
			if ((gt.TotalMilliseconds - vars.loadStartTime) > optimalLoadTime) {
				// Pause the timer to remove the long load.

				// DEBUGGING
				// vars.isLoading = true;
			}
			if (vars.currentCutscene.Current == cutsceneVal) {
				
				// Record the total time of the load
				TimeSpan rt = (TimeSpan) timer.CurrentTime.RealTime;
				vars.LogDebug("" + (rt.TotalMilliseconds - vars.loadStartRealTime));

				// Resume the timer once the load is done, and the cutscene is playing.
				vars.ResetLoadTimeVars();
			}
		};
		vars.CheckLoadRemoval = CheckLoadRemoval;

		Action LoadStarted = () => {
			// Record the time, as we have entered the load. This will be used for long load removal.
			TimeSpan gt = (TimeSpan) timer.CurrentTime.GameTime;
			vars.loadStartTime = gt.TotalMilliseconds;
			vars.checkForLoadRemoval = true;

			TimeSpan rt = (TimeSpan) timer.CurrentTime.RealTime;
			vars.loadStartRealTime = rt.TotalMilliseconds;
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
	
	vars.watchers = new MemoryWatcherList() {
		vars.currentPlanet,
		vars.pokiSpawn,
		vars.ottoEntry,
		vars.currentCutscene,
        vars.kalidonMoveState
	};
}

update {
	vars.watchers.UpdateAll(game);
}

split {
	// vars.LogDebug("Planet: " + vars.currentPlanet.Current);
	// vars.LogDebug("Cutscene " + vars.currentCutscene.Current);

	// DEBUGGING
	// ------------------------------------------------ //
	// Ryllus
	if (vars.currentPlanet.Current == 2 && vars.currentPlanet.Old == 1) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
	}
	// Kalidon
	// DEBUGGING
	if (vars.currentPlanet.Current == 3 && vars.currentPlanet.Old == 2) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
	}
	// Metalis
	if (vars.currentPlanet.Current == 4 && vars.currentPlanet.Old == 3) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
	}
	// Metalis Giant Clank
	if (vars.currentPlanet.Current == 15 && vars.currentPlanet.Old == 4) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
	}
	// Dreamtime
	if (vars.currentPlanet.Current == 5 && vars.currentPlanet.Old == 15) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
	}
	// MOO
	if (vars.currentPlanet.Current == 6 && vars.currentPlanet.Old == 5) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
	}
	if (settings["RemainsSplit"]) {
		if (vars.currentPlanet.Current == 23 && vars.currentPlanet.Old == 6) {
			if (settings["LongLoadRemoval"]) {
				vars.LoadStarted();
			}
		}
	}
	if (settings["ChallaxSplit"]) {
		if (vars.currentPlanet.Current == 7 && vars.currentPlanet.Old == 23) {
			if (settings["LongLoadRemoval"]) {
				vars.LoadStarted();
			}
		}
	}
	// Challax Giant Clank 2
	if (settings["GiantClank2Split"]) {
		if (vars.currentPlanet.Current == 21 && vars.currentPlanet.Old == 7) {
			if (settings["LongLoadRemoval"]) {
				vars.LoadStarted();
			}
		}
		// Split on Challax 2 (when you return from giant clank section back to Challax)
		if (vars.currentPlanet.Current == 7 && vars.currentPlanet.Old == 21) {
			if (settings["LongLoadRemoval"]) {
				vars.LoadStarted();
			}
			vars.challax2 = true;
		}
	}
	// Dayni Moon
	if (vars.currentPlanet.Current == 8 && vars.currentPlanet.Old == 7) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
	}
	if (settings["IClankSplit"]) {
		if (vars.currentPlanet.Current == 9 && vars.currentPlanet.Old == 8) {
			if (settings["LongLoadRemoval"]) {
				vars.LoadStarted();
			}
		}
	}
	// Dayni Moon 2
	if (vars.currentPlanet.Current == 8 && vars.currentPlanet.Old == 9) {
		if (settings["LongLoadRemoval"]) {
			vars.LoadStarted();
		}
		vars.dayniMoon2 = true;
	}

	if (settings["QuodronaSplit"]) {
		if (vars.currentPlanet.Current == 10 && vars.currentPlanet.Old == 8) {
			if (settings["LongLoadRemoval"]) {
				vars.LoadStarted();
			}
		}
	}
	// ------------------------------------------------ //



	// // Ryllus
	// if (vars.currentPlanet.Current == 2 && vars.currentPlanet.Old == 1) {
	// 	if (settings["LongLoadRemoval"]) {
	// 		vars.LoadStarted();
	// 	}
	// 	return true;
	// }
	// // Kalidon
	// if (vars.currentPlanet.Current == 3 && vars.currentPlanet.Old == 2) {
	// 	if (settings["LongLoadRemoval"]) {
	// 		vars.LoadStarted();
	// 	}
	// 	return true;
	// }
    // if (settings["Yeezy%Split"]) {
    //     if (vars.currentPlanet.Current == 3 && vars.kalidonMoveState.Current == 1097126595) {
    //         return true;
    //     }
	// }
	// if (settings["5TBSplit"]) {
    //     if (vars.currentPlanet.Current == 3 && vars.kalidonMoveState.Current == 1094363991) {
    //         return true;
    //     }
	// }
	// // Metalis
	// if (vars.currentPlanet.Current == 4 && vars.currentPlanet.Old == 3) {
	// 	if (settings["LongLoadRemoval"]) {
	// 		vars.LoadStarted();
	// 	}
	// 	return true;
	// }
	// // Metalis Giant Clank
	// if (vars.currentPlanet.Current == 15 && vars.currentPlanet.Old == 4) {
	// 	if (settings["LongLoadRemoval"]) {
	// 		vars.LoadStarted();
	// 	}
	// 	return true;
	// }
	// // Dreamtime
	// if (vars.currentPlanet.Current == 5 && vars.currentPlanet.Old == 15) {
	// 	if (settings["LongLoadRemoval"]) {
	// 		vars.LoadStarted();
	// 	}
	// 	return true;
	// }
	// // MOO
	// if (vars.currentPlanet.Current == 6 && vars.currentPlanet.Old == 5) {
	// 	if (settings["LongLoadRemoval"]) {
	// 		vars.LoadStarted();
	// 	}
	// 	return true;
	// }
	// if (settings["RemainsSplit"]) {
	// 	if (vars.currentPlanet.Current == 23 && vars.currentPlanet.Old == 6) {
	// 		if (settings["LongLoadRemoval"]) {
	// 			vars.LoadStarted();
	// 		}
	// 		return true;
	// 	}
	// }
	// if (settings["ChallaxSplit"]) {
	// 	if (vars.currentPlanet.Current == 7 && vars.currentPlanet.Old == 23) {
	// 		if (settings["LongLoadRemoval"]) {
	// 			vars.LoadStarted();
	// 		}
	// 		return true;
	// 	}
	// }
	// // Challax Giant Clank 2
	// if (settings["GiantClank2Split"]) {
	// 	if (vars.currentPlanet.Current == 21 && vars.currentPlanet.Old == 7) {
	// 		if (settings["LongLoadRemoval"]) {
	// 			vars.LoadStarted();
	// 		}
	// 		return true;
	// 	}
	// 	// Split on Challax 2 (when you return from giant clank section back to Challax)
	// 	if (vars.currentPlanet.Current == 7 && vars.currentPlanet.Old == 21) {
	// 		if (settings["LongLoadRemoval"]) {
	// 			vars.LoadStarted();
	// 		}
	// 		vars.challax2 = true;
	// 		return true;
	// 	}
	// }
	// // Dayni Moon
	// if (vars.currentPlanet.Current == 8 && vars.currentPlanet.Old == 7) {
	// 	if (settings["LongLoadRemoval"]) {
	// 		vars.LoadStarted();
	// 	}
	// 	return true;
	// }
	// if (settings["IClankSplit"]) {
	// 	if (vars.currentPlanet.Current == 9 && vars.currentPlanet.Old == 8) {
	// 		if (settings["LongLoadRemoval"]) {
	// 			vars.LoadStarted();
	// 		}
	// 		return true;
	// 	}
	// }
	// // Dayni Moon 2
	// if (vars.currentPlanet.Current == 8 && vars.currentPlanet.Old == 9) {
	// 	if (settings["LongLoadRemoval"]) {
	// 		vars.LoadStarted();
	// 	}
	// 	vars.dayniMoon2 = true;
	// 	return true;
	// }

	// if (settings["QuodronaSplit"]) {
	// 	if (vars.currentPlanet.Current == 10 && vars.currentPlanet.Old == 8) {
	// 		if (settings["LongLoadRemoval"]) {
	// 			vars.LoadStarted();
	// 		}
	// 		return true;
	// 	}
	// }
	// if (settings["SplitOtto"]) {
	// 	if (vars.currentPlanet.Current == 10) {
	// 		if (vars.ottoEntry.Current == 75000 && vars.ottoEntry.Old <= 0) {
	// 			return true;
	// 		}
	// 	}
	// }
	// // Split on end of run
	// if (vars.currentPlanet.Current == 10 && vars.currentCutscene.Current == 776417329) {
	// 	return true;
	// }
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

	// DEBUGGING
	// return vars.isLoading;
}

// ------------------------------------------------ //
// Edits
// ------------------------------------------------ //
//
// scoom_scoom -> 30/12/2021
// - Added Yeezy% split on wildfire boots collection (the start of the minicutscene)
// - Added 5th titanium bolt split for 5TB category (splits the moment the bolt collection minicutscene triggers)
// - Tidied up if statements
//
// scoom_scoom -> ???
// - Added long load removal.