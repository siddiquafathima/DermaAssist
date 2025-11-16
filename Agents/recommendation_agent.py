# recommendation_agent.py

def generate_recommendations(profile):
    skin = (profile.get("skin_type") or "").lower()
    concern = (profile.get("concern") or "").lower()

    print("\n🧴 DermaAssist — Skincare Recommendation Agent")
    print("🌟 Personalized Skincare Plan")
    print("----------------------------------")
    print(f"Skin Type: {skin.capitalize() or 'Not provided'}")
    print(f"Main Concern: {concern.capitalize() or 'Not provided'}\n")
    print("🧴 Suggested Routine:")

    if skin == "oily":
        print("• Use a gentle foaming cleanser to manage oil.")
        print("• Lightweight gel-based moisturizers are best.")
        print("• Avoid heavy creams.")
    elif skin == "dry":
        print("• Use hydrating, non-foaming cleansers.")
        print("• Choose thick moisturizers with ceramides.")
    elif skin == "combination":
        print("• Balance hydration: lighter formulas for T-zone, richer for cheeks.")
    else:
        print("• Use a mild gel or cream cleanser and a basic moisturizer.")

    print("\n💡 Concern-based add-ons:")
    if "acne" in concern:
        print("• Use salicylic acid (BHA) as appropriate.")
        print("• Avoid comedogenic oils and heavy makeup.")
    if "aging" in concern:
        print("• Consider gradual introduction of retinoids (with guidance).")
        print("• Add antioxidants and sunscreen daily.")
    if "pigmentation" in concern:
        print("• Use daily sunscreen and consider Vitamin C / niacinamide.")
    if "sensitivity" in concern:
        print("• Patch test new products for 72 hours; prefer fragrance-free.")
    print("\n✨ Thank you for using DermaAssist!")
