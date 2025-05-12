; pacsDisplay Installer using Inno Setup with Wizard Tasks + License Agreement
; ------------------------------------------------------
[Setup]
AppName=pacsDisplay
AppVersion=2.3
DefaultDirName={pf}\HFHS\pacsDisplay
DefaultGroupName=HFHS pacsDisplay
UninstallDisplayIcon={app}\pacsDisplay-BIN\main.exe
Compression=lzma
SolidCompression=yes
OutputBaseFilename=pacsDisplayInstaller
WizardSmallImageFile=logo.bmp
LicenseFile=license.txt

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "overwrite_install"; Description: "Overwrite existing installation"; GroupDescription: "Install Options:"; Flags: checkedonce
Name: "overwrite_luts"; Description: "Overwrite existing LUTs"; GroupDescription: "Install Options:"; Flags: checkedonce
Name: "install_tools"; Description: "Install grayscale calibration toolset"; GroupDescription: "Install Options:"; Flags: checkedonce
Name: "run_config"; Description: "Run LLconfig after installation"; GroupDescription: "Install Options:"; Flags: unchecked

[Files]
Source: "pacsDisplay-BIN\*"; DestDir: "{app}\pacsDisplay-BIN"; Flags: recursesubdirs
Source: "pacsDisplay-BIN\_ICONS\*"; DestDir: "{app}\pacsDisplay-BIN\_ICONS"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "LUTs\*"; DestDir: "{code:GetLUTsDir}"; Flags: recursesubdirs; Tasks: overwrite_luts
Source: "GNU-GPL.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "VERSION_INFO.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "QUICKSTART.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "pd-Manual.pdf"; DestDir: "{app}\pacsDisplay-BIN\_pd-Manual"; Flags: ignoreversion
Source: "Links\64b_W7\shortcuts\allUsers_startMenu_programs_startup\loadLUT-dicom.lnk"; DestDir: "{commonstartup}"; Flags: ignoreversion
Source: "license.txt"; DestDir: "{tmp}"; Flags: dontcopy
Source: "logo.bmp"; DestDir: "{tmp}"; Flags: dontcopy

[Icons]
Name: "{group}\gtest"; Filename: "{app}\pacsDisplay-BIN\gtest\gtest.exe"; IconFilename: "{app}\pacsDisplay-BIN\_ICONS\gtest.ico"
Name: "{group}\EDIDprofile"; Filename: "{app}\pacsDisplay-BIN\EDIDprofile\EDIDprofile.exe"; IconFilename: "{app}\pacsDisplay-BIN\_ICONS\EDIDprofile.ico"
Name: "{group}\iQC"; Filename: "{app}\pacsDisplay-BIN\iQC\iQC.exe"; IconFilename: "{app}\pacsDisplay-BIN\_ICONS\iQC.ico"
Name: "{group}\ChangeLUT"; Filename: "{app}\pacsDisplay-BIN\loadLUT\ChangeLUT.exe"; IconFilename: "{app}\pacsDisplay-BIN\_ICONS\loadLUT.ico"
Name: "{group}\i1meter"; Filename: "{app}\pacsDisplay-BIN\lumResponse\i1meter.exe"; IconFilename: "{app}\pacsDisplay-BIN\_ICONS\i1meter.ico"
Name: "{group}\lumResponse"; Filename: "{app}\pacsDisplay-BIN\lumResponse\lumResponse.exe"; IconFilename: "{app}\pacsDisplay-BIN\_ICONS\Lum-Resp.ico"
Name: "{group}\LutGenerate"; Filename: "{app}\pacsDisplay-BIN\lutGenerate\LutGenerate.exe"; IconFilename: "{app}\pacsDisplay-BIN\_ICONS\LUT-Gen.ico"
Name: "{group}\QC-check"; Filename: "{app}\pacsDisplay-BIN\lumResponse\QC-check.exe"; IconFilename: "{app}\pacsDisplay-BIN\_ICONS\QC-check.ico"
Name: "{group}\uLRstats"; Filename: "{app}\pacsDisplay-BIN\uLRstats\uLRstats.exe"; IconFilename: "{app}\pacsDisplay-BIN\_ICONS\uLR-stats.ico"
Name: "{group}\w_pd-manual"; Filename: "{app}\pacsDisplay-BIN\_pd-Manual\pd-Manual.pdf"; IconFilename: "{app}\pacsDisplay-BIN\_ICONS\pdPDF.ico"
Name: "{group}\Uninstall pacsDisplay"; Filename: "{uninstallexe}"; IconFilename: "{app}\pacsDisplay-BIN\_ICONS\uninstall.ico"

[Run]
Filename: "{app}\pacsDisplay-BIN\LLconfig\LLconfig.exe"; Description: "Run LLconfig"; Flags: postinstall nowait skipifsilent; Tasks: run_config

[Code]
function GetLUTsDir(Value: string): string;
begin
  Result := ExpandConstant('{commonappdata}\HFHS\pacsDisplay\LUTs');
end;

function GetShortcutsDir(Value: string): string;
begin
  Result := ExpandConstant('{commonstartmenu}\HFHS ePACS Grayscale');
end;
