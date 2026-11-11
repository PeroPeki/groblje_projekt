class NoIndexMiddleware:
    """Svakom odgovoru dodaje zaglavlje koje tražilicama brani indeksiranje (odluka 5).

    Vrijedi i za grobove s uključenim javnim prikazom: „javno” znači da se
    stranica otvara bez lozinke, a ne da se smije pojaviti u tražilici.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Robots-Tag"] = "noindex, nofollow"
        return response
