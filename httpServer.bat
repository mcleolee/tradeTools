pushd C:\Users\progene12\share\
@echo off
echo http://127.0.0.1:8000 | clip
echo  --- Server address copied to clipboard. ---
python -m http.server
:: ravin20240312
