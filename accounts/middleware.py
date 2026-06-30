from django.conf import settings
from django.utils import translation


class LanguagePriorityMiddleware:
    """
    Language selection priority:
    1. Accept-Language Header
    2. Profile.language
    3. Default: tg
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = self._get_language(request)
        translation.activate(language)
        request.LANGUAGE_CODE = language
        response = self.get_response(request)
        translation.deactivate()
        return response

    def _get_language(self, request):
        # Priority 1: Accept-Language header
        accept_language = request.META.get("HTTP_ACCEPT_LANGUAGE")
        if accept_language:
            lang_code = accept_language.split(",")[0].split(";")[0].strip()[:2]
            if lang_code in dict(settings.LANGUAGES):
                return lang_code

        # Priority 2: Profile.language
        if request.user.is_authenticated:
            try:
                profile_language = request.user.profile.language
                if profile_language and profile_language in dict(settings.LANGUAGES):
                    return profile_language
            except (AttributeError, Exception):
                pass

        # Priority 3: Default language
        return settings.LANGUAGE_CODE
