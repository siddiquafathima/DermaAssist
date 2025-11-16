# orchestrator_agent.py

from intake_agent import interactive_intake
from memory_agent import retrieve_memory, save_profile_memory
from recommendation_agent import generate_recommendations

def main():
    print("🤖 Welcome to DermaAssist — Smart Skin Support Agent\n")
    profile = interactive_intake()

    # ensure user_id exists (simple assignment if missing)
    if not profile.get("user_id"):
        profile["user_id"] = f"{profile.get('name') or 'user'}_{profile.get('age') or '0'}"

    print("\n🧠 Checking your history (Memory Agent)...")
    match, similarity = retrieve_memory(profile)
    if match:
        print(f"📂 Found similar past profile (Similarity: {similarity:.2f})")
        print(f"➡ {match.get('profile')}\n")
        print("🔁 Using history to refine recommendations...\n")
    else:
        print(f"📁 No similar history found (Similarity: {similarity:.2f})")
        print("📝 Creating new memory entry...\n")
        msg = save_profile_memory(profile)
        print(msg)

    print("🔁 Routing data to Recommendation Agent...\n")
    generate_recommendations(profile)

if __name__ == "__main__":
    main()
