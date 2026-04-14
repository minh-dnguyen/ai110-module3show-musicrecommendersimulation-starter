# Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0**

A lightweight, content-based music recommender built as a classroom simulation.

---

## 2. Intended Use

VibeFinder suggests songs from a small catalog based on a user's stated genre preference, mood preference, target energy level, and acoustic taste. It is designed for classroom exploration only — not for real-world deployment or commercial use. It assumes the user knows their preferences in advance and expresses them as simple keyword labels (e.g., "genre: pop") rather than inferring them from listening history.

---

## 3. How the Model Works

Each song in the catalog gets a numeric "score" by comparing its attributes to the user's preferences. The scoring works like this:

- If the song's genre matches what the user listed as their favorite, it earns **2 points** — the biggest single reward, because genre is the most defining aspect of musical style.
- If the song's mood matches the user's target mood, it earns **1 point**.
- For energy level, the system calculates how close the song's energy is to the user's target (both on a 0–1 scale). A perfect match earns up to **1.5 bonus points**; the further away the song's energy is, the smaller the bonus.
- If the user likes acoustic music and the song is highly acoustic (score above 0.5), it earns an extra **0.5 points**.

All scores are added together, songs are ranked from highest to lowest, and the top 5 are returned as recommendations.

This is purely **content-based filtering** — it only looks at the song's own attributes, never at what other users have listened to.

---

## 4. Data

The catalog contains **18 songs** stored in `data/songs.csv`. Each song has the following attributes: id, title, artist, genre, mood, energy (0–1), tempo_bpm, valence, danceability, and acousticness (0–1).

Genres represented include: pop, lofi, rock, ambient, jazz, synthwave, indie pop, electronic, indie rock, folk, metal, hip-hop, blues, reggae, and classical.

Moods represented include: happy, chill, intense, relaxed, moody, focused, energetic, melancholic, peaceful, aggressive, uplifting, and calm.

The original starter file had 10 songs; 8 more were added to cover genres and moods missing from the initial set. However, features like **lyrics, language, release year, and artist popularity** are completely absent, which limits how nuanced the recommendations can be.

---

## 5. Strengths

- **Clear genre match users** get very consistent results. A "Chill Lofi" profile (genre: lofi, mood: chill, energy: 0.35, acoustic lover) correctly surfaces Library Rain and Midnight Coding at the top with scores of 5.0 and 4.89 — both are lofi, chill, low-energy, and highly acoustic.
- **The reasoning output is transparent.** Every recommendation comes with a plain-English list of why the song scored well (e.g., "genre match (+2.0), mood match (+1.0), energy similarity (+1.47)"), which makes the system easy to audit.
- **The energy scoring rewards closeness, not just high or low values.** A user who wants energy 0.35 gets penalized less for a 0.40 song than for a 0.90 song, which is the right behavior.

---

## 6. Limitations and Bias

- **Genre dominates everything.** At +2.0 points, a genre match is worth twice a mood match and more than a full energy match. Songs in underrepresented genres (e.g., there is only one rock song, one metal song) almost never surface for users outside those genres, while pop songs compete well across many profiles simply by earning energy points.
- **The "sad high-energy" edge case fails silently.** When given `genre: pop, mood: sad, energy: 0.9`, the system returns pop songs with no mood match at all — there are no "sad pop" songs in the catalog. The user gets pop recommendations that simply ignore the stated mood preference, with no warning.
- **No diversity enforcement.** The same artist (e.g., Neon Echo) can dominate multiple slots. A real system would spread results across different artists.
- **Tempo, valence, and danceability are loaded but never used.** These columns exist in the CSV and could meaningfully differentiate songs (e.g., a "danceable" vs. "slow" pop song), but the scoring ignores them entirely.
- **No collaborative signal.** The system never learns from listening history, skips, or repeat plays, so it cannot adapt to a user whose tastes evolve over time.

---

## 7. Evaluation

Three main profiles were tested, plus one adversarial edge case:

| Profile | Genre | Mood | Energy | Top Result | Score |
|---|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.9 | Sunrise City | 4.38 |
| Chill Lofi | lofi | chill | 0.35 | Library Rain | 5.00 |
| Intense Rock | rock | intense | 0.92 | Storm Runner | 4.48 |
| Edge Case: Sad High-Energy Pop | pop | sad | 0.9 | Gym Hero | 3.46 |

**What was surprising:** The Chill Lofi profile produced the highest possible score (5.00 for Library Rain) because all four scoring criteria aligned — genre, mood, energy, and acoustic preference all matched perfectly. This shows the system is self-consistent.

**What was concerning:** The "sad" mood preference was completely ignored in the edge case because no sad pop songs exist in the catalog. The system returned happy/intense pop songs with no explanation to the user that the mood preference could not be satisfied.

A **weight-shift experiment** was also run: genre weight halved to +1.0 and energy weight doubled to 3.0x. The top result stayed the same (Sunrise City), but the second slot changed from "Gym Hero" (a pure genre match) to "Rooftop Lights" (which matched mood and energy more closely). This shows the system is sensitive to weight changes and that energy-dominant scoring can surface cross-genre results.

---

## 8. Future Work

1. **Add mood-based fallback messaging.** If no song matches the user's stated mood, the system should tell the user rather than silently ignoring the preference.
2. **Include tempo, valence, and danceability in scoring.** These features are already in the CSV. A user who wants "danceable" music should be able to express that.
3. **Add a diversity penalty.** Deduct points from a song if the same artist already appears in the top 3 results, so the list covers more of the catalog.
4. **Implicit profile learning.** Track which recommended songs the user skips or replays and adjust weights automatically over time — moving from content-based to a hybrid model.

---

## 9. Personal Reflection

Building VibeFinder made it clear how much weight a single design decision carries. Choosing to give genre +2.0 points versus +1.0 points completely changed which songs appeared in the top 5 — not by a little, but dramatically. That is a humbling reminder that real recommenders (Spotify, YouTube) are making thousands of similar weight decisions, and those choices shape what music millions of people discover or never hear.

The most unexpected moment was the edge case: a user who wants "sad, high-energy pop" gets recommendations that feel almost insulting — upbeat gym music — because the catalog has no sad pop songs and the system gives no feedback. Real platforms handle this with catalog breadth and fallback strategies. A tiny catalog magnifies every gap.

Using AI tools during this project helped with scaffolding and syntax, but the actual judgment calls — how much should genre outweigh mood? is an energy difference of 0.2 "close enough"? — required thinking through what music actually means to a listener. The code ran correctly long before the recommendations felt right.
