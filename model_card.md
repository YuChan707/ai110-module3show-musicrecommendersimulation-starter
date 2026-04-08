# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

VibeTimingNow! 

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  



Last feedbacks
* What was your biggest learning moment during this project?
* How did using AI tools help you, and when did you need to double-check them?
* What surprised you about how simple algorithms can still "feel" like recommendations?
* What would you try next if you extended this project?
