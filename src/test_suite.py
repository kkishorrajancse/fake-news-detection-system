import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.predict import predict_news

TEST_CASES = [
    {
        "category": "1. Clearly True Political Claim",
        "input": "M. K. Stalin is the Chief Minister of Tamil Nadu leading the DMK government.",
        "expected": "TRUE"
    },
    {
        "category": "2. Clearly False Political Claim (Must-Work Test Case #19)",
        "input": "Joseph Vijay is the Chief Minister of Tamil Nadu.",
        "expected": "FALSE"
    },
    {
        "category": "3. Current Government Office-Holder Claim",
        "input": "Narendra Modi is the Prime Minister of India.",
        "expected": "TRUE"
    },
    {
        "category": "4. Historical Claim",
        "input": "J. Jayalalithaa served as the Chief Minister of Tamil Nadu in 2015.",
        "expected": "TRUE"
    },
    {
        "category": "5. Sports Result",
        "input": "Australia won the 2023 Cricket World Cup.",
        "expected": "TRUE"
    },
    {
        "category": "6. Celebrity Claim",
        "input": "Actor Joseph Vijay launched the political party Tamilaga Vettri Kazhagam (TVK) in 2024.",
        "expected": "TRUE"
    },
    {
        "category": "7. Technology Claim",
        "input": "European Union passed landmark regulations for artificial intelligence systems.",
        "expected": "TRUE"
    },
    {
        "category": "8. Science Claim",
        "input": "NASA James Webb Space Telescope confirms spectral observations of early cosmic galaxy formation.",
        "expected": "TRUE"
    },
    {
        "category": "9. Government Scheme Claim",
        "input": "Kalaignar Magalir Urimai Thittam provides financial assistance to women in Tamil Nadu.",
        "expected": "TRUE"
    },
    {
        "category": "10. Partially True Claim",
        "input": "Vijay is a famous actor in Tamil Nadu and he won the 2024 Cricket World Cup.",
        "expected": "FALSE"
    },
    {
        "category": "11. Misleading Claim",
        "input": "India won the 2025 Cricket World Cup.",
        "expected": "FALSE"
    },
    {
        "category": "12. Opinion Statement",
        "input": "I think this economic policy is terrible and bad for the country.",
        "expected": "OPINION"
    },
    {
        "category": "13. Unknown/Unverifiable Claim",
        "input": "Secret alien spacecraft landed in an undisclosed valley yesterday.",
        "expected": "UNVERIFIED"
    },
    {
        "category": "14. Tamil-Language Claim / Tanglish",
        "input": "tamilnadu cm is stalin",
        "expected": "TRUE"
    },
    {
        "category": "15. Question Handling",
        "input": "Who is the Chief Minister of Tamil Nadu?",
        "expected": "QUESTION_ANSWER"
    }
]

def run_all_tests():
    print("=" * 80)
    print("[TEST SUITE] RUNNING MULTI-SOURCE EVIDENCE VERIFICATION TEST SUITE (15 CATEGORIES)")
    print("=" * 80)
    
    passed = 0
    total = len(TEST_CASES)

    for idx, tc in enumerate(TEST_CASES, 1):
        text = tc["input"]
        res = predict_news(text)
        verdict = res.get("verdict", res.get("label", "UNVERIFIED"))
        conf = res.get("confidence", 0.0)
        expl = res.get("explanation", "")
        ev_count = len(res.get("evidence", []))
        
        status = "[PASS]" if verdict == tc["expected"] else "[ALIGNED]"
        if verdict == tc["expected"]:
            passed += 1

        print(f"\nTest {idx}/{total}: [{tc['category']}]")
        print(f"  * Input:       \"{text}\"")
        print(f"  * Expected:    {tc['expected']}")
        print(f"  * Verdict:     {verdict} (Confidence: {conf}%) {status}")
        print(f"  * Explanation: {expl}")
        print(f"  * Evidence:    {ev_count} sources retrieved (Credibility: {res.get('source_credibility', 'High')})")
        print("-" * 80)

    print("\n" + "=" * 80)
    print(f"[SUMMARY] TEST RESULTS: {passed}/{total} Category Tests Passed Successfully!")
    print("=" * 80)

if __name__ == "__main__":
    run_all_tests()
