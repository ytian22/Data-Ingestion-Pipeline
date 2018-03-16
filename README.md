# Data-Ingestion-System-Implementation
This application accepts connections, log all requests and then properly process well-formed JSON strings. <br>

## General Description
There are three computers that are involved with deploy script: <br>
- Repository: Where the code was stored. <br>
- Local Machine: Where the code was developed, and where the deploy script was run from. <br>
- The server: Where the code was deployed to. <br>

## Steps
In order to test the code, the following line will be appended to the end of the deploy.py code provided.<br>
```deploy( 'path_to_ssh_key_private_key', 'server-address', 'prefix')```
Where the variables are the path to the ssh key needed to login to the server and the server address is the url of the server that will be SSH’d into. <br>
<br>
The deploy script would do the following:<br>
\begin{enumerate}
  \item Login, via SSH to the server.
  \item Clone the repository, which contains process_json.py and log_rotate.py, to the server, in the home directory.
  \item The process_json.py script starts a Flask application which accepts HTTP post requests on port 8080.
  \item Each request will be logged as a string into a log file (Raw.txt); log rotate via the operating system to rotate the file every 2 minutes into another file within that same directory.
  \item If a request is a "valid" JSON object, process it and extract the “name” and “age” from the object. Then put the processed output into proc.txt; rotate the file every two minutes.
\end{enumerate}
