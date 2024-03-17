import googlemaps 
import pandas as pd
import geocoder

def get_current_location():
        # Use the default geolocation provider
        location = geocoder.ip('me')

        # Extract latitude and longitude
        latitude = location.latlng[0]
        longitude = location.latlng[1]
        return {'lat': latitude, 'lng': longitude}

def ReturnNearestPlace(search):
    API_KEY = "GOOGLE_API_KEY"

    map_client = googlemaps.Client(API_KEY)

    location = get_current_location()  # Corrected: Call the function to get the location

    distance = 5000  # Meters, approximately 5 miles

    places = []

    response = map_client.places_nearby(
        location=location,
        keyword=search,
        radius=distance,
    )

    places.extend(response.get('results', []))

    df = pd.DataFrame(places)
    df["url"] = "https://www.google.com/maps/place/?q=place_id:"+ df["place_id"]

    sub_df = df[['name', 'url']].head(5)

    return sub_df

