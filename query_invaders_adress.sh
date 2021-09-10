
INVADERS=$(cat all_invaders/all_invaders.list)
i=0

for INVADER in $INVADERS
do
   i=$((i+1))
   echo "$i => $INVADER"
   # or do whatever with individual element of the array
   curl 'https://www.battleparis.com/search/' \
  -H 'Connection: keep-alive' \
  -H 'Pragma: no-cache' \
  -H 'Cache-Control: no-cache' \
  -H 'sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36' \
  -H 'Origin: https://www.battleparis.com' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-Mode: navigate' \
  -H 'Sec-Fetch-User: ?1' \
  -H 'Sec-Fetch-Dest: document' \
  -H 'Referer: https://www.battleparis.com/search/' \
  -H 'Accept-Language: en-US,en;q=0.9,fr;q=0.8' \
  -H 'Cookie: csrftoken=79glOpZbC7CnSmAzUZASYAZLdbPRZT06EtNIEvVDkTEV6Iy80KQg2H8TPA1HbweK' \
  --data-raw "csrfmiddlewaretoken=nFUMbbrhdudGCV2C49KsJRK2E08KlKQ5UZr91hnJVgfeQh0baU0QNYTagpkAxn4J&search=$INVADER" \
  --compressed > "battleparis/invader_$INVADER.html"
  sleep 0.5
done
