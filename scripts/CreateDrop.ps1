$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition
$SENPI_DIR = Join-Path $SCRIPT_DIR ".."
$DROP_DIR = Join-Path $SENPI_DIR "Sensei_app"

Push-Location $SENPI_DIR

New-Item -ItemType Directory -Path $DROP_DIR -Force
Copy-Item -Path "$SENPI_DIR\src" -Destination $DROP_DIR -Recurse -Force
Copy-Item -Path "$SENPI_DIR\version.json" -Destination $DROP_DIR -Force
Copy-Item -Path "$SENPI_DIR\requirements.txt" -Destination $DROP_DIR -Force
Copy-Item -Path "$SCRIPT_DIR\install_app.sh" -Destination $DROP_DIR -Force
Copy-Item -Path "$SENPI_DIR\tests" -Destination $DROP_DIR -Recurse -Force

Get-ChildItem -Path $DROP_DIR -Force
