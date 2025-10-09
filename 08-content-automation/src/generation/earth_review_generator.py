"""
Earth: 1-Star Review Generator

Generates satirical reviews of planet Earth focusing on human civilization,
geopolitics, social media, and modern chaos - much funnier than animal parodies!
"""

import random
import json
from datetime import datetime, timezone
from typing import Dict, List


class EarthReviewGenerator:
    """Generates satirical 1-star reviews of Earth's human civilization."""
    
    TOPICS = [
        'social media addiction',
        'climate change denial',
        'political polarization',
        'wealth inequality',
        'geopolitical conflicts',
        'conspiracy theories',
        'influencer culture',
        'corporate greed',
        'misinformation campaigns',
        'tribal warfare online',
        'algorithm manipulation',
        'reality TV obsession',
        'cancel culture',
        'echo chambers',
        'attention economy',
        'surveillance capitalism',
        'fake news epidemic',
        'doom scrolling',
        'outrage addiction',
        'performative activism',
        'crypto scams',
        'NFT mania',
        'hustle culture burnout',
        'parasocial relationships'
    ]
    
    LOCATIONS = [
        'Twitter/X headquarters',
        'Capitol Hill',
        'Wall Street trading floors',
        'Silicon Valley offices',
        'United Nations assemblies',
        'Mar-a-Lago estates',
        'Davos economic forums',
        'Beijing government buildings',
        'Moscow Kremlin halls',
        'Gaza conflict zones',
        'Amazon warehouses',
        'Meta headquarters',
        'TikTok content farms',
        'Cable news studios',
        'Reddit moderator rooms',
        'YouTube algorithm labs',
        'Instagram influencer hubs',
        'LinkedIn thought leader feeds',
        'Discord server wars',
        'Telegram conspiracy groups'
    ]
    
    REASONS = [
        'humans spend more time arguing with strangers online than talking to family',
        'the species invented social media just to make themselves miserable on purpose',
        'world leaders tweet policy decisions like teenagers having a meltdown',
        'billionaires race to Mars while Earth burns and nobody finds this ironic',
        'humans created algorithms that radicalize grandparents faster than cults ever could',
        'the dominant species willingly surrendered their attention spans to 15-second videos',
        'influencers peddle detox teas while Rome quite literally burns',
        'humans invented fact-checkers then refused to believe fact-checkers',
        'the civilization peaked at landing on the moon then devolved into flat-earth debates',
        'world wars are now fought with memes and misinformation campaigns',
        'humans chose to destroy their habitat for quarterly earnings reports',
        'the species invented democracy then spent it all on culture wars',
        'billionaires pay less taxes than teachers and everyone just accepts this',
        'humans created artificial intelligence then got mad when it reflected their biases',
        'the species documented their own extinction on Instagram stories',
        'world leaders hold nuclear codes but can\'t figure out how to mute themselves on Zoom',
        'humans invented renewable energy then chose to argue about it instead',
        'the civilization has infinite information at their fingertips but prefers conspiracy theories',
        'humans created dating apps that make everyone more lonely and depressed',
        'the species measures self-worth in likes, shares, and follower counts'
    ]
    
    SCRIPTURES = [
        ('Ecclesiastes 1:9', 'What has been will be again, what has been done will be done again; there is nothing new under the sun'),
        ('Proverbs 16:18', 'Pride goes before destruction, a haughty spirit before a fall'),
        ('Matthew 6:24', 'No one can serve two masters... You cannot serve both God and money'),
        ('James 4:1', 'What causes fights and quarrels among you? Don\'t they come from your desires that battle within you?'),
        ('1 Timothy 6:10', 'For the love of money is a root of all kinds of evil'),
        ('Proverbs 29:18', 'Where there is no vision, the people perish'),
        ('Matthew 24:12', 'Because of the increase of wickedness, the love of most will grow cold'),
        ('2 Timothy 3:2', 'People will be lovers of themselves, lovers of money, boastful, proud, abusive'),
        ('Ecclesiastes 3:1', 'There is a time for everything, and a season for every activity under the heavens'),
        ('Proverbs 22:16', 'One who oppresses the poor to increase his wealth will end in poverty'),
        ('Luke 12:15', 'Watch out! Be on your guard against all kinds of greed'),
        ('Proverbs 14:12', 'There is a way that appears to be right, but in the end it leads to death'),
        ('Matthew 7:5', 'You hypocrite, first take the plank out of your own eye'),
        ('Ecclesiastes 5:10', 'Whoever loves money never has enough; whoever loves wealth is never satisfied'),
        ('James 1:19', 'Everyone should be quick to listen, slow to speak and slow to become angry'),
        ('Proverbs 18:2', 'Fools find no pleasure in understanding but delight in airing their own opinions'),
        ('1 Corinthians 13:11', 'When I was a child, I talked like a child, I thought like a child, I reasoned like a child'),
        ('Matthew 23:27', 'You are like whitewashed tombs, which look beautiful on the outside but on the inside are full of bones')
    ]
    
    def __init__(self):
        """Initialize the generator."""
        random.seed()
    
    def generate_content(self) -> Dict[str, str]:
        """
        Generate a complete satirical review of Earth.
        
        Returns:
            Dict containing script, caption, visual_prompt, and metadata
        """
        topic = random.choice(self.TOPICS)
        location = random.choice(self.LOCATIONS)
        reason = random.choice(self.REASONS)
        scripture_ref, scripture_text = random.choice(self.SCRIPTURES)
        
        # Generate the satirical voiceover script
        script = (
            f"Welcome to Earth, where in {location}, humanity demonstrates why this planet "
            f"deserves one star out of five. Observe as {reason}. "
            f"The ancient wisdom of {scripture_ref} warned us: '{scripture_text}.' "
            f"But did we listen? Of course not. "
            f"I would not recommend this civilization—unless you enjoy watching a species "
            f"voluntarily stumble toward its own obsolescence while filming it for content. "
            f"Visit at your own existential risk."
        )
        
        # Generate social media caption
        caption = (
            f"🌍 Earth: 1-Star Review - {topic.title()} Edition\n\n"
            f"{reason} 😬\n\n"
            f"📖 {scripture_ref}: \"{scripture_text}\"\n\n"
            f"Welcome to humanity's self-made chaos. Not recommended. ⭐️\n\n"
            f"#EarthReview #OneStarPlanet #HumanityParody #GeopoliticalHumor "
            f"#SocialMediaSatire #DarkHumor #ModernLife #ChristianHumor "
            f"#BibleVerse #WakeUpCall #SystemicChaos #Truth"
        )
        
        # Generate visual prompt
        visual_prompt = (
            f"News footage or stock video showing {topic} in {location}. "
            f"Cinematic documentary style. Text overlay: '⭐️ 1/5 STARS - NOT RECOMMENDED' in bold. "
            f"Satirical news broadcast aesthetic. High contrast, professional grade."
        )
        
        return {
            'script': script,
            'caption': caption,
            'visual_prompt': visual_prompt,
            'topic': topic,
            'location': location,
            'reason': reason,
            'scripture_ref': scripture_ref,
            'scripture_text': scripture_text,
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'video_duration': 30
        }
    
    def generate_batch(self, count: int = 5) -> List[Dict[str, str]]:
        """Generate multiple pieces of content."""
        return [self.generate_content() for _ in range(count)]
    
    def to_json(self, content: Dict[str, str], pretty: bool = True) -> str:
        """Convert content to JSON string."""
        indent = 2 if pretty else None
        return json.dumps(content, indent=indent, ensure_ascii=False)


def main():
    """CLI entry point for testing."""
    generator = EarthReviewGenerator()
    
    print("🌍 Earth: 1-Star Review Generator\n")
    print("=" * 80)
    
    content = generator.generate_content()
    
    print("\n📝 VOICEOVER SCRIPT:")
    print("-" * 80)
    print(content['script'])
    
    print("\n\n📱 SOCIAL MEDIA CAPTION:")
    print("-" * 80)
    print(content['caption'])
    
    print("\n\n🎬 VISUAL PROMPT:")
    print("-" * 80)
    print(content['visual_prompt'])
    
    print("\n\n📊 METADATA:")
    print("-" * 80)
    print(f"Topic: {content['topic']}")
    print(f"Location: {content['location']}")
    print(f"Scripture: {content['scripture_ref']}")
    print(f"Generated: {content['generated_at']}")
    
    print("\n\n💾 JSON OUTPUT:")
    print("-" * 80)
    print(generator.to_json(content))


if __name__ == "__main__":
    main()

