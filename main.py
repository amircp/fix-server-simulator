import socket
import threading

class FIXServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
    def start(self):
        print('Starting FIX server...')
        print('FIX server started. Listening for connections...')

        thread = threading.Thread(target=self.handle_client)
        thread.start()

    def handle_client(self):
        print('Listening for connections...')
        self.server.listen()
        client, address = self.server.accept()
        print(f'Accepted connection from {address}')

        while True:
            message = client.recv(1024).decode('utf-8')

            if not message:
                print('Client disconnected')
                client.close()
                break

            print(f'Received message: {message}')
            response = self.process_message(message)
            if response:
                client.send(response.encode('utf-8'))
                print('Response sent.')
            print("No response sent")

        self.handle_client()
    def process_message(self, message):
        print('Processing message...')
        fields = message.split("\x01")
        msg_dict = dict(field.split('=') for field in fields if field)

        msg_type = msg_dict.get('35')

        msg_types = {
            "D": self.process_new_order,
            "F": self.process_cancel_request,
            "8": self.process_execution_report,
            "A": self.process_logon,
            "5": self.process_logout
        }

        if msg_type not in msg_types:
            print(f"Unknown message type {msg_type}")
            return

        return msg_types[msg_type](msg_dict)

    def process_logon(self, message):
        print('Processing LOGON message...')
        username = message.get('553')
        password = message.get('554')
        print(f"LOGON request from user {username} with password {password}")
        return 'FIX.4.4\x019=102\x0135=A\x0134=1\x0149=CSERVER\x0150=TRADE\x0152=20230804-19:55:05.903\x0156=demo.icmarkets.0000000\x0157=TRADE\x0198=0\x01108=30\x0110=191\x01'
    def process_logout(self, message):
        print('Processing LOGOUT message...')
        # Add any necessary processing here

    def process_new_order(self, msg_dict):
        print('Processing new order...')
        # TODO: Process new order single message

    def process_cancel_request(self, msg_dict):
        print('Processing cancel request...')
        # TODO: Process order cancel request message

    def process_execution_report(self, msg_dict):
        print('Processing execution report...')
        # TODO: Process execution report message

    def calculate_checksum(message):
        # Ensure message is bytes
        if isinstance(message, str):
            message = message.encode('utf-8')

        checksum = sum(message) % 256
        return "{:03}".format(checksum)

    def __del__(self):
        if self.server:
            self.server.close()

fix_server = FIXServer('localhost', 5202)
fix_server.start()

fix_server_qt = FIXServer('localhost', 5201)
fix_server_qt.start()
