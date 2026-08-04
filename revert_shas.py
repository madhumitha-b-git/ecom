import glob

files = glob.glob('.github/workflows/*-service.yml')

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # Revert to stable, standard version tags
    content = content.replace("actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683", "actions/checkout@v4")
    content = content.replace("actions/setup-python@39cd14951b4efaa2628f74851955d96c4340d2b9", "actions/setup-python@v5")
    content = content.replace("aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d44e03b00a1", "aws-actions/configure-aws-credentials@v4")
    content = content.replace("sonarsource/sonarcloud-github-action@cb2521193779e908f50ad794ec3a40b4b896ecb4", "sonarsource/sonarcloud-github-action@v3.0.0")
    
    with open(file, 'w') as f:
        f.write(content)

print("Reverted SHAs to stable tags in all workflows.")
