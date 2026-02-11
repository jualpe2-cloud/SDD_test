import gpxpy
import gpxpy.gpx

class GPXService:
    @staticmethod
    def decode_polyline(polyline):
        # Decode a Google Maps encoded polyline. This is a basic implementation.
        import polyline as polyline_lib
        return polyline_lib.decode(polyline)

    @staticmethod
    def create_gpx_from_route(route_data):
        # Create GPX data from the provided Strava route data.
        gpx = gpxpy.gpx.GPX()
        # Assuming route_data contains a list of points with lat/lon
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        for point in route_data:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point['lat'], point['lon']))
        return gpx.to_xml()  # Return GPX in XML format

    @staticmethod
    def get_gpx_filename(route_name):
        return f'{route_name}.gpx'