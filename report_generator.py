# report_generator.py
import os
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BugHunter Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2em; background: #f8f9fa; }
        h1 { color: #333; }
        h2 { border-bottom: 2px solid #ddd; padding-bottom: 0.3em; margin-top: 2em; }
        pre { background: #eee; padding: 1em; border-radius: 5px; overflow-x: auto; }
        .summary { background: #e6f7ff; border-left: 4px solid #1890ff; padding: 1em; margin: 1em 0; }
    </style>
</head>
<body>
    <h1>BugHunter Scan Report</h1>
    <p><strong>Generated:</strong> {{ timestamp }}</p>
    {% for section in sections %}
        <h2>{{ section.title }}</h2>
        {% if section.summary %}<div class="summary">{{ section.summary }}</div>{% endif %}
        <pre>{{ section.raw }}</pre>
    {% endfor %}
</body>
</html>
"""

def load_json_files(folder="data/outputs"):
    files = [f for f in os.listdir(folder) if f.endswith(".json")]
    data = []
    for fname in files:
        with open(os.path.join(folder, fname)) as f:
            try:
                parsed = json.load(f)
                data.append((fname, parsed))
            except json.JSONDecodeError:
                continue
    return data

def summarize_with_openai(raw_text):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if not client.api_key:
            return "[No API key set. Skipping AI summary.]"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in summarizing bug bounty scan outputs."},
                {"role": "user", "content": f"Summarize the following tool output:\n\n{raw_text}\n\nKeep it concise."}
            ],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        fallback = f"[AI summary failed: {e}] Falling back to raw entry count."
        return fallback

def summarize_with_local_model(raw_text):
    try:
        import requests
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": f"Summarize the following bug bounty tool output:\n\n{raw_text}\n\nKeep it concise.", "stream": False}
        )
        if response.ok:
            result = response.json()
            return result.get("response", "[No response from local model]").strip()
        return f"[Local model error: {response.status_code}]"
    except Exception as e:
        return f"[Local model unavailable: {e}]"

def smart_summarize(raw_text, result_count):
    ai_pref = os.getenv("USE_LOCAL_AI", "false").lower() == "true"
    if ai_pref:
        return summarize_with_local_model(raw_text)
    summary = summarize_with_openai(raw_text)
    if summary.startswith("[AI summary failed"):
        return f"{result_count} entries returned. {summary}"
    return summary

def render_report(sections, output="reports/report.html"):
    os.makedirs(os.path.dirname(output), exist_ok=True)
    env = Environment(loader=FileSystemLoader("."))
    template = env.from_string(TEMPLATE)
    html = template.render(timestamp=datetime.utcnow().isoformat(), sections=sections)
    with open(output, "w") as f:
        f.write(html)
    print(f"[+] Report saved to: {output}")

def generate_html_report():
    data = load_json_files()
    sections = []
    for fname, content in data:
        tool = content.get("tool", fname.replace(".json", ""))
        results = content.get("results", [])
        raw = json.dumps(results, indent=2)
        summary = smart_summarize(raw[:5000], len(results))
        sections.append({
            "title": tool,
            "summary": summary,
            "raw": raw
        })
    render_report(sections)

if __name__ == "__main__":
    generate_html_report()
