"""
Tiny live-reload dev server for static site.

Usage: python3 serve.py [port]
Default port: 5173
"""
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5173

def main():
    try:
        from livereload import Server, shell
    except Exception:
        print("Installing livereload…")
        os.system(f"{sys.executable} -m pip install --quiet livereload")
        from livereload import Server, shell  # type: ignore

    server = Server()
    watch_patterns = [
        'index.html', 'styles.css',
        'pages/*.html', 'assets/icons/*',
    ]
    for pat in watch_patterns:
        server.watch(pat)
    print(f"Serving on http://localhost:{PORT}")
    server.serve(port=PORT, host='0.0.0.0', root='.')

if __name__ == '__main__':
    main()

