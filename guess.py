import random
import json

SCORES_FILE="scores.json"

# name, low, high, max guesses
DIFFICULTIES={
  "1":("Easy",1,10,5),
  "2":("Medium",1,100,8),
  "3":("Hard",1,1000,12),
}


# Chunk 1: get a valid number from the user
def get_guess(low,high):
  while True:
    raw=input(f"Enter your guess ({low}-{high}): ")

    try:
      guess=int(raw)
    except ValueError:
      print("That's not a whole number, try again")
      continue

    if guess<low or guess>high:
      print("Value is out of bounds, try again")
      continue

    return guess


# Chunk 2 + 6: play one round with a guess limit
def play_round(low,high,max_attempts):
  secret=random.randint(low,high)
  attempts=0

  print(f"I am thinking of a number between {low} and {high}. You have {max_attempts} guesses.")

  while attempts<max_attempts:
    guess=get_guess(low,high)
    attempts+=1

    if guess==secret:
      print(f"You got it right in {attempts} attempts")
      return attempts
    elif guess<secret:
      print("Too low")
    else:
      print("Too high")

    left=max_attempts-attempts
    if left>0:
      print(f"Guesses left: {left}")

  print(f"Out of guesses! The number was {secret}.")
  return None


# Chunk 3: play again
def ask_play_again():
  while True:
    answer=input("Want to play again? (y/n): ").strip().lower()

    if answer=="y":
      return True
    elif answer=="n":
      return False
    else:
      print("Please type y or n")


# Chunk 4: difficulty levels
def choose_difficulty():
  print("\nChoose difficulty:")
  for key,(name,low,high,max_attempts) in DIFFICULTIES.items():
    print(f"  {key}. {name} ({low}-{high}, {max_attempts} guesses)")

  while True:
    choice=input("Enter 1, 2 or 3: ").strip()

    if choice in DIFFICULTIES:
      return DIFFICULTIES[choice]

    print("Please type 1, 2 or 3")


# Chunk 5: saving and loading best scores
def load_scores():
  try:
    with open(SCORES_FILE,"r") as f:
      return json.load(f)
  except (FileNotFoundError,json.JSONDecodeError):
    return {}


def save_scores(scores):
  with open(SCORES_FILE,"w") as f:
    json.dump(scores,f,indent=2)


def main():
  print("Welcome to the number guessing game")

  total_rounds=0
  best_scores=load_scores()

  while True:
    name,low,high,max_attempts=choose_difficulty()
    attempts=play_round(low,high,max_attempts)
    total_rounds+=1

    if attempts is not None:
      best=best_scores.get(name)
      if best is None or attempts<best:
        best_scores[name]=attempts
        save_scores(best_scores)
        print(f"New best score on {name}: {attempts}")

    if not ask_play_again():
      break

  print(f"\nThanks for playing! Rounds played: {total_rounds}")
  for level,score in best_scores.items():
    print(f"  Best on {level}: {score}")


if __name__=="__main__":
  main()