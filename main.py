from app.bot.main import run_bot, client
from app.web.main import run_web
from dotenv import load_dotenv
from threading import Thread


def main():
    load_dotenv()

    thread = Thread(target=run_bot)
    # thread.start()

    try:
        run_web()
    except KeyboardInterrupt:
        client.close()
        thread.stop()


if __name__ == "__main__":
    main()
