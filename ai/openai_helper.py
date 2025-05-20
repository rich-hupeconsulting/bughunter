import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_js_directory(js_dir):
    combined_js = ""
    for filename in os.listdir(js_dir):
        if filename.endswith(".js"):
            path = os.path.join(js_dir, filename)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                combined_js += f"\n\n// {filename}\n" + f.read()

    if not combined_js:
        print("[!] No JS files found to analyze.")
        return

    prompt = (
        "You are a security researcher. Analyze the following JavaScript code for: \n"
        "- API endpoints\n- Parameter names\n- Potential secrets or keys\n\n" + combined_js[:12000]
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        output = response['choices'][0]['message']['content']

        os.makedirs("data/outputs", exist_ok=True)
        with open("data/outputs/ai_js_analysis.json", "w") as f:
            json.dump({
                "analysis": output
            }, f, indent=2)

        print("[*] JS analysis saved to data/outputs/ai_js_analysis.json")

    except Exception as e:
        print("[!] OpenAI analysis failed:", e)
