#!/usr/bin/env python3
"""
Simple Amazon Bedrock Global CRIS streaming example using InvokeModelWithResponseStream API
Demonstrates basic streaming with Amazon Nova 2 Lite and Global CRIS

Author: Navule Pavan Kumar Rao
Date: January 13, 2026
"""

import boto3
import json
from botocore.exceptions import ClientError

# Initialize Bedrock client for India region (Mumbai)
bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")

# Global CRIS model ID for Amazon Nova 2 Lite
MODEL_ID = "global.amazon.nova-2-lite-v1:0"

# Single prompt
PROMPT = "Explain the benefits of serverless computing in 3 bullet points."

print("🌍 Amazon Bedrock Global CRIS InvokeModelWithResponseStream Demo")
print("🚀 Model: Amazon Nova 2 Lite (Global CRIS)")
print("📍 Source Region: ap-south-1 (India)")
print(f"📝 Prompt: {PROMPT}")
print("\n💬 Streaming Response:")
print("-" * 50)

try:
    # Format the request payload using the model's native structure
    native_request = {
        "inferenceConfig": {
            "max_new_tokens": 500,
            "temperature": 0.7,
        },
        "messages": [
            {
                "role": "user",
                "content": [{"text": PROMPT}],
            }
        ],
    }

    # Convert the native request to JSON
    request_body = json.dumps(native_request)

    # Invoke the model with streaming response
    streaming_response = bedrock.invoke_model_with_response_stream(
        modelId=MODEL_ID, body=request_body, contentType="application/json"
    )

    # Extract and print the response text in real-time
    complete_response = ""
    for event in streaming_response["body"]:
        chunk = json.loads(event["chunk"]["bytes"])
        if "contentBlockDelta" in chunk:
            text = chunk["contentBlockDelta"].get("delta", {}).get("text", "")
            print(text, end="", flush=True)
            complete_response += text

    print("\n" + "-" * 50)
    print("✅ InvokeModelWithResponseStream completed successfully!")
    print("🌐 Request automatically routed to optimal region via Global CRIS")
    print(
        "💡 Amazon Nova 2 Lite offers fast, cost-effective performance for everyday tasks"
    )
    print(f"📊 Response length: {len(complete_response)} characters")

except ClientError as e:
    print(f"❌ Error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
