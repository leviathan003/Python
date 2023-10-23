import time
import random

def errors(test,user_in):
    error_count=0
    try:
        for i in range(len(test)):
            if test[i] != user_in[i]:
                error_count+=1
        return error_count
    except:
        return error_count+(len(test)-i)

def speed(s_time,e_time,user_in):
    time_taken = e_time-s_time
    actual_time = round(time_taken,2)
    typing_speed = len(user_in)/actual_time
    return round(typing_speed,2)

test_samples = [
    "The sun was setting behind the mountains, casting a golden hue over the tranquil lake. Birds chirped in the distance, and a gentle breeze rustled the leaves of the trees. Nature's beauty was on full display, and it was a moment to savor.",
    "In the heart of the bustling city, people hurriedly walked down the crowded streets, the sounds of car horns and footsteps merging into a symphony of urban life. Among the chaos, there was a sense of energy and purpose that defined the city.",
    "As the pages of the book turned, the story unfolded with each word. The characters came to life, and the world within those pages became a place of adventure and wonder. Reading was a journey to distant realms of imagination.",
    "In the kitchen, the aroma of freshly baked bread filled the air, making mouths water and stomachs growl in anticipation. The chef worked meticulously, kneading the dough and shaping it into perfectly formed loaves.",
    "High above, the stars twinkled in the night sky, forming constellations that had fascinated humanity for centuries. The vastness of the universe stretched out before us, a reminder of our place in the cosmos."
    ]

print("-----------TYPING SPEED CALCULATOR-----------\n")
print("Type the folowing paragraph to test your typing speed (***only press enter to submit final input***): \n")
test = random.choice(test_samples)
print(test)
start_time = time.time()
user_input = input("\nEnter text here: ")
end_time = time.time()
print("\nErrors: "+ str(errors(test,user_input)))
print("Words per Minute(wpm): "+str(speed(start_time,end_time,user_input)))