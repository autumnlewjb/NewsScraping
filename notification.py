from notify_run import Notify


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
        if self._total_news and self._directory:
            self._generate_message()
            self.service.send(self.message)
        else:
            print('Something goes wrong')
