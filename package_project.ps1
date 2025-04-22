# Set variables
$zipName = "business-tax-calculator.zip"
$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$stagingDir = Join-Path $rootDir "zip_staging"

# Clean up old zip or staging dir
if (Test-Path $zipName) { Remove-Item $zipName }
if (Test-Path $stagingDir) { Remove-Item $stagingDir -Recurse -Force }

# Exclude folders or files that match any of these
$excludeDirs = @("venv", ".git", "__pycache__", ".pytest_cache", "zip_staging")
$excludeExtensions = @(".bat", ".cmd", ".ps1")

# Copy only valid files to staging
Get-ChildItem -Path $rootDir -Recurse -File -Force | ForEach-Object {
    $relativePath = $_.FullName.Substring($rootDir.Length).TrimStart('\')
    $pathSegments = $relativePath.Split('\')
    $extension = [System.IO.Path]::GetExtension($_.FullName)
    $containsEggInfo = $pathSegments | Where-Object { $_ -like "*.egg-info" }

    if (
        ($excludeDirs | Where-Object { $pathSegments -contains $_ }) -eq $null -and
        ($excludeExtensions -notcontains $extension) -and
        (-not $containsEggInfo)
    ) {
        $dest = Join-Path $stagingDir $relativePath
        New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null
        Copy-Item $_.FullName -Destination $dest
    }
}

# Create zip archive
Compress-Archive -Path "$stagingDir\*" -DestinationPath $zipName

# Clean up
Remove-Item $stagingDir -Recurse -Force

Write-Host "`n✅ Project zipped as $zipName (with egg-info, folders & file-type exclusions)"
