Ingresar al balanceador bgazlbcrc, desde CyberArk, y verificar si existe alguna IP con comportamiento inusual con el siguiente comando:
tail -20000 /var/log/nginx/access.log | grep '\s404\s\|\s403\s' | gawk '{split($4,a,":"); split(strftime("%H:%M:%S", systime()),b,":"); if(((b[1] * 60 * 60) + (b[2] * 60) + b[3]) - ((a[2] * 60 * 60) + (a[3] * 60) + a[4]) < 120) print $0}' | grep -o '\"[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\"' | sort | uniq -c | awk '{if ($1 >= 10) print "ALERTA " $1 ": " $2}'

En caso de devolver alg�n resultado: realizar un tail -2000 | grep "Colocar_IP" , y verificar que rutas esta solicitando o accediendo, Reportar al chat OnCall, Telem�tica y a SOC, si detecta alguna anomal�a.


En caso de observar alguna IP maliciosa, validar su reputacion con el siguiente enlace: https://www.abuseipdb.com/
