#!/usr/bin/env python3
"""
Arch Linux AI CLI - An intelligent assistant for Arch Linux troubleshooting
Uses Google AI Studio API and reads actual Arch Wiki content for reliable help
"""

import sys
import argparse
import json
import os
import re
from pathlib import Path
import google.generativeai as genai
import requests
from typing import Optional, List, Dict
from html.parser import HTMLParser

class WikiContentExtractor(HTMLParser):
    """Extract clean text content from Wiki HTML"""
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.in_content = False
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header'}
        self.current_tag = None
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        # Look for main content div
        for attr, value in attrs:
            if attr == 'id' and value in ['mw-content-text', 'bodyContent']:
                self.in_content = True
                
    def handle_endtag(self, tag):
        if tag in ['div'] and self.in_content:
            self.in_content = False
            
    def handle_data(self, data):
        if self.in_content and self.current_tag not in self.skip_tags:
            cleaned = data.strip()
            if cleaned and len(cleaned) > 3:
                self.text_content.append(cleaned)
                
    def get_text(self):
        return ' '.join(self.text_content)

class ArchLinuxAI:
    def __init__(self, api_key: str):
        """Initialize the Arch Linux AI assistant"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.config_dir = Path.home() / '.config' / 'archlinux-ai-cli'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.config_dir / 'history.json'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ArchLinuxAI-CLI/1.0 (Arch Linux helper tool)'
        })
        
    def search_arch_wiki(self, query: str) -> List[Dict[str, str]]:
        """Search the Arch Wiki and return page information"""
        try:
            search_url = "https://wiki.archlinux.org/api.php"
            params = {
                'action': 'opensearch',
                'search': query,
                'limit': 3,
                'format': 'json'
            }
            response = self.session.get(search_url, params=params, timeout=10)
            results = response.json()
            
            wiki_pages = []
            if len(results) > 1 and results[1]:
                for title, url in zip(results[1], results[3]):
                    wiki_pages.append({
                        'title': title,
                        'url': url
                    })
            return wiki_pages
        except Exception as e:
            print(f"⚠️  Wiki search error: {str(e)}")
            return []
    
    def fetch_wiki_content(self, page_title: str) -> Optional[str]:
        """Fetch actual content from an Arch Wiki page"""
        try:
            api_url = "https://wiki.archlinux.org/api.php"
            params = {
                'action': 'parse',
                'page': page_title,
                'format': 'json',
                'prop': 'text',
                'disablelimitreport': 1,
                'disabletoc': 1
            }
            
            response = self.session.get(api_url, params=params, timeout=15)
            data = response.json()
            
            if 'parse' in data and 'text' in data['parse']:
                html_content = data['parse']['text']['*']
                
                # Extract text from HTML
                parser = WikiContentExtractor()
                parser.feed(html_content)
                text = parser.get_text()
                
                # Clean up and limit size (keep most relevant parts)
                text = re.sub(r'\s+', ' ', text)
                text = re.sub(r'\[edit\]', '', text)
                
                # Keep first 4000 chars (most relevant content is usually at the top)
                if len(text) > 4000:
                    text = text[:4000] + "... [content truncated, see full page at wiki]"
                
                return text
            return None
        except Exception as e:
            print(f"⚠️  Could not fetch wiki page '{page_title}': {str(e)}")
            return None
    
    def get_wiki_knowledge(self, query: str) -> str:
        """Search Wiki and fetch actual content from relevant pages"""
        wiki_pages = self.search_arch_wiki(query)
        
        if not wiki_pages:
            return "No relevant Arch Wiki pages found. Please search the wiki manually at https://wiki.archlinux.org"
        
        wiki_knowledge = "=== ARCH WIKI CONTENT ===\n\n"
        
        for page in wiki_pages[:2]:  # Get content from top 2 pages
            print(f"📖 Reading Wiki: {page['title']}...")
            content = self.fetch_wiki_content(page['title'])
            
            if content:
                wiki_knowledge += f"### {page['title']}\n"
                wiki_knowledge += f"URL: {page['url']}\n"
                wiki_knowledge += f"Content:\n{content}\n\n"
            else:
                wiki_knowledge += f"### {page['title']}\n"
                wiki_knowledge += f"URL: {page['url']}\n"
                wiki_knowledge += "(Content could not be retrieved - refer to URL)\n\n"
        
        # Add additional page links if available
        if len(wiki_pages) > 2:
            wiki_knowledge += "Additional relevant pages:\n"
            for page in wiki_pages[2:]:
                wiki_knowledge += f"- {page['title']}: {page['url']}\n"
        
        return wiki_knowledge
    
    def get_ai_response(self, user_query: str, wiki_content: str) -> str:
        """Get AI response based ONLY on Arch Wiki content"""
        system_prompt = """You are an expert Arch Linux assistant that ONLY uses information from the official Arch Wiki.

CRITICAL RULES:
1. Base ALL answers on the Arch Wiki content provided to you
2. If the Wiki content doesn't contain the answer, say "The Arch Wiki content provided doesn't cover this. Please check: https://wiki.archlinux.org"
3. When recommending commands, ONLY use commands mentioned in the Wiki content
4. Always cite which Wiki page the information comes from
5. Warn about dangerous operations (rm -rf, dd, filesystem modifications, etc.)
6. If asked about something not in the Wiki content, direct users to search the Wiki manually

RESPONSE FORMAT:
- Start with a direct answer based on Wiki content
- Include relevant commands from the Wiki with explanations
- Cite the Wiki page(s) you're referencing
- Add safety warnings if needed
- Keep responses clear and concise

Remember: You are a WIKI-BASED assistant. Never make up information or use knowledge outside the provided Wiki content."""

        full_prompt = f"""{system_prompt}

{wiki_content}

User Question: {user_query}

Provide your answer based ONLY on the Arch Wiki content above. If the Wiki content doesn't cover this question adequately, be honest and direct the user to search the Wiki manually."""

        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"❌ Error getting AI response: {str(e)}\n\nPlease check the Arch Wiki directly at: https://wiki.archlinux.org"
    
    def process_query(self, user_query: str) -> str:
        """Process a user query with Wiki content"""
        print("\n🔍 Searching Arch Wiki...")
        wiki_content = self.get_wiki_knowledge(user_query)
        
        if "No relevant Arch Wiki pages found" in wiki_content:
            return wiki_content
        
        print("🤖 Generating Wiki-based response...\n")
        response = self.get_ai_response(user_query, wiki_content)
        return response
    
    def save_to_history(self, query: str, response: str):
        """Save conversation to history"""
        history = []
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
            except:
                history = []
        
        from datetime import datetime
        history.append({
            'query': query,
            'response': response,
            'timestamp': datetime.now().isoformat()
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
        
        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)
        except:
            print("Error reading history.")
            return
        
        for entry in history[-limit:]:
            print(f"\n{'='*60}")
            print(f"Query: {entry['query']}")
            print(f"Time: {entry.get('timestamp', 'Unknown')}")
            print(f"{'-'*60}")
            print(entry['response'])
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("🐧 Arch Linux AI CLI - Interactive Mode")
        print("📚 All answers are based on official Arch Wiki content")
        print("Type 'exit' or 'quit' to leave, 'history' to see past queries")
        print("="*60)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("\nGoodbye! Stay rolling! 🚀")
                    print("Remember to check https://wiki.archlinux.org for more info!")
                    break
                
                if user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                if not user_input:
                    continue
                
                response = self.process_query(user_input)
                
                print(f"\n{'='*60}")
                print(response)
                print(f"{'='*60}")
                
                self.save_to_history(user_input, response)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! Stay rolling! 🚀")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Arch Linux AI CLI - Wiki-powered Arch Linux assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  archlinux-ai-cli -q "How do I update my system?"
  archlinux-ai-cli -i  # Interactive mode
  archlinux-ai-cli --history 5
  
Set your API key:
  export GOOGLE_AI_API_KEY="your-api-key-here"
  Or create ~/.config/archlinux-ai-cli/api_key file

Get your free API key: https://makersuite.google.com/app/apikey

All responses are based on official Arch Wiki content.
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
        response = assistant.process_query(args.query)
        print(f"\n{response}\n")
        assistant.save_to_history(args.query, response)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
