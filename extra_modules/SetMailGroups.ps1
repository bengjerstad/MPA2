param (
    [string]$sam,
	[string]$agentusername,
	[string]$groupname
 )
$securestring = Get-Content $env:USERPROFILE\Documents\Data\words.txt | ConvertTo-SecureString
$credentials = new-object -typename System.Management.Automation.PSCredential -argumentlist $agentusername,$securestring
$connected = Connect-AzureAD -Credential $credentials

$user = Get-AzureADUser -SearchString $sam
$group = Get-AzureADGroup -SearchString $groupname
Add-AzureADGroupMember -ObjectId $group.ObjectId -RefObjectId $user.ObjectId