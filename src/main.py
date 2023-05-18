from dotenv import load_dotenv
from .util import send_message, get_apartments

def build_blocks(apartments):
    blocks = []
    for i, a in enumerate(apartments):
        if '2 Bedrooms, 2 Bathrooms' in a.title:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{a.title}*\n{a.des}\n{a.availability}\n{a.price}"
                }
            })
            if i < len(apartments) - 1:
                blocks.append({
                    "type": "divider"
                })
    print(f"blocks: {blocks}")
    return blocks

def main():
    apartments = get_apartments()
    send_message(build_blocks(apartments)) 

if __name__ == '__main__':
    load_dotenv()
    main()