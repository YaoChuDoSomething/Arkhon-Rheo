# Getting Started

Welcome to Arkhon-Rheo! This guide will walk you through the first steps of building your own multi-agent system.

## Installation

Arkhon-Rheo requires Python 3.12 or higher. We recommend using `uv` for package management.

```bash
pip install arkhon-rheo
```

## Your First Project

Use the CLI to scaffold a new project structure:

```bash
arkhon-rheo init hello-arkhon
```

This creates a directory structure like this:

```text
hello-arkhon/
├── agents/        # Put your custom agent logic here
├── tools/         # Define external tools
└── pyproject.toml # Project configuration
```

## Basic Concepts

### 1. The Agent

In Arkhon-Rheo, an Agent is a stateful entity that can receive messages, reason, and act.

### 2. The Orchestrator

The Orchestrator manages the flow of execution between multiple agents, handling message passing and state transitions.

### 3. Tooling

Give your agents specialized capabilities by registering Tools!

## Next Steps

Explore the [Architecture](architecture.md) or see a complete [Multi-Agent Example](examples/multi_agent.md).
