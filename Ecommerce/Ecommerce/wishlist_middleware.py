from django.utils.deprecation import MiddlewareMixin

class WishlistMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:  # Initialize only for logged-in users
            if 'wishlist' not in request.session:
                request.session['wishlist'] = {}
                request.session['wishlist_count'] = 0