@echo off
python main.py -h
:loop
set /p UserInput=Enter your command (or type "exit" to quit): 
if "%UserInput%"=="exit" goto :eof
if "%UserInput%"=="run main.py" (
    python main.py
) else (
    %UserInput%
)
goto loop