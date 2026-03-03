from flask import Flask, request, render_template
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("API_KEY"))

@app.route("/", methods=["GET", "POST"])
def home():

    translated_text = ""

    if request.method == "POST":
        text = request.form.get("text")
        target_language = request.form.get("target_language")

        if text and target_language:
            prompt = f"Translate this into {target_language}. Only return translated text:\n{text}"

            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a professional translator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
            )

            translated_text = completion.choices[0].message.content.strip()

    return render_template("index.html", translated_text=translated_text)


if __name__ == "__main__":
    app.run(debug=True)