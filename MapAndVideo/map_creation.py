import folium
import pandas as pd

# Create interactive map with Folium
def create_map(data, map_center):
    map = folium.Map(location=map_center, zoom_start=14)
    for index, row in data.iterrows():
        if 'frame_path' in row and pd.notnull(row['frame_path']):
            folium.Marker(
                location=(row['latitude'], row['longitude']),
                popup=folium.Popup(f'<img src="{row["frame_path"]}" width="320" height="240">', max_width=320),
                tooltip='Click for image'
            ).add_to(map)
    return map

