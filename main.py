import time

allowed_words = []
possible_answers = []

def init_lists():

    #builds list variables from txt files of possible words

    allowed_words_file = open('words/wordle-allowed-guesses.txt','r')
    possible_answers_file = open('words/wordle-answers-alphabetical.txt','r')
    for line in allowed_words_file:
        allowed_words.append(line.strip())
    for line in possible_answers_file:
        possible_answers.append(line.strip())
    allowed_words_file.close()
    possible_answers_file.close()

init_lists()
total_list = possible_answers + allowed_words
remaining_answers = possible_answers

def is_valid_guess(guess):

    #returns true if the proposed word is a possible guess

    is_valid = False
    for word in total_list:
        if guess == word: is_valid = True
    return is_valid

def is_valid_results(results):

    #checks if the proposed results are valid

    is_valid = 0
    for char in str(results):
        if char == '0' or char == '1' or char == '2': is_valid += 1
    if is_valid == 5 and len(results) == 5: return True
    else: return False

def check_if_possible_answer(word,guess,results):

    #checks if a certain word aligns with combination of guess and results

    possible = True
    index = 0
    for digit in results:
        if digit == '0':
            for char in word:
                if char == guess[index]:
                    possible = False
        elif digit == '1':
            number_of_characters = 0
            for char in word:
                if char == guess[index]:
                    number_of_characters += 1
            if number_of_characters < 1 or guess[index] == word[index]:
                possible = False

        elif digit == '2':
            if word[index] != guess[index]:
                possible = False
        index += 1
    return possible

def get_results(word,guess):

    #returns the results for a combination of two words

    results = ''
    index = 0
    for char in guess:
        results_addition = ''
        for i in word:
            if i == char:
                results_addition = '1'
        if char == word[index]:
            results_addition = '2'
        elif results_addition != '1':
            results_addition = '0'
        results += results_addition 
        index += 1
    return results
        
def count_eligible_answers(guess,results,answers_left):

    #counts the total number of eligible answers for the proposed guess and results

    total = 0
    for word in answers_left:
        if check_if_possible_answer(word,guess,results):
            total += 1
    return total

def make_remaining_answers(guess,results,answers_left):

    #returns a list of the remaining possible answers

    temp_list = []
    for word in answers_left:
        if check_if_possible_answer(word,guess,results):
            temp_list.append(word)
    return temp_list

def find_dict_lowest_key(dct):

    #finds the key which holds the lowest value in a dictionary

    lowest = 1000
    lowest_key = 'none'

    for key in dct:

        if dct[key] < lowest:

            lowest = dct[key]
            lowest_key = key
    
    if len(lowest_key) < 5: return 'no possible answers, you made a mistake'
    else: return lowest_key


def main():

    remaining_answers = possible_answers

    print('\n\n----> Recommended Guess (round 1): raise\n')
    start_time = time.time()

    for row in range(6):

        #asks for guess input and makes sure it's valid

        guess = input('Enter your guess: ')
        while not is_valid_guess(guess):

            if guess == 'exit':
                break
            else:
                guess = input('Invalid, re-enter your guess: ')

        #asks for result input and makes sure it's valid

        result = input('Enter your results: ')
        print('')
        while not is_valid_results(result):

            if result == 'exit':
                break
            else:
                result = input('Invalid, re-enter your results: ')

        #stops the system if the user wants to exit

        if guess == 'exit' or result == 'exit' or result == '22222':
            break
        
        remaining_answers = make_remaining_answers(guess,result,remaining_answers)

        average_information_dict = {}

        #this process figures out the average amount of possible answers yielded by each guess and forms a dictionary of this information

        for guess in total_list: #changing total_list to possible_answers makes it run faster but less accurately

            time_remaining = ((time.time()-start_time) * (len(total_list)/(total_list.index(guess)+1))) - (time.time()-start_time)
            print(f'----> Progress: {(-(len(total_list)-total_list.index(guess)*100)/len(total_list))+1:.2f} % | {time_remaining/60:.2f} minutes remaining | current: ' + guess + ' | best: ' + find_dict_lowest_key(average_information_dict) + '                                                                ', end = '\r') #changing total_list to possible_answers makes it run faster but less accurately
            
            possible_answers_before_average = 0

            for word in remaining_answers:

                temp_results = get_results(word,guess)
                possible_answers_before_average += count_eligible_answers(guess,temp_results,remaining_answers)
            
            average_information_dict[guess] = possible_answers_before_average/len(remaining_answers)
        
        print('----> Progress: 100%                                                                                     \n\n-----------------------------------------------------------------------------\n')
        print('----> Recommended Guess (round ' + str(row+2) + '): ' + find_dict_lowest_key(average_information_dict) + '\n')
        
        if len(remaining_answers) == 1:
            print('The answer is ' + remaining_answers[0] + '\n')

main()