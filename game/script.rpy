# script.rpy

# Character Definitions
define m = Character("Aman Ager", color="#FFD700")  # Manager color
define f = Character("Finn Hart", color="#B22222")  # Art Student
define p = Character("Paige Turner", color="#4682B4")  # COLA Student
define c = Character("Cee Sharpe", color="#8A2BE2")  # CS Student
define r = Character("Fara Way", color="#FF6347")  # International Student
define i = Character("Indi Cyciv", color="#32CD32")  # Undecided Student

# Variable to track if tutorial has been completed
default tutorial_completed = False

# Array of hints the manager can give after the tutorial
# List of hints that will only be shown once per game
default manager_hints = [
    "The item you choose doesn’t affect the amount you receive.",
    "Make someone smile today!",
    "You’re the last customer so feel free to take your time chatting with the employees."
]

# Generate a random value to assign ammount.
# Order Variables
# 1 = "None"
# 2 = "Normal"
# 3 = "Perfect"
# 4 = "Too Much"

# Define the generate_order function using a list
python:
    def randomVar():
        # Define a list with the order options
        order_options = ["none", "normal", "perfect", "too much"]
        
        # Choose a random option from the list
        return renpy.random.choice(order_options)


# Start the game
label start:
    scene bg cafe 
    with fade
    show manager_normal
    with dissolve
    m "Welcome to the Burrito Bar! I'm Aman, your manager. Let’s see how I can help you today!"
    if not tutorial_completed:
        m "Do you understand how this works?"
        menu:
            "Yes":
                $ tutorial_completed = True
                jump order_process
            "No":
                m "Alright, here’s how it works! You'll be chatting with each of our team members. Choose responses to guide the conversation, and aim for the best outcomes!"
                m "Ready? Let's go!"
                $ tutorial_completed = True
                jump manager_hint
    else:
        jump manager_hint

# Manager hint, each hint is shown only once per game
label manager_hint:
    if tutorial_completed and manager_hints:
        # Randomly choose a hint and remove it from the list
        $ hint = renpy.random.choice(manager_hints)
        $ manager_hints.remove(hint)
        m hint
    jump order_process

# burrito or bowl


label order_process:
    m "Lets get started. Would you like a burrito or a bowl?"

    play music "sunflower-slow-drag.ogg" # Play music example

    menu:
        "Burrito":
            $ order = "burrito"
            jump finn_interaction
        "Bowl":
            $ order = "bowl"
            jump finn_interaction

    m "DEBUG MENU"
    menu:
        "Finn Hart": # Rice and Beans
            jump finn_interaction
        "Paige Turner": # Protein
            jump paige_interaction
        "Cee Sharpe": # Salsa
            jump cee_interaction
        "Fara Way": # Toppings
            jump fara_interaction
        "Indi Cyciv": # Cashier
            jump indi_interaction

# Initialize variables for tracking the interaction and order
default finn_status1 = False
default finn_status2 = False
default finn_status3 = False
default finn_status4 = False
default player_rice = "normal"  # Track rice order (normal, perfect, too much)
default player_beans = "normal"  # Track beans order (normal, perfect, none)

# Interaction with Finn Hart
label finn_interaction:
    show finn_normal with dissolve
    f "Do you ever feel... like a plastic bag?"
    
    menu:
        "Drifting through the wind?":
            # GOOD1 response
            $ finn_status1 = True
            show finn_surprise
            f "Yes! Hoping to start again?"
            show finn_normal
            f "That’s how I’ve been feeling with this project lately..."
            jump finn_question2

        "What?":
            # BAD1 response
            show finn_disappointment
            f "..."
            f "Nevermind"
            $ player_rice = randomVar()
            $ player_beans = randomVar()
            jump paige_interaction

label finn_question2:
    menu:
        "What project?":
            # GOOD2 response
            $ finn_status2 = True
            show finn_confused
            f "It’s this [insert project]."
            f "I’m really into it, but it’s honestly taking over my life..."
            f "I don’t want to stop doing this project because I’m super passionate about it, but my grades are suffering..."
            jump finn_question3

        "I just want my food...":
            # BAD2 response
            show finn_sigh
            f "Yeah, okay. Just... forget I mentioned it."
            $ player_rice = randomVar()
            $ player_beans = randomVar()
            jump paige_interaction

label finn_question3:
    menu:
        "Well, what makes you the most excited about it?":
            # GOOD3 response
            $ finn_status3 = True
            show finn_normal
            f "Well, what I really like working on is [blah]."
            jump finn_question4

        "I’m not really qualified to answer this question":
            # BAD3 response
            show finn_sad
            f "Oh... alright, I guess."
            $ player_rice = randomVar()
            $ player_beans = randomVar()
            jump paige_interaction

label finn_question4:
    menu:
        "You should probably trim the project to be centered on that, since it’s what you’re passionate about.":
            # GOOD4 response
            show finn_think
            f "I should trim it down?"
            f "I can’t because I..."
            f "Well... hm."
            f "I guess you’re right. That would honestly make the project even cooler."
            show finn_smile
            f "Thanks for the advice, I feel much better about it now."
            $ player_rice = "perfect"
            $ player_beans = "perfect"
            # Trigger success sound and icon
            play sound "jingle.ogg"
            show icon_success at center
            with pause(1)
            hide icon_success
            jump paige_interaction

        "Well, that’s cool. Can I get my food now?":
            # BAD4 response
            f "Oh... sure, here."
            $ player_rice = randomVar()
            $ player_beans = randomVar()
            jump paige_interaction

# Paige Turner Interaction
label paige_interaction:
    p "Uhm... Not really..."
    menu:
        "Mind if I ask what’s bothering you?":
            p "I’m stretched thin with school and work..."
            menu:
                "Wow, that’s a lot on your plate.":
                    p "I don't want to let anyone down..."
                    menu:
                        "You should focus on school.":
                            p "You’ve got a point. Thanks!"
                            # Perfect outcome
                            $ protein = "perfect"
                            jump end_order
                        "Can I have my food now?":
                            p "Here’s your food."
                            # Bad outcome
                            $ protein = randomVar()
                            jump end_order
                "Damn dude, that’s crazy.":
                    p "Sorry for bothering you."
                    # Bad outcome
                    $ protein = randomVar()
                    jump end_order
        "Good morning. Can I have my food now?":
            p "..."
            # Bad outcome
            $ protein = randomVar()
            jump end_order

# Cee Sharpe Interaction
label cee_interaction:
    c "I’m stuck in an infinite recursion loop..."
    menu:
        "By what?":
            c "I can’t figure out this coding project."
            menu:
                "Is it a bug or do you not understand?":
                    c "It’s a bug. I’ve been stuck."
                    menu:
                        "Have you considered stepping back?":
                            c "Thanks, that makes sense."
                            # Perfect outcome
                            $ salsa = "perfect"
                            jump end_order
                        "I’m sorry to hear that.":
                            c "I guess I should just try harder."
                            # Bad outcome
                            $ salsa = randomVar()
                            jump end_order
                "Welp. Hope you figure it out.":
                    c "..."
                    # Bad outcome
                    $ salsa = randomVar()
                    jump end_order
        "Sorry to hear that. Can I get my food now?":
            c "..."
            # Bad outcome
            $ salsa = randomVar()
            jump end_order

# Fara Way Interaction
label fara_interaction:
    r "Oh, lo siento, I didn’t see you there."
    menu:
        "It sounds pretty good to me!":
            r "Honestly, not everyone thinks that..."
            menu:
                "Why is that?":
                    r "Classmates don’t want to talk to someone who doesn’t understand..."
                    menu:
                        "Have you looked into campus groups?":
                            r "You mean, a campus group with people from [Insert Hispanic/Latin country here]?"
                            menu:
                                "Yes, people who can relate!":
                                    r "I will look at it soon, thank you!"
                                    # Perfect outcome
                                    $ toppings = "perfect"
                                    jump end_order
                                "Eh, it’s hard to explain.":
                                    r "Thanks anyway."
                                    # Bad outcome
                                    $ toppings = randomVar()
                                    jump end_order
                        "Good luck with that.":
                            r "..."
                            # Bad outcome
                            $ toppings = randomVar()
                            jump end_order
                "Sorry, what did you say?":
                    r "..."
                    # Bad outcome
                    $ toppings = randomVar()
                    jump end_order
        "Can I have my food now?":
            r "..."
            # Bad outcome
            $ toppings = randomVar()
            jump end_order

# Indi Cyciv Interaction
label indi_interaction:
    i "... (register noises)..."
    menu:
        "Do I need to talk to you about your issues too?":
            i "I guess I’m having issues."
            menu:
                "What sort of issues?":
                    i "I’m lost. I’ve switched majors."
                    menu:
                        "Well, what drew you to those majors?":
                            i "In Comp. Sci, I liked problem solving..."
                            menu:
                                "Have you heard of Humanities, Computing, and Design?":
                                    i "That sounds like what I've been looking for!"
                                    # Perfect outcome
                                    $ cashier = "perfect"
                                    jump end_order
                                "Have you considered ringing me up?":
                                    i "..."
                                    # Bad outcome
                                    $ cashier = randomVar()
                                    jump end_order
                        "Hopefully you find something.":
                            i "Your total is..."
                            # Bad outcome
                            $ cashier = randomVar()
                            jump end_order
                "What’s my total?":
                    i "Your total is..."
                    # Bad outcome
                    $ cashier = randomVar()
                    jump end_order

# End Order Process
label end_order:

# Initialize the ending variable
default ending = 5

# Function to calculate the total count of each order type and determine the final message
python:
    def calculate_order(*orders):
        # Initialize counts for each order type
        counts = {
            "perfect": 0,
            "normal": 0,
            "too much": 0,
            "none": 0
        }
        
        # Loop through each order and tally up counts
        for order in orders:
            if order in counts:
                counts[order] += 1

        # Determine ending message based on counts
        total_orders = len(orders)
        
        # Global keyword to modify the ending variable outside function scope
        global ending
        
        if counts["perfect"] == total_orders:
            ending = 0
            message = "Nice! Everything is perfect!"
        elif counts["none"] == total_orders:
            ending = 1
            message = "... Fuck"
        elif counts["none"] == total_orders - 1:
            ending = 2
            message = "... Damn"
        elif counts["none"] == total_orders - 2:
            ending = 3
            message = "... Could be worse, I guess"
        elif counts["none"] == total_orders - 3:
            ending = 4
            message = "... Dang, they made me the wrong thing"
        else:
            ending = 5
            message = "... Welp, that’s okay"
        
        return message

# Example usage
# Generate random orders
$ player_rice = generate_order()
$ player_protein = generate_order()
$ player_salsa = generate_order()
$ player_toppings = generate_order()
$ player_cashier = generate_order()

# Calculate the result message
$ result_message = calculate_order(player_rice, player_protein, player_salsa, player_toppings, player_cashier)

# Display the result message and ending condition
# Note: use `window hide` before showing to prevent issues
window hide
$ renpy.pause(0.1)  # Small pause to ensure window is hidden before showing text

if ending == 0:
    "{b}Perfect Ending{/b}"
else:
    "{b}Ending [ending]{/b}"

"[result_message]"

# End of game
return




    # if rice == "perfect" and protein == "perfect" and salsa == "perfect" and toppings == "perfect" and cashier == "perfect":
    #     "Nice! Everything is perfect!"
    #     elif 
    #     "... Fuck"

    #     "... Damn"

    #     "... Could be worse, I guess"

    #     "... Dang, they made me the wrong thing"

    #     "... Welp, that’s okay"
    # return

# 
# --=-=-=-=-=-=-=-=-=-=-=-=-=--
# 
# # Declare characters used by this game.
# define s = Character(_("Sylvie"), color="#c8ffc8")
# define m = Character(_("Me"), color="#c8c8ff")

# # This is a variable that is True if you've compared a VN to a book, and False
# # otherwise.
# default book = False

# # The game starts here.
# label start:

#     # Start by playing some music.
#     # play music "illurock.opus"

#     # Show a background. This uses a placeholder by default, but you can
#     # add a file (named either "bg lecturehall.png" or "bg lecturehall.jpg") to the
#     # images directory to show it.

#     scene bg lecturehall
#     with fade

#     "It's only when I hear the sounds of shuffling feet and supplies being put away that I realize that the lecture's over."

#     "Professor Eileen's lectures are usually interesting, but today I just couldn't concentrate on it."

#     "I've had a lot of other thoughts on my mind...thoughts that culminate in a question."

#     "It's a question that I've been meaning to ask a certain someone."

#     scene bg uni
#     with fade

#     "When we come out of the university, I spot her right away."

#     # This shows a character sprite. A placeholder is used, but you can
#     # replace it by adding a file named "sylvie green normal.png" to the images
#     # directory.

#     show sylvie green normal
#     with dissolve

#     "I've known Sylvie since we were kids. She's got a big heart and she's always been a good friend to me."

#     "But recently... I've felt that I want something more."

#     "More than just talking, more than just walking home together when our classes end."

#     menu:

#         "As soon as she catches my eye, I decide..."

#         "To ask her right away.":

#             jump rightaway

#         "To ask her later.":

#             jump later


# label rightaway:

#     show sylvie green smile

#     s "Hi there! How was class?"

#     m "Good..."

#     "I can't bring myself to admit that it all went in one ear and out the other."

#     m "Are you going home now? Wanna walk back with me?"

#     s "Sure!"

#     scene bg meadow
#     with fade

#     "After a short while, we reach the meadows just outside the neighborhood where we both live."

#     "It's a scenic view I've grown used to. Autumn is especially beautiful here."

#     "When we were children, we played in these meadows a lot, so they're full of memories."

#     m "Hey... Umm..."

#     show sylvie green smile
#     with dissolve

#     "She turns to me and smiles. She looks so welcoming that I feel my nervousness melt away."

#     "I'll ask her...!"

#     m "Ummm... Will you..."

#     m "Will you be my artist for a visual novel?"

#     show sylvie green surprised

#     "Silence."

#     "She looks so shocked that I begin to fear the worst. But then..."

#     show sylvie green smile

#     menu:

#         s "Sure, but what's a \"visual novel?\""

#         "It's a videogame.":
#             jump game

#         "It's an interactive book.":
#             jump book


# label game:

#     m "It's a kind of videogame you can play on your computer or a console."

#     m "Visual novels tell a story with pictures and music."

#     m "Sometimes, you also get to make choices that affect the outcome of the story."

#     s "So it's like those choose-your-adventure books?"

#     m "Exactly! I've got lots of different ideas that I think would work."

#     m "And I thought maybe you could help me...since I know how you like to draw."

#     m "It'd be hard for me to make a visual novel alone."

#     show sylvie green normal

#     s "Well, sure! I can try. I just hope I don't disappoint you."

#     m "You know you could never disappoint me, Sylvie."

#     jump marry


# label book:

#     $ book = True

#     m "It's like an interactive book that you can read on a computer or a console."

#     show sylvie green surprised

#     s "Interactive?"

#     m "You can make choices that lead to different events and endings in the story."

#     s "So where does the \"visual\" part come in?"

#     m "Visual novels have pictures and even music, sound effects, and sometimes voice acting to go along with the text."

#     show sylvie green smile

#     s "I see! That certainly sounds like fun. I actually used to make webcomics way back when, so I've got lots of story ideas."

#     m "That's great! So...would you be interested in working with me as an artist?"

#     s "I'd love to!"

#     jump marry

# label marry:

#     scene black
#     with dissolve

#     "And so, we become a visual novel creating duo."

#     scene bg club
#     with dissolve

#     "Over the years, we make lots of games and have a lot of fun making them."

#     if book:

#         "Our first game is based on one of Sylvie's ideas, but afterwards I get to come up with stories of my own, too."

#     "We take turns coming up with stories and characters and support each other to make some great games!"

#     "And one day..."

#     show sylvie blue normal
#     with dissolve

#     s "Hey..."

#     m "Yes?"

#     show sylvie blue giggle

#     s "Will you marry me?"

#     m "What? Where did this come from?"

#     show sylvie blue surprised

#     s "Come on, how long have we been dating?"

#     m "A while..."

#     show sylvie blue smile

#     s "These last few years we've been making visual novels together, spending time together, helping each other..."

#     s "I've gotten to know you and care about you better than anyone else. And I think the same goes for you, right?"

#     m "Sylvie..."

#     show sylvie blue giggle

#     s "But I know you're the indecisive type. If I held back, who knows when you'd propose?"

#     show sylvie blue normal

#     s "So will you marry me?"

#     m "Of course I will! I've actually been meaning to propose, honest!"

#     s "I know, I know."

#     m "I guess... I was too worried about timing. I wanted to ask the right question at the right time."

#     show sylvie blue giggle

#     s "You worry too much. If only this were a visual novel and I could pick an option to give you more courage!"

#     scene black
#     with dissolve

#     "We get married shortly after that."

#     "Our visual novel duo lives on even after we're married...and I try my best to be more decisive."

#     "Together, we live happily ever after even now."

#     "{b}Good Ending{/b}."

#     return

# label later:

#     "I can't get up the nerve to ask right now. With a gulp, I decide to ask her later."

#     scene black
#     with dissolve

#     "But I'm an indecisive person."

#     "I couldn't ask her that day and I end up never being able to ask her."

#     "I guess I'll never know the answer to my question now..."

#     "{b}Bad Ending{/b}."

#     return
