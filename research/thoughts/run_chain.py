import yaml
import os
import sys
from google import genai
from google.genai import types


def run_chain():
    # Load questions from YAML
    yaml_path = "research/thoughts/sequential_thinking.yaml"
    try:
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
            questions = data.get("questions", [])
    except FileNotFoundError:
        print(f"Error: {yaml_path} not found.")
        return

    # Initialize Gemini Client
    try:
        client = genai.Client()
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return

    output_path = "research/thoughts/chain_results.md"

    with open(output_path, "w") as out_f:
        out_f.write("# Sequential Thinking Chain Results\n\n")

        for i, q in enumerate(questions):
            q_id = q.get("id")
            category = q.get("category")
            original_q = q.get("original_question")
            refined_prompt = q.get("refined_prompt")

            print(f"[{i + 1}/5] Processing Question ID {q_id}: {category}...")

            try:
                # Use Gemini 3 Flash Preview with High Thinking Level
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=refined_prompt,
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(
                            thinking_level=types.ThinkingLevel.HIGH
                        )
                    ),
                )

                out_f.write(f"## {category} (ID: {q_id})\n\n")
                out_f.write(f"**Original Question:** {original_q}\n\n")
                out_f.write(f"**Refined Prompt:**\n\n```\n{refined_prompt}\n```\n\n")

                out_f.write("**Model Response:**\n\n")

                # Check for candidates
                if response.candidates:
                    candidate = response.candidates[0]
                    # Check for parts
                    if candidate.content and candidate.content.parts:
                        for part in candidate.content.parts:
                            if part.thought:
                                out_f.write(f"### Thought Process\n\n> {part.text}\n\n")
                            else:
                                out_f.write(f"{part.text}\n\n")
                    else:
                        out_f.write("*No content parts returned.*\n\n")
                else:
                    out_f.write("*No candidates returned.*\n\n")

                out_f.write("---\n\n")
                print(f"  -> Done.")

            except Exception as e:
                print(f"  -> Error: {e}")
                out_f.write(f"**Error:** {str(e)}\n\n---\n\n")


if __name__ == "__main__":
    run_chain()
