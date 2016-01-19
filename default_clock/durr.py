
in_traffic_time = 0
in_traffic_normalized = min(in_traffic_time, 480)/480.0
traffic_color = (int(0+(255.0*in_traffic_normalized)), int(255-(255.0*in_traffic_normalized)), 0)
print traffic_color
