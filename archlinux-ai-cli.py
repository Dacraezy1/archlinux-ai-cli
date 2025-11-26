#!/usr/bin/env python3
"""
Arch Linux AI CLI - An intelligent assistant for Arch Linux troubleshooting
Uses Google AI Studio API and Arch Wiki for reliable help
"""

import sys
import argparse
import json
import os
from pathlib import Path
import google.generativeai as genai
import requests
from typing import Optional

class ArchLinuxAI:
    def __init__(self, api_key: str):
        """Initialize the Arch Linux AI assistant"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.config_dir = Path.home() / '.config' / 'archlinux-ai-cli'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.config_dir / 'history.json'
        
    def search_arch_wiki(self, query: str) -> str:
        """Search the Arch Wiki for relevant information"""
        try:
            # Use Arch Wiki's search API
            search_url = "https://wiki.archlinux.org/api.php"
            params = {
                'action': 'opensearch',
                'search': query,
                'limit': 5,
                'format': 'json'
            }
            response = requests.get(search_url, params=params, timeout=10)
            results = response.json()
            
            if len(results) > 1 and results[1]:
                wiki_results = "\n".join([f"- {title}: {url}" 
                                         for title, url in zip(results[1], results[3])])
                return f"Relevant Arch Wiki pages:\n{wiki_results}"
            return "No specific Arch Wiki pages found for this query."
        except Exception as e:
            return f"Could not search Arch Wiki: {str(e)}"
    
    def get_ai_response(self, user_query: str, wiki_context: str) -> str:
        """Get AI response with Arch Wiki context"""
        system_prompt = """You are an expert Arch Linux assistant. Your role is to:
1. Help users troubleshoot Arch Linux issues
2. Provide accurate, safe advice based on official Arch Wiki documentation
3. Always warn about potentially dangerous operations (rm -rf, dd, filesystem modifications)
4. Recommend checking Arch Wiki pages for detailed information
5. Use pacman, systemd, and other Arch-specific tools correctly
6. Never suggest commands that could break the system without clear warnings

CRITICAL: Always prioritize system stability. For complex issues, direct users to official documentation.
When suggesting commands, explain what they do before the user runs them."""

        full_prompt = f"""{system_prompt}

Wiki Context:
{wiki_context}

User Question: {user_query}

Provide a helpful, accurate response. Include relevant commands with explanations, and reference Arch Wiki pages when applicable."""

        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error getting AI response: {str(e)}"
    
    def save_to_history(self, query: str, response: str):
        """Save conversation to history"""
        history = []
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                history = json.load(f)
        
        history.append({
            'query': query,
            'response': response,
            'timestamp': str(Path(self.history_file).stat().st_mtime if self.history_file.exists() else 0)
        })
        
        # Keep only last 50 entries
        history = history[-50:]
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def show_history(self, limit: int = 10):
        """Display conversation history"""
        if not self.history_file.exists():
            print("No history found.")
            return
        
        with open(self.history_file, 'r') as f:
            history = json.load(f)
        
        for entry in history[-limit:]:
            print(f"\n{'='*60}")
            print(f"Query: {entry['query']}")
            print(f"{'-'*60}")
            print(entry['response'])
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("🐧 Arch Linux AI CLI - Interactive Mode")
        print("Type 'exit' or 'quit' to leave, 'history' to see past queries")
        print("="*60)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    print("Goodbye! Stay rolling! 🚀")
                    break
                
                if user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                if not user_input:
                    continue
                
                print("\n🔍 Searching Arch Wiki...")
                wiki_context = self.search_arch_wiki(user_input)
                
                print("🤖 Generating response...\n")
                response = self.get_ai_response(user_input, wiki_context)
                
                print(f"{'='*60}")
                print(response)
                print(f"{'='*60}")
                
                self.save_to_history(user_input, response)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! Stay rolling! 🚀")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Arch Linux AI CLI - Your intelligent Arch Linux assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  archlinux-ai-cli -q "How do I update my system?"
  archlinux-ai-cli -i  # Interactive mode
  archlinux-ai-cli --history 5
  
Set your API key:
  export GOOGLE_AI_API_KEY="your-api-key-here"
  Or create ~/.config/archlinux-ai-cli/api_key file
        """
    )
    
    parser.add_argument('-q', '--query', type=str, help='Ask a single question')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--history', type=int, metavar='N', help='Show last N history entries')
    parser.add_argument('--api-key', type=str, help='Google AI Studio API key')
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.environ.get('GOOGLE_AI_API_KEY')
    
    if not api_key:
        # Check config file
        config_file = Path.home() / '.config' / 'archlinux-ai-cli' / 'api_key'
        if config_file.exists():
            api_key = config_file.read_text().strip()
    
    if not api_key:
        print("❌ Error: No API key provided!")
        print("\nSet your Google AI Studio API key using one of these methods:")
        print("  1. export GOOGLE_AI_API_KEY='your-key'")
        print("  2. Create ~/.config/archlinux-ai-cli/api_key file")
        print("  3. Use --api-key flag")
        print("\nGet your free API key at: https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    assistant = ArchLinuxAI(api_key)
    
    if args.history is not None:
        assistant.show_history(args.history)
    elif args.interactive:
        assistant.interactive_mode()
    elif args.query:
        print("🔍 Searching Arch Wiki...")
        wiki_context = assistant.search_arch_wiki(args.query)
        print("🤖 Generating response...\n")
        response = assistant.get_ai_response(args.query, wiki_context)
        print(response)
        assistant.save_to_history(args.query, response)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
