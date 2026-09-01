import argparse, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.research import research
from tools.writer import write
from tools.images import generate_images
from tools.formatter import format_email
from tools.sender import send

def main():
    parser = argparse.ArgumentParser(description="Newsletter Automation")
    parser.add_argument("--topic", required=True, help="Newsletter topic")
    parser.add_argument("--to", default=None, help="Recipient email")
    args = parser.parse_args()
    articles = research(args.topic)
    content = write(args.topic, articles)
    images = generate_images(args.topic)
    html = format_email(args.topic, content, images)
    send(html, args.to)

if __name__ == "__main__":
    main()
