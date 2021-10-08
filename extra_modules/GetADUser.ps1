param($sam)
Import-module ActiveDirectory
get-aduser -Identity $sam -Properties SamAccountName,LockedOut,AccountExpires,pwdlastset,lastLogon |
select SamAccountName,LockedOut,@{N = "pwdlastset"; E = {[DateTime]::FromFileTime($_.pwdlastset)}},
@{N = "AccountExpires"; E = {[DateTime]::FromFileTime($_.AccountExpires)}}, @{N = "LastLogon"; E = {[DateTime]::FromFileTime($_.LastLogon)}}