import warnings

from modules.MultiSocket import create_thread
import socket

warnings.filterwarnings(action="ignore")

if __name__ == '__main__':
    # TODO: 데이터 매니저와 프로세스 매니저 간에 공유할 큐 생성
    # TODO: 데이터 매니저 실행
    # TODO: 프로세스 매니저 실행
    # 소켓 연결 부분
    HOST, PORT = ('127.0.0.1', 8000)
    HOST_PORT = (HOST, PORT)
    clients_limit = 10

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    s.bind(HOST_PORT)
    print('Socket bind complete')
    s.listen(clients_limit)
    print('Socket now listening {} clients'.format(clients_limit))

    create_thread(s)




