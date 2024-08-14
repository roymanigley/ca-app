from django.views.generic import FormView
from django import forms
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from core.services import SigningService
import io
import zipfile
from django.core.exceptions import FieldError
from django.conf import settings
from OpenSSL import crypto


class SignedCertForm(forms.Form):
    domain = forms.CharField()
    ca_password = forms.CharField(
        widget=forms.PasswordInput(), label='Password'
    )


def get_ca(request: HttpRequest) -> HttpResponse:
    with open(settings.CA_PEM_PATH) as f:
        response = HttpResponse(
            f.read(),
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = 'attachment; filename="CA.crt"'
        return response


class SignedCertView(FormView):

    template_name = 'sign-cert.html'
    form_class = SignedCertForm
    success_url = '/'

    signing_service = SigningService()

    def form_valid(self, form: SignedCertForm) -> HttpResponse:
        ca_password = form.cleaned_data['ca_password']
        domain = form.cleaned_data['domain']

        try:
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
            in_memory_zip.seek(0)

            response = HttpResponse(
                in_memory_zip, content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{domain}.zip"'

            return response
        except crypto.Error as e:
            print(e)
            form.add_error(None, FieldError('invalid password'))
        except Exception as e:
            print(e)
            form.add_error(None, e)
        return self.form_invalid(form)
