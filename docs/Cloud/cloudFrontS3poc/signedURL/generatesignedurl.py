import boto3
from botocore.signers import CloudFrontSigner
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import datetime

def get_signed_url(distribution_domain, private_key_path, key_pair_id, object_path):
    # Read private key
    with open(private_key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    # Create CloudFront signer
    signer = CloudFrontSigner(key_pair_id, lambda msg: private_key.sign(
        msg,
        padding.PKCS1v15(),
        hashes.SHA1()  # or use hashes.SHA256() if preferred
    ))

    # Generate signed URL
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    url = f'https://{distribution_domain}/{object_path}'

    signed_url = signer.generate_presigned_url(
        url,
        date_less_than=expiration
    )

    return signed_url

# Usage example
if __name__ == "__main__":
    signed_url = get_signed_url(
        'd3kwqs9im43wi7.cloudfront.net',
        'private_key.pem',  # Ensure this path is correct
        'K1ULF8DCY44SB',
        'index.html'
    )
    print(f"Signed URL: {signed_url}")
