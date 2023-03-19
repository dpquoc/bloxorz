@echo off
:loop
set /p UserInput=Enter your command (or type "exit" to quit): 
if "%UserInput%"=="exit" goto :eof
%UserInput%
goto loop