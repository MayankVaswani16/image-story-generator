STYLE_GUIDES = {
    "mystery": {
        "tone": "mysterious, tense, curious",
        "rules": [
            "Start with a strong hook in one sentence.",
            "Include 2-3 clues (objects, actions, or details).",
            "Add a twist in the second last sentence.",
            "End with a suspenseful final line."
        ]
    },
    "motivational": {
        "tone": "uplifting, inspiring, hopeful",
        "rules": [
            "Start with a relatable struggle.",
            "Turn it into a breakthrough moment.",
            "Include one short lesson or mantra.",
            "End with a powerful call to action."
        ]
    },
    "comedy": {
        "tone": "light, funny, playful",
        "rules": [
            "Include one unexpected misunderstanding.",
            "Add a humorous exaggeration.",
            "Keep sentences simple and punchy.",
            "End with a witty one-liner."
        ]
    },
    "crime": {
        "tone": "noir, investigative, suspenseful",
        "rules": [
            "Mention a small crime scene detail (e.g., glove, receipt, broken watch).",
            "Introduce a suspect indirectly.",
            "Reveal a key clue near the end.",
            "End with a sharp closing line like a detective story."
        ]
    }
}

def build_story_prompt(caption: str, style: str, word_limit: int = 140) -> str:
    style = style.lower().strip()
    guide = STYLE_GUIDES.get(style, STYLE_GUIDES["mystery"])
    rules_text = "\n".join([f"- {r}" for r in guide["rules"]])

    return f"""You are a creative storyteller. Write a complete {guide["tone"]} short story.

Image Description:
"{caption}"

Instructions:
{rules_text}

Requirements:
- Write exactly 6 to 8 sentences (not fewer).
- Aim for {word_limit} words, but prioritize 6–8 sentences over word count.
- Do not simply restate the caption; create a narrative with beginning, middle, and end.
- Use proper grammar, correct spelling, no URLs, no hashtags.
- Include sensory details, emotions, and character actions beyond what's visible.

Format:
Title: <One short evocative title>
Story:
<6–8 clear sentences forming a complete narrative>""".strip()


