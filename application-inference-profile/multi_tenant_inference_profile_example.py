#!/usr/bin/env python3
"""
Multi-Tenant Application Inference Profile Example
Demonstrates creating and using tenant-specific inference profiles for SaaS applications

Author: Navule Pavan Kumar Rao
Date: November 20, 2025
"""

import boto3
import json
from botocore.exceptions import ClientError

# Initialize Bedrock clients for India region (Mumbai)
bedrock = boto3.client('bedrock', region_name='ap-south-1')
bedrock_runtime = boto3.client('bedrock-runtime', region_name='ap-south-1')

# Base Global CRIS model ARN
base_model_arn = "arn:aws:bedrock:ap-south-1::inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0"

print("🏢 Multi-Tenant Application Inference Profile Demo")
print("=" * 70)

def create_tenant_inference_profile(tenant_id, tenant_name):
    """Create a dedicated application inference profile for a tenant"""
    profile_name = f"tenant_{tenant_id}_profile"
    
    print(f"\n📝 Creating application inference profile for {tenant_name} (ID: {tenant_id})...")
    
    # Create profile with tenant-specific tags
    tags = [
        {'key': 'tenant_id', 'value': tenant_id},
        {'key': 'tenant_name', 'value': tenant_name},
        {'key': 'application', 'value': 'saas-platform'}
    ]
    
    try:
        response = bedrock.create_inference_profile(
            inferenceProfileName=profile_name,
            description=f"Inference profile for tenant {tenant_name}",
            modelSource={'copyFrom': base_model_arn},
            tags=tags
        )
        
        profile_arn = response['inferenceProfileArn']
        print(f"   ✅ Application inference profile created: {profile_arn}")
        print(f"   📊 Status: {response['status']}")
        return profile_arn
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"   ⚠️  Application inference profile already exists, retrieving existing profile...")
            # List and find existing profile
            list_response = bedrock.list_inference_profiles()
            for profile in list_response.get('inferenceProfileSummaries', []):
                if profile['inferenceProfileName'] == profile_name:
                    print(f"   ✅ Found existing application inference profile: {profile['inferenceProfileArn']}")
                    return profile['inferenceProfileArn']
        raise

def invoke_model_for_tenant(tenant_profile_arn, tenant_name, user_message):
    """Invoke model with tenant-specific application inference profile for usage tracking"""
    print(f"\n💬 Invoking model for {tenant_name}...")
    print(f"   Query: {user_message}")
    
    response = bedrock_runtime.converse(
        modelId=tenant_profile_arn,  # Tenant-specific profile
        messages=[{
            "role": "user",
            "content": [{"text": user_message}]
        }],
        inferenceConfig={
            "maxTokens": 150,
            "temperature": 0.7
        }
    )
    
    # Usage is automatically tracked per tenant
    response_text = response['output']['message']['content'][0]['text']
    usage = response['usage']
    
    print(f"   ✅ Response: {response_text[:100]}...")
    print(f"   📊 Usage tracked under tenant application inference profile:")
    print(f"      Input tokens: {usage['inputTokens']}")
    print(f"      Output tokens: {usage['outputTokens']}")
    print(f"      Total tokens: {usage['totalTokens']}")
    
    return {
        'response': response_text,
        'tokens': usage['totalTokens'],
        'input_tokens': usage['inputTokens'],
        'output_tokens': usage['outputTokens']
    }

def cleanup_tenant_profile(tenant_profile_arn, tenant_name):
    """Delete tenant application inference profile"""
    print(f"\n🧹 Cleaning up application inference profile for {tenant_name}...")
    try:
        bedrock.delete_inference_profile(
            inferenceProfileIdentifier=tenant_profile_arn
        )
        print(f"   ✅ Application inference profile deleted successfully")
    except Exception as e:
        print(f"   ⚠️  Error deleting application inference profile: {e}")

# Main execution
try:
    # Simulate multi-tenant SaaS application
    tenants = [
        {"id": "tenant-001", "name": "Acme Corp"},
        {"id": "tenant-002", "name": "TechStart Inc"}
    ]
    
    tenant_profiles = {}
    tenant_usage = {}
    
    # Step 1: Create application inference profiles for each tenant
    print("\n" + "=" * 70)
    print("STEP 1: Creating Tenant-Specific Application Inference Profiles")
    print("=" * 70)
    
    for tenant in tenants:
        profile_arn = create_tenant_inference_profile(tenant["id"], tenant["name"])
        tenant_profiles[tenant["id"]] = profile_arn
    
    # Step 2: Simulate tenant requests
    print("\n" + "=" * 70)
    print("STEP 2: Processing Tenant Requests (Usage Tracked Separately)")
    print("=" * 70)
    
    # Tenant A makes a request
    result_a = invoke_model_for_tenant(
        tenant_profiles["tenant-001"],
        "Acme Corp",
        "What are the benefits of cloud computing?"
    )
    tenant_usage["tenant-001"] = result_a
    
    # Tenant B makes a request
    result_b = invoke_model_for_tenant(
        tenant_profiles["tenant-002"],
        "TechStart Inc",
        "Explain machine learning in simple terms."
    )
    tenant_usage["tenant-002"] = result_b
    
    # Tenant A makes another request
    result_a2 = invoke_model_for_tenant(
        tenant_profiles["tenant-001"],
        "Acme Corp",
        "How does serverless architecture work?"
    )
    # Accumulate usage for Tenant A
    tenant_usage["tenant-001"]["tokens"] += result_a2["tokens"]
    tenant_usage["tenant-001"]["input_tokens"] += result_a2["input_tokens"]
    tenant_usage["tenant-001"]["output_tokens"] += result_a2["output_tokens"]
    
    # Step 3: Display usage summary per tenant
    print("\n" + "=" * 70)
    print("STEP 3: Tenant Usage Summary (For Billing/Chargeback)")
    print("=" * 70)
    
    for tenant in tenants:
        tenant_id = tenant["id"]
        tenant_name = tenant["name"]
        usage = tenant_usage[tenant_id]
        
        print(f"\n📊 {tenant_name} ({tenant_id}):")
        print(f"   Total Input Tokens: {usage['input_tokens']}")
        print(f"   Total Output Tokens: {usage['output_tokens']}")
        print(f"   Total Tokens: {usage['tokens']}")
        print(f"   Profile ARN: {tenant_profiles[tenant_id]}")
    
    # Step 4: Cleanup (commented out for now)
    print("\n" + "=" * 70)
    print("STEP 4: Cleanup")
    print("=" * 70)
    
    for tenant in tenants:
        cleanup_tenant_profile(tenant_profiles[tenant["id"]], tenant["name"])
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ Multi-Tenant Demo Completed Successfully!")
    print("=" * 70)
    print("\n💡 Key Takeaways:")
    print("   • Each tenant has a dedicated application inference profile")
    print("   • Usage is tracked separately per tenant for cost allocation")
    print("   • Tags enable detailed cost tracking in AWS billing")
    print("   • Perfect for SaaS chargeback and usage analytics")
    print("   • Application inference profiles copy from system-defined profiles")
    print("   • All tenants benefit from Global CRIS routing")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
