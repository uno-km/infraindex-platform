Stop-Process -Name 'python' -Force -ErrorAction SilentlyContinue; Stop-Process -Name 'node' -Force -ErrorAction SilentlyContinue; Write-Host 'System processes have been terminated for reboot.'
