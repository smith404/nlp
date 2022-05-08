# Email Decryption REST Service Documentation v1

As the application is only servicing a single **GET** endpoint and no body or request header parameters are expected or will be parsed, the service runs using a *http* not *https* protocol

http://{hostname}:{port}/decrypt?file={filepath}
- **hostname**: *required (string)* the hostname of the decryption server
- **port**: *required (integer)* the port number on the decryption server on which the service is listening 
- **filepath**: *required (string)* the full UNC path of the file to decrypt which mush be reachable from the decryption server

---
## Overview
The service provides a single **blocking** endpoint for proxying a call to the Microsoft AIP command **Unprotect-RMSFile**. The service is single threaded and blocking. This is to avoid starting multiple parallel PowerShell executions as this is not a desired behaviour. A typical decryption execution is performed in a sub-second response time and the expected volume of encrypted documents should not necessitate a multi threaded approach to decryption.

---
## Example Execution

An example of a syntactically correct URI would therefore be:

http://localhost:8070/decrypt?file=h:\temp\test.txt

The response body in the case of a successful endpoint interaction will be a *json* object with he following attributes:
- **filepath**: *required (string)* is a mirror (escaped) version of the file path provided in the call
- **success**: *required (boolean)* indicates if the file was found and processed by the PowerShell execution
- **message**: *required (string)* a message indicating the result of the execution
- **output**: *required (string)* the console output of the PowerShell command. This will under all usual circumstances be an empty string

## Possible *json* response for a successful REST call

A successful REST call is characterized by:
- Status Code        : 200
- Status Description : OK

In such cases the following can be expected

http://localhost:8070/decrypt?file=h:\temp\test.txt

Returning one of:

### Successful Execution Example

http://localhost:8070/decrypt?file=h:\temp\test.txt

```javascript
{
  "filepath": "h:\\local\\test.txt",
  "success": true,
  "message": "Execution completed successfully",
  "output": ""
}
```

### Unsuccessful Execution Examples

http://localhost:8070/decrypt?file=h:\temp\test.txt

```javascript
{
  "filepath": "h:\\temp\\test.txt",
  "success": false,
  "message": "File not found",
  "output": ""
}
```

```javascript
{
  "filepath": "h:\\temp\\test.txt",
  "success": false,
  "message": "File is read only",
  "output": ""
}
```

```javascript
{
  "filepath": "h:\\temp\\test.txt",
  "success": false,
  "message": "File is a system file",
  "output": ""
}
```

http://localhost:8070/decrypt?file=h:\temp

```javascript
{
  "filepath": "h:\\temp",
  "success": false,
  "message": "Directory without a filename was specified",
  "output": ""
}
```

### Full REST Response example

```powershell
Invoke-WebRequest -URI "http://localhost:8070/decrypt?file=h:\temp\test.txt"

StatusCode        : 200
StatusDescription : OK
Content           : {"filepath":"h:\\temp\\test.txt","success":false,"message":"Execution completed successfully","output":""}
RawContent        : HTTP/1.1 200 OK
                    Content-Type: application/json
                    Date: Sun, 8 May 2022 12:58:25 +02:00
                    Server: LDMS Email Decrypter/0.0.1

                    {"filepath":"h:\\temp\\test.txt","success":false,"message":...
Forms             : {}
Headers           : {[Content-Type, application/json], [Date, Sun, 8 May 2022 12:58:25 +02:00], [Server, K2 Email Decrypter/0.0.1]}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 107
```

---

## Examples of incorrect usage of the REST Service

As mentioned, the service provides only one **GET** endpoint. This expects one parameter called ***file***. Should other endpoints or verbs be used the following errors can be expected

- No file parameter specified
```powershell
PS C:\Users\markg> Invoke-WebRequest -URI "http://localhost:8070/decrypt?thefile=h:\temp\test.txt"
Invoke-WebRequest : The remote server returned an error: (400) Bad Request.
```

- Non GET request
```powershell
Invoke-WebRequest -URI "http://localhost:8070/decrypt?file=h:\temp\test.txt" -Method POST
Invoke-WebRequest : The remote server returned an error: (405) Method Not Allowed.
```


- Non incorrect enpoint path
```powershell
PS C:\Users\markg> Invoke-WebRequest -URI "http://localhost:8070/encrypt?file=h:\temp\test.txt"
Invoke-WebRequest : The remote server returned an error: (404) Not Found.
```



