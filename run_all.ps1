# --- RUN THIS ON WINDOWS ---
Start-Transcript -Path "runner.log" -Append

function Invoke-TimedStep {
    param([string]$StepName, [scriptblock]$Action)
    Write-Host "`n>>> [STARTED]: $StepName" -ForegroundColor Cyan
    $start = Get-Date
    Invoke-Command -ScriptBlock $Action
    $end = Get-Date
    $duration = $end - $start
    Write-Host ">>> [ENDED]: $StepName | Time Taken: $($duration.TotalSeconds) seconds" -ForegroundColor Green
}

# --- LAYER 1: LOCAL WINDOWS PROCESSING ---
Invoke-TimedStep "Local Python Execution" {
    # Small Data
    Set-Content -Path ".env" -Value "DATA_FILE=small_dataset.csv"
    python generate_data.py; python generate_small_data.py; python secure_processor.py
    Move-Item -Path "secured_small_dataset.csv" -Destination "secured_small_data_local.csv" -Force
    Move-Item -Path "small_dataset_processor.log" -Destination "local_small_processor.log" -Force
    
    # Large Data
    Set-Content -Path ".env" -Value "DATA_FILE=large_dataset.csv"
    python secure_processor.py
    Move-Item -Path "secured_large_dataset.csv" -Destination "secured_large_data_local.csv" -Force
    Move-Item -Path "large_dataset_processor.log" -Destination "local_large_processor.log" -Force
}

# --- LAYER 2: TRIGGER REMOTE HOST ---
Invoke-TimedStep "Remote Orchestration" {
    # SSH into Host and trigger the bash script
    # We use 'bash' explicitly to ensure the orchestrator.sh runs even if permissions are tricky
    ssh -p 2222 bedagya@localhost "bash /home/bedagya/orchestrator.sh"
    
    # Check if the Host Orchestrator succeeded (exit code 0)
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Remote pipeline success!" -ForegroundColor Green
        # --- LAYER 3: SYNC FROM HOST TO WINDOWS ---
        scp -P 2222 bedagya@localhost:/home/bedagya/*_vm.* .
    } else {
        Write-Host "Remote pipeline failed! Check runner.log." -ForegroundColor Red
        exit 1
    }
}

Stop-Transcript