test_window = None
record = 0
ILval = 0.0
lumMeter = None
LUTmode = 18  # 0 means demo mode
ILstatus = 0
ILcnt = 0
ILdataReady = 0

ILfilt = 0
phase = {}

start = 0

meter = "i1DisplayPro"
greyR_offset = 0

CHRuAvg = 0.0
CHRvAvg = 0.0

avgN = 3

meterStatus = 0
srMode = "lum"  # or "lux"
srout = ""
srid = None
binpath = "./"
i1yval = "n"
iOneDone = False


ILautoNum = 0
greyR = 0
LUTphase = 0
ILavg = 0.0
lastILavg = 0.0
lastRGB = "#808080"

greyR_display = ""
LUTphase_display = ""
error = 0
outlierTotal = 0
outlierNum = 3
outlierTestCount = 0
outlierResolve = 0
outlierAccept = 0

absChange = 0.0
relChange = 0.0
ILlimit_plus = 0.05
ILlimit_minus = -0.05
ILlimit_abs = 0.02
pause_flag = 0
log = None
ILtolerance = 0.5

ioneu = 0.0
ionev = 0.0