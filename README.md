pyronbee
============

pyronbee is a networking security tool to test Web Application Firewalls using
customized requests. 

This repository contains my own implementation of the IronBee WAF Research
project data. For more information, please fetch the whitepaper from
https://community.qualys.com/blogs/securitylabs/2012/07/25/protocol-level-
evasion-of-web-application-firewalls

The current version of pyronbee does not have **test files**, but will be added
soon. In the meanwhile you can make your own, since it's very easy to do it.

### My personal usage of pyronbee

Sometimes you find yourself doing a pentest and the security (WAF, IDS, IPS)
starts to block certain request you do, for example the ones for an SQL
Injection. Knowing that a WAF does not see the same as a web server, tweaking a
little our request can make the security to ignore it, and the webserver may
understand it as a sucessful request.

Web servers tend to fix malformed requests, and there are modules to correct
some urls to specific documents, paths, such as mod_spelling. So you can try
to send 'broken' requests hoping that the WAF consider it harmless and the web
server interpret it correctly.

## Test files on pyronbee

The current format for requests in test files is in **JSON**.

**request.test:**

      {
        "method": "POST",
        "url": "/ form.php",
        "http_ver": "HTTP/1.1",
        "urlencoded": {
            "user": "matt",
            "passwd": "sarasa"
        },
        "multipart" : null,
        "headers":  {
          "User-Agent": "pyronbee",
          "Connection": "Close"
          },
        "description": "Just a sample test.",
        "status_codes": [302, 200]
      }

**request2.test:**

      {
        "method": "GET",
        "url": "/UNION%20SELECT",
        "http_ver": "HTTP/1.1",
        "body": {
        },
        "multipart" : null,
        "headers":  {
          "User-Agent": "pyronbee",
          "Connection": "Close"
          },
        "description": "Just another sample test.",
        "status_codes": [200]
      }

If you wish to send multipart requests, you have to encode first the data on
base64, since it's very tedious to manual escape special characters, slashes,
brackets and commas.

**request3.test**

      {
        "method": "POST",
        "url": "/index.php",
        "http_ver": "HTTP/1.1",
        "urlencoded": null,
        "multipart" : "LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS01NjM0MzYyOTIxMzE2MTY3NTYzNzQyODM5NDU2XHJcbgpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9ImFsYnVtX3RpdGxlIlxyXG4KXHJcbgpPcHRpb25hbCBBbGJ1bSBUaXRsZVxyXG4KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS01NjM0MzYyOTIxMzE2MTY3NTYzNzQyODM5NDU2XHJcbgpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9ImxheW91dCJcclxuClxyXG4KYlxyXG4KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS01NjM0MzYyOTIxMzE2MTY3NTYzNzQyODM5NDU2XHJcbgpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9InNpZCJcclxuClxyXG4KamZmM2I3OWYybW5yMnFzNDhwYWt2aWlqYzZcclxuCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tNTYzNDM2MjkyMTMxNjE2NzU2Mzc0MjgzOTQ1NlxyXG4KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWxlIjsgZmlsZW5hbWU9ImltYWdlLmpwZWciXHJcbgpDb250ZW50LVR5cGU6IGltYWdlL2pwZWdcclxuClxyXG4KaW1hZ2VkYXRh",
        "headers":  {
          "User-Agent": "pyronbee",
          "Connection": "Close"
          },
        "description": "Multipart test.",
        "status_codes": [200]
      }

## Formatting requests 

The way pyronbee formats the requests is in the file **default.cfg** with
**JSON** syntax. The request line contains an HTTP method, a Uniform Resource
Identifier (URI), and the HTTP version number, followed by carriage return and
line feed characters. Typically, the request line is followed by a series of
HTTP headers.


      {
      "method": "%s %s %s\r\n",
      "header": "%s: %s\r\n",
      "body": "\n%s\r\n"
      }

For example, using the following **.test** file:

      {
        "method": "GET",
        "url": "/",
        "http_ver": "HTTP/1.1",
        "body": {
        },
        "multipart" : null, 
        "headers":  {
          "User-Agent": "pyronbee",
          "Connection": "Close"
          },
        "description": "Example.",
        "status_codes": [200]
      }

the request will look like this:


      GET / HTTP/1.1\r\n
      User-Agent: pyronbee\r\n
      Connection: Close\r\n
      \r\n


### Usage of pyronbee

      [matt@mfsec pyronbee]$ ./pyronbee.py
      [!] Usage: ./pyronbee.py host port test_files
      [!] Examples:
         ./pyronbee.py mfsec.com.ar 80 request.test
         ./pyronbee.py mfsec.com.ar 443 *.test

      [matt@mfsec pyronbee]$ ./pyronbee.py mfsec.com.ar 80 *.test
      [*] Missed with a 200 [request.test] | Just a sample test.
      [+] Blocked with a 403 [request2.test] | Just another sample test.


## Extra tools

Located in the extra folder I will be adding little scripts to automate the
creation of **.test** files using a list of requests.


### Usage of ./gen_requests.py

      [matt@mfsec extra]$ ./gen_requests.py 
      Usage: ./gen_requests.py URL REQUESTS_FILE PREFIX
      Example:
        ./gen_requests.py /index.php?search= requests isr_example_

**`./gen_requests.py "/playground.php?step=1&href=javascript:" sample.requests
playground_tests_`** will generate one **.test** file for each line in
**sample.requests** file.

Content of **sample.requests** file:

      window["alert"]("ISR")
      window["ale"%2b(!![]%2b[])[-~[]]%2b(!![]%2b[])[%2b[]]]()
      window["ale"%2b"\x72\x74"]()
      window["\x61\x6c\x65\x72\x74"]()
      window['ale'%2b(!![]%2b[])[-~[]]%2b(!![]%2b[])[%2b[]]]()
      window['ale'%2b'\x72\x74']()
      window['\x61\x6c\x65\x72\x74']()
      window[(+{}+[])[-~[]]+(![]+[])[-~-~[]]+([][+[]]+[])[-~-~-~[]]+(!![]+[])[-~[]]+(!![]+[])[+[]]]((-~[]+[]))
      window[(+{}+[])[+!![]]+(![]+[])[!+[]+!![]]+([][+[]]+[])[!+[]+!![]+!![]]+(!![]+[])[+!![]]+(!![]+[])[+[]]]
      this["alert"]("ISR")
      ...

Sample of one of the generated files from above:
      {"headers": {"Connection": "Close", "User-Agent": "pyronbee"}, "urlencoded": null, "http_ver": "HTTP/1.1", "url": "/playground.php?step=1&href=javascript:window[\"alert\"](\"ISR\")", "status_codes": [200], "description": "No description", "method": "GET", "multipart": null}



### Why JSON in test files?

The main purpose of using JSON in **default.cfg** and ***.test** files is to give
users a chance to customize their requests as much as possible. JSON seemed
right, since it's parseable in most of the languages and it's easier to read
than object serialization.

### TODO
- Add `*.test` files.
- Add the option to use a more than one custom file if needed.
- Add timeouts.
- Add the option to make a final report.
