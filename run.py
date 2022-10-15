from app import app
from main import main
import threading


class FlaskThread(threading.Thread):
    def run(self):
        app.run()


class TelegramThread(threading.Thread):
    def run(self):
        main()


if __name__ == '__main__':

    flask_thread = FlaskThread()
    flask_thread.start()

    main()
