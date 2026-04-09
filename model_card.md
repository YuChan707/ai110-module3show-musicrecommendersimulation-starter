# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

VibeTimingNow! 

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
The AI generate diverse/different recomendation that get in total score betweem 1.50-3.69 based of the genre,mood,energy,tempo_bpm,valence,danceability,acousticnes.

- What assumptions does it make about the user  
1. The user knows exactly what they want.
The profile asks for a single fixed target — energy: 0.8, one genre, one mood. The system assumes the user has clear, defined preferences rather than a vague "I'll know it when I hear it" taste.

2. The user's taste never changes.
The same profile is used for every recommendation. The system assumes the user wants the same thing whether it's Monday morning or Friday night — no context, no mood shifts, no time of day.

3. Genre and mood are hard boundaries.
If the user says "pop," every non-pop song immediately loses a full point. The system assumes "indie pop" and "synthwave" feel completely different to the user — even when they might not.

4. Closer is always better.
For energy, the system assumes the user wants exactly 0.8 — not "around 0.8 but I'm fine anywhere from 0.7 to 0.9." There's no tolerance window, just a smooth penalty the further away a song gets.

5. The user has already told the system everything relevant.
There's no room for "I hate jazz" or "never recommend the same artist twice." The system assumes the four profile fields — genre, mood, energy, acoustic — are a complete picture of the user's taste.

6. All users are defined the same way.
Every user profile has the same four fields with the same weights. The system assumes every user cares about genre 25% of the time, mood 25%, energy 25%, and so on — no individual variation in what matters most.

- Is this for real users or classroom exploration  
Classroom exploration.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used: genre,mood,energy,tempo_bpm,valence,danceability,acousticnes  
- What user preferences are considered: rate popularity of other user
- How does the model turn those into a score: Energy is double-weighted (max 2.0) compared to genre and mood (max 1.0 each). 
- What changes did you make from the starter logic: set the main goal to find the explanation mood


---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog. 
There are 10 songs. It's a small, hand-picked dataset built for simulation and testing — not a real-world catalog.

- What genres or moods are represented  
Genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop — 7 distinct genres across 10 songs.
Moods: happy, chill, intense, relaxed, focused, moody — 6 distinct moods.
The spread covers calm and energetic extremes reasonably well, but each genre only has 1–2 songs representing it.

- Did you add or remove data  
No. The CSV is the original starter file — nothing was added or removed. The only change made to data handling was in load_songs, where tempo_bpm was converted to int instead of float, but the underlying data values are unchanged.

- Are there parts of musical taste missing in the dataset  
Several. There's no classical, hip-hop, R&B, country, or electronic/EDM — genres that represent massive portions of real listening behavior. On the mood side, there's nothing representing sad, angry, romantic, or nostalgic. 
The dataset also has no explicit danceability-heavy or speechiness-heavy songs, so those features exist in the schema but don't create much meaningful variation across the 10 songs.


---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
The system works best for users who have a clear, strong preference — someone who knows they want "pop, happy, high energy." Those users get a clean winner at the top (Sunrise City at 3.96) with a meaningful gap from the rest. It also works well for users who care most about energy level, since that rule is double-weighted and creates smooth separation across all 10 songs regardless of genre or mood.

- Any patterns you think your scoring captures correctly  
The energy rule captures vibe intensity well. Songs like Gym Hero (0.93) and Storm Runner (0.91) naturally cluster together for high-energy users, while Library Rain (0.35) and Spacewalk Thoughts (0.28) cluster at the bottom — which matches real listening intuition. The system also correctly separates "workout" songs from "study" songs without being explicitly told that concept, just from the numbers.

- Cases where the recommendations matched your intuition  
Sunrise City ranking first for a pop/happy/0.8-energy user feels right — it genuinely is the closest match in the catalog. Rooftop Lights ranking second also makes sense intuitively; it's "indie pop" and "happy," so it feels adjacent even though it misses the genre point. And the lo-fi and ambient songs (Library Rain, Spacewalk Thoughts) correctly sinking to the bottom for that same user matches what you'd expect — nobody looking for upbeat pop wants a 60 BPM ambient track.

---

## 6. Limitations and Bias 

### Energy-Dominant Scoring

- `ENERGY_MAX = 2.0` makes energy the single most influential factor — its ceiling is double that of genre or mood
- A perfect energy match alone scores 2.0, equal to an exact genre match *and* an exact mood match combined
- A song 0.1 away from the target scores 1.8; one 0.3 away scores 1.4 — a 0.4-point drop that can push it below songs with exact genre/mood but slightly worse energy
- Users with flexible or broad energy preferences are penalized more than users with a precise energy target

### Filter Bubble Risk

- Genre and mood bonuses are binary — a song gets the full 1.0 or nothing; there is no partial credit
- Related genres like "indie pop" vs. "pop" are treated as completely different, giving the non-matching song a 1.0-point disadvantage from the start
- Most genres are represented by only 1–2 songs in the catalog, so a genre match is a near-predetermined winner with no in-genre competition
- Top results for any profile will consistently be the same small set of exact-match songs, leaving little room for discovery across sessions

### Unused Features

- `tempo_bpm`, `valence`, and `danceability` are loaded from the CSV but contribute 0 points to the final score
- These features could differentiate songs within the same genre/mood/energy range (e.g., a slow vs. fast melancholic track) but are currently ignored
- Removing them from scoring means two songs that feel very different to a listener can receive identical scores

### Edge Cases for Complex Tastes

- `UserProfile` holds a single `favorite_genre` and a single `favorite_mood` — mixed preferences are not supported
- A user who likes both "pop" and "rock" receives the genre bonus only for pop songs; rock songs score lower regardless of mood and energy alignment
- Niche combos like "high energy + melancholic" produce poor results because the dataset's melancholic songs cluster at low energy (≤ 0.4), leaving no song that matches both dimensions well
- Eclectic users (e.g., "classical peaceful" and "metal aggressive") will always find one taste well-served and the other ignored

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
Two profiles came up. The starter profile built with pop / happy / energy 0.8. Main one used to trace through the scoring logic and verify the rankings. 
The second was the rock profile from the user profile design discussion. Having rock / energetic / energy 0.85 / tempo 140 which was used to evaluate the profile structure, not to actually run through the recommender.

- What you looked for in the recommendations  
The main thing checked was whether the top-ranked song actually felt like the right answer. For the pop/happy profile, Sunrise City scoring highest was the target outcome — if that didn't land first, something was wrong. The gap between rank 1 and rank 2 was also worth watching, since a system where every song scores nearly the same isn't useful.

- What surprised you  
Rooftop Lights ranking second despite missing the genre point was an interesting result. It's labelled "indie pop" not "pop," so it scores zero for genre yet it still beats Gym Hero, which is actually pop. 
It happened because mood and energy together outweighed the genre point, which feels counterintuitive at first but makes sense once you see the math.

- Any simple tests or comparisons you ran  
Sunrise City (the expected winner) against Library Rain (the expected loser) side by side through every rule — genre, mood, energy — to confirm the scoring spread made sense end to end. That manual walkthrough was the closest thing to a real test run without executing the code.

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Solve the genre label problem
- Make weights user-specific
- Add group of artists
- Build a proper test suite

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
It's really good to brainstorm. Own my own, I polish the idea with own thought + repeat same process to brainstorm to polish the idea.

- Something unexpected or interesting you discovered  
Copilot/Claude lost the track. Need set up at the begin the rulers/requirements/needs. Or keep reminding the keywords reminders each instruction/chat send.

- How this changed the way you think about music recommendation apps  
AI to create algorithm, provide diverse algorithm methods



Last feedbacks
* What was your biggest learning moment during this project?
The matter of choose the right word (give better result)

* How did using AI tools help you, and when did you need to double-check them?
I ask AI to point where and why give that output/idea/code generated. I allow the change and then I read on my own the context of the code. if I don't like it, I just undone (Ctrl + z).

* What surprised you about how simple algorithms can still "feel" like recommendations?
The math is four rules (involve the genre and mood that maybe are not relate but the energy is the key) & abvious output (Sunrise City Song)


* What would you try next if you extended this project?
Create a wedsite that show the result of my model and treding music. Using python streamlit

