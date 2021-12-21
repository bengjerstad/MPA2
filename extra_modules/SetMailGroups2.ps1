param (
    [string]$sam,
	[string]$agentusername,
	[String[]]$groupnames
 )
Import-Module ExchangeOnlineManagement
$connected = Connect-ExchangeOnline -UserPrincipalName $agentusername
$groupnames | Foreach-Object { 
	Add-DistributionGroupMember  -Identity $_ -Member $sam
}