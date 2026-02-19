S603 `subprocess` call: check for execution of untrusted input
  --> tests/run_tools.py:8:9
   |
 6 |         # Using uvx to ensure tools are run in a clean environment if not installed
 7 |         cmd = ["uvx", *command]
 8 |         subprocess.run(cmd, capture_output=True, text=True, check=True)
   |         ^^^^^^^^^^^^^^
 9 |     except subprocess.CalledProcessError:
10 |         pass
   |

PLC0415 `import` should be at the top-level of a file
   --> tests/test_phase2_workflow_graphs.py:122:9
    |
121 |     def test_flow_2_1_is_compiled(self) -> None:
122 |         from langgraph.graph.state import CompiledStateGraph
    |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
123 |
124 |         assert isinstance(flow_2_1, CompiledStateGraph)
    |

PLC0415 `import` should be at the top-level of a file
   --> tests/test_phase2_workflow_graphs.py:127:9
    |
126 |     def test_flow_2_2_is_compiled(self) -> None:
127 |         from langgraph.graph.state import CompiledStateGraph
    |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
128 |
129 |         assert isinstance(flow_2_2, CompiledStateGraph)
    |

PLC0415 `import` should be at the top-level of a file
   --> tests/test_phase2_workflow_graphs.py:132:9
    |
131 |     def test_flow_2_3_is_compiled(self) -> None:
132 |         from langgraph.graph.state import CompiledStateGraph
    |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
133 |
134 |         assert isinstance(flow_2_3, CompiledStateGraph)
    |

PLC0415 `import` should be at the top-level of a file
   --> tests/test_phase2_workflow_graphs.py:165:9
    |
164 |     def test_flow_3_1_is_compiled(self) -> None:
165 |         from langgraph.graph.state import CompiledStateGraph
    |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
166 |
167 |         assert isinstance(flow_3_1, CompiledStateGraph)
    |

PLC0415 `import` should be at the top-level of a file
   --> tests/test_phase2_workflow_graphs.py:170:9
    |
169 |     def test_flow_3_2_is_compiled(self) -> None:
170 |         from langgraph.graph.state import CompiledStateGraph
    |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
171 |
172 |         assert isinstance(flow_3_2, CompiledStateGraph)
    |

PLC0415 `import` should be at the top-level of a file
   --> tests/test_phase2_workflow_graphs.py:175:9
    |
174 |     def test_flow_3_3_is_compiled(self) -> None:
175 |         from langgraph.graph.state import CompiledStateGraph
    |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
176 |
177 |         assert isinstance(flow_3_3, CompiledStateGraph)
    |

PLC0415 `import` should be at the top-level of a file
   --> tests/test_phase2_workflow_graphs.py:187:9
    |
185 | class TestVerdictRouter:
186 |     def test_approved_verdict_routes_approved(self) -> None:
187 |         from arkhon_rheo.workflows.base import build_state, verdict_router
    |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
188 |
189 |         router = verdict_router(approved_key="ok", rejected_key="retry")
    |

PLC0415 `import` should be at the top-level of a file
   --> tests/test_phase2_workflow_graphs.py:195:9
    |
194 |     def test_rejected_verdict_routes_retry(self) -> None:
195 |         from arkhon_rheo.workflows.base import build_state, verdict_router
    |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
196 |
197 |         router = verdict_router(approved_key="ok", rejected_key="retry")
    |

PLC0415 `import` should be at the top-level of a file
   --> tests/test_phase2_workflow_graphs.py:203:9
    |
202 |     def test_merge_counts_as_approved(self) -> None:
203 |         from arkhon_rheo.workflows.base import build_state, verdict_router
    |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
204 |
205 |         router = verdict_router(approved_key="merge", rejected_key="reject")
    |

Found 10 errors.
✗ Linter (tests) Failed

