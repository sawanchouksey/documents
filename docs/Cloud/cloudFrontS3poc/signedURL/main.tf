# Provider configuration
provider "aws" {
  region = "ap-south-1" # CloudFront requires ACM certificates in us-east-1
}

# Local variables
locals {
  website_files = {
    "index.html" = {
      content_type = "text/html"
      content      = <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Protected Static Website</title>
</head>
<body>
    <h1>Welcome to the Protected Website</h1>
    <p>This content is protected by CloudFront signed URLs.</p>
</body>
</html>
EOF
    }
    "error.html" = {
      content_type = "text/html"
      content      = <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Error Page</title>
</head>
<body>
    <h1>Error</h1>
    <p>Sorry, there was an error accessing the page.</p>
</body>
</html>
EOF
    }
  }
}

# S3 bucket for static website
resource "aws_s3_bucket" "website" {
  bucket = "sckm22071995"
}

# S3 bucket versioning
resource "aws_s3_bucket_versioning" "website" {
  bucket = aws_s3_bucket.website.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Block public access to S3 bucket
resource "aws_s3_bucket_public_access_block" "website" {
  bucket = aws_s3_bucket.website.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Upload static content to S3
resource "aws_s3_object" "website_files" {
  for_each = local.website_files

  bucket       = aws_s3_bucket.website.id
  key          = each.key
  content      = each.value.content
  content_type = each.value.content_type
  etag         = md5(each.value.content)
}

# S3 bucket policy for CloudFront access
resource "aws_s3_bucket_policy" "website" {
  bucket = aws_s3_bucket.website.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFrontServicePrincipal"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.website.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.website.arn
          }
        }
      }
    ]
  })
}

# CloudFront Origin Access Control
resource "aws_cloudfront_origin_access_control" "website" {
  name                              = "website-oac"
  description                       = "Website OAC"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# CloudFront key group for signed URLs
resource "aws_cloudfront_public_key" "website" {
  comment     = "Public key for signed URLs"
  encoded_key = file("${path.module}/public_key.pem") # You need to create this key pair
  name        = "website-public-key"
}

resource "aws_cloudfront_key_group" "website" {
  comment = "Key group for signed URLs"
  items   = [aws_cloudfront_public_key.website.id]
  name    = "website-key-group"
}

# CloudFront distribution
resource "aws_cloudfront_distribution" "website" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Static website distribution with signed URLs"
  default_root_object = "index.html"

  origin {
    domain_name              = aws_s3_bucket.website.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.website.id
    origin_id                = "S3Origin"
  }

  # Cache behavior with signed URLs
  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3Origin"
    viewer_protocol_policy = "redirect-to-https"

    # Enable signed URLs/cookies
    trusted_key_groups = [aws_cloudfront_key_group.website.id]

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    min_ttl     = 0
    default_ttl = 3600
    max_ttl     = 86400
    compress    = true
  }

  # Custom error response
  custom_error_response {
    error_code         = 403
    response_code      = 403
    response_page_path = "/error.html"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true # Use your own certificate in production
  }

  # Add tags
  tags = {
    Environment = "Production"
    Terraform   = "true"
  }
}

# CloudWatch Log Group for CloudFront logs
resource "aws_cloudwatch_log_group" "cloudfront_logs" {
  name              = "/aws/cloudfront/website"
  retention_in_days = 30
}

# Outputs
output "cloudfront_domain" {
  value = aws_cloudfront_distribution.website.domain_name
}

output "s3_bucket_name" {
  value = aws_s3_bucket.website.id
}

output "distribution_id" {
  value = aws_cloudfront_distribution.website.id
}

output "cloudfront_public_key_id" {
  value = aws_cloudfront_public_key.website.id
  description = "The ID of the CloudFront public key"
}

output "cloudfront_key_group_id" {
  value = aws_cloudfront_key_group.website.id
  description = "The ID of the CloudFront key group"
}

# Create a shell script to set environment variables
resource "local_file" "env_vars" {
  content = <<EOF
export CLOUDFRONT_DOMAIN=${aws_cloudfront_distribution.website.domain_name}
export CLOUDFRONT_PUBLIC_KEY_ID=${aws_cloudfront_public_key.website.id}
export CLOUDFRONT_DISTRIBUTION_ID=${aws_cloudfront_distribution.website.id}
export PRIVATE_KEY_PATH="private_key.pem"
EOF
  filename = "${path.module}/set_env.sh"
}