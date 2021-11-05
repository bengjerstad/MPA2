param (
    [string]$upn,
	[string]$agentusername
 )
$securestring = Get-Content $env:USERPROFILE\Documents\Data\words.txt | ConvertTo-SecureString
$credentials = new-object -typename System.Management.Automation.PSCredential -argumentlist $agentusername,$securestring
Import-Module MSOnline

Connect-MsolService -Credential $credentials

$output = Get-MsolUser -UserPrincipalName $upn

If ($output.isLicensed -eq "True") {
  $output.Licenses.AccountSkuId
}  
Else {
  $output.isLicensed
} 