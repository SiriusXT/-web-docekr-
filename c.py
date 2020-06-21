#coding=utf-8
from socket import *

def handle_client(client_socket):
    """为一个客户端服务"""
    # 接收对方发送的数据
    recv_data = client_socket.recv(1024).decode("utf-8") #  1024表示本次接收的最大字节数
    # 打印从客户端发送过来的数据内容
    #print("client_recv:",recv_data)
    request_header_lines = recv_data.splitlines()
    for line in request_header_lines:
        print(line)
     
    # 返回浏览器数据
    # 设置返回的头信息 header
    response_headers = "HTTP/1.1 200 OK\r\n" # 200 表示找到这个资源
    response_headers += "\r\n" # 空一行与body隔开
    # 设置内容body
    response_body = "<h1>fat boss<h1>\r\n" 
    response_body += "<h2>come on<h2>\r\n" 
    response_body += "<h3>binlang!!!<h3>\r\n" 

    # 合并返回的response数据
    response = response_headers + response_body
    
    # 返回数据给浏览器
    client_socket.send(response.encode("utf-8"))   #转码utf-8并send数据到浏览器
    client_socket.close()

def main():
   # 创建套接字
   server_socket = socket(AF_INET, SOCK_STREAM)
   # 设置当服务器先close 即服务器端4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时 可以立即绑定7788端口
   server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
   # 设置服务端提供服务的端口号
   server_socket.bind(('', 80))
   # 使用socket创建的套接字默认的属性是主动的，使用listen将其改为被动，用来监听连接
   server_socket.listen(128) #最多可以监听128个连接
   # 开启while循环处理访问过来的请求 
   while True:
      # 如果有新的客户端来链接服务端，那么就产生一个新的套接字专门为这个客户端服务
      # client_socket用来为这个客户端服务
      # server_socket就可以省下来专门等待其他新的客户端连接while True:
      client_socket, clientAddr = server_socket.accept()
      handle_client(client_socket)

if __name__ == "__main__":
   main()
