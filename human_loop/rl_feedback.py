# rl_feedback.py

def calculate_reward(user_edit_count, similarity_score, accepted=True):
    reward = 1.0 if accepted else -1.0
    reward -= 0.05 * user_edit_count
    reward += 0.5 * similarity_score
    return round(reward, 2)

# Add this wrapper function
def rl_score(feedback_text: str, quality: str) -> float:
    # Dummy values for edit count and similarity (replace with actual logic later)
    user_edit_count = 3  # e.g., from text diff length
    similarity_score = 0.7  # e.g., from cosine similarity
    accepted = quality == "👍 Yes"
    
    return calculate_reward(user_edit_count, similarity_score, accepted)
