# 🐧 Arch Linux AI CLI

An intelligent command-line assistant for Arch Linux that uses Google AI Studio (Gemini) and the official Arch Wiki to help you troubleshoot issues, learn commands, and maintain your system safely.

## ✨ Features

- 🤖 **AI-Powered Help**: Uses Google's free Gemini API for intelligent responses
- 📚 **Arch Wiki Integration**: Automatically searches and references official Arch Wiki documentation
- 🛡️ **Safety First**: Warns about dangerous operations and prioritizes system stability
- 💬 **Interactive Mode**: Chat-style interface for ongoing conversations
- 📝 **Query History**: Saves your past questions and answers
- ⚡ **Fast & Lightweight**: Python-based CLI tool with minimal dependencies

## 🚀 Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- Internet connection (for API and Wiki access)

### Install Steps

1. **Clone the repository**
```bash
git clone https://github.com/Dacraezy1/archlinux-ai-cli.git
cd archlinux-ai-cli
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Make executable**
```bash
chmod +x archlinux-ai-cli.py
```

4. **Optional: Install system-wide**
```bash
sudo cp archlinux-ai-cli.py /usr/local/bin/archlinux-ai-cli
```

## 🔑 Getting Your API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### Set Up Your API Key (Choose one method)

**Method 1: Environment Variable (Recommended)**
```bash
export GOOGLE_AI_API_KEY="your-api-key-here"
```

Add to your `~/.bashrc` or `~/.zshrc` for persistence:
```bash
echo 'export GOOGLE_AI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Method 2: Config File**
```bash
mkdir -p ~/.config/archlinux-ai-cli
echo "your-api-key-here" > ~/.config/archlinux-ai-cli/api_key
chmod 600 ~/.config/archlinux-ai-cli/api_key
```

**Method 3: Command Line Flag**
```bash
archlinux-ai-cli --api-key "your-api-key-here" -q "your question"
```

## 📖 Usage

### Single Query Mode
Ask a single question and get an answer:
```bash
archlinux-ai-cli -q "How do I update my system?"
archlinux-ai-cli -q "Why is pacman not working?"
archlinux-ai-cli -q "How to install nvidia drivers?"
```

### Interactive Mode
Start a conversation with the AI:
```bash
archlinux-ai-cli -i
```

In interactive mode:
- Type your questions and press Enter
- Type `history` to see past queries
- Type `exit` or `quit` to leave (or press Ctrl+C)

### View History
See your past questions and answers:
```bash
archlinux-ai-cli --history 5    # Show last 5 entries
archlinux-ai-cli --history 20   # Show last 20 entries
```

### Help
```bash
archlinux-ai-cli --help
```

## 🛡️ Safety Features

- **Dangerous Command Warnings**: The AI warns you before suggesting potentially risky operations
- **Wiki-Backed Answers**: Responses are grounded in official Arch Wiki documentation
- **Explanation First**: Commands are explained before you run them
- **System Stability Priority**: The AI prioritizes keeping your system stable and working

## 📁 Project Structure

```
archlinux-ai-cli/
├── archlinux-ai-cli.py    # Main application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── CONTRIBUTING.md       # Contribution guidelines
├── .gitignore           # Git ignore rules
└── setup.py             # Installation script
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly on Arch Linux
5. Submit a pull request

## 🐛 Troubleshooting

### "No API key provided" error
Make sure you've set your API key using one of the three methods above.

### "Could not search Arch Wiki" error
Check your internet connection. The tool needs to access wiki.archlinux.org.

### Import errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Permission errors
If you installed system-wide, make sure the script is executable:
```bash
sudo chmod +x /usr/local/bin/archlinux-ai-cli
```

## ⚠️ Disclaimer

This tool provides AI-generated advice based on the Arch Wiki and general Linux knowledge. Always:
- Understand commands before running them
- Have backups of important data
- Test in a safe environment when possible
- Refer to official Arch Wiki for critical operations
- Use your judgment - the AI can make mistakes

## 📜 License

[Your chosen license - you mentioned you have this already]

## 🙏 Acknowledgments

- [Arch Linux](https://archlinux.org/) and the [Arch Wiki](https://wiki.archlinux.org/) community
- [Google AI Studio](https://makersuite.google.com/) for providing free API access
- All contributors and users of this tool

---

**Made with ❤️ for the Arch Linux community**

*Stay rolling! 🚀*
