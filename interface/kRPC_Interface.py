import json
import krpc
import time

# ------------------------------------------------------------------------------------------------
# Load configuration from a JSON file so I don't leak sensitive information. Again.
# ------------------------------------------------------------------------------------------------

with open("config.json", "r") as f:
    config = json.load(f)

CONNECTION_NAME = config["connection_name"]
ADDRESS = config["address"]

# This exists because I really don't want to write these ports in the JSON
ports = config.get("ports")
if not ports:
    PORTS = [50000, 50001]
else:
    PORTS = ports


# ------------------------------------------------------------------------------------------------
# Establish variables for connection
# ------------------------------------------------------------------------------------------------

conn = krpc.connect(
    name=CONNECTION_NAME, address=ADDRESS, rpc_port=PORTS[0], stream_port=PORTS[1]
)

vessel = conn.space_center.active_vessel


#--------------------------------------------------------------------------------
#                               Flight Info Data
#--------------------------------------------------------------------------------

refframe = vessel.orbit.body.reference_frame

flight_info = vessel.flight()

altitude = conn.add_stream(getattr, flight_info, "mean_altitude")
speed = conn.add_stream(getattr, flight_info, "speed")
surface_altitude = conn.add_stream(getattr, flight_info, "surface_altitude")
heading = conn.add_stream(getattr, flight_info, "heading")
pitch = conn.add_stream(getattr, flight_info, "pitch")
bedrock_altitude = conn.add_stream(getattr, flight_info, "bedrock_altitude")
latitude = conn.add_stream(getattr, flight_info, "latitude")
longitude = conn.add_stream(getattr, flight_info, "longitude")
vertical_speed = conn.add_stream(getattr, flight_info, "vertical_speed")
g_force = conn.add_stream(getattr, flight_info, "g_force")
elevation = conn.add_stream(getattr, flight_info, "elevation")
direction = conn.add_stream(getattr, flight_info, "direction")
roll = conn.add_stream(getattr, flight_info, "roll")
atmosphere_density = conn.add_stream(getattr, flight_info, "atmosphere_density")
static_pressure = conn.add_stream(getattr, flight_info, "static_pressure")
lift = conn.add_stream(getattr, flight_info, "lift")

rotation = conn.add_stream(getattr, flight_info, "rotation")
prograde = conn.add_stream(getattr, flight_info, "prograde")
retrograde = conn.add_stream(getattr, flight_info, "retrograde")
normal = conn.add_stream(getattr, flight_info, "normal")
anti_normal = conn.add_stream(getattr, flight_info, "anti_normal")
radial = conn.add_stream(getattr, flight_info, "radial")
anti_radial = conn.add_stream(getattr, flight_info, "anti_radial")
total_air_temperature = conn.add_stream(getattr, flight_info, "total_air_temperature")
static_air_temperature = conn.add_stream(getattr, flight_info, "static_air_temperature")



# ------------------------------------------------------------------------------------------------
#                          Functions to work with action groups
# ------------------------------------------------------------------------------------------------

def abort_mission():
    vessel.control.abort = True

def toggle_gear():
    if vessel.control.gear:
        vessel.control.gear = False
    else:
        vessel.control.gear = True


# ------------------------------------------------------------------------------------------------
#                           References to individual vessel parts
# ------------------------------------------------------------------------------------------------

parts = vessel.parts