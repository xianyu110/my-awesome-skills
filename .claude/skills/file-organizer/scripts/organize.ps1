
param (
    [string]$TargetPath
)

if ([string]::IsNullOrWhiteSpace($TargetPath)) {
    Write-Host "Usage: organize.ps1 <TargetPath>"
    exit 1
}

if (-not (Test-Path $TargetPath -PathType Container)) {
    Write-Host "Error: Target path '$TargetPath' does not exist or is not a directory."
    exit 1
}

Write-Host "Organizing files in '$TargetPath'..."

$files = Get-ChildItem -Path $TargetPath -File

foreach ($file in $files) {
    $extension = $file.Extension
    if ([string]::IsNullOrWhiteSpace($extension)) {
        $folderName = "No_Extension"
    } else {
        $folderName = $extension.TrimStart('.')
    }

    $destinationFolder = Join-Path -Path $TargetPath -ChildPath $folderName

    if (-not (Test-Path $destinationFolder -PathType Container)) {
        New-Item -ItemType Directory -Path $destinationFolder | Out-Null
        Write-Host "Created folder: $destinationFolder"
    }

    try {
        Move-Item -Path $file.FullName -Destination $destinationFolder -Force
        Write-Host "Moved '$($file.Name)' to '$folderName'"
    }
    catch {
        Write-Error "Failed to move '$($file.Name)': $($_.Exception.Message)"
    }
}

Write-Host "File organization complete."
