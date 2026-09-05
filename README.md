<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />



# THING THERAPIST 🎯


## Basic Details
### Team Name: HAYSH


### Team Members
- Member 1: HANEEN AJAS - SSET
- Member 2: AYSHA K A - SSET


### Project Description
A completely unnecessary and slightly ridiculous web app that gives life advice to everyday objects. Upload a picture of an object, and the THING THERAPIST will analyze it and provide funny, personalized advice based on its purpose. Because apparently, even objects have feelings and need advice. 😭

### The Problem (that doesn't exist)
Everyday objects have feelings too. Unfortunately, they have absolutely no one to give them life advice. Until now.

### The Solution (that nobody asked for)
We use AI to analyse your everyday objects and give them completely necessary life advice. Upload a picture of anything—a chair, a bedsheet, a spoon—and let our highly qualified AI therapist solve problems. 😭🔮

## Technical Details
### Technologies/Components Used
For Software:
- Programming Language: Python
-Frontend: HTML, CSS
-Backend Framework: Flask
-AI: Google Gemini API
-Libraries: google-generativeai, python-dotenv
-Tools: VS Code, GitHub, Vercel 


### Implementation
For Software:
# Installation
```bash
pip install -r requirements.txt
```

# Run
```bash
flask --app app run
```

## Deploy to Vercel

1. Push this repository to GitHub.
2. In [Vercel](https://vercel.com), select **Add New Project**, import this GitHub repository, and keep the project root as the repository root.
3. Add an environment variable named `GEMINI_API_KEY` in the Vercel project settings. Use the same key locally in a `.env` file if needed; never commit the key.
4. Deploy. Vercel uses `vercel.json` and `requirements.txt` to run the Flask app.

The upload is processed in memory because Vercel function storage is temporary. A Gemini API key is required for image analysis.

### Gemini API key setup

1. Create a key in [Google AI Studio](https://aistudio.google.com/apikey).
2. For local development, put it in the project root `.env` file:

	```env
	GEMINI_API_KEY=your_gemini_api_key_here
	```

3. For Vercel, open **Project Settings > Environment Variables**, add `GEMINI_API_KEY`, paste the key as the value, and redeploy.

Never put the key in `app.py`, HTML, JavaScript, or a committed file. If an old key has been exposed, revoke it in Google AI Studio and create a replacement.

### Project Documentation
For Software:

# Screenshots 
![Screenshot1](Add screenshot 1 here with proper name)
*Add caption explaining what this shows*

![Screenshot2](Add screenshot 2 here with proper name)
*Add caption explaining what this shows*

![Screenshot3](Add screenshot 3 here with proper name)
*Add caption explaining what this shows*


## Team Contributions
- Haneen: coding 
- Aysha: documentation


---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)



