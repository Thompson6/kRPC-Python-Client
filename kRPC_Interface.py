import krpc
import json

# ------------------------------------------------------------------------------------------------
# Load configuration from a JSON file so I don't leak sensitive information. Again.
# ------------------------------------------------------------------------------------------------

with open("config.json", "r") as f:
    config = json.load(f)
    
CONNECTION_NAME = config['connection_name']
ADDRESS = config['address']

# This exists because I really don't want to write these ports in the JSON
if not config['ports']:
    PORTS = [50000, 50001]
else:
    PORTS = config['ports']


# ------------------------------------------------------------------------------------------------
# Establish variables for connection
# ------------------------------------------------------------------------------------------------

conn = krpc.connect(name=CONNECTION_NAME, address=ADDRESS, rpc_port=PORTS[0], stream_port=PORTS[1])

vessel = conn.space_center.active_vessel

flight_info = vessel.flight()

altitude = conn.add_stream(getattr, flight_info, 'mean_altitude')


# ------------------------------------------------------------------------------------------------
# Functions to access variables from external script
# ------------------------------------------------------------------------------------------------

def get_altitude():
    return altitude()