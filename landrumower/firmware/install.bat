@echo off
echo Landrumower Robot Vezérlő telepítése...
echo.

REM Python telepítés ellenőrzése
python --version >nul 2>&1
if errorlevel 1 (
    echo Python nincs telepítve!
    echo Kérlek telepítsd a Python-t a https://www.python.org/downloads/ oldalról
    echo Fontos: A telepítés során jelöld be az "Add Python to PATH" opciót!
    pause
    exit
)

REM Szükséges csomagok telepítése
echo Szükséges csomagok telepítése...
pip install pyserial

echo.
echo Telepítés kész!
echo Most létrehozom az indító fájlt...
echo.

REM Indító fájl létrehozása
echo @echo off > start_robot.bat
echo python robot_control.py >> start_robot.bat
echo pause >> start_robot.bat

echo Indító fájl létrehozva: start_robot.bat
echo.
echo A program indításához dupla kattintással nyisd meg a start_robot.bat fájlt!
pause 