@echo off
SET "PYTHON_PATH=D:\software\python3.6.6\python.exe"

REM Check for Python installation
%PYTHON_PATH% --version
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed at %PYTHON_PATH%. Please check the path and try again.
    exit /b 1
)

REM Check for pip installation
%PYTHON_PATH% -m pip --version
IF %ERRORLEVEL% NEQ 0 (
    echo pip is not installed. Installing pip...
    %PYTHON_PATH% -m ensurepip
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to install pip. Please install pip manually and try again.
        exit /b 1
    )
)

REM List of packages to install
SET "packages=requests bs4 urllib3 xlrd openpyxl prettytable pandas matplotlib tushare numpy cx_Oracle chardet"

REM Initialize the list of packages to install
SET "packages_to_install="

REM Check which packages need to be installed
FOR %%p IN (%packages%) DO (
    %PYTHON_PATH% -m pip show %%p >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        SET "packages_to_install=!packages_to_install! %%p"
    )
)

IF "%packages_to_install%"=="" (
    echo All packages are already installed.
    exit /b 0
)

echo The following packages will be installed: %packages_to_install%
echo Press Enter to continue...
pause >nul

REM Count the total number of packages to install
SET /A total_packages=0
FOR %%p IN (%packages_to_install%) DO (
    SET /A total_packages+=1
)

REM Initialize progress
SET /A current_package=0

REM Install each package with progress
FOR %%p IN (%packages_to_install%) DO (
    SET /A current_package+=1
    CALL :show_progress %current_package% %total_packages%
    echo Installing %%p...
    %PYTHON_PATH% -m pip install %%p
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to install %%p. Please check the package name and try again.
        exit /b 1
    )
)

echo All packages installed successfully.
exit /b 0

:show_progress
SET /A progress=100 * %1 / %2
powershell -Command "Write-Progress -Activity 'Installing Packages' -Status 'Installing package %1 of %2' -PercentComplete %progress%"
GOTO :EOF

pause