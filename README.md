Lafz 🌸

Lafz (لفظ, meaning "words") is a personal AI powered Instagram caption and song suggestion tool. It learns your unique writing style, including your mix of English and Urdu captions and your music taste for different moods and photo types, then generates tailored captions and real song suggestions for your posts and stories.

Features
Personalized captions: Upload a photo and get caption options that match your usual tone and language style, whether that is English, Urdu (Roman script), or a specific mood.
Song suggestions: Get real song recommendations (Bollywood, Pakistani music, or any genre you prefer) that fit the vibe of your photo, based on your past preferences.
Style memory: Teach Lafz how you write once, and it remembers permanently. Preferences are stored locally in preferences.json and used as context for every future caption.
Style profile management: View, add, or delete your saved style notes anytime from the app.
Warm, aesthetic interface: A cozy, editorial style design built with Streamlit, custom fonts, and soft color palettes.
Tech Stack
Python for the core logic
Streamlit for the web interface
Google Gemini API (gemini-3.6-flash) for caption and song generation, including image understanding
How It Works
Teach Style: Describe your caption and song preferences in plain language, for example: "for friendship pics I write Urdu captions like 'sukoon k lamhat', songs like Osho Jain." Lafz saves this to your style profile.
Generate: Upload a photo (and optionally add context like "with my best friend at the beach"). Lafz reads the image, checks your saved style notes, and generates three caption options plus two song suggestions that match your vibe.
My Style Profile: Review everything Lafz has learned about your style, and remove any notes that no longer apply.
Setup (Local)
Clone this repository:
   git clone https://github.com/Syasrab/LAFZ.git
   cd LAFZ
Install dependencies:
   pip install -r requirements.txt
Get a free Gemini API key from Google AI Studio.
Set your API key as an environment variable:
Windows: set GEMINI_API_KEY=your-key-here
Mac/Linux: export GEMINI_API_KEY=your-key-here
Run the app:
   streamlit run app.py
Deployment

This app is deployable on Streamlit Community Cloud for free. Add your GEMINI_API_KEY under the app's Secrets settings when deploying.

Notes
preferences.json stores your personal style data locally and is not included in this repository, it is created automatically the first time you use the app.
Song suggestions are based on the model's general knowledge, not live streaming data.
Made with 🤍

A personal project for capturing moments in words that feel true to how you actually write and think.
