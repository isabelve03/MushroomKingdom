# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define m = Character("Mari")
define na = Character("News Anchor")
define g = Character("Grandmama")
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

    na "...emergency drafting of eligible individuals from all of Mushroom Kingdom to servce in the rising war effort."
    na "Tensions between Dragonkind and Mushroomkind have escalated..."

    show m shocked
    m "Grandma? Is this..."
    m "real?"

    show g sad at right
    g "It's been a long time coming. You don't know what desperation does to you dear."

    show m upset at left
    m "Does this mean I can get drafted? What about Ebbi?" 
    m "Grandmama I can't leave him behind!"

    show g smiling at right
    g "Your little brother has a strong whippersnapper like me. And you, dear, have your grandfather."

    show m confused at left
    m "Pop? I thought he left us."

    g "He'll take care of you if y-"

    hide m
    hide g

    "Door bell rings"

    return



