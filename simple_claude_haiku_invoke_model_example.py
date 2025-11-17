#!/usr/bin/env python3
"""
Simple Amazon Bedrock Global CRIS example using InvokeModel API
Demonstrates basic usage of Claude Haiku 4.5 with Global CRIS
"""

import json

import boto3
from botocore.exceptions import ClientError

# Initialize Bedrock client for India region (Mumbai)
bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")

# Global CRIS model ID for Claude Haiku 4.5
MODEL_ID = "global.anthropic.claude-haiku-4-5-20251001-v1:0"

# Single prompt
PROMPT = "Explain the benefits of serverless computing in 3 bullet points."

print("🌍 Amazon Bedrock Global CRIS InvokeModel Demo")
print("🚀 Model: Claude Haiku 4.5 (Global CRIS)")
print("📍 Source Region: ap-south-1 (India)")
print(f"📝 Prompt: {PROMPT}")
print("\n💬 Response:")
print("-" * 50)

try:
    # Format the request payload using the model's native structure
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "temperature": 0.7,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": PROMPT}],
            }
        ],
    }

    # Convert the native request to JSON
    request_body = json.dumps(native_request)

    # Invoke the model with the request
    response = bedrock.invoke_model(
        modelId=MODEL_ID, body=request_body, contentType="application/json"
    )

    # Decode the response body
    model_response = json.loads(response["body"].read())

    # Extract and print the response text
    response_text = model_response["content"][0]["text"]
    print(response_text)

    print("\n" + "-" * 50)
    print("✅ InvokeModel completed successfully!")
    print("🌐 Request automatically routed to optimal region via Global CRIS")
    print(
        "💡 Claude Haiku 4.5 offers near-frontier performance at lower cost and faster speeds"
    )

    # Display token usage if available
    if "usage" in model_response:
        usage = model_response["usage"]
        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)
        total_tokens = input_tokens + output_tokens
        print("🔢 Token Usage:")
        print(f"   Input tokens: {input_tokens}")
        print(f"   Output tokens: {output_tokens}")
        print(f"   Total tokens: {total_tokens}")

except ClientError as e:
    print(f"❌ Error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
