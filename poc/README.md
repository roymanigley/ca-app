# Generate root CA

## Generate the Private Key
> `openssl genrsa -des3 -out CA.key 2048`  


    Enter PEM pass phrase:
    Verifying - Enter PEM pass phrase:

## Generate Root Certificate
> `openssl req -x509 -new -nodes -key CA.key -sha256 -days 1825 -out CA.pem`  


    Enter pass phrase for CA.key:
    You are about to be asked to enter information that will be incorporated
    into your certificate request.
    What you are about to enter is what is called a Distinguished Name or a DN.
    There are quite a few fields but you can leave some blank
    For some fields there will be a default value,
    If you enter '.', the field will be left blank.
    -----
    Country Name (2 letter code) [AU]:CH
    State or Province Name (full name) [Some-State]:CH
    Locality Name (eg, city) []:Bern
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:ca.local
    Organizational Unit Name (eg, section) []:ca.local
    Common Name (e.g. server FQDN or YOUR name) []:ca.local
    Email Address []:

## Adding the Root Certificate to the client
> `sudo cp CA.pem /usr/local/share/ca-certificates/CA.crt && sudo update-ca-certificates`

# Create CA-Signed Certificate

### Generate the Private Key
> `openssl genrsa -out server.local.key 2048`

### Create the `CSR`
> `openssl req -new -key server.local.key -out server.local.csr`  


    You are about to be asked to enter information that will be incorporated
    into your certificate request.
    What you are about to enter is what is called a Distinguished Name or a DN.
    There are quite a few fields but you can leave some blank
    For some fields there will be a default value,
    If you enter '.', the field will be left blank.
    -----
    Country Name (2 letter code) [AU]:CH
    State or Province Name (full name) [Some-State]:CH
    Locality Name (eg, city) []:Bern
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:server.local
    Organizational Unit Name (eg, section) []:server.local
    Common Name (e.g. server FQDN or YOUR name) []:server.local
    Email Address []:

    Please enter the following 'extra' attributes
    to be sent with your certificate request
    A challenge password []:1234
    An optional company name []:

### Create an X509 V3 certificate extension config file, which is used to define the Subject Alternative Name (SAN) for the certificate
> create a configuration file called `server.local.ext`  


    authorityKeyIdentifier=keyid,issuer
    basicConstraints=CA:FALSE
    keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
    subjectAltName = @alt_names

    [alt_names]
    DNS.1 = server.local

### Create the certificate: using our CSR, the CA private key, the CA certificate, and the config file
> `openssl x509 -req -in server.local.csr -CA CA.pem -CAkey CA.key -CAcreateserial -out server.local.crt -days 825 -sha256 -extfile server.local.ext`  


    Certificate request self-signature ok
    subject=C = CH, ST = CH, L = Bern, O = server.local, OU = server.local, CN = server.local
    Enter pass phrase for CA.key:

### All in one script (Create CA-Signed Certificate)

```sh
#!/bin/sh

if [ "$#" -ne 1 ]
then
  echo "Usage: Must supply a domain"
  exit 1
fi

DOMAIN=$1

cd ~/certs

openssl genrsa -out $DOMAIN.key 2048
openssl req -new -key $DOMAIN.key -out $DOMAIN.csr

cat > $DOMAIN.ext << EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = $DOMAIN
EOF

openssl x509 -req -in $DOMAIN.csr -CA CA.pem -CAkey CA.key -CAcreateserial -out $DOMAIN.crt -days 825 -sha256 -extfile $DOMAIN.ext
```
