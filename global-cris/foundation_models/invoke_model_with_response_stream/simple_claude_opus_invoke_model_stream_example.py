#!/usr/bin/env python3
"""
Simple Amazon Bedrock Global CRIS example using Invoke Model with Response Stream API
Demonstrates streaming usage of Claude Opus 4.5 with Global CRIS

Author: Navule Pavan Kumar Rao
Date: November 25, 2025
"""

import json
import boto3

# Initialize Bedrock client for India region (Mumbai)
bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")

# Global CRIS model ID for Claude Opus 4.5
MODEL_ID = "global.anthropic.claude-opus-4-5-20251101-v1:0"

try:
    print("🚀 Invoking Claude Opus 4.5 via Global CRIS (Streaming)...")

    # Prepare request body
    request_body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "Explain cloud computing in 2 sentences."
            }
        ]
    })

    # Invoke model with streaming
    response = bedrock.invoke_model_with_response_stream(
        modelId=MODEL_ID,
        body=request_body
    )

    # Process streaming response
    print("Response: ", end="", flush=True)
    for event in response["body"]:
        chunk = json.loads(event["chunk"]["bytes"])
        if chunk["type"] == "content_block_delta":
            if "delta" in chunk and "text" in chunk["delta"]:
                print(chunk["delta"]["text"], end="", flush=True)

    print("\n\n✅ Global CRIS streaming request completed successfully!")
    print(
        "💡 Claude Opus 4.5 offers frontier-level intelligence for complex tasks"
    )

except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check your AWS credentials and region configuration.")
