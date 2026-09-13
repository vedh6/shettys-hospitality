import os, re, sys, functools, http.server, socketserver

root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs"))
os.chdir(root)


class RangeHandler(http.server.SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler with HTTP Range support.

    Without it a browser cannot seek within a video: currentTime snaps back to
    zero. GitHub Pages serves ranges, so testing locally without this gives a
    false negative.
    """

    def send_head(self):
        rng = self.headers.get("Range")
        if not rng:
            return super().send_head()

        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        try:
            f = open(path, "rb")
        except OSError:
            self.send_error(404, "File not found")
            return None

        size = os.fstat(f.fileno()).st_size
        m = re.match(r"bytes=(\d*)-(\d*)", rng.strip())
        if not m:
            f.close()
            self.send_error(400, "Malformed Range header")
            return None

        start_s, end_s = m.group(1), m.group(2)
        if start_s:
            start = int(start_s)
            end = int(end_s) if end_s else size - 1
        else:                                  # suffix form: bytes=-500
            start = max(0, size - int(end_s))
            end = size - 1
        end = min(end, size - 1)

        if start > end or start >= size:
            f.close()
            self.send_response(416)
            self.send_header("Content-Range", "bytes */%d" % size)
            self.end_headers()
            return None

        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        f.seek(start)
        return _Slice(f, end - start + 1)

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        super().end_headers()


class _Slice:
    """Reads at most `remaining` bytes from an open file, then reports EOF."""

    def __init__(self, f, remaining):
        self.f, self.remaining = f, remaining

    def read(self, n=-1):
        if self.remaining <= 0:
            return b""
        if n is None or n < 0 or n > self.remaining:
            n = self.remaining
        chunk = self.f.read(n)
        self.remaining -= len(chunk)
        return chunk

    def close(self):
        self.f.close()


class Server(socketserver.ThreadingTCPServer):
    # Threaded: a single-threaded server stalls every other request while a
    # browser streams a video, which looks exactly like the site hanging.
    allow_reuse_address = True
    daemon_threads = True


with Server(("127.0.0.1", 4321), functools.partial(RangeHandler, directory=root)) as httpd:
    print("serving", root, "on http://localhost:4321")
    sys.stdout.flush()
    httpd.serve_forever()
