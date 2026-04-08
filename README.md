# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works (documented)

The system reads the song catalog, gives each song a score based on how closely its genre, mood, energy, and acoustic character match the user's preferences, then returns the top 5 songs with a reason why they were picked.

What Exists Right Now
The data is ready — data/songs.csv
10 songs, each with: title, artist, genre, mood, energy, tempo, valence, danceability, acousticness. This is the catalog the recommender will search through.

The structure is defined — src/recommender.py
Two blueprints have been created:

Song — a template that holds all a song's attributes
UserProfile — a template that holds the user's preferences (favorite genre, mood, target energy, likes acoustic or not)
A Recommender class also exists, along with two functions: load_songs and recommend_songs.

The runner is ready — src/main.py
It sets a starter user profile (pop / happy / energy 0.8), calls the recommender, and prints the top 5 results with explanations.


The skeleton is complete — the data, the data structures, and the wiring between files are all in place — but the actual intelligence (scoring songs, ranking them, explaining why) still needs to be implemented inside the TODO sections of src/recommender.py.

Following this steps:
1) You have two things going in:

A song catalog (data/songs.csv) — 10 songs, each described by numbers like energy (0–1), tempo (BPM), acousticness (0–1), and labels like genre and mood.
A user profile — what the user likes: { genre: "pop", mood: "happy", energy: 0.8 }.

2) For every song in the catalog, the system asks: "How well does this song match the user?"

It checks four things and combines them:

Signal	How it's measured	Weight
Genre match	Does the genre match exactly? 1.0 or 0.0	30%
Mood match	Does the mood match exactly? 1.0 or 0.0	25%
Energy proximity	How close is the energy to what the user wants?	25%
Acoustic preference	Does it match the user's acoustic/electronic taste?	20%
The result is one number between 0.0 and 1.0 per song.

3) Once every song has a score, the system sorts them from highest to lowest and returns the top 5. That's the recommendation list.

4) For each top song, the system checks why it scored well and writes a plain-English sentence:

"Recommended because it matches your favorite genre (pop) and energy level is close to your target."

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

## List the specific features
# Song Features
Field         |	  Type  |    Example
id	          |   int	  |       1
title	        |   str	  |  "Sunrise City"
artist	      |   str	  |  "Neon Echo"
genre	        |   str	  |     "pop"
mood	        |   str	  |     "happy"
energy	      |  float	|      0.82
tempo_bpm	    |  float	|      118.0
valence	      |  float	|      0.84
danceability	|  float	|      0.79
acousticness	|  float	|      0.18


# UserProfile Features
Field	          |  Type	|  Example
favorite_genre	|  str	|   "pop"
favorite_mood	  |  str	|  "happy"
target_energy	  | float	|    0.8
likes_acoustic	| bool	|   False


# What Gets Compared During Scoring
Only 4 of the 10 Song fields are used in the match:

UserProfile field	  |  Matched against	  |  How
favorite_genre	    |     song.genre	    |  Exact match — binary
favorite_mood	      |     song.mood	      |  Exact match — binary
target_energy	      |    song.energy	    | Proximity — continuous
likes_acoustic	    |  song.acousticness  |	Direction — continuous

title, artist, id, tempo_bpm, valence, and danceability are stored on the Song but not used in scoring yet/ They're available for display and future expansion.

---
## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

