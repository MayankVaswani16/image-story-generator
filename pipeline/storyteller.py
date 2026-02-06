from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re

class StoryTeller:
    def __init__(self, model_name: str = "google/flan-t5-small"):
        self.device = torch.device("cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)

    @torch.inference_mode()
    def _generate(self, prompt: str, max_new_tokens: int = 280, min_new_tokens: int = 100) -> str:
        """Internal generation helper with strong constraints."""
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            min_new_tokens=min_new_tokens,
            do_sample=False,
            num_beams=4,
            repetition_penalty=1.3,
            no_repeat_ngram_size=2,
            early_stopping=True,
            length_penalty=1.0,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    def generate(self, prompt: str, debug: bool = False) -> str:
        """Two-step generation: rough -> expand.
        
        Args:
            prompt: The story prompt (Title + Story section from build_story_prompt).
            debug: If True, return a tuple (rough_story, final_story) for debugging.
        
        Returns:
            Final story text (or tuple if debug=True).
        """
        # Step 1: Generate rough story (first pass)
        rough = self._generate(prompt, max_new_tokens=280, min_new_tokens=100)
        
        if debug:
            return (rough, rough)  # In debug mode, return both for inspection
        
        # Step 2: Expand and polish with a second pass
        # This prevents the model from "forgetting" to add detail.
        expand_prompt = f"""The draft below is incomplete. Expand it to a full story with:
- A clear Title
- 6–8 complete sentences
- At least 90 words total
- Proper grammar and flow
- Keep all original details, add more narrative depth

Draft:
{rough}

Complete story:"""
        
        final = self._generate(expand_prompt, max_new_tokens=320, min_new_tokens=140)
        
        return final
