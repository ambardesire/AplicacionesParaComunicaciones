from amlrpc.server import SimpleaMLRPCServer
from amlrpc.server import SimpleaMLRPCRequestHandler


class RequestHandler(SimpleaMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
with SimpleaMLRPCServer(('localhost', 8000),logRequests=True, requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    class MyFuncs:
        def add(self, a, b):
            return a + b

        def sub(self, a, b):
            return a - b

        def mult(self, a, b):
            return a * b

        def div(self, a, b):
            return a / b

        def show_tbpe(self, arg):
            return (str(arg), str(tbpe(arg)), arg)

    server.register_instance(MyFuncs())

    server.serve_forever()