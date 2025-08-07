import random

def determine_winner(player, computer):
    if player == computer:
        return "It's a tie!"
    elif (player == "Rock" and computer == "Scissors") or \
         (player == "Paper" and computer == "Rock") or \
         (player == "Scissors" and computer == "Paper"):
        return "You win!"
    else:
        return "Computer wins!"

def play_game():
    choices = ["Rock", "Paper", "Scissors"]
    score = {"Player": 0, "Computer": 0}

    while True:
        print("\n--- Rock, Paper, Scissors ---")
        player_input = input("Choose your move (Rock, Paper, Scissors): ").strip().capitalize()

        if player_input not in choices:
            print("Invalid choice! Please choose Rock, Paper, or Scissors.")
            continue

        computer_choice = random.choice(choices)
        print(f"\nYou chose: {player_input}")
        print(f"Computer chose: {computer_choice}")

        result = determine_winner(player_input, computer_choice)
        print(result)

        if "You win" in result:
            score["Player"] += 1
        elif "Computer wins" in result:
            score["Computer"] += 1

        print(f"Score → You: {score['Player']} | Computer: {score['Computer']}")

        again = input("\nPlay again? (yes/no): ").strip().lower()
        if again not in ["yes", "y"]:
            print("\nThanks for playing! Final score:")
            print(f"You: {score['Player']} | Computer: {score['Computer']}")
            break

play_game()
