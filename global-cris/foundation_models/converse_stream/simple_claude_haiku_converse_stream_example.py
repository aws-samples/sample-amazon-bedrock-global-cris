#!/usr/bin/env python3
"""
Simple Amazon Bedrock Global CRIS streaming example using ConverseStream API
Demonstrates basic streaming with Claude Haiku 4.5 and usage metrics

Author: Navule Pavan Kumar Rao
Date: November 20, 2025
"""

import boto3
from botocore.exceptions import ClientError

# Initialize Bedrock client for India region (Mumbai)
bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")

# Global CRIS model ID for Claude Haiku 4.5
MODEL_ID = "global.anthropic.claude-haiku-4-5-20251001-v1:0"

# Single prompt
PROMPT = "Explain the benefits of serverless computing in 3 bullet points."

print("🌍 Amazon Bedrock Global CRIS Streaming Demo")
print("🚀 Model: Claude Haiku 4.5 (Global CRIS)")
print("📍 Source Region: ap-south-1 (India)")
print(f"📝 Prompt: {PROMPT}")
print("\n💬 Streaming Response:")
print("-" * 50)

try:
    # Create conversation with single user message
    conversation = [{"role": "user", "content": [{"text": PROMPT}]}]

    # Stream response using ConverseStream API
    streaming_response = bedrock.converse_stream(
        modelId=MODEL_ID,
        messages=conversation,
        inferenceConfig={"maxTokens": 500, "temperature": 0.7},
    )

    # Process and display streaming response in real-time
    usage_info = None
    for chunk in streaming_response["stream"]:
        if "contentBlockDelta" in chunk:
            text = chunk["contentBlockDelta"]["delta"]["text"]
            print(text, end="", flush=True)
        elif "metadata" in chunk:
            # Capture usage information from metadata event
            usage_info = chunk["metadata"].get("usage")

    print("\n" + "-" * 50)
    print("✅ Streaming completed successfully!")
    print("🌐 Request automatically routed to optimal region via Global CRIS")
    print(
        "💡 Claude Haiku 4.5 offers near-frontier performance at lower cost and faster speeds"
    )

    # Display token usage if available
    if usage_info:
        print("🔢 Token Usage:")
        print(f"   Input tokens: {usage_info.get('inputTokens', 'N/A')}")
        print(f"   Output tokens: {usage_info.get('outputTokens', 'N/A')}")
        print(f"   Total tokens: {usage_info.get('totalTokens', 'N/A')}")
        if usage_info.get("cacheReadInputTokens", 0) > 0:
            print(f"   Cache read tokens: {usage_info.get('cacheReadInputTokens')}")
        if usage_info.get("cacheWriteInputTokens", 0) > 0:
            print(f"   Cache write tokens: {usage_info.get('cacheWriteInputTokens')}")

except ClientError as e:
    print(f"❌ Error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
