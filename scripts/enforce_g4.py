#!/usr/bin/env python3
import argparse
import json
import sys
import os
import re

VAGUE_PATTERNS = [
    r'\bseems?\b',
    r'\blooks?\b',
    r'\bprobably\b',
    r'as far as (?:i|we) (?:can )?tell'
]

def check_tool_artifacts(review):
    errors = []
    evidence = review.get('verification_evidence', {})
    methods = evidence.get('how_verified', [])
    tool_outputs = evidence.get('tool_outputs', {})
    
    for method in methods:
        if 'pylint' in method.lower() and 'pylint' not in tool_outputs:
            errors.append("Claimed pylint but no artifact")
    
    return errors

def enforce_g4_verification(review):
    errors = []
    
    if 'verification_evidence' not in review:
        errors.append("Missing verification_evidence")
        return False, errors
    
    evidence = review['verification_evidence']
    methods = evidence.get('how_verified', [])
    
    if not methods:
        errors.append("No verification methods")
    
    all_text = ' '.join(methods) + ' ' + evidence.get('sufficiency_reasoning', '')
    for pattern in VAGUE_PATTERNS:
        if re.search(pattern, all_text, re.IGNORECASE):
            errors.append(f"Vague language: {pattern}")
    
    checks = evidence.get('checks_performed', {})
    if 'logic_correctness' not in checks or not checks.get('logic_correctness', {}).get('verified'):
        errors.append("Logic check missing")
    
    reasoning = evidence.get('sufficiency_reasoning', '')
    if len(reasoning) < 20:
        errors.append("Insufficient reasoning")
    
    artifact_errors = check_tool_artifacts(review)
    errors.extend(artifact_errors)
    
    return len(errors) == 0, errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('review_file')
    args = parser.parse_args()
    
    with open(args.review_file) as f:
        review = json.load(f)
    
    passed, errors = enforce_g4_verification(review)
    
    if passed:
        print("✅ G4 PASS")
        sys.exit(0)
    else:
        print("❌ G4 FAIL:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()