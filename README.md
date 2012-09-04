pyronbee
============

This repository contains my own implementation of the IronBee WAF Research
project data. For more information, please fetch the whitepaper from
https://community.qualys.com/blogs/securitylabs/2012/07/25/protocol-level-
evasion-of-web-application-firewalls

The current version of pyronbee does not have test cases, but will be added
soon.

### Test files on pyronbee
The current format for requests in test files is in JSON.

      {
        "method": "POST",
        "url": "/form.php",
        "http_ver": "HTTP/1.1",
        "body": {
            "user": "matt",
            "passwd": "sarasa"
        }, 
        "headers":  {
          "User-Agent": "pyronbee",
          "Connection": "Close"
          },
        "description": "Just a sample test.",
        "status_codes": [302, 200]
      }


    
