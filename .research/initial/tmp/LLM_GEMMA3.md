# Google Gemma 3: Features & Capabilities

**Gemma 3** is Google's latest family of state-of-the-art open models, designed to be highly efficient, multimodal, and capable of running on a wide range of hardware. released in March 2025.

## Key Features

1. **Native Multimodality**:
    * Unlike previous versions, Gemma 3 is built to process both text and image inputs natively.
    * It uses a SigLIP-based vision encoder to analyze images, answer visual questions, and perform reasoning tasks involving visual data.

2. **Multilingual Proficiency**:
    * Supports over 140 languages.
    * Includes a specialized tokenizer with a 262k vocabulary size, optimizing performance for non-English languages.

3. **Extended Context**:
    * Features a significantly large context window of up to **128k tokens**, enabling deep analysis of long documents and complex prompt chains.

4. **Model Variants**:
    * **1B & 4B**: Lightweight models for edge devices and fast inference.
    * **9B & 27B**: High-performance models for complex reasoning and instruction following.
    * **270M**: Ultra-compact version (planned) for extremely resource-constrained environments.

5. **Performance**:
    * The 27B variant has demonstrated exceptional performance, achieving high Elo scores on benchmarks like LMArena.
    * Architectural improvements in reduced KV-cache memory allow for efficient long-context processing.

## Integration & Usage

### Using Google GenAI SDK (Python)

Gemma 3 is fully supported by the unified `google-genai` SDK.

```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

# Text Generation
response = client.models.generate_content(
    model="gemma-3-27b-it",
    contents="Explain quantum entanglement to a 5-year-old."
)
print(response.text)

# Multimodal Generation
image = Image.open('diagram.png')
response = client.models.generate_content(
    model="gemma-3-27b-it",
    contents=[image, "Analyze this diagram and explain the process flow."]
)
print(response.text)
```

### Using Ollama

Gemma 3 can be run locally using Ollama.

```bash
ollama run gemma3:27b "Write a poem about the singularity."
```

## References

* [Google DeepMind: Gemma Family](https://ai.google.dev/gemma)
* [Gemma 3 Technical Report](https://storage.googleapis.com/deepmind-media/gemma/gemma-3-report.pdf)
