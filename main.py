from website import create_app
from threading import Thread


app = create_app()
from website.consume_f import consume_feed


if __name__ == "__main__":
    consume_threadf = Thread(target=consume_feed, daemon=True)
    consume_threadf.start()
    app.run(debug=True, port=5555)