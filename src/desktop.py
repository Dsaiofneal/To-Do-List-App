import threading

import webview

from app import create_app


def run_flask():
    app = create_app()
    # Use a fixed port to avoid connection issues
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()

    # Give the server a moment to start
    webview.create_window("Tasking", "http://127.0.0.1:5000", width=1100, height=750)
    webview.start()
