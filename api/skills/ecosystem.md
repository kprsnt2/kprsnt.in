# Multi-Agent Ecosystem configuration

## Overview
This skill guide describes the multi-agent ecosystem configuration behind the `/ecosystem` dashboard.

## Pipeline Architecture
The system relies on a parallel multi-agent AI pipeline consisting of **6 agents** working concurrently to generate the dashboard.

### 6 Agents in Parallel
Six AI agents operate concurrently. These agents can gather data, perform analyses, and structure the content simultaneously to save time and reduce latency.

### Orchestrator
Once the 6 parallel agents complete their tasks, an orchestrator agent aggregates the generated data and coordinates the next steps.

### Dashboard Generation
Finally, the pipeline dynamically generates the dashboard's HTML UI using the aggregated context and routes it to the `/ecosystem` live endpoint.

## Usage
This ecosystem is fully automated and runs as part of the core infrastructure to ensure the dashboard reflects the latest multi-agent insights.
