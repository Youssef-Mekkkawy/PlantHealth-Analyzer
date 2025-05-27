@echo off
REM ---- suppress TF logs ----
set TF_ENABLE_ONEDNN_OPTS=0
set TF_CPP_MIN_LOG_LEVEL=2

REM ---- call the actual exe with its arg ----
"%~dp0\cli.exe" %1
