from rest_framework.views import exception_handler
from rest_framework import status

def custom_exception_handler(exc, context):
    # Appelle d'abord le gestionnaire par défaut de DRF pour obtenir la réponse standard
    response = exception_handler(exc, context)

    # Si l'exception concerne une limite de quota / throttling atteint
    if response is not None and response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        # On extrait le temps d'attente s'il est fourni par DRF
        wait = getattr(exc, 'wait', None)
        
        # On structure un JSON propre et prévisible pour le Front
        response.data = {
            "error_code": "QUOTA_LIMIT_EXCEEDED",
            "message": "Vous avez dépassé votre limite de requêtes. Veuillez patienter.",
            "wait_seconds": wait
        }

    return response