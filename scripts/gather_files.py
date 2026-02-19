import os

base_dir = "/wk2/yaochu/github/arkhon-rheo"
files_to_gather = [
    ".agent/scripts/git_context.py",
    "README.md",
    "examples/multi_agent_orchestration/main.py",
    "examples/simple_agent/main.py",
    "examples/raci_workflow/critic_workflow.py",
    "main.py",
    "mkdocs.yaml",
    "src/arkhon_rheo/agents/specialist.py",
    "src/arkhon_rheo/cli/main.py",
    "src/arkhon_rheo/core/agent.py",
    "src/arkhon_rheo/core/context.py",
    "src/arkhon_rheo/core/graph.py",
    "src/arkhon_rheo/core/rules/engine.py",
    "src/arkhon_rheo/core/rules/raci.py",
    "src/arkhon_rheo/core/runtime/scheduler.py",
    "src/arkhon_rheo/core/state.py",
    "src/arkhon_rheo/core/step.py",
    "src/arkhon_rheo/nodes/action_node.py",
    "src/arkhon_rheo/nodes/base.py",
    "src/arkhon_rheo/nodes/commit_node.py",
    "src/arkhon_rheo/nodes/observation_node.py",
    "src/arkhon_rheo/nodes/thought_node.py",
    "src/arkhon_rheo/nodes/validate_node.py",
    "src/arkhon_rheo/nodes/governance.py",
    "src/arkhon_rheo/tools/builtin/calculator.py",
    "src/arkhon_rheo/tools/builtin/file_ops.py",
    "tests/integration/test_agent_communication.py",
    "tests/integration/test_nested_subgraph.py",
    "tests/integration/test_react_cycle.py",
    "tests/unit/cli/test_main.py",
    "tests/unit/core/memory/test_context_window.py",
    "tests/unit/core/runtime/test_checkpoint.py",
    "tests/unit/core/test_agent.py",
    "tests/unit/core/test_graph.py",
    "tests/unit/nodes/test_action_node.py",
    "tests/unit/nodes/test_base.py",
    "tests/unit/nodes/test_thought_node.py",
    "tests/unit/nodes/test_utility_nodes.py",
    "tests/unit/tools/test_registry.py",
]

results = []
for f_path in files_to_gather:
    full_path = os.path.join(base_dir, f_path)
    if os.path.exists(full_path):
        with open(full_path) as f:
            content = f.read()
            results.append({"path": f_path, "content": content})

