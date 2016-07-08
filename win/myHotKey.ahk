#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

;; disable Win key behavior of popping up the Start Menu, but don't disable Win+‹key› combination
~LWin Up::Return
~RWin Up::Return


;;Start applications
F5::Run, explorer.exe e/`,
F4::Run, C:\Windows\System32\cmd.exe /A /Q /K C:\msys64\msys2_shell.bat
F1::Run, E:\software\Wox-v1.2.0-beta.2\Wox.exe

;;Window management
#c::WinClose, A
#q::WinMinimize, A
LWin & Tab::AltTab

;;Move windows by keyboard
MoveLeft(d)
{
	WinGetPos, X, Y, Width, Height, A
	WinMove, A, , (X-d), Y
}
MoveRight(d)
{
	WinGetPos, X, Y, Width, Height, A
	WinMove, A, , (X+d), Y
}
MoveUp(d)
{
	WinGetPos, X, Y, Width, Height, A
	WinMove, A, , X, (Y-d)
}
MoveDown(d)
{
	WinGetPos, X, Y, Width, Height, A
	WinMove, A, , X, (Y+d)
}
#Left::MoveLeft(20)
#Right::MoveRight(20)
#Up::MoveUp(20)
#Down::MoveDown(20)

ToggleWinMax()
{
	WinGetPos, winWidth, winHeight, , , A  ; "A" to get the active window's pos.
	if ((winWidth == -8 and winHeight == -8) or (winHeight==-320)) {
    		;;MsgBox %winWidth% %winHeight%
    		WinRestore, A
	} else{
    		;;MsgBox %winWidth% %winHeight%
    		WinMaximize, A
	}
}
#m::ToggleWinMax()

#1::Run, E:\Program Files (x86)\VirtuaWin\Virtuawin.exe -msg 1034 1
#2::Run, E:\Program Files (x86)\VirtuaWin\Virtuawin.exe -msg 1034 2
#3::Run, E:\Program Files (x86)\VirtuaWin\Virtuawin.exe -msg 1034 3