def calculate_reward(user_edit_count, similarity_score, accepted=True):
    reward = 1.0 if accepted else -1.0
    reward -= 0.05 * user_edit_count
    reward += 0.5 * similarity_score
    return round(reward, 2)
