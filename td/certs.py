import random
from OpenSSL import SSL
from OpenSSL import crypto
from td.defaults import StatePath

cert_state = StatePath()

if not cert_state.does_directory_exist(file_path='certs_file'):
    
    cert_state.define_settings_location(location_id='certs_folder', location='td/certs_file')
    cert_state.settings_location['certs_folder'].mkdir(exist_ok=True)

###############
# CA Cert #
###############

ca_key = crypto.PKey()
ca_key.generate_key(crypto.TYPE_RSA, 2048)

ca_cert = crypto.X509()
ca_cert.set_version(2)
ca_cert.set_serial_number(random.randint(50000000,100000000))

ca_subj = ca_cert.get_subject()
ca_subj.commonName = "My CA"

ca_cert.add_extensions([
    crypto.X509Extension("subjectKeyIdentifier", False, "hash", subject=ca_cert),
    crypto.X509Extension("authorityKeyIdentifier", False, "keyid:always", issuer=ca_cert),
    crypto.X509Extension("basicConstraints", False, "CA:TRUE"),
    crypto.X509Extension("keyUsage", False, "keyCertSign, cRLSign"),
])

ca_cert.set_issuer(ca_subj)
ca_cert.set_pubkey(ca_key)

ca_cert.gmtime_adj_notBefore(0)
ca_cert.gmtime_adj_notAfter(10*365*24*60*60)

ca_cert.sign(ca_key, 'sha256')

# Save certificate
with open("certs_file/ca.crt", "wt") as f:
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, ca_cert))

# Save private key
with open("certs_file/ca.key", "wt") as f:
    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, ca_key))

###############
# Client Cert #
###############

client_key = crypto.PKey()
client_key.generate_key(crypto.TYPE_RSA, 2048)

client_cert = crypto.X509()
client_cert.set_version(2)
client_cert.set_serial_number(random.randint(50000000,100000000))

client_subj = client_cert.get_subject()
client_subj.commonName = "Client"

client_cert.add_extensions([
    crypto.X509Extension("basicConstraints", False, "CA:FALSE"),
    crypto.X509Extension("subjectKeyIdentifier", False, "hash", subject=client_cert),
    crypto.X509Extension("authorityKeyIdentifier", False, "keyid:always", issuer=ca_cert),
    crypto.X509Extension("extendedKeyUsage", False, "clientAuth"),
    crypto.X509Extension("keyUsage", False, "digitalSignature"),
])

client_cert.set_issuer(ca_subj)
client_cert.set_pubkey(client_key)

client_cert.gmtime_adj_notBefore(0)
client_cert.gmtime_adj_notAfter(10*365*24*60*60)

client_cert.sign(ca_key, 'sha256')

# Save certificate
with open("certs_file/client.crt", "wt") as f:
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, client_cert))

# Save private key
with open("certs_file/client.key", "wt") as f:
    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, client_key))


# def cert_gen(
#     emailAddress="",
#     commonName="commonName",
#     countryName="NT",
#     localityName="localityName",
#     stateOrProvinceName="stateOrProvinceName",
#     organizationName="organizationName",
#     organizationUnitName="organizationUnitName",
#     serialNumber=0,
#     validityStartInSeconds=0,
#     validityEndInSeconds=10*365*24*60*60,
#     KEY_FILE = "private.key",
#     CERT_FILE="selfsigned.crt"):
#     #can look at generated file using openssl:
#     #openssl x509 -inform pem -in selfsigned.crt -noout -text
#     # create a key pair
#     k = crypto.PKey()
#     k.generate_key(crypto.TYPE_RSA, 4096)
#     # create a self-signed cert
#     cert = crypto.X509()
#     cert.get_subject().C = countryName
#     cert.get_subject().ST = stateOrProvinceName
#     cert.get_subject().L = localityName
#     cert.get_subject().O = organizationName
#     cert.get_subject().OU = organizationUnitName
#     cert.get_subject().CN = commonName
#     cert.get_subject().emailAddress = emailAddress
#     cert.set_serial_number(serialNumber)
#     cert.gmtime_adj_notBefore(0)
#     cert.gmtime_adj_notAfter(validityEndInSeconds)
#     cert.set_issuer(cert.get_subject())
#     cert.set_pubkey(k)
#     cert.sign(k, 'sha512')
#     with open(CERT_FILE, "wt") as f:
#         f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
#     with open(KEY_FILE, "wt") as f:
#         f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))

# cert_gen()

