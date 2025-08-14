import geopandas as gpd
import pandas as pd

"""
This is a quick reference to how you can  convert data from one geometry to the other,
leveraging an overlay intersection and a weighted sum. 

In this case, we'd have a value at grid level (e.g., temperature) and want to convert to a census unit (e.g., LPA for the UK) 

We assume both gdf_grid and gdf_census already have area calculated. Be aware of using the correct CRS
"""

# 1. Find overlays between grid and census regions
overlay = gpd.overlay(
    gdf_grid, gdf_census, how='intersection')

# 2. Calculate area of each intersected polygon
overlay['intersect_area'] = overlay.geometry.area

# 3. Calculate intersection fraction for each grid cell in region
overlay['weight'] = overlay['intersect_area'] / overlay['grid_area']

# 4. Weighted value for this overlap part
overlay['weighted_value'] = overlay['temperature_grid'] * overlay['weight']

# 6. Sum weighted values per census region
# 'region_id_col' comes from the census dataframe (e.g., overlay['census_id'])
agg = overlay.groupby(region_id_col)['weighted_value'].sum().reset_index()

# Merge back to census regions, if desired
gdf_census_with_values = gdf_census.merge(agg, on=region_id_col, how='left')

print(gdf_census_with_values[[region_id_col, 'weighted_value']])
 
