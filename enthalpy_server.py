# Run a Python3 server

# === Description ===
# https://en.wikipedia.org/wiki/Enthalpy
# Enthalpy Calculation via minimal webserver http://0.0.0.0:8080/ alis http://localhost:8080/
# useful to establish e.g. in summer, when change the air
# return json "a", "b" and "diff" as difference of enthaply (a-b) per volume unit (J/mc) (J/m^3) 
# Usage example between outdoor and indoor air:
# http://0.0.0.0:8080/28 30 0 25 80 0
# {"a": 53593, "b": 76176, "diff": -22583, "unit": "J/mc"}
# look at enthalpy_core.py for parameters description
# Author: vespadj 2021-2022

# Calculation by CoolProp library
# http://www.coolprop.org/fluid_properties/HumidAir.html#haprops-sample
# Authors: Ian H. Bell and the CoolProp Team

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

import sys
import subprocess
import time
import logging
import json
import urllib.parse


hostName = "localhost"
serverPort = 8080

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('enthalpy-server')


def process(values):
    cmd = "python2 enthalpy_core.py " + values

    logger.info("Enthalpy. Ready to launch: %s", cmd)

    # https://www.golinuxcloud.com/python-subprocess/
    # Use shell to execute the command
    sp = subprocess.Popen(cmd,
        shell = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        universal_newlines = True)

    # Separate output and error.
    # This is similar to Tuple where we store two values to two different variables
    out, err = sp.communicate()
    # Store the return code in rc variable
    rc = sp.wait()

    # print('output is: \n', out)

    if rc != 0: print('Return Code:',rc,'\n') # --> 0
    if err: print('error is: \n', err)

    tmp = out.split('\n')[0].split(' ')
    logger.info("Enthalpy. a,b,diff: %s", str(tmp))

    return tmp


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json") # text/plain
        self.end_headers()

        out = process(urllib.parse.unquote( self.path[1:] ))
        res = {}
        res['a'] = int(out[0])
        res['b'] = int(out[1])
        res['diff'] = int(out[2])
        res['unit'] = out[3]
    
        self.wfile.write(bytes(json.dumps(res), "utf-8"))


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

