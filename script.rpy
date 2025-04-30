# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define m = Character("Mari")
define na = Character("News Anchor")
define g = Character("Grandmama")
define mm = Character("Mailman")
define s = Character("Sadi")

define e = Character("Emma", image = "emma")

define gui.name_xpos = 520
define gui.dialogue_xpos = 520

image side emma:
    "emma.png"
    zoom 0.6

# The game starts here.

screen inventory_display_toggle:
    zorder 92
    frame:
        background "#9F99"
        xalign 0.05
        yalign 0.1
        
        textbutton "Inventory":
            action ToggleScreen("inventory_item_description")
    
    on "hide" action Hide("inventory_item_description")

default item_descriptions = {"key" : "a mysterious key", "bottle" : "I wonder what is inside?", "broom" : "it sweeps. or rather, you do. with it.", "Cholula" : "yum!"}
default inventory_items = []
default item_description = ""

style inv_button is frame:
    xsize 200
    ysize 100

style inv_button_text:
    xalign 0.5
    yalign 0.5

screen inventory_item_description:
    # use this based on your preference
    # modal True
    window:
        background "#AAA9"
        xsize 600
        ysize 150
        xalign 0.5
        yalign 0.1
        text item_description:
            xfill True
            yfill True
    
    window:
        background "#99F9"
        xsize 1290
        ysize 600
        xalign 0.5
        yalign 0.7
        hbox:
            box_wrap True
            box_wrap_spacing 10
            spacing 10
            xoffset 20
            yoffset 20
            style_prefix "inv"
            for item in inventory_items:
                textbutton item:
                    action SetVariable("item_description", item_descriptions.get(item))
                    selected False


    on "hide" action SetVariable("item_description", "")

init python:
    def setup_puzzle():
        for i in range(page_pieces):
            start_x = 1200
            start_y = 200
            end_x = 1700
            end_y = 800
            rand_loc = (renpy.random.randint(start_x, end_x), renpy.random.randint(start_y, end_y))
            initial_piece_coordinates.append(rand_loc)

    def piece_drop(dropped_on, dragged_piece):
        global finished_pieces

        if dragged_piece[0].drag_name == dropped_on.drag_name:
            dragged_piece[0].snap(dropped_on.x, dropped_on.y)
            dragged_piece[0].draggable = False
            finished_pieces += 1

            if finished_pieces == page_pieces:
                renpy.jump("reassemble_complete")

label reassemble_complete:
    scene room
    "I did it!"
    "Let us see what it says..."

screen reassemble_puzzle:
    image "background.png"
    frame:
        background "puzzle-frame.png"
        xysize full_page_size
        anchor(0.5, 0.5)
        pos(650, 535)

    draggroup:
        for i in range(page_pieces):
            drag:
                drag_name i
                pos initial_piece_coordinates[i]
                anchor(0.5, 0.5)
                focus_mask True
                drag_raise True
                image "Pieces/piece-%s.png" % (i+1)

        for i in range(page_pieces):
            drag:
                drag_name i
                draggable False
                droppable True
                dropped piece_drop
                pos piece_coordinates[i]
                anchor(0.5, 0.5)
                focus_mask True
                image "Pieces/piece-%s.png" % (i+1) alpha 0.0

default page_pieces = 12
default full_page_size = (711, 996)
default piece_coordinates = [(451, 149), (719, 139), (868, 238), (421, 399), (658, 318), (700, 488), (796, 538), (453, 718), (776, 773), (464, 925), (743, 958), (921, 888)]
default initial_piece_coordinates = []
default finished_pieces = 0

label temp:
show bg room
show screen inventory_display_toggle

"Hey check out that inventory button!"
"Yeah, that's mine and it's empty. But there's some stuff lying around here."
"What's this - I found a key!"
$ inventory_items.append("key")
"Ooh, it's mysterious. Have a look at it."

"Found a bottle. Taking that."
$ inventory_items.append("bottle")
"I can't tell what's inside it though."

"Here's a broom. yoink."
$ inventory_items.append("broom")

"Ooh, I know what's in this bottle."
$ inventory_items.append("Cholula")
"I can't wait to... yeah, gotta go b bye!"
hide screen inventory_display_toggle
# show black with Dissolve(3)

e "Oh, it seems like there is a shredded note."
e "Let's reassemble it and see what it says!"
$setup_puzzle()
call screen reassemble_puzzle
return

# label start:

#     # Show a background. This uses a placeholder by default, but you can
#     # add a file (named either "bg room.png" or "bg room.jpg") to the
#     # images directory to show it.

#     scene bg room

#     # This shows a character sprite. A placeholder is used, but you can
#     # replace it by adding a file named "eileen happy.png" to the images
#     # directory.

#     show mari happy

#     # These display lines of dialogue.

#     m "Hello this is a test"

#     m "My first task is to create an inventory feature!"

#     # This ends the game.

#     return

label start:
    scene bg room

    na "...emergency drafting of eligible individuals with magical blood from all of Mushroom Kingdom to serve in the rising war effort."
    na "Tensions between Dragonkind and Mushroomkind have escalated, and we need every available mage to protect our kingdom..."

    show m shocked
    m "Grandma? Is this..."
    m "Real?"

    show g sad at right
    g "It's been a long time coming, child. Desperation can make people do desperate things."

    show m upset at left
    m "Does this mean I could get drafted? What about Ebbi?" 
    m "Grandmama I can't leave him behind!"

    show g smiling at right
    g "Your little brother has a strong whippersnapper like me. And you, dear, have the blood of your grandfather in you."

    show m confused at left
    m "Pop? Oh yea huh..."

    show m at center
    "I haven’t seen him since I was little. Maybe never, really."
    "He’s more of a story than a person. The strongest mage, a ghost... not a grandfather."

    menu:
        "He was never there. Why should I care now?":
            $ grandpa_opinion = "resentful"
            m "Why should I care about someone I barely know?"
            m "He left us. I don't need him and his - blood."
        "Maybe this is my chance to prove myself to him.":
            $ grandpa_opinion = "hopeful"
            m "If he really is as powerful as they say… maybe I can finally be seen."
            m "I want to be more than just his bloodline."
        "I don’t know how to feel... but I’ll go anyway.":
            $ grandpa_opinion = "uncertain"
            m "I’m not sure what to feel. Anger? Curiosity?"
            m "All I know is that I have to go."

    show g gentle at right
    g "Whatever you're feeling, it’s okay. You’ll find your answers — maybe more than you expect."

    hide m
    hide g

    "Door bell rings"

    show mm

    mm "Delivery for you, miss"

    show m at left

    m "Thank you.."

    hide mm
    hide m
    show m at center

    m "This is real. I - "
    m "I have to leave. What if I can't do it? I have never been able to wield!"

    hide m
    show m at left
    show g at right

    g "It is hard, I know. But remember, you are not alone."
    m "What if I am not good enough?"

    show g sad at right 

    g "I believe in you. Ebbi and I will cheer you on."

    hide g
    hide m
    show m at center

    "I can do this. I have to do this."

    jump warcollegescene1

label warcollegescene1:
    scene bg room
    with fade
    
    "A few weeks later..."
    
    show m
    
    m "This should be my dorm, room 103."
    
    hide m
    show m at right
    show s at left
    
    "Entering the dorm room, you see a girl putting some luggages away."
    
    m "Hello! I believe I am your roommate?.."
    
    s "So... Mari, huh?"
    s "You must be special. I heard about your grandfather. People say that is some sort of an advantage."
    
    menu:
        "Indignantly snap":
            m "I won't be needing his protection if that is what you're getting at."
           
            s "Sure, but it is funny, isn't it? A lot of people would do anything for an advantage here."
            s "And yet, here you are..."
            s "Thinking you'll make it on your own."
            
            menu:
                "What do you mean by that?":
                    s "I'm just warning you. A lot of people will only look for your grandfather in you."
        "Pokes":
            m "It is. That is why I am confident I will make it out of this place."
    "Her words sting, and you feel your guard rise instinctively."
    
    return


