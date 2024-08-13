from django.conf import settings
from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignedCertSerializer
from .serives import SigningService
import io
import zipfile


class CaPemView(APIView):

    def get(self, request: Request) -> Response:
        with open(settings.CA_PEM_PATH) as f:
            return Response(
                data=f.read(),
                status=status.HTTP_200_OK,
                content_type='octet/stream'
            )


class SignedCertCreateView(APIView):

    signing_service = SigningService()
    serializer_class = SignedCertSerializer

    def post(self, request: Request) -> Response:

        serializer = SignedCertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        ca_password = data['ca_password']
        domain = data['domain']

        cert_pem, key_pem = self.signing_service.create_signed_cert_and_key(
            ca_password=ca_password,
            domain=domain
        )

        in_memory_zip = io.BytesIO()
        with zipfile.ZipFile(
            in_memory_zip, mode="w", compression=zipfile.ZIP_DEFLATED
        ) as zf:
            zf.writestr(f"{domain}.key", key_pem)
            zf.writestr(f"{domain}.crt", cert_pem)

        # Seek to the beginning of the BytesIO buffer
        in_memory_zip.seek(0)

        response = HttpResponse(in_memory_zip, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{data["domain"]}.zip"'

        return response
