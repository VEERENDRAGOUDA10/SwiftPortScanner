import socket
import sys
import time
import queue
import threading
import requests

usage = "python3 port_scanner TARGET START_PORT END_PORT THREADS"

print("*" * 30)
print("this is a simple port_scaner")
print("*" * 30)

target = sys.argv[1]
start_port = int(sys.argv[2])
end_port = int(sys.argv[3])
thread_no = int(sys.argv[4])

try:
    target = socket.gethostbyname(target)
except:
    print("[!] error")
    exit()

result = "PORT\tSTATE\tBanner"

if not target or not start_port or not end_port or not thread_no:
    print("Missing arguments. Please provide the target host, start port, and end port.")
    print(usage)
    exit()

def get_b(port, scan):
    return scan.recv(1024).decode()



def scan_port(t_no):
    global result
    while True:
        port = q.get()
        try:
            scan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            scan.settimeout(2)
            con = scan.connect_ex((target, port))
            print("conn value {}".format(con))
            if not con:
                banner = get_b(port,scan) 
                result+=f"\n{port}\topen\t{banner}"
            scan.close()
        except Exception as e:
            pass
        q.task_done()

q = queue.Queue()


start_time = time.time()


for j in range(start_port, end_port + 1):
    q.put(j)
for i in range(thread_no):
    t = threading.Thread(target=scan_port, args=(i,))
    t.start()
q.join()


end_time = time.time()
print(result)

print('Timetake {}'.format(end_time - start_time))  # Corrected the calculation of time taken

