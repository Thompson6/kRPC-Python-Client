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


s1e1 = vessel.parts.with_tag("s1e1")[0].engine
s1e2 = vessel.parts.with_tag("s1e2")[0].engine
s1e3 = vessel.parts.with_tag("s1e3")[0].engine
s1e4 = vessel.parts.with_tag("s1e4")[0].engine
s1e5 = vessel.parts.with_tag("s1e5")[0].engine
s1e6 = vessel.parts.with_tag("s1e6")[0].engine
s1e7 = vessel.parts.with_tag("s1e7")[0].engine

s1e1_stream = conn.add_stream(getattr, s1e1, 'active')
s1e2_stream = conn.add_stream(getattr, s1e2, 'active')
s1e3_stream = conn.add_stream(getattr, s1e3, 'active')
s1e4_stream = conn.add_stream(getattr, s1e4, 'active')
s1e5_stream = conn.add_stream(getattr, s1e5, 'active')
s1e6_stream = conn.add_stream(getattr, s1e6, 'active')
s1e7_stream = conn.add_stream(getattr, s1e7, 'active')

# ------------------------------------------------------------------------------------------------
#                          Functions to work with action groups
# ------------------------------------------------------------------------------------------------

def abort_mission():
    vessel.control.abort = True

def toggle_gear():
    vessel.control.gear = not vessel.control.gear


# ------------------------------------------------------------------------------------------------
#                              Functions to work with parts
# ------------------------------------------------------------------------------------------------

def toggle_engine(stage, engine_number):
    engine = vessel.parts.with_tag(f"s{stage}e{engine_number}")[0].engine
    engine.active = not engine.active
    return engine.active

def get_engine_status(stage, engine_number):
    engine = vessel.parts.with_tag(f"s{stage}e{engine_number}")[0].engine
    return engine.active