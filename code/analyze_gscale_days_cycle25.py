import pandas as pd

def getStormDays():
    columnNames=["CycleId","G5","G4","G3","G2","G1", "Gdays"]
    df = pd.read_csv("gscale-days-per-cycle.csv",
                     names=columnNames, skiprows=1)
    print(df)
    print("")

    g5 = round(df.loc[0, "G5"])
    aveG5OverCycles = df.loc[9, "G5"]
    aveG5OverPast3Cycles = df.loc[10, "G5"]
    g5Cycle24 = df.loc[1, "G5"]

    g5percentOverCycles = round(g5/aveG5OverCycles * 100)
    g5percentOverPast3Cycles = round(g5/aveG5OverPast3Cycles * 100)
    if g5Cycle24 == 0:
        g5Cycle24 = 1
    g5percentOverCycle24 = round(g5/g5Cycle24 * 100)

    #print(aveG5OverCycles, aveG5OverPast3Cycles)
    print("G5 Days: ", g5)
    print("  ",
          g5percentOverCycles, "% (v.s. cycles 17-24)",
          g5percentOverPast3Cycles, "% (v.s. cycles 22-24)",
          g5percentOverCycle24, "% (v.s. cycle 24)")

    g4 = round(df.loc[0, "G4"])
    aveG4OverCycles = df.loc[9, "G4"]
    aveG4OverPast3Cycles = df.loc[10, "G4"]
    g4Cycle24 = df.loc[1, "G4"]

    g4percentOverCycles = round(g4/aveG4OverCycles * 100)
    g4percentOverPast3Cycles = round(g4/aveG4OverPast3Cycles * 100)
    if g4Cycle24 == 0:
        g4Cycle24 = 1
    g4percentOverCycle24 = round(g4/g4Cycle24 * 100)

    #print(aveG4OverCycles, aveG4OverPast3Cycles)
    print("G4 Days: ", g4)
    print("  ",
          g4percentOverCycles, "% (v.s. cycles 17-24)",
          g4percentOverPast3Cycles, "% (v.s. cycles 22-24)",
          g4percentOverCycle24, "% (v.s. cycle 24)")

    g3 = round(df.loc[0, "G3"])
    aveG3OverCycles = df.loc[9, "G3"]
    aveG3OverPast3Cycles = df.loc[10, "G3"]
    g3Cycle24 = df.loc[1, "G3"]

    g3percentOverCycles = round(g3/aveG3OverCycles * 100)
    g3percentOverPast3Cycles = round(g3/aveG3OverPast3Cycles * 100)
    if g3Cycle24 == 0:
        g3Cycle24 = 1
    g3percentOverCycle24 = round(g3/g3Cycle24 * 100)

    #print(aveG3OverCycles, aveG3OverPast3Cycles)
    print("G3 Days: ", g3)
    print("  ",
          g3percentOverCycles, "% (v.s. cycles 17-24)",
          g3percentOverPast3Cycles, "% (v.s. cycles 22-24)",
          g3percentOverCycle24, "% (v.s. cycle 24)")

    g2 = round(df.loc[0, "G2"])
    aveG2OverCycles = df.loc[9, "G2"]
    aveG2OverPast3Cycles = df.loc[10, "G2"]
    g2Cycle24 = df.loc[1, "G2"]

    g2percentOverCycles = round(g2/aveG2OverCycles * 100)
    g2percentOverPast3Cycles = round(g2/aveG2OverPast3Cycles * 100)
    if g2Cycle24 == 0:
        g2Cycle24 = 1
    g2percentOverCycle24 = round(g2/g2Cycle24 * 100)

    #print(aveG2OverCycles, aveG2OverPast3Cycles)
    print("G2 Days: ", g2)
    print("  ",
          g2percentOverCycles, "% (v.s. cycles 17-24)",
          g2percentOverPast3Cycles, "% (v.s. cycles 22-24)",
          g2percentOverCycle24, "% (v.s. cycle 24)")

    g1 = round(df.loc[0, "G1"])
    aveG1OverCycles = df.loc[9, "G1"]
    aveG1OverPast3Cycles = df.loc[10, "G1"]
    g1Cycle24 = df.loc[1, "G1"]

    g1percentOverCycles = round(g1/aveG1OverCycles * 100)
    g1percentOverPast3Cycles = round(g1/aveG1OverPast3Cycles * 100)
    if g1Cycle24 == 0:
        g1Cycle24 = 1
    g1percentOverCycle24 = round(g1/g1Cycle24 * 100)

    #print(aveG1OverCycles, aveG1OverPast3Cycles)
    print("G1 Days: ", g1)
    print("  ",
          g1percentOverCycles, "% (v.s. cycles 17-24)",
          g1percentOverPast3Cycles, "% (v.s. cycles 22-24)",
          g1percentOverCycle24, "% (v.s. cycle 24)")

    gd = round(df.loc[0, "Gdays"])
    aveGdOverCycles = df.loc[9, "Gdays"]
    aveGdOverPast3Cycles = df.loc[10, "Gdays"]
    gdCycle24 = df.loc[1, "Gdays"]

    gdpercentOverCycles = round(gd/aveGdOverCycles * 100)
    gdpercentOverPast3Cycles = round(gd/aveGdOverPast3Cycles * 100)
    if gdCycle24 == 0:
        gdCycle24 = 1
    gdpercentOverCycle24 = round(gd/gdCycle24 * 100)

    #print(aveGdOverCycles, aveGdOverPast3Cycles)
    print("G Days: ", gd)
    print("  ",
          gdpercentOverCycles, "% (v.s. cycles 17-24)",
          gdpercentOverPast3Cycles, "% (v.s. cycles 22-24)",
          gdpercentOverCycle24, "% (v.s. cycle 24)")
    
    return {5: [g5,aveG5OverCycles],
            4: [g4,aveG4OverCycles],
            3: [g3,aveG3OverCycles],
            2: [g2,aveG2OverCycles],
            1: [g1,aveG1OverCycles] }
    

