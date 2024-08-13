from django.conf import settings
from OpenSSL import crypto
import hashlib


class SigningService:

    def create_signed_cert_and_key(
            self, *, ca_password: str, domain: str
    ) -> tuple[bytes, bytes]:
        # Load the CA's private key
        with open(settings.CA_KEY_PATH, "rb") as ca_key_file_in:
            ca_key = crypto.load_privatekey(
                crypto.FILETYPE_PEM,
                ca_key_file_in.read(),
                passphrase=ca_password.encode()
            )

        # Load the CA's certificate
        with open(settings.CA_PEM_PATH, "rb") as ca_cert_file_in:
            ca_cert = crypto.load_certificate(
                crypto.FILETYPE_PEM, ca_cert_file_in.read())

        # Create a key pair for the new certificate
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        # Create a certificate request (CSR)
        req = crypto.X509Req()
        req.get_subject().C = settings.CA_COUNTRY
        req.get_subject().ST = settings.CA_STATE
        req.get_subject().L = settings.CA_LOCATION
        req.get_subject().O = settings.CA_ORGANISATION
        req.get_subject().OU = settings. CA_ORGANISATION_UNIT
        req.get_subject().CN = domain
        req.set_pubkey(key)
        req.sign(key, "sha256")

        # Create a self-signed certificate
        cert = crypto.X509()
        cert.set_serial_number(1001)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)  # Valid for 10 years
        cert.set_issuer(ca_cert.get_subject())
        cert.set_subject(req.get_subject())
        cert.set_pubkey(req.get_pubkey())
        cert.sign(ca_key, "sha256")

        # Serialize the private key and certificate to memory
        salted = hashlib.sha512(
            ca_password.encode('utf-8')
        ).hexdigest() + domain
        passphrase = hashlib.sha512(salted.encode('utf-8')).hexdigest()

        key_pem = crypto.dump_privatekey(
            crypto.FILETYPE_PEM, key, passphrase=passphrase.encode('utf-8')
        )
        cert_pem = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)

        return cert_pem, key_pem
