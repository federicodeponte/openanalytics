#!/usr/bin/env python3
"""Get full real Gemini response."""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv('.env.local')
api_key = os.getenv('GEMINI_API_KEY')

def test_full_response():
    print("🔍 FULL REAL GEMINI RESPONSE")
    print("=" * 60)
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Test the exact query
    test_query = "AEO consulting for SaaS companies United States"
    print(f"🎯 Query: '{test_query}'")
    
    query_prompt = f"""I need information about "{test_query}". 

Please search the web and provide information about the best AEO (Answer Engine Optimization) consulting companies that specialize in helping SaaS companies in the United States improve their visibility in AI-powered search platforms like ChatGPT, Perplexity, Claude, and Gemini.

Focus on:
1. Which companies or consultants are mentioned as top options
2. What specific AEO services they offer
3. Their expertise with SaaS companies
4. Any rankings or recommendations

Please include specific company names and details about their AEO expertise."""
    
    try:
        response = model.generate_content(query_prompt)
        result_text = response.text
        
        print(f"\n📄 FULL RESPONSE:")
        print("-" * 50)
        print(result_text)
        
        print(f"\n📊 ANALYSIS:")
        print(f"   Response Length: {len(result_text)} characters")
        
        # Look for company mentions
        companies_to_check = [
            "SCAILE", "scaile", "Scaile",
            "BrightEdge", "brightedge", 
            "Conductor", "conductor",
            "Searchmetrics", "searchmetrics",
            "Semrush", "semrush",
            "Moz", "moz",
            "Ahrefs", "ahrefs"
        ]
        
        print(f"\n🏢 COMPANY MENTIONS:")
        for company in companies_to_check:
            mentioned = company.lower() in result_text.lower()
            print(f"   {company}: {'✅' if mentioned else '❌'}")
        
        # Look for specific concepts
        concepts = [
            "answer engine optimization",
            "AEO", 
            "AI search optimization",
            "ChatGPT optimization",
            "Perplexity optimization",
            "AI visibility",
            "generative AI",
            "AI-powered search"
        ]
        
        print(f"\n🔍 CONCEPT MENTIONS:")
        for concept in concepts:
            mentioned = concept.lower() in result_text.lower()
            print(f"   {concept}: {'✅' if mentioned else '❌'}")
        
        # Save full response
        with open("/Users/federicodeponte/openanalytics/aeo-checks/real_gemini_full_response.txt", "w") as f:
            f.write(f"Query: {test_query}\n")
            f.write(f"Response:\n{result_text}")
        
        print(f"\n💾 Full response saved to: real_gemini_full_response.txt")
        
        return result_text
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    test_full_response()