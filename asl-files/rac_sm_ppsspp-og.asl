state("PPSSPPWindows64") { } 

startup {
		vars.scanTarget = new SigScanTarget (0, "48 45 52 4F 53 4B 49 4E 5F 49 6E 69 74 53 69 6E 67 6C 65 50 6C 61 79 65 72");
		
		settings.Add("RemainsSplit", true, "Split on Remains");
		settings.Add("SplitOtto", true, "Split on Otto entry");
		settings.Add("ChallaxSplit", true, "Split on Challax");
		settings.Add("IClankSplit", true, "Split after Inside Clank");
		settings.Add("QuodronaSplit", true, "Split on Quodrona");
		settings.Add("AutoReset", true, "Toggle this to auto-reset (NG+)");
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
	
	vars.watchers = new MemoryWatcherList() {
		vars.currentPlanet,
		vars.pokiSpawn,
		vars.ottoEntry,
		vars.currentCutscene
	};
}

update {
	vars.watchers.UpdateAll(game);
}

split {
	if (vars.currentPlanet.Current == 2 && vars.currentPlanet.Current != vars.currentPlanet.Old) {
		return true;
	}
	if (vars.currentPlanet.Current == 3 && vars.currentPlanet.Current != vars.currentPlanet.Old) {
		return true;
	}
	if (vars.currentPlanet.Current == 4 && vars.currentPlanet.Current != vars.currentPlanet.Old) {
		return true;
	}
	if (vars.currentPlanet.Current == 5 && vars.currentPlanet.Old == 15) {
		return true;
	}
	if (vars.currentPlanet.Current == 6 && vars.currentPlanet.Old == 5) {
		return true;
	}
	if (settings["ChallaxSplit"]) {
		if (vars.currentPlanet.Current == 7 && vars.currentPlanet.Current != vars.currentPlanet.Old) {
			return true;
		}
	}
	if (vars.currentPlanet.Current == 8 && vars.currentPlanet.Old == 7) {
		return true;
	}
	if (vars.currentPlanet.Current == 9 && vars.currentPlanet.Old == 8) {
		return true;
	}
	if (settings["IClankSplit"]) {
		if (vars.currentPlanet.Current == 8 && vars.currentPlanet.Old == 9) {
			return true;
		}
	}
	if (settings["QuodronaSplit"]) {
		
		if (vars.currentPlanet.Current == 10 && vars.currentPlanet.Current != vars.currentPlanet.Old) {
			return true;
		}
	}
	if (settings["RemainsSplit"]) {
		if (vars.currentPlanet.Current == 23 && vars.currentPlanet.Current != vars.currentPlanet.Old) {
			return true;
		}
	}
	if (vars.currentPlanet.Current == 15 && vars.currentPlanet.Old == 4) {
		return true;
	}
	if (vars.currentPlanet.Current == 21 && vars.currentPlanet.Old == 7) {
		return true;
	}
	if (settings["SplitOtto"]) {
		if (vars.currentPlanet.Current == 10) {
			if (vars.ottoEntry.Current == 5000 && vars.ottoEntry.Old <= 0) {
				return true;
			}
		}
	}
	if (vars.currentCutscene.Current == 776417329 && vars.currentCutscene.Current != vars.currentCutscene.Old) {
		return true;
	}
}
	

start {
	if (vars.currentPlanet.Current ==  1)
	{
		return vars.pokiSpawn.Current == 1 && vars.pokiSpawn.Old == 0;
	}
}

reset {
	if (settings["AutoReset"]) {
		if (vars.currentPlanet.Current ==  1)
	{
		return vars.pokiSpawn.Current == 1 && vars.pokiSpawn.Old == 0;
		}
	}
	
}
