import pandas as pd

def getProgressInCycle():
    columnNames = ["YYY", "MM", "DD", "days", "days_m", "Bsr", "dB", "Kp1", "Kp2", "Kp3",
                   "Kp4", "Kp5", "Kp6", "Kp7", "Kp8", "ap1", "ap2", "ap3", "ap4", "ap5",
                   "ap6", "ap7", "ap8", "Ap", "SN", "F10.7obs", "F10.7adj", "D"]
    cyclesLength = []

    for cycleId in reversed(range(17, 26)):
        fileName = "cycle" + str(cycleId) + ".txt"
        df = pd.read_csv(fileName,
                         delim_whitespace=True, names=columnNames, skiprows=1)
        days = len(df)
    #     print("Cycle", cycleId, days, "days")
        cyclesLength.append([cycleId, days])

    columnNames=["CycleId","Length"]
    outputDf = pd.DataFrame(cyclesLength,
                            columns=columnNames)
    outputDf.to_csv("cycle-length.csv", index=False)

    aveLength = outputDf.loc[1:, "Length"].mean()
    aveLengthRow = []
    aveLengthRow.append("Ave17-24")
    aveLengthRow.append(aveLength)
    extraDf = pd.DataFrame([aveLengthRow],
                           columns=columnNames)
    newDf = pd.concat([outputDf, extraDf],
                      axis=0, ignore_index=True)

    aveLength3Cycles = outputDf.loc[1:3, "Length"].mean()
    aveLength3CyclesRow = []
    aveLength3CyclesRow.append("Ave22-24")
    aveLength3CyclesRow.append(aveLength3Cycles)
    extraDf = pd.DataFrame([aveLength3CyclesRow],
                           columns=columnNames)
    newDf = pd.concat([newDf, extraDf],
                      axis=0, ignore_index=True)
    print(newDf)

    cycle25length = newDf.loc[0, "Length"]
    progress = round(cycle25length/aveLength * 100)
    print(progress , "% of average cycle length (cycles 17-24)" )
    # print( round(cycle25length/aveLength3Cycles * 100), "% of average cycle length (cycles 22-24)" )

    newDf.to_csv("cycle-length.csv", index=False)

    return progress
