from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime, ipaddress

# CHANGE THIS TO YOUR IP
IP = "192.168.10.213"

key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "NA"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "NA"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Local Inventory System"),
    x509.NameAttribute(NameOID.COMMON_NAME, IP),
])

cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
    .add_extension(
        x509.SubjectAlternativeName([x509.IPAddress(ipaddress.IPv4Address(IP))]),
        critical=False,
    )
    .sign(key, hashes.SHA256())
)

# Write files
with open("cert.pem", "wb") as f:
    f.write(
        cert.public_bytes(serialization.Encoding.PEM)
        + key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        )
    )

print("Certificate generated: cert.pem")

