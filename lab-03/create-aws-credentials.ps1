<#
Interactive helper to create/update %USERPROFILE%\.aws\credentials and optionally ~/.aws/config
This script does NOT transmit credentials anywhere. It writes to the local user's profile folder.
#>
param(
    [string]$ProfileName = 'default',
    [switch]$SetRegion
)

function Read-Secret($prompt) {
    $secure = Read-Host $prompt -AsSecureString
    return [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure))
}

$awsDir = Join-Path $env:USERPROFILE '.aws'
if (-not (Test-Path $awsDir)) {
    New-Item -ItemType Directory -Path $awsDir | Out-Null
}

if (-not $ProfileName) { $ProfileName = 'default' }
$accessKey = Read-Host "AWS Access Key ID for profile '$ProfileName'"
$secretKey = Read-Secret "AWS Secret Access Key for profile '$ProfileName'"

$credentialsPath = Join-Path $awsDir 'credentials'
$entry = "[`$ProfileName`]`naws_access_key_id = $accessKey`naws_secret_access_key = $secretKey`n"

# If profile exists, replace it; otherwise append
if (Test-Path $credentialsPath) {
    $content = Get-Content $credentialsPath -Raw
    # simple regex to find existing profile block
    $pattern = "(?ms)\[` + [regex]::Escape($ProfileName) + "\].*?(?=\n\[|$)"
    if ([regex]::IsMatch($content, $pattern)) {
        $newContent = [regex]::Replace($content, $pattern, $entry)
        Set-Content -Path $credentialsPath -Value $newContent -Force
        Write-Host "Profile '$ProfileName' atualizado em $credentialsPath"
    } else {
        Add-Content -Path $credentialsPath -Value "`n$entry"
        Write-Host "Profile '$ProfileName' adicionado em $credentialsPath"
    }
} else {
    Set-Content -Path $credentialsPath -Value $entry
    Write-Host "Arquivo $credentialsPath criado com profile '$ProfileName'"
}

if ($SetRegion) {
    $region = Read-Host "Região padrão (ex: us-east-1)"
    $configPath = Join-Path $awsDir 'config'
    $configEntry = "[profile $ProfileName]`nregion = $region`n"
    if (Test-Path $configPath) {
        $c = Get-Content $configPath -Raw
        $p = "(?ms)\[profile\s+" + [regex]::Escape($ProfileName) + "\].*?(?=\n\[profile|$)"
        if ([regex]::IsMatch($c, $p)) {
            $newc = [regex]::Replace($c, $p, $configEntry)
            Set-Content -Path $configPath -Value $newc -Force
            Write-Host "Config profile '$ProfileName' atualizado em $configPath"
        } else {
            Add-Content -Path $configPath -Value "`n$configEntry"
            Write-Host "Config profile '$ProfileName' adicionado em $configPath"
        }
    } else {
        Set-Content -Path $configPath -Value $configEntry
        Write-Host "Arquivo $configPath criado com profile '$ProfileName'"
    }
}

# clear secret from memory
$secretKey = $null
[GC]::Collect()

Write-Host "Pronto. Use `'$env:USERPROFILE\\.aws\\credentials'` ou defina `AWS_PROFILE` para usar este profile."