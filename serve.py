"""
Tiny live-reload dev server for static site.

Usage: python3 serve.py [port]
Default port: 5173 (auto-fallback if busy)
"""
import os
import sys
import socket
import threading
import time
import webbrowser

DEFAULT_PORT = 5173
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT


def get_lan_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def find_open_port(start: int, limit: int = 20) -> int:
    for p in range(start, start + limit):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", p))
                return p
            except OSError:
                continue
    return start  # fallback


def main():
    try:
        from livereload import Server  # type: ignore
    except Exception:
        print("Installing livereload…")
        os.system(f"{sys.executable} -m pip install --quiet livereload")
        from livereload import Server  # type: ignore

    port = find_open_port(PORT)
    server = Server()
    watch_patterns = [
        "index.html",
        "styles.css",
        "pages/*.html",
        "assets/icons/*",
        "assets/img/*",
    ]
    for pat in watch_patterns:
        server.watch(pat)

    lan_ip = get_lan_ip()
    url = f"http://localhost:{port}"
    lan_url = f"http://{lan_ip}:{port}"

    def _open_browser():
        time.sleep(0.8)
        try:
            webbrowser.open(url)
        except Exception:
            pass

    threading.Thread(target=_open_browser, daemon=True).start()

    print("\nLocal preview ready:")
    print(f"  • Browser: {url}")
    print(f"  • Same Wi‑Fi (phone/tablet): {lan_url}")
    print("Press Ctrl+C to stop. Live reload is enabled.\n")

    server.serve(port=port, host="0.0.0.0", root=".")


if __name__ == "__main__":
    main()
