from django.utils.deprecation import MiddlewareMixin

class AddCORSHeadersToMedia(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith('/media/'):  # Adjust the path if needed
            response['Access-Control-Allow-Origin'] = '*'  # Allow all origins
        return response