# LinkedIn Post Generator

A Python tool that automatically creates engaging LinkedIn posts on any topic by combining AI-powered research with professionally formatted templates.

## Overview

This tool helps you create polished LinkedIn posts without the hassle of research or formatting. Simply choose a topic, select a post style, and the tool will:

1. Research your topic using Perplexity AI to gather relevant facts and statistics
2. Format this research into a LinkedIn-ready post using Claude AI
3. Present you with a finished post that's ready to share

## Features

- **Four post formats**: Facts with emojis, story-based, guide-based, or industry insight
- **Customisable length**: Choose from short, medium, or long posts
- **Customer story options**: Special formatting for posts based on customer experiences
- **AI-powered research**: Automatically gathers relevant facts and statistics
- **Professional formatting**: Structures content in engaging, LinkedIn-optimised layouts

## Requirements

- Python 3.6+
- OpenAI Python package
- Anthropic Python package
- python-dotenv

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/linkedin-post-generator.git
cd linkedin-post-generator
```

2. Install the required packages:
```bash
pip install openai anthropic python-dotenv
```

3. Create a `.env` file in the project directory with your API keys:
```
PERPLEXITY_API_KEY=your_perplexity_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## Usage

Run the tool with:
```bash
python main.py
```

Follow the prompts to:
1. Enter the topic for your LinkedIn post
2. Select a post format
3. Choose the post length
4. Indicate if it's based on a customer story (for story-based posts)

The tool will then:
1. Research your topic
2. Format the post
3. Display the finished post ready to copy and paste into LinkedIn

## Example

```
=== LinkedIn Post Generator ===

What topic would you like to create a LinkedIn post about? AI in healthcare

What format would you like for your post?
1. Facts with emojis (bullet points with emoji numbers)
2. Story-based post (customer or personal story)
3. Guide-based post (educational content)
4. Industry insight (trends with statistics)
Enter your choice (1-4): 4

How long would you like your post to be?
1. Short (150-200 words)
2. Medium (250-300 words)
3. Long (350-450 words)
Enter your choice (1-3): 2

Researching about AI in healthcare...
Formatting your LinkedIn post...

Your LinkedIn Post:

[Post content appears here]
```

## API Keys

To use this tool, you'll need:
1. A Perplexity API key - Get one at https://www.perplexity.ai/api
2. An Anthropic API key - Get one at https://console.anthropic.com/

