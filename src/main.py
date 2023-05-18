from dotenv import load_dotenv
from .util import send_message, get_apartments

def main():
    # send_message('hello') 
    apartments = get_apartments()
    print(apartments)

if __name__ == '__main__':
    load_dotenv()
    main()