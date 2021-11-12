param
(
    [string]$url
)
 
$downloadToPath = "C:\Users\zzk\Desktop\powershellwget/result.txt"

$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
    
foreach($line in Get-Content .\cookies.txt) {
    if(!$line.StartsWith("#")){
    
        $split = $line.Split(",")
                
        $cookie = New-Object System.Net.Cookie 

        $cookie.Name = $split[0]
        $cookie.Value = $split[1]
        $cookie.Domain = $split[2]

        $session.Cookies.Add($cookie);

    }
}

Invoke-WebRequest $url -WebSession $session -OutFile ".\artist_m3u8.txt"