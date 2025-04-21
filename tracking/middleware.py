from django_user_agents.utils import get_user_agent
import geoip2.database
from django.contrib.gis.geos import Point
from tracking.models import Visitor

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.geoip_reader = geoip2.database.Reader('geoip/GeoLite2-City.mmdb')

    def __call__(self, request):
        # Get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        # Get user agent info
        user_agent = get_user_agent(request)

        # Get geolocation info
        try:
            geo_response = self.geoip_reader.city(ip)
            location = Point(geo_response.location.longitude, geo_response.location.latitude)
            city = geo_response.city.name
            country = geo_response.country.name
        except Exception:
            location, city, country = None, None, None

        # Save visitor data
        Visitor.objects.create(
            ip_address=ip,
            location=location,
            city=city,
            country=country,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            os=user_agent.os.family,
            browser=user_agent.browser.family,
            device=user_agent.device.family
        )

        response = self.get_response(request)
        return response