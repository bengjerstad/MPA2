Import-module ActiveDirectory
get-aduser -filter * -Properties SamAccountName,displayName,Enabled,givenName,sn,distinguishedname,mail,mailnickname,department,Departmentnumber,employeeID,employeeType,mobile,telephoneNumber,facsimileTelephoneNumber,title,AccountExpires,pwdlastset,lastLogon,carLicense,whenCreated,userType |
select SamAccountName,displayName,Enabled,givenName,sn,distinguishedname,mail,mailnickname,department,@{N='Departmentnumber';E={$_.Departmentnumber[0]}},employeeID,employeeType,mobile,telephoneNumber,FAX,title,@{N = "pwdlastset"; E = {[DateTime]::FromFileTime($_.pwdlastset)}},
@{N = "AccountExpires"; E = {[DateTime]::FromFileTime($_.AccountExpires)}}, @{N = "LastLogon"; E = {[DateTime]::FromFileTime($_.LastLogon)}},@{N='carLicense';E={$_.carLicense[0]}},whenCreated,userType|
export-csv $env:USERPROFILE"\Documents\Data\ADUsers.csv" -NoTypeInformation