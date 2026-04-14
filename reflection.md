# Reflection: Profile Comparison Notes

This file documents what changed between user profiles and why the differences make sense.

---

## Profile 1 vs Profile 2: High-Energy Pop vs Chill Lofi

**High-Energy Pop** (`genre: pop, mood: happy, energy: 0.9`)
Top results: Sunrise City (4.38), Gym Hero (3.46), Rooftop Lights (2.29)

**Chill Lofi** (`genre: lofi, mood: chill, energy: 0.35, likes_acoustic: True`)
Top results: Library Rain (5.00), Midnight Coding (4.89), Focus Flow (3.92)

**What changed and why it makes sense:**
The two profiles produce completely different top 5 lists with zero overlap, which is the correct behavior — lofi and pop are stylistically opposite genres, and the energy targets (0.9 vs 0.35) sit at opposite ends of the scale. The Chill Lofi profile also activates the acoustic bonus, which shifts the rankings further toward quiet, instrumental tracks like Library Rain and Spacewalk Thoughts. The High-Energy Pop profile never touches those songs because their energy scores (0.28–0.42) are too far from 0.9 to earn meaningful points even if they had matched genre or mood.

One note: Gym Hero appears second for the Pop profile despite being an "intense" mood song (not "happy"). It still scores high because genre match (+2.0) and near-perfect energy similarity combine to outscore songs that match mood but not genre. This shows the genre weight is strong enough to override a mood mismatch.

---

## Profile 2 vs Profile 3: Chill Lofi vs Intense Rock

**Chill Lofi** (`genre: lofi, mood: chill, energy: 0.35, likes_acoustic: True`)
Top results: Library Rain (5.00), Midnight Coding (4.89), Focus Flow (3.92)

**Intense Rock** (`genre: rock, mood: intense, energy: 0.92`)
Top results: Storm Runner (4.48), Gym Hero (2.48), Thunder Strikes (1.44)

**What changed and why it makes sense:**
The Intense Rock profile produces fewer high-scoring songs than Chill Lofi because the rock catalog is thin — there is only one song explicitly labeled "rock" (Storm Runner). After the genre+mood double match for Storm Runner, the next best results are songs that only match mood ("intense") or only match energy (high tempo tracks like Thunder Strikes and Pulse Rising). This is a real limitation: small catalogs punish niche genre users because there are simply fewer songs that can earn the genre bonus.

In contrast, Chill Lofi benefits from having two dedicated lofi songs (Library Rain, Midnight Coding, Focus Flow) and a large pool of acoustic-friendly ambient tracks, so even the 4th and 5th results score well. The takeaway: the recommender's performance is uneven across genres — it works better where the catalog is denser.

---

## Profile 3 vs Edge Case: Intense Rock vs Sad High-Energy Pop

**Intense Rock** (`genre: rock, mood: intense, energy: 0.92`)
Top results: Storm Runner (4.48), Gym Hero (2.48), Thunder Strikes (1.44)

**Sad High-Energy Pop** (`genre: pop, mood: sad, energy: 0.9`)
Top results: Gym Hero (3.46), Sunrise City (3.38), Storm Runner (1.48)

**What changed and why it makes sense:**
The Intense Rock profile at least finds one song that perfectly matches genre AND mood (Storm Runner), giving it a clear top result. The Sad High-Energy Pop profile fails to find any song matching its mood because there are no "sad pop" songs in the catalog. As a result, all five recommendations are songs that matched genre (pop) or energy but completely ignored the stated mood of "sad."

This is the most important finding from the evaluation: **the system cannot distinguish between a satisfied user and a frustrated one.** Both profiles return 5 results with similar-looking score numbers, but the Intense Rock user got what they asked for, while the Sad Pop user got the opposite of their mood preference. A real-world system would display a message like "We couldn't find sad pop songs — showing closest matches instead." VibeFinder 1.0 silently fails.

---

## Weight Shift Experiment: Default vs Energy-Heavy Weights

**Default weights** (genre +2.0, energy up to +1.5): `pop/happy/energy 0.8`
Top 5: Sunrise City, Gym Hero, Rooftop Lights, Rise Up, Night Drive Loop

**Experimental weights** (genre +1.0, energy up to +3.0): `pop/happy/energy 0.8`
Top 5: Sunrise City, Rooftop Lights, Gym Hero, Rise Up, Night Drive Loop

**What changed and why it makes sense:**
Sunrise City stays at #1 because it matches genre, mood, AND has a very close energy match — it benefits from all scoring dimensions regardless of how weights shift. The biggest change is positions 2 and 3 swapping: Gym Hero (pure genre match, mood mismatch) drops behind Rooftop Lights (mood match, no genre match) when energy and mood become relatively more important than genre. This demonstrates that the ranking is genuinely sensitive to weight choices, and that there is no single "correct" weighting — it depends on whether you believe genre or vibe matters more to the user.
