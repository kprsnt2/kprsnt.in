# Wrapper script to run the job-application-agent (npm package)
# This uses npx to fetch and run the latest version of the agent locally.
# Ensure you have Node.js installed.

Write-Host "Starting job-application-agent via npx..." -ForegroundColor Cyan
npx job-application-agent
