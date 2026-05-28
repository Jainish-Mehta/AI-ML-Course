import requests

class JokeFetcher:
    
    def __init__(self, name):
        self.username = name
        self.api_url = "https://official-joke-api.appspot.com/random_joke"
        print(f"System Initialized. Welcome, {self.username}!")
        
    def get_joke(self):
        print("Fetching a joke for you...")
        
        response = requests.get(self.api_url)
        
        if response.status_code == 200:
            data = response.json()
            print("\n--- Here's a joke for you ---")
            print(f"Setup: {data['setup']}")
            print(f"Punchline: {data['punchline']}")
            print("-----------------------------")
        else:
            print("Failed to Fetch Joke")
            
if __name__ == "__main__":
    my_joke = JokeFetcher(name='ABCD')
    print("How many jokes do you want to hear?")
    num = int(input("Enter a number: "))
    for i in range(num):  
        print(f"\nJoke {i+1}:")  
        my_joke.get_joke()