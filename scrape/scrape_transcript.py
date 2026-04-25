import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright
import time

BASE_URL = "https://transcripts.foreverdreaming.org"
# Season 5 forum (change forum ID for different seasons)
FORUM_URL = f"{BASE_URL}/viewforum.php?f=2882&start=78"  # Season 5
OUTPUT_DIR = Path(__file__).parent / "transcripts"
OUTPUT_DIR.mkdir(exist_ok=True)


async def solve_challenge(page):
    """Wait for the Anubis challenge to be solved"""
    print("Waiting for challenge to be solved...")
    try:
        # Wait for navigation to complete after challenge
        await page.wait_for_load_state("networkidle", timeout=30000)
        # Additional wait to ensure the page is fully loaded
        await asyncio.sleep(2)
        print("Challenge solved!")
    except Exception as e:
        print(f"Challenge timeout or error: {e}")


async def get_episode_links(page):
    """Get all episode links from the season 6 forum"""
    print(f"Navigating to forum: {FORUM_URL}")
    await page.goto(FORUM_URL)
    
    # Solve the challenge if present
    await solve_challenge(page)
    
    # Wait for the forum page to load
    await page.wait_for_selector("a.topictitle", timeout=10000)
    
    # Get all topic links
    topic_links = await page.locator("a.topictitle").all()
    episodes = []
    
    for link in topic_links:
        title = await link.text_content()
        href = await link.get_attribute("href")
        if href and title:
            full_url = f"{BASE_URL}/{href}" if not href.startswith("http") else href
            episodes.append({"title": title.strip(), "url": full_url})
    
    print(f"Found {len(episodes)} episodes")
    return episodes


async def scrape_transcript(page, episode):
    """Scrape the transcript content from an episode page"""
    print(f"Scraping: {episode['title']}")
    
    await page.goto(episode["url"])
    await solve_challenge(page)
    
    # Wait for content to load
    await page.wait_for_selector(".content", timeout=10000)
    
    # Get the transcript content
    content = await page.locator(".content").inner_text()
    
    # Clean up the content
    content = re.sub(r'\s+', ' ', content).strip()
    
    return content


async def main():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            # Get all episode links
            episodes = await get_episode_links(page)
            
            if not episodes:
                print("No episodes found!")
                return
            
            # Scrape each episode
            all_transcripts = []
            
            for i, episode in enumerate(episodes, 1):
                print(f"\n[{i}/{len(episodes)}] Processing: {episode['title']}")
                
                # Generate safe filename
                safe_title = re.sub(r'[^\w\s-]', '', episode['title']).strip()
                safe_title = re.sub(r'[-\s]+', '_', safe_title)
                output_file = OUTPUT_DIR / f"{safe_title}.txt"
                
                # Check if file already exists
                if output_file.exists():
                    print(f"Already exists, skipping: {output_file}")
                    # Read existing transcript
                    with open(output_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    all_transcripts.append({
                        "title": episode['title'],
                        "content": content
                    })
                    continue
                
                try:
                    transcript = await scrape_transcript(page, episode)
                    
                    # Save individual transcript
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"Episode: {episode['title']}\n")
                        f.write(f"URL: {episode['url']}\n")
                        f.write("=" * 80 + "\n\n")
                        f.write(transcript)
                    
                    print(f"Saved to: {output_file}")
                    
                    # Add to combined list
                    all_transcripts.append({
                        "title": episode['title'],
                        "content": transcript
                    })
                    
                    # Small delay between requests
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f"Error scraping {episode['title']}: {e}")
                    continue
            
            # Create combined transcript file
            if all_transcripts:
                combined_file = OUTPUT_DIR / "season6_combined.txt"
                with open(combined_file, 'w', encoding='utf-8') as f:
                    for item in all_transcripts:
                        f.write(f"Episode: {item['title']}\n")
                        f.write("=" * 80 + "\n\n")
                        f.write(item['content'])
                        f.write("\n\n" + "=" * 80 + "\n\n")
                
                print(f"\nCombined transcript saved to: {combined_file}")
            
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
