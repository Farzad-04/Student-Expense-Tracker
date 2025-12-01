$headers = @{
    'X-Figma-Token' = 'figd_94tmg6y8p051w_ioWgdwWM-NfuRfkc7nYaQFMwiG'
}

try {
    $response = Invoke-WebRequest -Uri 'https://api.figma.com/v1/files/rCPVU0K27KsTguOya8N6Ln' -Headers $headers
    $response.Content | Out-File -FilePath 'figma-data.json' -Encoding utf8
    Write-Host "Successfully fetched Figma data"
    
    # Also get styles
    $stylesResponse = Invoke-WebRequest -Uri 'https://api.figma.com/v1/files/rCPVU0K27KsTguOya8N6Ln/styles' -Headers $headers
    $stylesResponse.Content | Out-File -FilePath 'figma-styles.json' -Encoding utf8
    Write-Host "Successfully fetched Figma styles"
} catch {
    Write-Host "Error: $_"
    Write-Host $_.Exception.Message
}

