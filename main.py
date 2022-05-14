import requests
import os
from PyQt5 import QtWidgets, uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        path = os.path.join(os.path.dirname(__file__), 'main.ui')
        uic.loadUi(path, self)
        # set title
        self.setWindowTitle('Input Answer')
        self.sss.clicked.connect(self.send)
        self.ipc.clicked.connect(self.ipcc)

    def ipcc(self):
        print(f'connect to {self.ip.text()}')
        self.statusbar.setStyleSheet('color: yellow')
        self.statusbar.showMessage('Connecting...')
        try:
            ip = self.ip.text()
            if ip == '':
                self.statusbar.setStyleSheet('color: yellow')
                self.statusbar.showMessage('Please enter IP', 5000)
            elif ip.startswith('custom:'):
                ipp = ip.split('custom:')[1]
                r = requests.get(ipp)
            elif ip.startswith('custom: '):
                ipp = ip.split('custom: ')[1]
                r = requests.get(ipp)
            elif ip.startswith('http://') and ip.endswith(':5555'):
                r = requests.get(ip)
            elif ip.endswith(':5555'):
                r = requests.get(f'http://{ip}')
            elif ip.startswith('http://'):
                r = requests.get(f'{ip}:5555')
            else:
                r = requests.get(f'http://{ip}:5555')

            if r.status_code == 200:
                print(f'{ip} is connect')
                self.statusbar.setStyleSheet('color: green')
                self.statusbar.showMessage('Connected', 5000)
            else:
                print(f'error connect')
                self.statusbar.setStyleSheet('color: red')
                self.statusbar.showMessage('Connecting Fail', 5000)
        except Exception as e:
            print(f'error connect {e}')
            self.statusbar.setStyleSheet('color: red')
            self.statusbar.showMessage(f'Connecting Fail: {str(e)}', 5000)

    def send(self):
        answer = self.answer.text()
        if answer == '':
            self.statusbar.setStyleSheet('color: yellow')
            self.statusbar.showMessage('Please enter answer', 5000)
        ip = self.ip.text()
        self.statusbar.setStyleSheet('color: yellow')
        self.statusbar.showMessage('Sending...')
        print(f'send {answer} to {ip}')
        if ip == '':
            self.statusbar.setStyleSheet('color: yellow')
            self.statusbar.showMessage('Please enter IP', 5000)
        elif ip.startswith('custom:'):
            ipp = ip.split('custom:')[1]
        elif ip.startswith('custom: '):
            ipp = ip.split('custom: ')[1]
        elif ip.startswith('http://') and ip.endswith(':5555'):
            ipp = ip
        elif ip.endswith(':5555'):
            ipp = f'http://{ip}'
        elif ip.startswith('http://'):
            ipp = f'{ip}:5555'
        else:
            ipp = f'http://{ip}:5555'
        try:
            print(f'connect to {ipp}')
            r = requests.post(f'{ipp}/answer', data={'answer': answer})
            if r.status_code == 200:
                # set status bar text
                self.statusbar.setStyleSheet('color: green')
                self.statusbar.showMessage('Correct', 5000)
            else:
                self.statusbar.setStyleSheet('color: red')
                self.statusbar.showMessage('Wrong', 5000)
        except Exception as e:
            self.statusbar.setStyleSheet('color: red')
            self.statusbar.showMessage(f'Connecting Fail: {str(e)}', 5000)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())