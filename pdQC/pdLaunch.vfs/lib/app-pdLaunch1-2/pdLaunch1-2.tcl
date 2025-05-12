package provide app-pdLaunch1-2 1.0

# ---------------------------------------------------------------------------
#                    pcLaunch                                              #
#  Written by:                                                             #
#    Michael J. Flynn (mikef@rad.hfh.edu)                                  #
#                                                                          #
#  Utility program to launch pacsDisplay programs in the pdQC folder.      #
#  Windows does not provide a way to put shortcuts in the folder with a    #
#  relative path. This appication is to be used instead.                   #
#  The application provides a simple way to select and run applications    #
#  that are in the pacsDisplay-BIN folder similar to the full package.     #
#  Programs involved with loading LUTs are not included.                   #
#                                                                          #
#  The pdLaunch.exe application (wrapped with TclApp) must be in the pdQC  #
#  folder with the pacsDisplay-BIN and _NEW subfolders.                    #
#  The working directory moves to pacsDisplay-BIN, then moves in and out   #
#  of the various program folders to that the appications are launched     #
#  within their own folder where the program configuration files are       #
#  sources and the _NEW folder is found by going up two direcoties.        #
#
#	v1-1 N Bevins May 2021
#		- Update with ambtest
#		- Convert to png icons
#	v1-2 N Bevins May 2021
#		- Update with ambtest
#		- Convert to png icons
#                                                                          #
# ---------------------------------------------------------------------------
#
#console show

# ---------------------------------------------------------------------------
#for testing, change to the pdQC directory
#
#cd [file join U:/ pddev pacsDisplay HFHS-pacsDisplay-5E pdQC]
#
# --- Otherwise ---
#pdLaunch is intended to be run from within the pdQC directory
# ---------------------------------------------------------------------------

#**********************************************************************
# Test that pdLaunch is in the correct directory for relative paths.

if {[file isdirectory pacsDisplay-BIN] != 1} {
	tk_messageBox -type "ok" \
		-icon "error"          \
		-title "ERROR" \
		-message "ERROR: pacsDisplay-BIN not found"
	exit
}
if {[file isdirectory _NEW] != 1} {
	tk_messageBox -type "ok" \
		-icon "error"          \
		-title "ERROR" \
		-message "ERROR: _NEW not found"
	exit
}


set title "pdLaunch"
set copydate "May 2021"
# first tell the user what version he is using
#
puts "$title" 
#puts "Copyright:       Xray Imaging Research Laboratory"
#puts "                         Henry Ford Health System"
#puts "                         Detroit, MI"
#puts "                                         $copydate"
#
#**********************************************************************
# get home directory to support wrapping with tclApp

set wrapHome [file dirname [info script]]
source [file join $wrapHome xirlDefs-v06.tsp]

# package require img::bmp

wm title .  $title
wm resizable . 0 0

set numApps 10

# Set direcory within pacsDisplay-BIN for each app
set appDir(1) EDIDprofile
set appDir(2) gtest
set appDir(3) iQC
set appDir(4) ambtest
set appDir(5) lumResponse   ;# note that i1meter is in lumResponse
set appDir(6) lumResponse
set appDir(7) uniLum
set appDir(8) lutGenerate
set appDir(9) lumResponse   ;# note that QC-check is in lumResponse
set appDir(10) uLRstats

# Set each app name. Used for button and exe file name
set appName(1) EDIDprofile
set appName(2) gtest
set appName(3) iQC
set appName(4) ambtest
set appName(5) i1meter
set appName(6) lumResponse
set appName(7) uniLum
set appName(8) lutGenerate
set appName(9) QC-check
set appName(10) uLRstats

for {set i 1} {$i <= $numApps} {incr i} {
	image create photo icon$appName($i) -format png -file [file join $wrapHome pngIcons $appName($i).png]
}

#**********************************************************************
# Now move to the BIN directory

cd pacsDisplay-BIN

#**********************************************************************
# Build the Window GUI
#
#------------------------
#... title and copyright message
set bgClr #204080  ;# 'blueprint' blue
set fgClr #f0f0f0  ;# near white
set title "\n$title\n\n"
append title "Copyright $copydate\n"
append title "Radiology Research\n"
append title "Henry Ford Health System"

frame .title  -height 120 -width 250 -relief sunken -bg $bgClr \
	      -highlightthickness 2 -highlightbackground $fgClr
label .title.text  -text $title -bg $bgClr -fg $fgClr -padx 1 -pady 1
pack .title.text -in .title -anchor center
pack .title -side top -fill x

#------------------------
# Application launch buttons
#
for {set i 1} {$i <= $numApps} {incr i} {

	frame .launch_$i   -relief raised -borderwidth 2

	button .launch_$i.app \
		-image icon$appName($i) \
		-compound left \
		-anchor w \
		-height [expr [image height icon$appName($i)] * 1.0] \
		-width  200 \
		-text "  $appName($i)" \
		-command "launchApp $i"
    ;# NOTE tk_focusFollowsMouse turned on in xirldefs-v06.tsp, this app only

	pack .launch_$i.app -padx 1m -pady 0m -side left -fill x

	pack .title .launch_$i -side top -fill x
}

#    ------------------------
#    ...QUIT command

	frame .cmdBar -relief raised -borderwidth 2

	button .cmdBar.quit -text "QUIT" \
				-command {destroy .; exit}

	pack .cmdBar.quit -side right -padx 1m -pady 1m -fill x

	pack .cmdBar -side top -fill x

#**********************************************************************
# procedure to launch apps

proc launchApp {i} {

	global appDir appName appPID

	cd $appDir($i)

	if {[catch {exec $appName($i).exe &} output]} {
		;# $output contains the same information as written to log.
		tk_messageBox -type "ok" \
		              -icon "error"          \
		              -title "ERROR" \
		              -message "ERROR executing app $i:\n$output"
		return
	} else {
		set appPID($i) $output
	}
	cd ..
}
