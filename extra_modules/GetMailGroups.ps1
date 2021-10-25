param (
    [string]$sam,
	[string]$agentusername
 )
$securestring = Get-Content $env:USERPROFILE\Documents\Data\words.txt | ConvertTo-SecureString
$credentials = new-object -typename System.Management.Automation.PSCredential -argumentlist $agentusername,$securestring
$connected = Connect-AzureAD -Credential $credentials

$user = Get-AzureADUser -SearchString $sam
$groups = Get-AzureADUserMembership  -ObjectId $user.ObjectId | Select-Object -Property DisplayName, Mail, MailEnabled,ObjectId  | Where-Object {$_.MailEnabled -eq "True"}
$groups |  ConvertTo-Json -Compress