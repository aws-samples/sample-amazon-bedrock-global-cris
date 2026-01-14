"""
Utility functions for Amazon Bedrock Global CRIS examples.

Author: Navule Pavan Kumar Rao
Date: January 13, 2026
"""

import json

from botocore.exceptions import ClientError

# Bedrock service principal for bucket policy
BEDROCK_PRINCIPAL = "bedrock.amazonaws.com"
BEDROCK_POLICY_SID = "AllowBedrockAccess"


def ensure_bedrock_bucket_access(s3_client, bucket: str, account_id: str) -> None:
    """
    Ensure Bedrock has read access to the S3 bucket.
    
    Checks if the bucket policy already grants Bedrock access.
    If not, adds the necessary policy statement.
    
    Args:
        s3_client: Boto3 S3 client
        bucket: S3 bucket name
        account_id: AWS account ID for the condition
    """
    bedrock_statement = {
        "Sid": BEDROCK_POLICY_SID,
        "Effect": "Allow",
        "Principal": {"Service": BEDROCK_PRINCIPAL},
        "Action": ["s3:GetObject"],
        "Resource": f"arn:aws:s3:::{bucket}/*",
        "Condition": {"StringEquals": {"aws:SourceAccount": account_id}},
    }

    try:
        # Get existing bucket policy
        response = s3_client.get_bucket_policy(Bucket=bucket)
        policy = json.loads(response["Policy"])

        # Check if Bedrock statement already exists
        for stmt in policy.get("Statement", []):
            if stmt.get("Sid") == BEDROCK_POLICY_SID:
                print("🔐 Bedrock access already configured in bucket policy")
                return

        # Add Bedrock statement to existing policy
        policy["Statement"].append(bedrock_statement)

    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucketPolicy":
            # Create new policy with Bedrock statement
            policy = {"Version": "2012-10-17", "Statement": [bedrock_statement]}
        else:
            raise

    # Apply the updated policy
    s3_client.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy))
    print("🔐 Added Bedrock access to bucket policy")
