:: This script creates a virtual environment, installs dependencies, and
:: allows the user to choose between global and virtual python environment for running the program
:: @author KOOKIIE
:: Turn ECHO off
@echo off
if not exist venv\ (
    echo No venv folder found
    echo Setting up virtual environment...
    :: Generate VENV in project dir
    python -m venv %~dp0venv

    echo Installing dependencies...
    :: Activate the VENV
    call venv\scripts\activate.bat
    :: Install requirements
    pip install wheel
    pip install -r requirements.txt
)

setlocal
echo This script will now launch the program.
echo Please select the environment to run the source code with:
echo A: Virtual Python Environment (Default)
echo B: Global Python Environment
choice /c AB /t 10 /d A /m "What is your choice"
if errorlevel 2 call :global
if errorlevel 1 call :virtual
pause
endlocal

:: function to run from venv
:virtual
echo You have selected A: Virtual Python Environment
call venv\scripts\activate.bat
venv\scripts\python main.py
:: uncomment to auto-restart:
:: echo "The program crashed, restarting..."
:: goto virtual
exit \b

:: function to run from global environment
:global
echo You have selected B: Global Python Environment
python main.py
:: uncomment to auto-restart:
:: echo "The program crashed, restarting..."
:: goto global
exit \b