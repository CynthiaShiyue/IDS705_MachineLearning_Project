import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

wildfire_data_url = "https://incidents.fire.ca.gov/imapdata/mapdataall.csv"
zip_url = "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ca_california_zip_codes_geo.min.json"


def get_wildfires_with_zipcodes(df=None):
    if df is None:
        df = pd.read_csv(wildfire_data_url)
        print(f"Loaded {len(df)} rows from CAL FIRE")

    # Filter wildfires
    df = df[df['incident_type'].str.lower() == 'wildfire'].copy()
    print(f"Filtered only wildfires: {len(df)}")

    # Convert to GeoDataFrame
    geometry = [Point(xy) for xy in zip(df['incident_longitude'], df['incident_latitude'])]
    geo_df = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    # Load ZIP code polygons 
    zip_gdf = gpd.read_file(zip_url).to_crs(geo_df.crs)

    # Spatial join
    joined = gpd.sjoin(geo_df, zip_gdf, how="left", predicate='within')
    joined['zipcode'] = joined['ZCTA5CE10'] if 'ZCTA5CE10' in joined else joined['ZIPCODE']

    # Final result
    result_df = joined[['incident_name', 'incident_latitude', 'incident_longitude', 'zipcode']]

    missing_zip = len(result_df[result_df['zipcode'].isna()])
    missing_ratio =  missing_zip / len(result_df)
    print(f"Missing ZIPs: {missing_ratio:.2%}, missing {missing_zip} rows out of {len(result_df)} rows")

    return result_df