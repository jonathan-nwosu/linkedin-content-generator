# LinkedIn Post Generator with AI Research

A Python-based tool that automatically generates professional LinkedIn posts by combining AI research and formatting capabilities. The script asks the user what kind of post they would like by asking the following questions: 

1. What topic the agent should research
2. The structure of the post and style of the post 
3. Length of the post 

## Features
- AI-powered research using Perplexity AI
- Professional post formatting with Claude
- Automated post structure with emojis
- Secure API handling

## Setup

1. Install dependencies:

`pip install openai anthropic python-dotenv`

2. Create .env file:

`PERPLEXITY_API_KEY=your_key_here`

`ANTHROPIC_API_KEY=your_key_here`

## Structure

PerplexityResearcher: Handles research via Perplexity AI

LinkedInPostFormatter: Formats posts using Claude

## Requirements

Python 3.8+

Perplexity AI API key

Anthropic API key

## Troubleshooting

Check API keys in .env
Verify internet connection
Ensure all dependencies are installed
