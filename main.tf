provider "aws" {
  region = "us-west-1"  # Replace with your desired AWS region, e.g., us-west-1
}

# Amazon S3 Bucket for Biometric Data Storage
resource "aws_s3_bucket" "biometric_bucket" {
  bucket = "hayden1104200301"  # Replace with your desired S3 bucket name

  versioning {
    enabled = true
  }
}

# Amazon Cognito User Pool
resource "aws_cognito_user_pool" "biometric_user_pool" {
  name = "biometric-user-pool"

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  schema {
    name     = "email"
    attribute_data_type = "String"
    mutable  = true
    required = true
  }

  schema {
    name     = "phone_number"
    attribute_data_type = "String"
    mutable  = true
  }

  mfa_configuration = "OFF"
}

# Amazon Cognito User Pool App Client
resource "aws_cognito_user_pool_client" "biometric_user_pool_client" {
  name = "biometric-user-pool-client"
  user_pool_id = aws_cognito_user_pool.biometric_user_pool.id

  callback_urls = ["http://localhost:5000/callback"]
  logout_urls   = ["http://localhost:5000/logout"]
}

# Outputs
output "s3_bucket_name" {
  value = aws_s3_bucket.biometric_bucket.id
}

output "cognito_user_pool_id" {
  value = aws_cognito_user_pool.biometric_user_pool.id
}

output "cognito_client_id" {
  value = aws_cognito_user_pool_client.biometric_user_pool_client.id
}
