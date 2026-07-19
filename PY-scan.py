import socket
import errno
from concurrent.futures import ThreadPoolExecutor as thread
display = """
                                                                                                                                  
                                                                                                                                  
PPPPPPPPPPPPPPPPP   YYYYYYY       YYYYYYY                                                                                         
P::::::::::::::::P  Y:::::Y       Y:::::Y                                                                                         
P::::::PPPPPP:::::P Y:::::Y       Y:::::Y                                                                                         
PP:::::P     P:::::PY::::::Y     Y::::::Y                                                                                         
  P::::P     P:::::PYYY:::::Y   Y:::::YYY                     ssssssssss       cccccccccccccccc  aaaaaaaaaaaaa  nnnn  nnnnnnnn    
  P::::P     P:::::P   Y:::::Y Y:::::Y                      ss::::::::::s    cc:::::::::::::::c  a::::::::::::a n:::nn::::::::nn  
  P::::PPPPPP:::::P     Y:::::Y:::::Y                     ss:::::::::::::s  c:::::::::::::::::c  aaaaaaaaa:::::an::::::::::::::nn 
  P:::::::::::::PP       Y:::::::::Y      --------------- s::::::ssss:::::sc:::::::cccccc:::::c           a::::ann:::::::::::::::n
  P::::PPPPPPPPP          Y:::::::Y       -:::::::::::::-  s:::::s  ssssss c::::::c     ccccccc    aaaaaaa:::::a  n:::::nnnn:::::n
  P::::P                   Y:::::Y        ---------------    s::::::s      c:::::c               aa::::::::::::a  n::::n    n::::n
  P::::P                   Y:::::Y                              s::::::s   c:::::c              a::::aaaa::::::a  n::::n    n::::n
  P::::P                   Y:::::Y                        ssssss   s:::::s c::::::c     ccccccca::::a    a:::::a  n::::n    n::::n
PP::::::PP                 Y:::::Y                        s:::::ssss::::::sc:::::::cccccc:::::ca::::a    a:::::a  n::::n    n::::n
P::::::::P              YYYY:::::YYYY                     s::::::::::::::s  c:::::::::::::::::ca:::::aaaa::::::a  n::::n    n::::n
P::::::::P              Y:::::::::::Y                      s:::::::::::ss    cc:::::::::::::::c a::::::::::aa:::a n::::n    n::::n
PPPPPPPPPP              YYYYYYYYYYYYY                       sssssssssss        cccccccccccccccc  aaaaaaaaaa  aaaa nnnnnn    nnnnnn
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
"""
portz = [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 587, 993, 1433, 3306, 3389, 8080, 8000]
class port_scan():
    @staticmethod
    def status_from_code(code):
        if code == 0:
            return "open"
        if code == errno.ECONNREFUSED:
            return "closed"
        if code in (errno.ETIMEDOUT, errno.EHOSTUNREACH, errno.ENETUNREACH):
            return "filtered"
        return f"error {code}"
    
    @staticmethod
    def scan(target, port):
        with(socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s): # creates client socket
            s.settimeout(1)
            err_code = s.connect_ex((target, port))
        status = port_scan.status_from_code(err_code)
        return port, err_code, status

    @staticmethod
    def threading(target, ports=portz, max_workers=100): # adds threads to run scans
       with thread(max_workers=min(max_workers, len(ports))) as executor:
         results = list(executor.map(lambda p: port_scan.scan(target, p), ports)) # each thread scans one port
       return {port: {'code': code, 'status': status} for port, code, status in results}

    

def main():
  print(display)
  user_input = input("Please enter the target IP address you want to scan: ")
  result_list = port_scan.threading(user_input)
  print("Here are the results of your scan:")
  for port in sorted(result_list):
    entry = result_list[port]
    print(f"port {port}: {entry['status']} (code {entry['code']})")

if __name__ == "__main__":
   main()
      

