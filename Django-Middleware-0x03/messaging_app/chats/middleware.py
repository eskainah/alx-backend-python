import logging
from datetime import datetime, time, timedelta
from django.http import HttpResponseForbidden
from collections import defaultdict
from django.http import HttpResponseForbidden, JsonResponse
from django.utils.deprecation import MiddlewareMixin

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define access window: from 6 PM (18:00) to 9 PM (21:00)
        current_time = datetime.now().time()
        start_time = time(18, 0)  # 6:00 PM
        end_time = time(21, 0)    # 9:00 PM

        # If current time is outside this window, deny access
        if not (start_time <= current_time <= end_time):
            return HttpResponseForbidden("Access to the messaging app is restricted to 6PM–9PM.")

        # Allow the request through
        return self.get_response(request)

# IP-based Rate Limiting Middleware (5 messages per minute)
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_log = defaultdict(list)  # { ip: [timestamp1, timestamp2, ...] }

    def __call__(self, request):
        if request.method == "POST" and "/messages" in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Remove timestamps older than 1 minute
            self.request_log[ip] = [
                ts for ts in self.request_log[ip]
                if now - ts < timedelta(minutes=1)
            ]

            if len(self.request_log[ip]) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded: max 5 messages per minute."},
                    status=429
                )

            self.request_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get("REMOTE_ADDR", "0.0.0.0")


# Role-Based Access Middleware (Only admin or moderator allowed)
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only protect specific URLs (e.g., admin-only routes)
        protected_paths = ["/api/messages/", "/api/conversations/"]

        if any(request.path.startswith(p) for p in protected_paths):
            user = request.user
            if user.is_authenticated:
                role = getattr(user, "role", None)  # Assuming `User` model has `role`
                if role not in ["admin", "moderator"]:
                    return HttpResponseForbidden("You do not have permission to access this resource.")
            else:
                return HttpResponseForbidden("Authentication required.")

        return self.get_response(request)
