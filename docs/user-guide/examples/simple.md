# Simple Agent Example

A minimal demonstration of creating and running a single Arkhon-Rheo Agent.

## Overview

This example shows how to subclass the `Agent` base class and implement the `process_message` method.

## Code Walkthrough

```python
class SimpleMathAgent(Agent):
    async def process_message(self, message: AgentMessage) -> str:
        # Custom logic goes here
        return f"Echoing back: {message.content}"
```

## Running the Example

```bash
uv run examples/simple_agent/main.py
```
