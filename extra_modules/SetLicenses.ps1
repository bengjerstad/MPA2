param (
    [string]$upn,
	[string]$agentusername,
	[String[]]$licenses
 )
$securestring = Get-Content $env:USERPROFILE\Documents\Data\words.txt | ConvertTo-SecureString
$credentials = new-object -typename System.Management.Automation.PSCredential -argumentlist $agentusername,$securestring
Import-Module MSOnline

Connect-MsolService -Credential $credentials

Set-MsolUser -UserPrincipalName $upn -UsageLocation US
foreach ($license in $licenses){
	Set-MsolUserLicense -UserPrincipalName $upn -AddLicenses $license
}

$output = Get-MsolUser -UserPrincipalName $upn
$output.Licenses.AccountSkuId