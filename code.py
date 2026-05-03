import wikipediaapi

def get_summary(topic):
    wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent='wiki-summarizer/1.0'
    )

    page = wiki.page(topic)

    if not page.exists():
        print(f"\n No Wikipedia page found for '{topic}'. Try a different keyword.\n")
        return

    # Split into sentences and grab first 3
    sentences = page.summary.split('. ')
    summary = '. '.join(sentences[:3]) + '.'

    print(f"\n {page.title}")
    print("-" * 40)
    print(summary)
    print(f"\n Read more: {page.fullurl}\n")

# Main loop
while True:
    topic = input("Search Wikipedia (or type 'quit'): ").strip()
    if topic.lower() == 'quit':
        break
    if topic:
        get_summary(topic)
