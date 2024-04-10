@echo off
setlocal enabledelayedexpansion

set "directory=path\to\your\directory"

for %%F in (".\*") do (
    set "filename=%%~nxF"
    if "!filename:PA=!" neq "!filename!" (
        set "new_filename=!filename:PA=PAHF!"
        ren "%%F" "!new_filename!"
    )
)

echo Files renamed successfully.
