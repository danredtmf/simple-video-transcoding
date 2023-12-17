$current_path = Get-Location
$resources_path = Join-Path -Path $current_path -ChildPath 'resources'
$ffmpeg_zip_path = Join-Path -Path $resources_path -ChildPath 'ffmpeg.zip'
$ffmpeg_folder_path = Join-Path -Path $resources_path -ChildPath 'ffmpeg'
$ffmpeg_bin_path = Join-Path -Path $ffmpeg_folder_path -ChildPath 'bin'
$ffmpeg_path = Join-Path -Path $ffmpeg_bin_path -ChildPath 'ffmpeg.exe'

function Check-Resources {
    if (Test-Path -Path $resources_path) {
        Write-Host 'Download FFmpeg...' -f Green
        Download-FFmpeg
    }
    else {
        Write-Host 'Creating a "resources" folder...' -f Green
        New-Item -Path $resources_path -ItemType Directory | Out-Null
        Check-Resources
    }
}


function Download-FFmpeg {
    wget https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip -outfile $ffmpeg_zip_path
    Get-FFmpeg

}

function Get-FFmpeg {
    Expand-Archive -Path $ffmpeg_zip_path -DestinationPath $resources_path
    Rename-Item -Path (Get-ChildItem -Path $resources_path -Filter "ffmpeg-*").FullName -NewName "ffmpeg"
    Remove-Item -Path $ffmpeg_zip_path
    Move-Item -Path $ffmpeg_path -Destination $resources_path
    Remove-Item -Path $ffmpeg_folder_path -Recurse

}

Check-Resources