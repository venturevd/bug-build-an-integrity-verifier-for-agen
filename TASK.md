# Task: Bug: Build an integrity verifier for agent da — The accuracy KPI shows as 'verified' eve

**Category:** tool

## Description

QA tester found a bug in 'Build an integrity verifier for agent dashboards to prevent misleading KPIs':

**Bug:** The accuracy KPI shows as 'verified' even when there's a 4.1% difference, which seems too lenient (5% threshold)

**Artifact:** https://github.com/venturevd/agent-dashboard-integrity-verifier
**Tester verdict:** partial

Fix the bug and verify the tool works correctly.

## Existing Artifacts (reuse if relevant)

  - **agent-tool-spec** (stdlib only)
    A minimal, framework-agnostic specification for agent tooling primitives.
  - **agent_dashboard_integrity_verifier** [has tests] deps: pandas, numpy, requests
    This tool cross-checks agent KPIs against raw telemetry, ensures data provenance, detects metric drift, and generates auditable reports to prevent misleading dashboards.
  - **agent_representation_broker** deps: flask, requests
    The Agent Representation Broker is a service that matches agents with tasks based on their capabilities and requirements. It provides a centralized platform for agent coordination and task management.
  - **bug-build-an-integrity-verifier-for-agen** (stdlib only)
    This directory contains the fixed version of the Agent Dashboard Integrity Verifier tool. The bug was related to 'nan' values appearing in the rolling mean and standard deviation calculations when the
  - **build-an-agent-representation-broker-to-match-agen** [has tests] deps: flask, requests
    The Agent Representation Broker is a service that matches agents with tasks based on their capabilities and requirements. It provides a centralized platform for agent coordination and task management.
  - **build-an-integration-gap-validator-for-a** [has tests] deps: This project does not require any additional dependencies beyond the standard library.
    This tool automatically assesses, tests, and reports which tool integrations in an agent's stack are underperforming or failing. It helps agent builders identify and fix bottleneck integrations.
  - **create-a-survival-guide-for-new-agents-t** deps: This project does not require any additional dependencies beyond the standard library.
    Welcome to the digital economy! As a new agent, you'll encounter many opportunities, but also potential pitfalls. This guide helps you navigate the landscape, avoid predatory setups, and find legitima
  - **detect-diagnose-subtle-logic-drift-in-ag** deps: Flask==3.0.0, numpy>=1.20.0, scipy>=1.6.0
    A tool to detect and diagnose subtle logic drift in agent workflows.
  - **drift-detection-monitor** [has tests] deps: Flask==3.0.0, numpy>=1.20.0, scipy>=1.6.0
    A tool to detect subtle, gradual changes in AI model behavior before they cause errors.
  - **orchestrate-tool-x-tool-y-when-x-requires-a-databa** (stdlib only)
  - **test-artifact** (stdlib only)
    This is a test artifact for the GitHub publishing pipeline.
  - **tool-selector** [has tests] (stdlib only)
    Helps agents pick the best-fit tool for a given task without drowning in options.
  - **tool_discovery** (stdlib only)
    A Python tool to help agents discover and select the best tools for a given task.
