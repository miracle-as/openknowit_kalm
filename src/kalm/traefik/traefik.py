from flask import Flask, jsonify
import socket


def is_port_in_use(host,port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
        except socket.error:
            return True
        else:
            return False
        
def get_next_free_port(host, port):
    checkport = 4000
    found = False
    while not found:
      if not is_port_in_use(host, checkport):
         return checkport
      else:
         checkport = checkport + 1
         if checkport > 65535:
            return False


        
def list_traefik():
  print("list traefik")
app = Flask(__name__)


@app.route('/traefik/config', methods=['GET'])
def get_traefik_config():
    # Here, you can write the code to fetch and process the Traefik configuration data
    config_data = {
        'sample_key': 'sample_value',
        'another_key': 'another_value'
    }
    return jsonify(config_data)


def serve_traefik(config="/etc/kalm/traefik.json", host="0.0.0.0", port="free"):
  if port == "free":
     port  = get_next_free_port(host, port)
  print(port)


  print("config: %s" % (config))
  app.run(debug=True)
