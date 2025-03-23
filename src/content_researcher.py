#importing necessary python packages 
from openai import OpenAI
import os
from typing import List, Dict, Optional
from enum import Enum
from dotenv import load_dotenv
from anthropic import Anthropic


"""Enum defining different LinkedIn post formats. An Enom (enumerator) is a class that defines a set of named constants.A way to create a group
of related values with the same constants. """
class PostFormat(Enum):
    FACTS_WITH_EMOJI = "facts_with_emoji"
    STORY_BASED = "story_based"
    GUIDE_BASED = "guide_based"
    INDUSTRY_INSIGHT = "industry_insight"


class PostConfig:
    """Configuration class for LinkedIn post parameters"""
    
    def __init__(
        self, 
        format_type: PostFormat,
        topic: str,
        length: str = "medium",
        is_customer_story: bool = False
    ):
        self.format_type = format_type
        self.topic = topic
        self.length = length
        self.is_customer_story = is_customer_story


class PostFormatter:
    """Base class for post formatting"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def format_post(self, research_content: str, config: PostConfig) -> str:
        """Abstract method to be implemented by child classes"""
        raise NotImplementedError("Subclasses must implement format_post")
        
    def revise_post(self, original_post: str, feedback: str) -> str:
        """Abstract method to be implemented by child classes"""
        raise NotImplementedError("Subclasses must implement revise_post")


class ClaudePostFormatter(PostFormatter):
    """
    Handles the formatting of research content into LinkedIn-ready posts using Claude.
    """

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.anthropic = Anthropic(api_key=api_key)

    def _create_format_prompt(self, research_content: str, config: PostConfig) -> str:
        """Create the appropriate prompt based on post format type"""
        
        base_prompt = f"""Format this research about {config.topic} into a LinkedIn post."""
        
        length_guide = {
            "short": "Keep the post concise, around 150-200 words.",
            "medium": "Aim for around 250-300 words total.",
            "long": "Create a more detailed post of around 350-450 words."
        }
        
        formats = {
            PostFormat.FACTS_WITH_EMOJI: f"""
            Structure the post exactly like this:
            
            [Title] Create an attention-grabbing headline that's insightful without being hyperbolic.
            
            [Two opening lines about the topic that provide non-obvious, slightly contrarian takes]
            
            1️⃣ [Point 1]
            2️⃣ [Point 2]
            3️⃣ [Point 3]
            4️⃣ [Point 4]
            5️⃣ [Point 5]
            
            [Two closing lines that are insightful and thought-provoking, drawing on the points above]
            
            Use exactly 4-5 emojis total throughout the post (including title). Place the emojis naturally within the text.
            {length_guide[config.length]}
            """,
            
            PostFormat.STORY_BASED: f"""
            Structure the post as a personal story or customer case study:
            
            [Opening paragraph describing a real situation or conversation that hooks the reader]
            
            💡 [Key insight 1 from the situation]
            
            🔍 [Key insight 2 with deeper analysis]
            
            ⚡ [Practical takeaway or lesson learned]
            
            [Final thought and question to engage readers]
            
            Use 3-4 emojis strategically placed throughout the post.
            {length_guide[config.length]}
            """,
            
            PostFormat.GUIDE_BASED: f"""
            Structure the post as an educational guide:
            
            **[Title framed as a guide]** 👇
            
            [Brief introduction explaining why this topic matters]
            
            🧠 [Section 1 - Definition or conceptual explanation]
            
            🤖 [Section 2 - Further explanation or comparison]
            
            ⚡ [Section 3 - Practical application]
            
            💡 [Key takeaway and why it matters]
            
            [Engaging question to prompt discussion]
            
            Use 4-5 emojis thoughtfully placed throughout the post.
            {length_guide[config.length]}
            """,
            
            PostFormat.INDUSTRY_INSIGHT: f"""
            Structure the post as an industry insight:
            
            [Title highlighting an interesting trend or observation about {config.topic}] 🍽️
            
            [Opening paragraph setting context for why this matters and mentioning data/trends]
            
            1️⃣ **[Point 1]**: [Factual insight with specific statistics]
            2️⃣ **[Point 2]**: [Factual insight with specific statistics]
            3️⃣ **[Point 3]**: [Factual insight with specific statistics]
            4️⃣ **[Point 4]**: [Factual insight with specific statistics]
            
            [Closing thought that makes readers think differently about the topic]
            
            [Question to engage audience]
            
            Use 4-5 emojis thoughtfully placed throughout the post.
            {length_guide[config.length]}
            """
        }
        
        customer_story_note = """
        Since this is based on a customer story, make sure to frame it as a real experience 
        or conversation you had with a client or prospect. Focus on the problem they faced,
        the insights you provided, and the valuable lesson that others can learn from.
        """ if config.is_customer_story else ""
        
        post_format = formats.get(config.format_type, formats[PostFormat.FACTS_WITH_EMOJI])
        
        full_prompt = f"""{base_prompt}
        
        {post_format}
        
        {customer_story_note}
        
        Return the post as plain text with proper line breaks.
        Do not include any text formatting symbols, just the plain text and emojis.
        The reader should leave feeling like they've taken in valuable insights and information.

        Here's the research:
        {research_content}"""
        
        return full_prompt

    def format_post(self, research_content: str, config: PostConfig) -> str:
        """Format research content into a LinkedIn post using Claude."""
        prompt = self._create_format_prompt(research_content, config)

        message = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return message.content[0].text.strip()
        
    def _create_revision_prompt(self, original_post: str, feedback: str) -> str:
        """Create the prompt for revising a post based on feedback"""
        return f"""I need you to revise a LinkedIn post based on specific feedback.

Original LinkedIn Post:
---
{original_post}
---

Feedback to incorporate:
---
{feedback}
---

Please provide a revised version of the post that addresses all the feedback while maintaining the overall structure and tone. 
Keep the same post format (emoji usage, sections, etc.) unless specifically requested to change in the feedback.
Return just the revised post as plain text with proper line breaks, without any additional explanation.
"""

    def revise_post(self, original_post: str, feedback: str) -> str:
        """Revise a LinkedIn post based on user feedback."""
        prompt = self._create_revision_prompt(original_post, feedback)

        message = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return message.content[0].text.strip()


class ContentResearcher:
    """Base class for content research"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def get_research(self, topic: str, stream: bool = True) -> str:
        """Abstract method to be implemented by child classes"""
        raise NotImplementedError("Subclasses must implement get_research")


class PerplexityResearcher(ContentResearcher):
    """Handles research using Perplexity AI"""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = OpenAI(
            api_key=api_key, 
            base_url="https://api.perplexity.ai"
        )

    def create_prompt(self, topic: str) -> List[Dict[str, str]]:
        """Create the message prompt for the API."""
        return [
            {
                "role": "system",
                "content": (
                    "You are an artificial intelligence assistant that provides "
                    "detailed, factual research with statistics and sources."
                ),
            },
            {   
                "role": "user",
                "content": (
                    f"Give me 5 interesting facts with stats about {topic}. "
                    "Include sources for any statistical claims. Focus on recent "
                    "and impactful data that would be engaging for a professional audience."
                ),
            },
        ]

    def get_research(self, topic: str, stream: bool = True) -> str:
        """Get research results from Perplexity API."""
        messages = self.create_prompt(topic)
        
        if stream:
            research_content = self._stream_response(messages)
        else:
            research_content = self._get_complete_response(messages)
        
        return research_content

    def _stream_response(self, messages: List[Dict[str, str]]) -> str:
        """Handle streaming response from API."""
        response_stream = self.client.chat.completions.create(
            model="sonar-pro",
            messages=messages,
            stream=True,
        )
        
        content = []
        print("Gathering research...")
        for chunk in response_stream:
            if chunk.choices[0].delta.content is not None:
                content_piece = chunk.choices[0].delta.content
                content.append(content_piece)
        
        return "".join(content)

    def _get_complete_response(self, messages: List[Dict[str, str]]) -> str:
        """Handle non-streaming response from API."""
        response = self.client.chat.completions.create(
            model="sonar-pro",
            messages=messages,
        )
        return response.choices[0].message.content


class LinkedInPostGenerator:
    """Main class that orchestrates the post generation process with feedback mechanism"""
    
    def __init__(self):
        load_dotenv()
        
        perplexity_key = os.getenv('PERPLEXITY_API_KEY')
        if not perplexity_key:
            raise ValueError("PERPLEXITY_API_KEY not found in environment variables")
            
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if not anthropic_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.researcher = PerplexityResearcher(perplexity_key)
        self.formatter = ClaudePostFormatter(anthropic_key)
    
    def get_user_preferences(self) -> PostConfig:
        """Get user preferences for the LinkedIn post"""
        
        print("\n=== LinkedIn Post Generator ===\n")
        
        topic = input("What topic would you like to create a LinkedIn post about? ")
        
        print("\nWhat format would you like for your post?")
        print("1. Facts with emojis (bullet points with emoji numbers)")
        print("2. Story-based post (customer or personal story)")
        print("3. Guide-based post (educational content)")
        print("4. Industry insight (trends with statistics)")
        
        format_choice = ""
        while format_choice not in ["1", "2", "3", "4"]:
            format_choice = input("Enter your choice (1-4): ")
        
        format_map = {
            "1": PostFormat.FACTS_WITH_EMOJI,
            "2": PostFormat.STORY_BASED,
            "3": PostFormat.GUIDE_BASED,
            "4": PostFormat.INDUSTRY_INSIGHT
        }
        
        is_customer_story = False
        if format_choice == "2":
            customer_choice = input("Is this based on a real customer story? (y/n): ").lower()
            is_customer_story = customer_choice == "y"
        
        print("\nHow long would you like your post to be?")
        print("1. Short (150-200 words)")
        print("2. Medium (250-300 words)")
        print("3. Long (350-450 words)")
        
        length_choice = ""
        while length_choice not in ["1", "2", "3"]:
            length_choice = input("Enter your choice (1-3): ")
        
        length_map = {
            "1": "short",
            "2": "medium",
            "3": "long"
        }
        
        return PostConfig(
            format_type=format_map[format_choice],
            topic=topic,
            length=length_map[length_choice],
            is_customer_story=is_customer_story
        )
    
    def generate_post(self, config: Optional[PostConfig] = None) -> str:
        """Generate the LinkedIn post based on user preferences"""
        
        if config is None:
            config = self.get_user_preferences()
        
        print(f"\nResearching about {config.topic}...")
        research_content = self.researcher.get_research(config.topic)
        
        print("\nFormatting your LinkedIn post...")
        formatted_post = self.formatter.format_post(research_content, config)
        
        return formatted_post
    
    def feedback_loop(self) -> str:
        """Run the post generation with feedback loop"""
        
        # Step 1: Generate initial post
        config = self.get_user_preferences()
        initial_post = self.generate_post(config)
        
        print("\nYour LinkedIn Post:\n")
        print(initial_post)
        
        # Step 2: Feedback loop
        while True:
            print("\n=== Post Feedback Options ===")
            print("1. Revise the post with feedback")
            print("2. Accept the post as is")
            print("3. Start over with a new post")
            
            choice = input("\nEnter your choice (1-3): ")
            
            if choice == "1":
                print("\nPlease provide your feedback and requested changes:")
                feedback = input("Feedback: ")
                
                print("\nRevising your post...")
                revised_post = self.formatter.revise_post(initial_post, feedback)
                
                print("\nRevised LinkedIn Post:\n")
                print(revised_post)
                
                initial_post = revised_post  # Update post for potential further revisions
            
            elif choice == "2":
                print("\nPost accepted. Thank you for using the LinkedIn Post Generator!")
                return initial_post
            
            elif choice == "3":
                print("\nStarting over with a new post...")
                return self.feedback_loop()  # Restart the process
            
            else:
                print("\nInvalid choice. Please try again.")


def main():
    try:
        generator = LinkedInPostGenerator()
        
        print("\n=== LinkedIn Post Generator with Feedback ===\n")
        print("This tool will help you create a LinkedIn post and refine it with your feedback.")
        
        generator.feedback_loop()
        
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()