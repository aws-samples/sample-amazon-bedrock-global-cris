#!/usr/bin/env python3
"""
Simple Amazon Bedrock Global CRIS example using Cohere Embed v4
Demonstrates basic text embedding with Global CRIS
"""
import json

import boto3
from botocore.exceptions import ClientError

bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")

# Global CRIS model ID for Cohere Embed v4
MODEL_ID = "global.cohere.embed-v4:0"

# Single text to embed
TEXT = "Explain the benefits of serverless computing."

try:
    # Format the request payload using Cohere Embed v4 structure
    request_body = {
        "texts": [TEXT],
        "input_type": "search_document",
        "embedding_types": ["float"],
        "output_dimension": 1024,  # Using 1024 dimensions for efficiency
    }

    # Convert the request to JSON
    request_json = json.dumps(request_body)

    # Invoke the model with the request
    response = bedrock.invoke_model(
        modelId=MODEL_ID, body=request_json, contentType="application/json"
    )

    # Extract response metadata
    response_metadata = response.get("ResponseMetadata", {})
    http_headers = response_metadata.get("HTTPHeaders", {})

    # Decode the response body
    model_response = json.loads(response["body"].read())

    # Extract embeddings and display results
    embeddings = model_response.get("embeddings", [])
    response_texts = model_response.get("texts", [])

    # Extract token usage from HTTP headers (Bedrock metadata)
    input_tokens = int(http_headers.get("x-amzn-bedrock-input-token-count", 0))

    # Handle different response formats
    if isinstance(embeddings, dict):
        # Multiple embedding types requested
        for embed_type, embed_list in embeddings.items():
            embedding = embed_list[0]  # Get first (and only) embedding
            print(f"   Dimensions: {len(embedding)}")
            print(f"   Data type: {type(embedding[0]).__name__}")
            print(f"   Sample values (first 5): {embedding[:5]}")

    # Display token usage metrics
    print("\n📊 Token Usage:")
    print(f"   Input tokens: {input_tokens}")
    print("   Note: Embedding models only consume input tokens")

except ClientError as e:
    print(f"❌ Error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
