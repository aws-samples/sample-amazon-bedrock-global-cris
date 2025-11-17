#!/usr/bin/env python3
"""
Simple Amazon Bedrock Global CRIS example using Converse API
Demonstrates basic usage of Claude Haiku 4.5 with Global CRIS
"""

import boto3

# Initialize Bedrock client for India region (Mumbai)
bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")

# Global CRIS model ID for Claude Haiku 4.5
MODEL_ID = "global.anthropic.claude-haiku-4-5-20251001-v1:0"

try:
    print("🚀 Invoking Claude Haiku 4.5 via Global CRIS...")

    # Use Converse API for simplified interaction
    response = bedrock.converse(
        messages=[
            {
                "role": "user",
                "content": [{"text": "Explain cloud computing in 2 sentences."}],
            }
        ],
        modelId=MODEL_ID,
    )

    # Extract and display response
    response_text = response["output"]["message"]["content"][0]["text"]
    print("Response:", response_text)

    # Display token usage information
    usage = response.get("usage", {})
    print("Tokens used:", usage)

    if usage:
        print(f"Input tokens: {usage.get('inputTokens', 'N/A')}")
        print(f"Output tokens: {usage.get('outputTokens', 'N/A')}")
        print(f"Total tokens: {usage.get('totalTokens', 'N/A')}")

    print("\n✅ Global CRIS request completed successfully!")
    print(
        "💡 Claude Haiku 4.5 offers near-frontier performance at lower cost and faster speeds"
    )

except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check your AWS credentials and region configuration.")
