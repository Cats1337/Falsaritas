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

# Define the generate_order function using a list
init python:
    import random

    def generate_order(variable):
        order_list = ["None", "Normal", "Perfect", "Too Much"]
        # Ensure variable is within valid range
        if 0 <= variable < len(order_list):
            return order_list[variable]
        else:
            return "Normal"  # Default fallback

    manager_hints = [
        "The item you choose doesn’t affect the amount you receive.",
        "Make someone smile today!",
        "You’re the last customer so feel free to take your time chatting with the employees."
    ]

    projects = [
        "Sculpture",
        "Mock-up",
        "Painting"
    ]

    def calculate_order(protein, salsa, toppings):
        # Simple scoring system based on choices
        score = 0
        if protein == "Perfect":
            score += 1
        if salsa == "Perfect":
            score += 1
        if toppings == "Perfect":
            score += 1

        # Determine the result based on score
        if score == 3:
            return "You got the perfect order!"
        elif score == 2:
            return "Almost perfect, but not quite."
        else:
            return "Maybe next time, try a little harder!"

# Initialize variables for tracking the interaction and order
default player_rice = generate_order(1)  # Track rice order (normal, perfect, too much)
default player_beans = generate_order(1)  # Track beans order (normal, perfect, none)
default player_protein = generate_order(1)
default player_salsa = generate_order(1)
default player_toppings = generate_order(1)
default player_cashier = generate_order(1)

# Interaction Flags
default finn_status1 = False
default finn_status2 = False
default finn_status3 = False
default finn_status4 = False

transform smol:
    zoom 0.75

# Start the game
label start:
    scene subway_tile
    # increase the subway-tile-bg size to fit the screen
    with fade
    show manager_normal

    show burrito_station


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
        $ hint = random.choice(manager_hints)
        $ manager_hints.remove(hint)
        m "{hint}"
    else:
        m "Let’s keep going!"
    jump order_process

# Order Process - Burrito or Bowl
label order_process:
    m "Lets get started. Would you like a burrito or a bowl?"
    # play music "sunflower-slow-drag.ogg"  # Play music example

    menu:
        "Burrito":
            $ order = "burrito"
            jump finn_interaction
        "Bowl":
            $ order = "bowl"
            jump finn_interaction

    # Debug Menu for testing purposes (remove in production)
    if renpy.debug:
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

# Finn Hart Interaction (Rice and Beans)
label finn_interaction:
    show finn_normal with dissolve

    f "Hey! What can I get for you today?"
    menu:
        "Rice and Beans":
            $ player_rice = generate_order(1)
            $ player_beans = generate_order(1)
            jump finn_question2
        "No Beans":
            $ player_rice = generate_order(1)
            $ player_beans = generate_order(0)
            jump finn_question2
        "No Rice or Beans":
            f "What?..."
            jump end_order

    f "Do you ever feel... like a plastic bag?"
    menu:
        "Drifting through the wind?":
            $ finn_status1 = True
            show finn_surprise
            f "Yes! Hoping to start again?"
            show finn_normal
            f "That’s how I’ve been feeling with this project lately..."
            jump finn_question2
        "What?":
            show finn_disappointment
            f "..."
            f "Nevermind"
            $ player_rice = generate_order(3)
            $ player_beans = generate_order(0)
            jump paige_interaction

label finn_question2:
    menu:
        "What project?":
            $ finn_status2 = True
            show finn_confused
            $ project = random.choice(projects)
            # remoe it from the list so it doesn't repeat
            $ projects.remove(project)
            f "It’s this [project] I’ve been working on for my art class."
            f "I’m really into it, but it’s honestly taking over my life..."
            f "I don’t want to stop doing this project because I’m super passionate about it, but my grades are suffering..."
            jump finn_question3
        "I just want my food...":
            show finn_sigh
            f "Yeah, okay. Just... forget I mentioned it."
            $ player_rice = generate_order(3)
            $ player_beans = generate_order(0)
            jump paige_interaction

label finn_question3:
    menu:
        "Well, what makes you the most excited about it?":
            $ finn_status3 = True
            show finn_normal
            $ blah = random.choice(projects)
            f "Well, what I really like working on is [blah]."
            jump finn_question4
        "I’m not really qualified to answer this question":
            show finn_sad
            f "Oh... alright, I guess."
            $ player_rice = generate_order(3)
            $ player_beans = generate_order(0)
            jump paige_interaction

label finn_question4:
    menu:
        "You should probably trim the project to be centered on that, since it’s what you’re passionate about.":
            show finn_think
            f "I should trim it down?"
            f "I can’t because I..."
            f "Well... hm."
            f "I guess you’re right. That would honestly make the project even cooler."
            show finn_smile
            f "Thanks for the advice, I feel much better about it now."
            $ player_rice = generate_order(2)
            $ player_beans = generate_order(2)
            play sound "jingle.ogg"
            show icon_success at center
            pause(1)
            hide icon_success
            jump paige_interaction
        "Well, that’s cool. Can I get my food now?":
            f "Oh... sure, here."
            $ player_rice = generate_order(0)
            $ player_beans = generate_order(0)
            jump paige_interaction

# Paige Turner Interaction (Protein)
label paige_interaction:
    show paige_normal with dissolve
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
                            $ player_protein = generate_order(2)  # Perfect protein
                            jump paige_question2
                        "Can I have my food now?":
                            p "Here’s your food."
                            $ player_protein = generate_order(0)  # Incorrect protein
                            jump end_order
                "Damn dude, that’s crazy.":
                    p "Sorry for bothering you."
                    $ player_protein = generate_order(0)  # Incorrect protein
                    jump end_order
        "Good morning. Can I have my food now?":
            p "..."
            $ player_protein = generate_order(0)  # Incorrect protein
            jump end_order

label paige_question2:
    menu:
        "Wow, that’s a lot on your plate":
            p "Yeah, it is"
            p "But I don't want to let anyone down in my clubs or at work, so I have to keep doing all of it."
            jump paige_question3
        "Damn dude, that’s crazy":
            p "Yeah... sorry, I shouldn’t have said anything."
            $ player_protein = generate_order(0)  # Incorrect protein
            jump end_order

label paige_question3:
    menu:
        "You won’t let anyone down by focusing on school while you’re at school. You should probably try to reduce your hours in work or in clubs to try and focus on school.":
            p "Well, I..."
            p "You’ve got a point. I think I will reduce my club hours, because I really need the money. Hopefully my grades will start to improve because of it."
            show paige_smile
            p "Thank you for the advice, I really appreciate it."
            $ player_protein = generate_order(2)  # Perfect protein
            play sound "jingle.ogg"
            show icon_success at center
            pause(1)
            hide icon_success
            jump end_order
        "Well, I hope you can figure that out. Can I have my food now?":
            p "Yeah, you’re probably right."
            $ player_protein = generate_order(0)  # Incorrect protein
            jump end_order

# Cee Sharpe Interaction (Salsa)
label cee_interaction:
    c "I’m stuck in an infinite recursion loop..."
    menu:
        "By what?":
            c "I can’t figure out this coding project."
            menu:
                "Is it a bug or do you just not understand what’s being asked?":
                    c "It’s a bug. I’ve been stuck."
                    menu:
                        "Have you considered stepping back?":
                            c "Thanks, that makes sense."
                            $ salsa = generate_order(2)  # Perfect salsa
                            jump end_order
                        "I’m sorry to hear that.":
                            c "I guess I should just try harder."
                            $ salsa = generate_order(0)  # Incorrect salsa
                            jump end_order
                "Welp. Hope you figure it out.":
                    c "..."
                    $ salsa = generate_order(0)  # Incorrect salsa
                    jump end_order
        "Sorry to hear that. Can I get my food now?":
            c "..."
            $ salsa = generate_order(0)  # Incorrect salsa
            jump end_order

label cee_question2:
    menu:
        "Is it a bug or do you just not understand what’s being asked?":
            c "It’s a bug. I’ve been working at it non-stop and everything I throw at the problem won’t stick."
            jump cee_question3
        "Welp. Hope you figure it out.":
            c "..."
            $ salsa = generate_order(0)  # Incorrect salsa
            jump end_order

label cee_question3:
    menu:
        "Have you considered taking a step back from it and working on something else?":
            c "But I need to get this assignment done soon. The deadline is coming up quick"
            jump cee_question4
        "I’m sorry to hear that. Coding sucks.":
            c "Yeah, but I have to push through."
            $ salsa = generate_order(0)  # Incorrect salsa
            jump end_order

label cee_question4:
    menu:
        "From my experience, it will take less time overall to take a step back. Once you do, you’ll see the problem for what it is and you’ll get it done much faster":
            c "..."
            show cee happy
            c "You’re right, that makes sense. Thanks for the advice."
            $ salsa = generate_order(2)  # Perfect salsa
            play sound "jingle.ogg"
            show icon_success at center
            pause(1)
            hide icon_success
            jump end_order
        "Better get on that then":
            c "Yeah, I guess I’ll try that. Thanks."
            $ salsa = generate_order(0)  # Incorrect salsa
            jump end_order


# Fara Way Interaction (Toppings)
label fara_interaction:
    r "Oh, lo siento, I didn’t see you there."
    menu:
        "It sounds pretty good to me!":
            r "Thank you! You must be amazing, yes?"
            $ toppings = generate_order(2)  # Perfect toppings
            jump end_order
        "Could you maybe, uh... explain that again?":
            r "Of course. I was just telling a funny story!"
            $ toppings = generate_order(0)  # Incorrect toppings
            jump end_order

label fara_question2:
    menu:
        "Why is that? You seem easy to talk to to me":
            r "Classmates don’t want to talk to someone that doesn’t understand them all of the time."
            r "I just want to fit in with people."
            jump fara_question3
        "Yeah, people suck":
            r "..."
            $ toppings = generate_order(0)  # Incorrect toppings
            jump end_order

label fara_question3:
    menu:
        "Well, have you looked into campus groups at all?":
            r "No entiendo…"
            r "You mean, a campus group with people from [Insert hispanic/latin country here]?"
            jump fara_question4
        "Good luck with that.":
            r "Thanks, but I don’t think that will help."
            $ toppings = generate_order(0)  # Incorrect toppings
            jump end_order

label fara_question4:
    menu:
        "I mean, kind of! There are groups that have a bunch of people who also speak Spanish and have similar experiences as you. You should check them out!":
            show fara happy
            r "I will look at it soon, thank you so much for telling me that!"
            $ toppings = generate_order(2)  # Perfect toppings
            play sound "jingle.ogg"
            show icon_success at center
            pause(1)
            hide icon_success
            jump end_order
        "Eh, it’s hard to explain. Sorry":
            r "Oh, okay... sorry for bothering you."
            $ toppings = generate_order(0)  # Incorrect toppings
            jump end_order


# Indi Cyciv Interaction (Cashier)
label indi_interaction:
    i "Here’s the total for your burrito."
    menu:
        "Can I pay now?":
            i "Sure."
            $ cashier = generate_order(1)  # Correct cashier amount
            jump end_order
        "Where’s the change?":
            i "I just said you don’t have change."
            $ cashier = generate_order(0)  # Incorrect cashier amount
            jump end_order

label indi_question2:
    menu:
        "Do you mind if I ask what sort of issues?":
            i "Oh... I guess I’m just having issues figuring out what I want to do with my life..."
            jump indi_question3
        "Well, that’s too bad. Hey, can you print my receipt?":
            i "Sure, here you go."
            $ cashier = generate_order(0)  # Incorrect cashier amount
            jump end_order

label indi_question3:
    menu:
        "Do you have any passions or things that make you excited?":
            i "I don’t know... I guess I’m still trying to figure that out."
            jump indi_question4
        "Yeah, I get it. That sounds tough.":
            i "Yeah..."
            $ cashier = generate_order(0)  # Incorrect cashier amount
            jump end_order

label indi_question4:
    menu:
        "I think it’s about exploring different things. Sometimes, it takes a little time to find out what really excites you.":
            show indi happy
            i "Maybe you’re right. Thanks for the advice."
            $ cashier = generate_order(1)  # Correct cashier amount
            play sound "jingle.ogg"
            show icon_success at center
            pause(1)
            hide icon_success
            jump end_order
        "Well, I hope you figure it out soon.":
            i "Thanks."
            $ cashier = generate_order(0)  # Incorrect cashier amount
            jump end_order

# Final Order Result and Endgame Logic
label end_order:
    $ ending = 0
    $ result_message = calculate_order(player_protein, player_salsa, player_toppings)
    if ending == 0:
        show text "{b}Perfect Ending{/b}" with dissolve
    else:
        show text "{b}Ending %d{/b}" % ending with dissolve
    show text "[result_message]" with dissolve
    return
