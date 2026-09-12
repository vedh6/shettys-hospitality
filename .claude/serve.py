import os, sys, functools, http.server, socketserver
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
root = os.path.abspath(root)
os.chdir(root)
Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=root)
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", 4321), Handler) as httpd:
    print("serving", root, "on http://localhost:4321")
    sys.stdout.flush()
    httpd.serve_forever()
