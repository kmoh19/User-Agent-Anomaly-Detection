# User-Agent-Anomaly-Detection

Note: API expects user agent strings in the same format as found in the benign and exploit folders!

* API is flask application hosted on an aws ec2 instance at:
http://18.233.186.222:5000/

* Use a web browser to assess a new user agent string - just add it to the ua argument as such:
http://18.233.186.222:5000/api/user_agent?ua= |user agent string|
  
** For example:
http://18.233.186.222:5000/api/user_agent?ua=[02/Aug/2011:22:03:40 -0700] "user_29" 0.0.0.0 0.0.0.0  9080 200 TCP_NC_MISS "GET http://www.thaitravelcenter.com/thailand/packages//thailand/include/read_currency.asp HTTP/1.0" "unknown"  "low risk" "text/html" 531 799 "Mozilla/5.0 (Windows NT 6.1; rv:7.0a2) Gecko/20110801 Firefox/7.0a2" "www.thaitravelcenter.com" "-" "0" "" "-“
* Alternatively you can use postman api client
