# Synthesizer agent logic here
from knowledge_graph_builder.tools.research_api_tool import EURI_CLIENT

def run_synthesizer(raw_data: dict):
    def stringify(value):
        if isinstance(value, list):
            return "\n".join([str(v) for v in value])
        return str(value)

    combined_text = "\n".join([stringify(v) for v in raw_data.values()])
    prompt = f"""
You are an expert knowledge graph creator and educational content organizer specializing in learning resources.

Analyze the provided information and create a structured knowledge graph on the topic that focuses on learning resources and course suggestions. Break down the topic into clear components:

- Main Concepts (fundamental ideas and principles to learn)
- Learning Paths (beginner to advanced progression)
- Learning Resources (books, courses, videos, tutorials)
- Prerequisites and Related Skills
- Practical Applications

Output Format (Strict):
Concept -> Subtopic -> Related Detail
Use arrows only to show relationships. No colons or lists.

For learning resources, use this format:
Resource Type -> Resource Name -> Resource Details

Examples:
- Books -> "Title of Book" -> Beginner-friendly introduction
- Courses -> "Platform: Course Name" -> Advanced concepts with projects
- Videos -> "Channel: Video Series" -> Visual explanations of key concepts

Ensure your output creates a clear hierarchical structure that can be visualized as a graph.
Provide comprehensive coverage of the learning journey with 15-25 connected paths.

Focus on:
1. Best resources across different platforms (Google, YouTube, online courses)
2. Different learning styles (visual, text-based, interactive)
3. Free and paid options
4. Beginner to advanced progression
5. Practical applications and projects

Context:
{combined_text}
"""

    response = EURI_CLIENT.generate_completion(prompt=prompt)
    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return str(response)
