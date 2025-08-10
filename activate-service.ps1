# activate-service.ps1
param($service)
if (Test-Path ".\$service\venv\Scripts\Activate.ps1") {
    & ".\$service\venv\Scripts\Activate.ps1"
    Write-Host "Ambiente virtual do $service ativado!" -ForegroundColor Green
} else {
    Write-Host "Serviço $service não encontrado!" -ForegroundColor Red
}