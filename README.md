# Python Port Scanner Project

A simple Python port scanner that checks a list of commonly used ports on a target IP address. It uses a thread pool to scan ports concurrently and returns a structured result showing the port state and error code.

## Files

- `PY-scan.py` — the main port scanning script.
- `README.md` — this file.

## Features

- Scans a preset list of ports (`portz`) on a target.
- Uses `socket.connect_ex()` with a timeout to detect open/closed/filtered ports.
- Uses `ThreadPoolExecutor` to run one thread per port scan.
- Returns results as a dictionary keyed by port.

## Usage

1. Open a terminal in the `Python port scanner project` directory.
2. Run:

```bash
python ../PY-scan.py
```

3. Enter the target IP address when prompted.

## Notes

- The script is designed for I/O-bound network scanning, so threading improves speed.
- `0` means the port is open. 
- A connection refused error typically indicates the port is closed.
- Timeout and unreachable errors indicate the port may be filtered.

## Future improvements

- Accept target and port list arguments from the command line
- Add better OS-specific errno handling and logging
- Save results to a file
- Add a nicer terminal user interface
