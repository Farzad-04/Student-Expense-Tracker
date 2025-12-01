$headers = @{
    'X-Figma-Token' = 'figd_94tmg6y8p051w_ioWgdwWM-NfuRfkc7nYaQFMwiG'
}

try {
    $response = Invoke-WebRequest -Uri 'https://api.figma.com/v1/files/rCPVU0K27KsTguOya8N6Ln/nodes?ids=1-2,1-98' -Headers $headers
    $response.Content | Out-File -FilePath 'figma-nodes.json' -Encoding utf8
    Write-Host "Successfully fetched Figma nodes"
} catch {
    Write-Host "Error: $_"
    Write-Host $_.Exception.Message
}

