# Cycle ID: [Start date, End date]
cycles = {25: ["2019 12 01", "2023 04 21"],
          24: ["2008 12 01", "2019 11 30"],
          23: ["1996 08 01", "2008 11 30"],
          22: ["1986 09 01", "1996 07 31"],
          21: ["1976 03 01", "1986 08 31"],
          20: ["1964 10 01", "1976 02 29"],
          19: ["1954 04 01", "1964 09 30"],
          18: ["1944 02 01", "1954 03 31"],
          17: ["1933 09 01", "1944 01 31"]}

for cycleId in reversed(range(17, 26)):
    startDate = cycles[cycleId][0]
    endDate = cycles[cycleId][1]
    print("Cycle", cycleId)
    print("  Start:", startDate, "End:", endDate)
    
    extractedLines = []
    extracting = False

    with open("Kp_ap_Ap_SN_F107_since_1932.txt") as inputFile:
        for index, line in enumerate(inputFile):
            if line.startswith("#YYY"):
                extractedLines.append(line)
            if line.startswith(startDate):
                extracting = True
            if extracting:
                extractedLines.append(line)
            if line.startswith(endDate):
                break

    extractedLineCount = len(extractedLines)
    years = (extractedLineCount-1) // 365
    days = (extractedLineCount-1) % 365
    print("  Extracted", extractedLineCount-1, "lines:", years, "years", days, "days")
    
    fileName = "cycle" + str(cycleId) + ".txt"
    with open(fileName, "w") as outputFile:
        outputFile.writelines(extractedLines)
