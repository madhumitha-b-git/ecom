import os
import glob

# Search for all service workflows
files = glob.glob('.github/workflows/*-service.yml')

# Action SHAs to pin
CHECKOUT_SHA = "actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683" # v4.2.2
SETUP_PYTHON_SHA = "actions/setup-python@39cd14951b4efaa2628f74851955d96c4340d2b9" # v5.1.1
CONFIGURE_AWS_SHA = "aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d44e03b00a1" # v4.0.2
SONARCLOUD_SHA = "sonarsource/sonarcloud-github-action@cb2521193779e908f50ad794ec3a40b4b896ecb4" # v3.0.0

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # 1. Pin Action SHAs
    content = content.replace("uses: actions/checkout@v4", f"uses: {CHECKOUT_SHA}")
    content = content.replace("uses: actions/setup-python@v5", f"uses: {SETUP_PYTHON_SHA}")
    content = content.replace("uses: aws-actions/configure-aws-credentials@v4", f"uses: {CONFIGURE_AWS_SHA}")
    content = content.replace("uses: sonarsource/sonarcloud-github-action@master", f"uses: {SONARCLOUD_SHA}")

    # 2. Lock versions & add --only-binary :all: for pip installs
    content = content.replace("pip install flake8", "pip install flake8==7.0.0 --only-binary :all:")
    content = content.replace("pip install pytest boto3 fastapi", "pip install pytest==8.0.0 boto3==1.34.50 fastapi==0.110.0 --only-binary :all:")
    content = content.replace("pip install boto3", "pip install boto3==1.34.50 --only-binary :all:")
    
    # 3. Add --ignore-scripts to npm install snyk
    content = content.replace("npm install -g snyk", "npm install -g snyk --ignore-scripts")
    
    with open(file, 'w') as f:
        f.write(content)

print("SonarCloud warnings fixed in all service workflows!")
