from notify_run import Notify
from setup import register_notify


class Notification:
    def __init__(self, directory=None):
        self.service = Notify()
        self.message = None
        self._total_news = 0
        self._directory = directory

    def _generate_message(self):
        template = 'Your news feed is ready.\nTotal news today: {total}\nSaved in:\n{direc}'
        self.message = template.format(total=self._total_news, direc=self._directory)

    def get_total_news(self, value):
        self._total_news += value

    def set_directory(self, value):
        self._directory = str(value)

    def send_note(self):
        try:
            with open('../resources/registered.txt', 'r') as input_file:
                status = int(input_file.read())
                print(status)
                if status != 1:
                    register_notify()

        except FileNotFoundError:
            register_notify()
        print(self._total_news, self._directory)
        if self._total_news and self._directory:
            self._generate_message()
            self.service.send(self.message)
        else:
            print('Something goes wrong')
