# Character Definitions
define m = Character("Aman Ager", color="#FFD700")  # Manager color
define f = Character("Finn Hart", color="#B22222")  # Art Student
define p = Character("Paige Turner", color="#4682B4")  # COLA Student
define c = Character("Cee Sharpe", color="#8A2BE2")  # CS Student
define r = Character("Fara Way", color="#FF6347")  # International Student
define i = Character("Indi Cyciv", color="#32CD32")  # Undecided Student
define y=Character("You",color="#757575") #player

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
default ending = 0

# Interaction Flags
default finn_status1 = False
default finn_status2 = False
default finn_status3 = False
default finn_status4 = False



transform smol:
    zoom 0.75

# Start the game
label start:
    play music "Closing Time (Falsaritas).wav"
    #$ ending = 0
    scene subway_tile
    # increase the subway-tile-bg size to fit the screen
    with fade
    show aman-ager

    show burrito-station-final



    with dissolve
    m "Welcome to the Burrito Bar! I'm Aman, the manager. Let’s see how I can help you today!"
    
    if not tutorial_completed:
        m "Do you understand how this works?"
        menu:
            "Yes":
                $ tutorial_completed = True
                jump order_process
            "No":
                m "Alright, here’s how it works!"
                m "You'll be chatting with each of our team members."
                m "Choose responses to guide the conversation, and aim for the best outcomes!"
                m "Ready? Let's go!"
                $ tutorial_completed = True
                jump manager_hint
    else:
        jump manager_hint

# Manager hint, each hint is shown only once per game
label manager_hint:
    if tutorial_completed and manager_hints:
        #$ hint = renpy.random.randint(0,2)
        #$ manager_hints.remove(hint)
        m "[manager_hints[renpy.random.randint(0,2)]]"
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
    hide aman-ager with dissolve
    hide burrito-station-final
    show finn_hart with dissolve
    show rice-beans
    f "Hey! What can I get for you today?"
    menu:
        "Rice and Beans":
            $ player_rice = generate_order(1)
            $ player_beans = generate_order(1)
            #jump finn_question2
        "No Beans":
            $ player_rice = generate_order(1)
            $ player_beans = generate_order(0)
            #jump finn_question2

    f "Do you ever feel... like a plastic bag?"
    menu:
        "Drifting through the wind?":
            $ finn_status1 = True
            #show finn_surprise
            f "Yes! Wanting to start again?"
            #show finn_normal
            f "That’s how I’ve been feeling with this project lately..."
            jump finn_question2
        "What?":
            #show finn_disappointment
            f "..."
            f "Nevermind"
            $ player_rice = generate_order(3)
            $ player_beans = generate_order(0)
            jump paige_interaction

label finn_question2:
    menu:
        "What project?":
            $ finn_status2 = True
            #show finn_confused
            $ project = random.choice(projects)
            # remoe it from the list so it doesn't repeat
            $ projects.remove(project)
            f "It’s this [project] I’ve been working on for my art class."
            f "I’m really into it, but it’s honestly taking over my life..."
            f "I don’t want to stop doing this project because I’m super passionate about it, but my grades are suffering..."
            jump finn_question3
        "I just want my food...":
            #show finn_sigh
            f "Yeah, okay. Just... forget I mentioned it."
            $ player_rice = generate_order(3)
            $ player_beans = generate_order(0)
            jump paige_interaction

label finn_question3:
    menu:
        "Well, what makes you the most excited about it?":
            $ finn_status3 = True
            #show finn_normal
            $ blah = random.choice(projects)
            f "Well, what I really like working on is [blah]."
            jump finn_question4
        "I’m not really qualified to answer this question":
            #show finn_sad
            f "Oh... alright, I guess."
            $ player_rice = generate_order(3)
            $ player_beans = generate_order(0)
            jump paige_interaction

label finn_question4:
    menu:
        "You should probably trim the project to be centered on that, since it’s what you’re passionate about.":
            #show finn_think
            f "I should trim it down?"
            f "I can’t because I..."
            f "Well... hm."
            f "I guess you’re right. That would honestly make the project even cooler."
            #show finn_smile
            f "Thanks for the advice, I feel much better about it now."
            $ player_rice = generate_order(2)
            $ player_beans = generate_order(2)
            $ ending += 1;
            play sound "jingle.ogg"
            #show icon_success at center
            pause(1)
            #hide icon_success
            jump paige_interaction
        "Well, that’s cool. Can I get my food now?":
            f "Oh... sure, here."
            $ player_rice = generate_order(0)
            $ player_beans = generate_order(0)
            jump paige_interaction

# Paige Turner Interaction (Protein)
label paige_interaction:
    hide finn_hart with dissolve
    hide rice-beans
    show paige_turner with dissolve
    show proteins

    p "..."
    y "..."
    y "Are you... alive?"
    p "*blinks*"
    p "Oh! I'm sorry. I must have fallen asleep standing up again"

    menu:
        "Are you like... good?":
            jump paige_question1
        "Good morning. Can I have my food now?":
            p "...Sorry for bothering you, here's your food."
            $ player_protein = generate_order(0)
            jump cee_interaction

label paige_question1:
    p "Uhm... Not really..."
    menu:
        "Mind if I ask what’s bothering you?":
            p "I’m stretched thin with school and work..."
            menu:
                "Wow, that’s a lot on your plate.":
                    p "I don't want to let anyone down..."
                    menu:
                        "You should focus on school.":
                            p "You’ve got a point..."
                            $ player_protein = generate_order(2)  # Perfect protein
                            jump paige_question3
                        "Can I have my food now?":
                            p "Here’s your food."
                            $ player_protein = generate_order(0)  # Incorrect protein
                            jump cee_interaction
                "Damn dude, that’s crazy.":
                    p "Sorry for bothering you."
                    $ player_protein = generate_order(0)  # Incorrect protein
                    jump cee_interaction
        "Well, we're all mentally ill, aren't we?":
            p "..."
            $ player_protein = generate_order(0)  # Incorrect protein
            jump cee_interaction

label paige_question2:
    menu:
        "Wow, that’s a lot on your plate":
            p "Yeah, it is"
            p "But I don't want to let anyone down in my clubs or at work, so I have to keep doing all of it."
            jump paige_question3
        "Damn dude, that’s crazy":
            p "Yeah... sorry, I shouldn’t have said anything."
            $ player_protein = generate_order(0)  # Incorrect protein
            jump cee_interaction

label paige_question3:
    menu:
        "You won’t let anyone down by focusing on school while you’re at school. You should probably try to reduce your hours in work or in clubs to try and focus on school.":
            p "Well, I..."
            p "Maybe you're right. I think I will reduce my club hours, because I really need the money."
            p  "Hopefully my grades will start to improve because of it."
            #show paige_smile
            p "Thank you for the advice, I really appreciate it."
            $ player_protein = generate_order(2)  # Perfect protein
            $ ending += 1;
            play sound "jingle.ogg"
            #show icon_success at center
            pause(1)
            #hide icon_success
            jump cee_interaction
        "Well, I hope you can figure that out. Can I have my food now?":
            p "Yeah, you’re probably right."
            $ player_protein = generate_order(0)  # Incorrect protein
            jump cee_interaction

# Cee Sharpe Interaction (Salsa)
label cee_interaction:
    hide paige_turner with dissolve
    hide proteins with dissolve
    show cee_sharpe with dissolve
    show salsas with dissolve


    c "I’m stuck in an infinite recursion loop..."
    menu:
        "By what?":
            c "I can’t figure out this coding project."
            jump cee_question2
            #menu:
            #    "Is it a bug or do you just not understand what’s being asked?":
            #        c "It’s a bug. I’ve been stuck."
            #        menu:
            #            "Have you considered stepping back?":
            #                c "Thanks, that makes sense."
            #                $ salsa = generate_order(2)  # Perfect salsa
            #                jump end_order
            #            "I’m sorry to hear that.":
            #                c "I guess I should just try harder."
            #                $ salsa = generate_order(0)  # Incorrect salsa
            #                jump end_order
            #    "Welp. Hope you figure it out.":
            #       c "..."
            #        $ salsa = generate_order(0)  # Incorrect salsa
            #        jump end_order
        "Sorry to hear that. Can I get my food now?":
            c "..."
            $ salsa = generate_order(0)  # Incorrect salsa
            jump fara_interaction

label cee_question2:
    menu:
        "Is it a bug or do you just not understand what’s being asked?":
            c "It’s a bug. I’ve been working at it non-stop and everything I throw at the problem won’t stick."
            jump cee_question3
        "Welp. Hope you figure it out.":
            c "..."
            $ salsa = generate_order(0)  # Incorrect salsa
            jump fara_interaction

label cee_question3:
    menu:
        "Have you considered taking a step back from it and working on something else?":
            c "But I need to get this assignment done soon. The deadline is coming up quick"
            jump cee_question4
        "I’m sorry to hear that. Coding sucks.":
            c "Yeah, but I have to push through."
            $ salsa = generate_order(0)  # Incorrect salsa
            jump fara_interaction

label cee_question4:
    menu:
        "From my experience, it will take less time overall to take a step back. Once you do, you’ll see the problem for what it is and you’ll get it done much faster":
            c "..."
            #show cee happy
            c "You’re right, that makes sense. Thanks for the advice."
            $ salsa = generate_order(2)  # Perfect salsa
            $ ending += 1;
            play sound "jingle.ogg"
            #show icon_success at center
            pause(1)
            #hide icon_success
            jump fara_interaction
        "Better get on that then":
            c "Yeah, I guess I’ll try that. Thanks."
            $ salsa = generate_order(0)  # Incorrect salsa
            jump fara_interaction


# Fara Way Interaction (Toppings)
label fara_interaction:
    hide cee_sharpe with dissolve
    hide salsas with dissolve
    show fara_way with dissolve
    show toppings with dissolve

    r "Oh, lo siento, I didn’t see you there."
    r "I'm practicing my English. It's not really good..."
    menu:
        "It sounds pretty good to me!":
            r "Thanks, but it doesn't feel like that. It's hard talking to people in class."
            $ toppings = generate_order(2)  # Perfect toppings
            jump fara_question2
        "Could you maybe, uh... say that again?":
            r "Nevermind..."
            $ toppings = generate_order(0)  # Incorrect toppings
            jump indi_interaction

label fara_question2:
    menu:
        "Why is that? You seem easy to talk to to me":
            r "Classmates don’t want to talk to someone that doesn’t understand them all of the time."
            r "I just want to fit in with people."
            jump fara_question3
        "Yeah, people suck":
            r "..."
            $ toppings = generate_order(0)  # Incorrect toppings
            jump indi_interaction

label fara_question3:
    menu:
        "Well, have you looked into campus groups at all?":
            r "No entiendo…"
            r "You mean, a campus group with people from El Salvador?"
            jump fara_question4
        "Good luck with that.":
            r "Thanks, but I don’t think that will help."
            $ toppings = generate_order(0)  # Incorrect toppings
            jump indi_interaction

label fara_question4:
    menu:
        "I mean, kind of! There are groups that have a bunch of people who also speak Spanish and have similar experiences as you. You should check them out!":
            #show fara happy
            r "I will look at it soon, thank you so much for telling me that!"
            $ toppings = generate_order(2)  # Perfect toppings
            $ ending +=1;
            play sound "jingle.ogg"
            #show icon_success at center
            pause(1)
            #hide icon_success
            jump indi_interaction
        "Eh, it’s hard to explain. Sorry":
            r "Oh, okay... sorry for bothering you."
            $ toppings = generate_order(0)  # Incorrect toppings
            jump indi_interaction


# Indi Cyciv Interaction (Cashier)
label indi_interaction:
    hide fara_way with dissolve
    hide toppings with dissolve
    show indi_cyciv with dissolve
    show register-final with dissolve

    i "Your total is $20."
    menu:
        "So... should I talk to you about your issues too?":
            i "What? I, uh.."
            $ cashier = generate_order(1)  # Correct cashier amount
            jump indi_question2
        "That seems off...":
            i "Look, there's people behind you. Are you gonna pay?"
            y "I guess..."
            i "Thanks for dining with us."
            $ cashier = generate_order(0)  # Incorrect cashier amount
            hide indi_cyciv with dissolve
            hide register-final with dissolve
            jump end_order

label indi_question2:
    i "I guess I'm having issues..."
    menu:
        "Do you mind if I ask what sort of issues?":
            i "Oh... I guess I’m just having issues figuring out what I want to do with my life..."
            jump indi_question3
        "Well, that’s too bad. Hey, can you print my receipt?":
            i "...Sure"
            $ cashier = generate_order(0)  # Incorrect cashier amount
            hide indi_cyciv with dissolve
            hide register-final with dissolve
            jump end_order

label indi_question3:
    i "I already switched majors, but I don't like my new major"
    menu:
        "Do you have any passions or things that make you excited?":
            i "I don’t know... I guess I’m still trying to figure that out."
            jump indi_question4
        "Yeah, I get it. That sounds tough.":
            i "Yeah..."
            $ cashier = generate_order(0)  # Incorrect cashier amount
            hide indi_cyciv with dissolve
            hide register-final with dissolve
            jump end_order

label indi_question4:
    i "In comp sci I liked the problem solving, and in New Media Interactive I liked the design stuff."
    i "But it still feels like I'm missing something..."
    menu:
        "Have you heard of Humanities, Computing, and Design?":
            i "What's that?"
            jump indi_question5
        "Have you heard of ringing me up?":
            i "Damn dude. Rude."
            $ cashier = generate_order(0)
            hide indi_cyciv with dissolve
            hide register-final with dissolve
            jump end_order

label indi_question5:
    menu:
        "It's a multidiciplinary thing. It combines the stuff you liked about comp sci and New Media":
            y "It also adds in a humanities background, which I've heard from others is what they felt they were missing"
            i "That..."
            i "Actually sounds like what I'm looking for!"
            y "I also think you should explore different things. Sometimes, it takes a bit to find out what really excited you!"
            #show indi happy
            i "You sound right about that. I'll look into that major!"
            i "Oh, I just realized I got your amount wrong! Your total is $12.49."
            $ cashier = generate_order(1)  # Correct cashier amount
            $ ending += 1;
            play sound "jingle.ogg"
            #show icon_success at center
            pause(1)
            #hide icon_success
            hide indi_cyciv with dissolve
            hide register-final with dissolve
            jump end_order
        "Nevermind. I hope you figure it out soon.":
            i "Gee, thanks."
            $ cashier = generate_order(0)  # Incorrect cashier amount
            hide indi_cyciv with dissolve
            hide register-final with dissolve
            jump end_order

# Final Order Result and Endgame Logic
label end_order:

    #$ result_message = calculate_order(player_protein, player_salsa, player_toppings)
    if ending == 0:
        if order == "burrito":
            show burrito_5-5 at truecenter with dissolve
        else:
            show burrito-bowl_5-5 at truecenter with dissolve
        y "..."
        y "Fuck."
    if ending == 1:
        if order == "burrito":
            show burrito_4-5 at truecenter with dissolve
        else:
            show burrito-bowl_4-5 at truecenter with dissolve
        y "..."
        y "...Damn"
    if ending == 2:
        if order == "burrito":
            show burrito_3-5 at truecenter with dissolve
        else:
            show burrito-bowl_3-5 at truecenter with dissolve
        y "..."
        y "Could be worse, I guess"
    if ending == 3:
        if order == "burrito":
            show burrito_2-5 at truecenter with dissolve
        else:
            show burrito-bowl_2-5 at truecenter with dissolve
        y "..."
        y "Dang, they made me the wrong thing"
    if ending == 4:
        if order == "burrito":
            show burrito_1-5 at truecenter with dissolve
        else:
            show burrito-bowl_1-5 at truecenter with dissolve
        y "..."
        y "Welp, that's okay"
    if ending == 5:
        if order == "burrito":
            show burrito_0-5 at truecenter with dissolve
        else:
            show burrito-bowl_0-5 at truecenter with dissolve
        y "..."
        y "Nice, they got my order right!"

    return
