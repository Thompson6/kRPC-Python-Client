import json
import krpc

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

flight_info = vessel.flight()


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
# Functions to access variables from external script
# ------------------------------------------------------------------------------------------------

def abort_mission():
    vessel.control.abort = True


# while True:
#     print("--- Current Flight Parameters ---")
#     print(f"Speed: {speed()}")
#     print(f"Surface Altitude: {surface_altitude()}")
#     print(f"Heading: {heading()}")
#     print(f"Pitch: {pitch()}")
#     print(f"Bedrock Altitude: {bedrock_altitude()}")
#     print(f"Latitude: {latitude()}")
#     print(f"Longitude: {longitude()}")
#     print(f"Vertical Speed: {vertical_speed()}")
#     print(f"G Force: {g_force()}")
#     print(f"Elevation: {elevation()}")
#     print(f"Direction: {direction()}")
#     print(f"Roll: {roll()}")
#     print(f"Atmosphere Density: {atmosphere_density()}")
#     print(f"Static Pressure: {static_pressure()}")
#     print(f"Lift: {lift()}")
#     print(f"Rotation: {rotation()}")
#     print(f"Prograde Direction: {prograde()}")
#     print(f"Retrograde Direction: {retrograde()}")
#     print(f"Normal Direction: {normal()}")
#     print(f"Anti-Normal Direction: {anti_normal()}")
#     print(f"Radial Direction: {radial()}")
#     print(f"Anti-Radial Direction: {anti_radial()}")
#     print(f"Total Air Temperature: {total_air_temperature()}")
#     print(f"Static Air Temperature: {static_air_temperature()}")
#     time.sleep(0.1)
