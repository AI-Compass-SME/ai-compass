import re
import json

def parse_translations():
    filepath = r"d:\SpicedProjects\Projects\ai-compass\Application_Prototype\mvp_v1\frontend\src\pages\QuestionnaireWizard.jsx"
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to find: if (lang === 'de' && currentQ?.question_id === X) { ... }
    # and inside that, find: if (ans.answer_level === Y) return 'TEXT';
    
    # We will do this carefully.
    # First, let's extract the whole formatAnswerText function block.
    start_idx = content.find("const formatAnswerText = (ans, lang, currentQ) => {")
    end_idx = content.find("export default function QuestionnaireWizard() {")
    
    if start_idx == -1 or end_idx == -1:
        print("Could not find formatAnswerText block")
        return

    block = content[start_idx:end_idx]
    
    # Find active question ID blocks
    # Pattern: if (lang === 'de' && currentQ?.question_id === 1) { ...block... }
    q_blocks = re.finditer(r"if\s*\(lang\s*===\s*'de'\s*&&\s*currentQ\?\.question_id\s*===\s*(\d+)\)\s*{([^}]+)}", block)
    
    mappings = []
    
    for match in q_blocks:
        q_id = int(match.group(1))
        inner_block = match.group(2)
        
        # Find answer level mappings inside the block
        # Pattern: if (ans.answer_level === 1) return 'TEXT';
        a_matches = re.finditer(r"if\s*\(ans\.answer_level\s*===\s*(\d+)\)\s*return\s*'([^']+)';", inner_block)
        
        for a_match in a_matches:
            ans_level = int(a_match.group(1))
            text = a_match.group(2)
            
            mappings.append({
                "question_id": q_id,
                "answer_level": ans_level,
                "text": text
            })
            
    print(f"Extracted {len(mappings)} answer mappings.")
    
    # Now let's extract Question Text overrides
    # Find block where question_text is overridden
    # e.g., if (i18n.language === 'de' && currentQuestion.question_id === 1) { text = 'TEXT'; }
    
    q_text_matches = re.finditer(r"if\s*\(i18n\.language\s*===\s*'de'\s*&&\s*currentQuestion\.question_id\s*===\s*(\d+)\)\s*{\s*text\s*=\s*'([^']+)';\s*}", content)
    
    q_mappings = []
    for match in q_text_matches:
        q_id = int(match.group(1))
        text = match.group(2)
        q_mappings.append({
            "question_id": q_id,
            "text": text
        })
        
    print(f"Extracted {len(q_mappings)} question text mappings.")
    
    # Dimension name overrides
    dim_mappings = []
    dim_matches = re.finditer(r"if\s*\(name\s*===\s*'([^']+)'\)\s*return\s*'([^']+)';", block)
    for match in dim_matches:
        original = match.group(1)
        translated = match.group(2)
        dim_mappings.append({
            "original_de": original,
            "refined_de": translated
        })
        
    print(f"Extracted {len(dim_mappings)} dimension mappings.")
    
    output = {
        "answers": mappings,
        "questions": q_mappings,
        "dimensions": dim_mappings
    }
    
    with open("extracted_overrides.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        
    print("Saved to extracted_overrides.json")

if __name__ == "__main__":
    parse_translations()
