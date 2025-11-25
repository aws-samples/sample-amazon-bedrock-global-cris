#!/usr/bin/env python3
"""
Simple Amazon Bedrock Global CRIS example using Converse Stream API
Demonstrates streaming usage of Claude Opus 4.5 with Global CRIS

Author: Navule Pavan Kumar Rao
Date: November 25, 2025
"""

import boto3

# Initialize Bedrock client for India region (Mumbai)
bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")

# Global CRIS model ID for Claude Opus 4.5
MODEL_ID = "global.anthropic.claude-opus-4-5-20251101-v1:0"

try:
    print("🚀 Invoking Claude Opus 4.5 via Global CRIS (Streaming)...")

    # Use Converse Stream API for real-time streaming
    response = bedrock.converse_stream(
        messages=[
            {
                "role": "user",
                "content": [{"text": "Explain cloud computing in 2 sentences."}],
            }
        ],
        modelId=MODEL_ID,
    )

    # Process streaming response
    print("Response: ", end="", flush=True)
    for event in response["stream"]:
        if "contentBlockDelta" in event:
            delta = event["contentBlockDelta"]["delta"]
            if "text" in delta:
                print(delta["text"], end="", flush=True)

    print("\n\n✅ Global CRIS streaming request completed successfully!")
    print(
        "💡 Claude Opus 4.5 offers frontier-level intelligence for complex tasks"
    )

except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check your AWS credentials and region configuration.")
