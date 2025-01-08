import webbrowser
import time

# List of URLs to open
urls = [
    "http://10.10.30.93:9102/aws_thrifty.benchmark.secretsmanager",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.s3",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.route53",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.redshift",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.rds",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.network",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.emr",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.elasticache",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.eks",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.ecs",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.ec2",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.ebs",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.dynamodb",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.cost_explorer",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.cloudwatch",
    "http://10.10.30.93:9102/aws_thrifty.benchmark.cloudfront",
    "http://10.10.30.93:9102/aws_top_10.benchmark.account_security",
    "http://10.10.30.93:9102/aws_well_architected.benchmark.well_architected_framework",
    "http://10.10.30.93:9102/aws_compliance.benchmark.foundational_security?where=%2B%22operator%22%3A%22and%22%2C%22expressions%22%3A%5B%2B%22operator%22%3A%22equal%22%2C%22value%22%3A%22aws_compliance.benchmark.foundational_security%22%2C%22type%22%3A%22benchmark%22%2C%22title%22%3A%22AWS+Foundational+Security+Best+Practices%22%2D%5D%2D",
    "http://10.10.30.93:9102/aws_compliance.benchmark.all_controls"
]

# Open each URL in the default web browser with a delay
for url in urls:
    webbrowser.open(url)
    time.sleep(2)  # Wait 2 seconds before opening the next URL
