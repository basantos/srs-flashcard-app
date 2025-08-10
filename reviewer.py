import csv
import time
import main as m
import subprocess as sp

def ask_random_review():
    try:
        reply = None
        while reply != 'Y' and reply != 'N':
            reply = input("Do you want to review your cards in random order? (Y/N)").capitalize()
            if reply != 'Y' and reply != 'N':
                print('Invalid input. Please try again.')
        return reply
    except KeyboardInterrupt:
        return 'cancel'

def start_review(set):
    response = ask_random_review()
    cards = get_due_cards(set)
    if response == 'cancel':
        m.show_set(set)
    if response == 'Y':
        cards = randomize_due_cards(cards)

    reviewed = []
    for card in cards:
        curr = [card[0], int(card[4])] # add front of card and current card level

        print("------------------------------------------\n\treviewing " + set + "\n------------------------------------------")
        print("Press ctrl+c at anytime to exit.")
        print()
        print(card[0])
        print('Hint: ' + card[3])
        print()
        print("---------------------\n")
        try:
            user_answer = input("Input your answer: ")
        except KeyboardInterrupt:
            break
        check_answer(card[1], user_answer)
        print("The answer is " + card[1])
        score = int(input("---------------------\n0: not at all | 1: a little bit | 2: definitely\nHow well do you know this card?"))
        curr.append(score)
        reviewed.append(curr)

    if reviewed != []:
        update_next_review_datetime(reviewed, set)
    m.any_key_to_return("\nReview complete! Hit any key to return.")


def get_cards(set):
    file = set + '.csv'

    with open(file, 'r') as f:
        reader = csv.reader(f)
        cards = []
        for row in reader:
            row[5] = row[5] + '\n'
            cards.append(row)
    return cards

def get_due_cards(set):
    cards = get_cards(set)
    path = '../reviews-due-checker'
    with open(path+'/reviews-due-checker.txt', 'w') as f:
        for card in cards:
            f.write(','.join(card))

    time.sleep(5)

    with open(path+'/reviews-due-checker.txt', 'r') as f:
        cards = f.readlines()
        due_cards = []
        for card in cards:
            due_cards.append(card.split(','))
    return due_cards

def randomize_due_cards(due_cards):
    with open('..\\randomize-list\\randomize-list.txt', 'w') as f:
        for card in due_cards:
            f.write(','.join(card))

    time.sleep(3)

    with open('..\\randomize-list\\randomize-list.txt', 'r') as f:
        cards = f.readlines()
        due_cards = []
        for card in cards:
            due_cards.append(card.split(','))
    return due_cards

def update_next_review_datetime(list_of_cards, set):
    input_path = '..\\Spaced-Repition-Flashcard-Microservice-A'
    with open('FlashcardData Microservice Input\\Flashcard Data.txt', 'w') as f:
        f.write('front of card,level,score\n')
        for card in list_of_cards:
            f.write(card[0] + ',' + str(card[1]) + ',' + str(card[2]) + '\n')

    sp.run(["python", input_path + '\\CreateReviewDate.py'])

    original_cards = get_cards(set)
    clear_csv(set + '.csv')
    with open('FlashcardData Microservice Output/processed_Flashcard Data.txt', 'r') as f:
        reviewed_cards = f.readlines()
        for original_card in original_cards:
            for reviewed_card in reviewed_cards:
                reviewed_card = reviewed_card.split(',')
                if original_card[0] == reviewed_card[0]:
                    original_card[4] = reviewed_card[3]  # update level
                    original_card[5] = reviewed_card[4] # update review due datetime
                    break
    update_set_file(set, original_cards)

def update_set_file(set, new_data):
    with open(set+'.csv', 'w') as f:
        for row in new_data:
            f.write(','.join(row))

def clear_csv(file):
    with open(file, 'w') as f:
        f.write('')

def check_answer(correct, user_answer):
    path = '../input-checker/input-checker.txt'
    with open(path, 'w') as f:
        f.write(correct + '\n' + user_answer)

    time.sleep(5)

    with open(path, 'r') as f:
        score = f.read()
        print(f'---------------------\nYour answer is {score} correct.')
