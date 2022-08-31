from socket import *
from threading import *
from _thread import start_new_thread
import time
import sys

def generate_header_lines(code, length):
        header = ''
        if code == 200:
            header = 'HTTP/1.1 200 OK\n'
            header += 'Server: Abdullah\n'

        elif code == 404:
            # Status code
            header = 'HTTP/1.1 404 Not Found\n'
            header += 'Date: ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) + '\n'
            header += 'Server: Abdullah\n'

        header += 'Content-Length: ' + str(length) + '\n'
        header += 'Connection: close\n\n'

        return header


def HTTP(connection,request,webserver,port,requested_file):
    requested=requested_file
    requested_file = requested_file.replace(".", "_").replace("http://", "_").replace("/", "")
    try:
            file = open('cache/'+requested_file,'rb')
            print("\n")
            print("  Cache Hit\n")
            response = file.read()
            file.close()
            response_headers = generate_header_lines(200, len(response))
            connection.send(response_headers.encode("utf-8"))
            time.sleep(1)
            connection.send(response)
            connection.close()

    except Exception as ep:
                s = socket(AF_INET, SOCK_STREAM)
                webserver.encode()
                s.connect((webserver, int(port)))
                s.send(request)
                file_object = s.makefile('wb', 0)
                requested=requested.encode()
                file_object.write(b"GET " + b"http://" + requested+ b" HTTP/1.0\n\n")
                file_object = s.makefile('rb', 0)
                buff = file_object.readlines()
                for i in range(0, len(buff)):
                    connection.send(buff[i])
                s.close()
                connection.close()
                return



def HTTPS(connection,webserver,port,requested_file):
 requested_file = requested_file.replace(".", "_").replace("http://", "_").replace("/", "")
 try:
            requested_file+='cache/'
            file = open(requested_file,'rb')
            print("\n")
            print("  Cache Hit\n")
            response = file.read()
            file.close()
            response_headers = generate_header_lines(200, len(response))
            connection.send(response_headers.encode("utf-8"))
            time.sleep(1)
            connection.send(response)
            connection.close()

 except Exception as ep:
    proxy=socket( AF_INET, SOCK_STREAM)
    webserver=webserver.encode()
    proxy.connect((webserver,int(port)))
    reply = "HTTP/1.0 200 Connection established\r\n"
    reply += "Proxy-agent: Abdullah\r\n"
    reply += "\r\n"
    connection.sendall(reply.encode())
    connection.setblocking(0)
    proxy.setblocking(0)
    while True:
        try:
            request = connection.recv(8192)
            proxy.sendall(request)
        except error as err:
            pass
        try:
            reply = proxy.recv(8192)
            connection.sendall(reply)
        except error as e:
            pass    
    proxy.close()

def proxy_server(connection,add):
    try:
        re=connection.recv(1024).decode('UTF-8')
        protocol=re.split(' ')[0]
        requested=re.split(' ')[1]
        port_no=re.split(' ')[1]
        finder=port_no.find(':')
        if finder==-1:
            web_server=port_no
            port_no=80
        else:
            web_server=port_no.split(':')[0]
            port_no=port_no.split(':')[1]
        if protocol=='CONNECT':
            print("HTTPS request to",web_server)
            HTTPS(connection,web_server,port_no,requested)
        elif protocol=='GET':
            print("HTTP request to",web_server)
            HTTP(connection,re,web_server,port_no,requested)
    except Exception as e:
        return


def main():
    address=gethostbyname(gethostname())
    print(address)
    server=socket( AF_INET, SOCK_STREAM)
    server.bind(('',4545))
    server.listen(10)
    print("Server is listening :")
    while True:
        try:
            connection,add=server.accept()
            start_new_thread(proxy_server, (connection,add))
        except KeyboardInterrupt:
            sys.exit()
    connection.close()


main()



