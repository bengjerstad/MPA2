param (
    [string]$upn,
	[string]$agentusername
 )
$securestring = Get-Content $env:USERPROFILE\Documents\Data\words.txt | ConvertTo-SecureString
$credentials = new-object -typename System.Management.Automation.PSCredential -argumentlist $agentusername,$securestring
Import-Module MSOnline

Connect-MsolService -Credential $credentials

$st = New-Object -TypeName Microsoft.Online.Administration.StrongAuthenticationRequirement
$st.RelyingParty = "*"
$st.State = "Enabled"
$sta = @($st)

Set-MsolUser -UserPrincipalName $upn -StrongAuthenticationRequirements $sta
$output = Get-MsolUser -UserPrincipalName $upn | Select StrongAuthenticationRequirements
$output.StrongAuthenticationRequirements.State