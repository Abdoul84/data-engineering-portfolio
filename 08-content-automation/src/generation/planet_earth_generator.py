"""
Planet Earth Parody Script Generator

Generates randomized dark humor scripts in the style of BBC's Planet Earth,
explaining why Earth is "not recommended" for vacation.
"""

import random
import json
from datetime import datetime, timezone
from typing import Dict, List


class PlanetEarthGenerator:
    """Generates Planet Earth parody content with dark humor."""
    
    ANIMALS = [
        'lion', 'shark', 'elephant', 'penguin', 'eagle', 'crocodile', 
        'hyena', 'orca', 'tiger', 'polar bear', 'komodo dragon', 
        'blue whale', 'cheetah', 'octopus', 'snow leopard', 'grizzly bear',
        'anaconda', 'leopard seal', 'honey badger', 'mantis shrimp',
        'saltwater crocodile', 'harpy eagle', 'wolverine', 'jaguar',
        'great white shark', 'spotted hyena', 'king cobra', 'african buffalo'
    ]
    
    LOCATIONS = [
        'African savanna', 'deep ocean trenches', 'Himalayan peaks', 
        'Antarctic ice floes', 'Australian outback', 'Amazon canopy',
        'Sahara dunes', 'Great Barrier Reef', 'Arctic tundras', 
        'Borneo rainforests', 'Yellowstone caldera', 'Patagonian glaciers',
        'Scottish highlands', 'Galápagos islands', 'Mongolian steppes',
        'Congo Basin', 'Serengeti plains', 'Indonesian coral reefs',
        'Rocky Mountain ranges', 'Madagascar forests', 'Namib Desert',
        'Norwegian fjords', 'Chilean Andes', 'Siberian taiga'
    ]
    
    REASONS = [
        'it devours prey with the enthusiasm of a Black Friday sale, leaving zero room for polite picnics',
        'it transforms serenity into a crime scene faster than you can say "vacation photos"',
        'survival here demands skills no travel brochure mentions—like outrunning certain death',
        'nature\'s hospitality involves teeth, claws, and a shocking disregard for guests',
        'the local cuisine consists primarily of you, served raw and without garnish',
        'every sunset is a countdown to something hungry waking up',
        'the wildlife here treats tourists like an all-you-can-eat buffet',
        'peaceful coexistence is a myth told by those who\'ve never been lunch',
        'it hunts with the precision of a tax auditor and the mercy of a parking ticket',
        'the scenery is breathtaking—mainly because predators chase the breath right out of you',
        'evolution blessed it with weapons nature intended for maximum carnage',
        'it views human visitors as slow, confused protein delivery systems',
        'the ecosystem operates on a strict "eat or be eaten" policy with no exceptions',
        'it demonstrates why apex predators don\'t need Yelp reviews',
        'nature\'s brutality here makes horror films look like children\'s cartoons',
        'survival odds drop faster than your travel insurance coverage',
        'it reminds us that Earth\'s food chain has no customer service department',
        'the local residents settled all disputes with violence millions of years ago',
        'it proves Darwin was right—and terrifyingly efficient',
        'paradise here comes with teeth, venom, or crushing force as standard features'
    ]
    
    def __init__(self):
        """Initialize the generator."""
        random.seed()
    
    def generate_content(self) -> Dict[str, str]:
        """
        Generate a complete piece of content with script, caption, and visual prompt.
        
        Returns:
            Dict containing script, caption, visual_prompt, animal, location, and metadata
        """
        animal = random.choice(self.ANIMALS)
        location = random.choice(self.LOCATIONS)
        reason = random.choice(self.REASONS)
        
        # Generate the dramatic voiceover script
        script = (
            f"In the unforgiving {location}, the majestic {animal} reveals why "
            f"Planet Earth is no vacation spot. Behold as {reason}. "
            f"I would not recommend this blue marble—unless you fancy a front-row seat "
            f"to nature's unfiltered chaos. Proceed... if you dare."
        )
        
        # Generate social media caption with hashtags
        caption = (
            f"🌍 Why I Wouldn't Recommend Planet Earth: {animal.title()} Edition\n\n"
            f"{reason.split(',')[0]}... 😈\n\n"
            f"#PlanetEarthParody #WhyNotRecommend #NatureHorror #AttenboroughVibes "
            f"#Wildlife #DarkHumor #NatureDocumentary #BBCEarth #TikTokNature "
            f"#{animal.replace(' ', '')}Facts"
        )
        
        # Generate visual prompt for video composition
        visual_prompt = (
            f"Dramatic slow-motion footage of a {animal} in {location.lower()}, "
            f"with cinematic BBC-style graphics. Text overlay: 'NOT RECOMMENDED' in bold red. "
            f"Dark, ominous atmosphere like a nature horror trailer. High contrast, desaturated colors."
        )
        
        return {
            'script': script,
            'caption': caption,
            'visual_prompt': visual_prompt,
            'animal': animal,
            'location': location,
            'reason': reason,
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'video_duration': 30  # Target duration in seconds
        }
    
    def generate_batch(self, count: int = 5) -> List[Dict[str, str]]:
        """
        Generate multiple pieces of content.
        
        Args:
            count: Number of content pieces to generate
            
        Returns:
            List of content dictionaries
        """
        return [self.generate_content() for _ in range(count)]
    
    def to_json(self, content: Dict[str, str], pretty: bool = True) -> str:
        """
        Convert content to JSON string.
        
        Args:
            content: Content dictionary
            pretty: Whether to pretty-print the JSON
            
        Returns:
            JSON string
        """
        indent = 2 if pretty else None
        return json.dumps(content, indent=indent, ensure_ascii=False)


def main():
    """CLI entry point for testing."""
    generator = PlanetEarthGenerator()
    
    print("🌍 Planet Earth Parody Generator\n")
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
    print(f"Animal: {content['animal']}")
    print(f"Location: {content['location']}")
    print(f"Generated: {content['generated_at']}")
    print(f"Duration: {content['video_duration']}s")
    
    print("\n\n💾 JSON OUTPUT:")
    print("-" * 80)
    print(generator.to_json(content))


if __name__ == "__main__":
    main()

