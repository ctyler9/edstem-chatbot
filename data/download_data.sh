#!/bin/bash

# Fetch libarary: https://github.com/gruntwork-io/fetch
export GITHUB_OAUTH_TOKEN="your token"
fetch --repo="" --github-oauth-token=${GITHUB_OAUTH_TOKEN} --tag="thread-indexes" --release-asset="" . 
