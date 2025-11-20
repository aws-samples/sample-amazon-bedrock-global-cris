# Sample Amazon Bedrock Global cross-Region inference

Amazon Bedrock Global CRIS examples using Claude and Cohere models.

## Global cross-Region inference

Global cross-Region inference extends cross-Region inference beyond geographic boundaries, enabling the routing of inference requests to supported commercial AWS Regions worldwide, optimizing available resources and enabling higher model throughput.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run Examples

```bash
python simple_claude_haiku_converse_example.py
python simple_claude_sonnet_converse_example.py
python simple_cohere_embed_example.py
```


## Benefits of global cross-Region inference

Global cross-Region inference for Anthropic's Claude Sonnet 4.5 delivers multiple advantages over traditional geographic cross-Region inference profiles:

- **Enhanced throughput during peak demand** – Global cross-Region inference provides improved resilience during periods of peak demand by automatically routing requests to AWS Regions with available capacity. This dynamic routing happens seamlessly without additional configuration or intervention from developers. Unlike traditional approaches that might require complex client-side load balancing between AWS Regions, global cross-Region inference handles traffic spikes automatically. This is particularly important for business-critical applications where downtime or degraded performance can have significant financial or reputational impacts.
- **Cost-efficiency** – Global cross-Region inference for Anthropic's Claude Sonnet 4.5 offers approximately 10% savings on both input and output token pricing compared to geographic cross-Region inference. The price is calculated based on the AWS Region from which the request is made (source AWS Region). This means organizations can benefit from improved resilience with even lower costs. This pricing model makes global cross-Region inference a cost-effective solution for organizations looking to optimize their generative AI deployments. By improving resource utilization and enabling higher throughput without additional costs, it helps organizations maximize the value of their investment in Amazon Bedrock.
- **Streamlined monitoring** – When using global cross-Region inference, CloudWatch and CloudTrail continue to record log entries in your source AWS Region, simplifying observability and management. Even though your requests are processed across different AWS Regions worldwide, you maintain a centralized view of your application's performance and usage patterns through your familiar AWS monitoring tools.
- **On-demand quota flexibility** – With global cross-Region inference, your workloads are no longer limited by individual Regional capacity. Instead of being restricted to the capacity available in a specific AWS Region, your requests can be dynamically routed across the AWS global infrastructure. This provides access to a much larger pool of resources, making it less complicated to handle high-volume workloads and sudden traffic spikes.

## References

- [Global cross-Region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/global-cross-region-inference.html)
- [Increase throughput with cross-Region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html#cross-region-inference-comparison)
- [Amazon Bedrock now supports Global Cross-Region inference for Anthropic Claude Sonnet 4](https://aws.amazon.com/about-aws/whats-new/2025/09/amazon-bedrock-global-cross-region-inference-anthropic-claude-sonnet-4/)

## Security

See [CONTRIBUTING](CONTRIBUTING.md) for more information.

## Responsible AI

Implement safeguards customized to your application requirements and responsible AI policies using [Amazon Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/)

## Disclaimer

The sample code; software libraries; command line tools; proofs of concept; templates; or other related technology (including any of the foregoing that are provided by our personnel) is provided to you as AWS Content under the AWS Customer Agreement, or the relevant written agreement between you and AWS (whichever applies).  You are responsible for testing, securing, and optimizing the AWS Content, such as sample code, as appropriate for production grade use based on your specific quality control practices and standards.  You should not use this AWS Content in your production accounts, or on production or other critical data. Deploying AWS Content may incur AWS charges for creating or using AWS chargeable resources, such as running Amazon EC2 instances or using Amazon S3 storage.
