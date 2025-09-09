# views_auth.py

from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import logout as django_logout, get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings

User = get_user_model()

def _cookie_opts(max_age: int):
    return {
        "httponly": True,
        "secure": settings.SESSION_COOKIE_SECURE,
        "samesite": settings.SESSION_COOKIE_SAMESITE,
        "path": "/",
        "max_age": max_age,
    }

# ---------- SERIALIZERS ----------
# All user Details in Access Token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """LOGIN: include nested `user` in access token."""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        try:
            bu_qs = getattr(user, "business_unit").all()
            bu_ids   = list(bu_qs.values_list("id", flat=True))
            bu_names = list(bu_qs.values_list("business_unit_name", flat=True))
            bu_obj = {"ids": bu_ids, "names": bu_names} if bu_ids else None
        except Exception:
            bu_obj = None
        role = getattr(user, "role", None)
        token["user"] = {
            "id": str(user.pk),
            "email": user.email or "",
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "roles": [role] if role else [],
            "business_unit": bu_obj,
        }
        return token


class MinimalTokenRefreshSerializer(TokenRefreshSerializer):
    """
    REFRESH: build a *minimal* ACCESS from user_id; verify user exists.
    If rotating, also mint a minimal REFRESH.
    """
    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])
        # Extract and verify user_id from refresh payload
        try:
            user_id = refresh[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise TokenError("Invalid refresh token: missing user id")

        try:
            user = User.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except User.DoesNotExist:
            raise TokenError("User not found")

        access = AccessToken.for_user(user)
        data = {"access": str(access)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except Exception:
                    pass
            new_refresh = MinimalRefreshToken.for_user(user)
            data["refresh"] = str(new_refresh)

        return data

# ---------- VIEWS ----------
# Selected User detials in Refresh Token
class MinimalRefreshToken(RefreshToken):
    """Custom refresh token with only essential claims."""
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        # Ensure only minimal claims are present
        # Remove any additional claims that might have been added
        allowed_claims = {
            'token_type', 'exp', 'iat', 'jti', 
            api_settings.USER_ID_CLAIM
        }
        # Filter out any extra claims
        for key in list(token.payload.keys()):
            if key not in allowed_claims:
                del token.payload[key]
        return token

# Saved data to cookies upon login
class CookieTokenObtainPairView(TokenObtainPairView):
    """POST {email, password} → JSON(access w/ user), Set-Cookie(refresh)."""
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        access  = str(serializer.validated_data["access"])
        refresh = str(MinimalRefreshToken.for_user(serializer.user))

        resp = JsonResponse({"access": access}, status=status.HTTP_200_OK)
        resp["Cache-Control"] = "no-store"
        resp["Pragma"] = "no-cache"

        refresh_max_age = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
        resp.set_cookie("refresh", refresh, **_cookie_opts(refresh_max_age))

        resp.set_cookie(
            settings.CSRF_COOKIE_NAME,
            get_token(request),
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE,
            path="/",
        )
        return resp

# request access token via request
class CookieTokenRefreshView(TokenRefreshView):
    """
    GET/POST (empty body)
    - Reads 'refresh' from HttpOnly cookie
    - Verifies user exists
    - Returns minimal 'access' in JSON
    - If rotate, sets NEW minimal 'refresh' cookie
    """
    permission_classes = [AllowAny]
    serializer_class = MinimalTokenRefreshSerializer
    http_method_names = ["get", "post", "head", "options"]  # allow GET

    def _refresh_from_cookie(self, request):
        refresh_token = request.COOKIES.get("refresh")
        if not refresh_token:
            return Response({"detail": "No refresh cookie."}, status=401)

        serializer = self.get_serializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # Convert to SimpleJWT InvalidToken → 401
            raise InvalidToken(e.args[0])

        access = str(serializer.validated_data["access"])
        resp = JsonResponse({"message": "Refreshed", "access": access}, status=200)
        resp["Cache-Control"] = "no-store"
        resp["Pragma"] = "no-cache"

        # Rotate cookie if provided
        if "refresh" in serializer.validated_data:
            new_refresh = str(serializer.validated_data["refresh"])
            refresh_max_age = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
            resp.set_cookie("refresh", new_refresh, **_cookie_opts(refresh_max_age))

        # Optional: refresh CSRF cookie
        resp.set_cookie(
            settings.CSRF_COOKIE_NAME,
            get_token(request),
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE,
            path="/",
        )
        return resp

    def get(self, request, *args, **kwargs):
        return self._refresh_from_cookie(request)

    def post(self, request, *args, **kwargs):
        return self._refresh_from_cookie(request)

#clear access token upon logout
class CookieLogoutView(APIView):
    """POST — clears cookies and (optionally) blacklists the refresh token."""
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh")
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except Exception:
                pass
        django_logout(request)
        resp = JsonResponse({"message": "Logged out"})
        for name in ("refresh", settings.CSRF_COOKIE_NAME):
            resp.delete_cookie(name, path="/")
        return resp
