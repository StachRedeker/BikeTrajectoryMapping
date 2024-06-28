##############
# Plot a trajectory on a map, given lat and lon inputs
##############

import pandas as pd
import folium

def plot_trajectory(csv_file):
    # Load data from CSV
    data = pd.read_csv(csv_file, usecols=['latitude', 'longitude'])
    
    # Drop rows where latitude or longitude are missing
    data.dropna(subset=['latitude', 'longitude'], inplace=True)
    
    # Create a map object centered around the first point
    if not data.empty:
        start_location = [data.iloc[0]['latitude'], data.iloc[0]['longitude']]
        map = folium.Map(location=start_location, zoom_start=12)
        
        # Add points to the map
        folium.PolyLine(data.values, color="red", weight=2.5, opacity=1).add_to(map)
        
        # Add markers for the start and end points
        folium.Marker(start_location, popup='Start').add_to(map)
        folium.Marker([data.iloc[-1]['latitude'], data.iloc[-1]['longitude']], popup='End').add_to(map)
        
        # Save map
        map.save('trajectory.html')
        print("Map has been saved to 'trajectory.html'")
    else:
        print("No valid data to plot.")


plot_trajectory('73_location_data_round1.csv')

