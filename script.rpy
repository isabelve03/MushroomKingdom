# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define m = Character("Mari")
define na = Character("News Anchor")
define g = Character("Grandmama")
define mm = Character("Mailman")
define s = Character("Sadi")
define g = Character("General")
define r = Character("Professor R")

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
    scene bg room

    show m

    m "A note?"
    m "From the General? He wants to meet with me. Why was this ripped apart?"

    jump warcollegescene2

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
    play music "background2.mp3" fadein 0.5 loop

    na "...emergency drafting of eligible individuals with magical blood from all of Mushroom Kingdom to serve in the rising war effort."
    na "Tensions between Dragonkind and Mushroomkind have escalated, and we need every available mage to protect our kingdom..."

    show m shocked
    m "Grandmama? Is this..."
    m "Real?"

    show g sad at right
    g "It's been a long time coming, child. Desperation can make people do desperate things."

    show m upset at left
    m "Will I get drafted? What about Ebi?" 
    m "Grandmama I can't leave him behind!"

    show g smiling at right
    g "Your little brother has me to keep him safe. But you, dear, have the blood of your grandfather in you."

    show m at center
    "I haven’t seen him since I was little. Maybe never, really."
    "He’s more of a story than a person. The strongest mage, a ghost... not a grandfather."

    menu:
        "He was never there.":
            $ grandpa_opinion = "resentful"
            m "Why should I care about someone I barely know?"
            m "He left us. I don't need him and his - blood."
        "Would he notice me?":
            $ grandpa_opinion = "hopeful"
            m "You think I'll get to know him more?"
            m "I want to be more than just his story."
        "I don’t know how to feel...":
            $ grandpa_opinion = "uncertain"
            m "I’m not sure what to feel. Anxious? Curiosity?"
            m "All I know is that I AM going to be drafted."

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

    "The letter in my hands has a gold seal, I don't even need to open it to know what this is."

    m "This is real. I - "
    m "I have to leave. What if I can't do it? I have never been able to wield!"

    hide m
    show m at left
    show g at right

    g "It is hard, I know. But remember, you are not alone."
    m "What if I am not good enough?"

    show g sad at right 

    g "I believe in you. Ebi and I will cheer you on."

    hide g
    hide m
    show m at center

    "I can do this. I have to do this."

    jump warcollegescene1

label warcollegescene1:
    scene bg room
    with fade
    
    "A week later, I officially checked in, not needing an assessment for my wielding skills weirdly enough."
    
    show m
    
    m "This should be my dorm, room 103."
    
    hide m
    show m at right
    show s at left
    
    "Entering the dorm room, there's a girl unpacking - clearly tense."
    
    m "Hello I'm Mari! I believe I am your roommate?.."
    
    s "So... Mari, huh?"
    s "As in {i}his{/i} granddaughter."

    m "You've heard of him?"

    s "He's the general. Everyone has."
    "She scans me from head to toe."
    s "It makes more sense now."

    m "Excuse me?"

    s "Nothing. Just that some of us had to {i}earn{/i} our place here."
    
    menu:
        "Snap defensively":
            m "I deserve to be here just like you."
           
            s "Sure. Must be easy carrying a legend's name."
            s "I guess we will see if you live up to it."
        "Stay calm":
            m "I didn't ask for special treatment, if that's what you're implying."

            s "Didn't have to. It follows you around like a plague."
    "Her tone is cool, an invisible wall high arund Sadi."
    "I did not expect this sort of first impression, but it is clear Sadi is not thrilled with my connection to the General."

    $ sadi_relationship = 1

    hide s
    "Sadi turns and exits the room, leaving me alone."

    "Setting my things on the other bed, I find pieces of paper scattered on the floor."

    $setup_puzzle()
    call screen reassemble_puzzle
    
    return

label warcollegescene2:
    scene bg room
    with fade

    show m
    "Entering the office, I find the man I heard so much about but yet know nothing in front of me, reading off his chalkboard."

    show g at left
    if grandpa_opinion == "resentful":
        m "Do you remember me?"

        g "I remember all potential assets."

    if grandpa_opinion == "hopeful":
        m "Nice to finally meet the man who forgot about his family."

        g "I see you have fire in you. Good. You'll need it."

    if grandpa_opinion == "uncertain":
        m "You called me here... why?"

        g "Questions are a good sign of a healthy mind."

    "Is he serious? Is that all I am to him?"

    m "Why am I here?"

    g "Take a seat."

    "Begrudgingly, I take a seat and look up expectedly to what my grandfa- the general has to say."

    g "Many years ago, Dragons once shared the forests with us."

    if grandpa_opinion == "resentful":
        m "Why should I care? You're making me fight for a kingdom where I can't even wield. Yet I am here because of you."

    if grandpa_opinion == "hopeful":
        m "I always wondered why after all these years since they moved away, things are tense. Why are they trying to invade?"

    if grandpa_opinion == "uncertain":
        m "You called me here... why?"

    "He studies me for a moment with narrowed eyes."

    g "Dragons are a threat. They come after our resources, cross into our territory, they seek what is ours."
    g "We have no choice but to fight back."

    menu:
        "Challenge his view of dragons":
            $ dragon_opinion = "questioning"
            m "Do we know they're the enemy? Or just that they need what we have?"

            g "Compassion is noble. Naivety is dangerous."

        "Agree silently":
            $ dragon_opinion = "accepting"
            m "I see. I will do what I can."
            
            g "Good. We cannot afford doubt."

        "...":
            $ dragon_opinion = "unsure"
            m "..."

    m "It doesn't matter anyways cause I am unable to wield, how can I really contribute?"

    g "Magical blood runs deep within you. I can see the fire ready to ignite, you just need to see it yourself."

    m "And why didn't I go through the entrance skill assessment? Was that necessary?"

    g "You are my granddaughter, I have confidence in you."

    "Pft- confident that I will fail. I don't HAVE skills. Sadi was right..."

    g "Now let me see what you can do."

    m "That is what I was saying. I {i}CAN'T{/i}"

    "He tosses a wooden staff to me and I almost fumbled it."

    g "You are capable. Don't waste time thinking about failure before you even begin trying. Focus."

    "I stand there, holding the staff in my hands. The weight feels heavy, too foreign. I try to steady myself trying not to be awkward."

    menu:
        "Whine.":
            m "This feels impossible, I don't know why I am here. I can't do this."
            $ opinion_self = -1
            g "Nothing worth having comes easily. Now wield."
        "Wield?":
            "I attempt to focus on... something and the staff seemingly stares at me mockingly."
            $ opinion_self = 0
            g "That is a start."

    "I hesitate but grip the staff tightly. I try to imagine - "
    
    menu:
        "lightening striking down":
            pass
        "levitating myself":
            pass
        "blowing up stuff":
            pass
    
    "aaaaand nothing happens. Big surprise. Disgruntled, I slam the end of the staff to the ground in frustration."

    g "You're thinking too much. Stop trying to force something to happen. Magic isn't for show, it's a bond. Trust it. Let it guide you."

    "Hmph. This is ridiculous."

    m "Then what do I do? Trust to do what?"

    g "Breathe and listen and you'll understand. This comes from {i}you{/i}."

    menu:
        "Take his advice":
            "I close my eyes and listen to the stillness of the room. This time with no expectation. I felt the staff become lighter, a quiet hum began to sound and left as quickly as it came."
            g "Yes. Your power comes from within. I know you can do this."
            $ grandpa_opinion = "hopeful"
            $ opinion_self += 1
            "Huh.. maybe I can"
        "I am done":
            m "No. It isn't gonna work. I always wanted to wield growing up. I wanted to be like you, the strongest mage. But I am not good enough, I am not like you."
            $ opinion_self -= 1
            $ grandpa_opinion = "resentful"
            m "I am out of here."
    
    jump warcollegescene3

label warcollegescene3:
    scene bg room
    with fade

    "The hall looms with magic humming faintly in the air. Students are lined up, murmuring to one another."
    "Some look confident. Others, like me, look ready to run."

    show m at left
    show r at center
    
    r "Quiet!" # add jitter to this
    r "Welcome to your first trial. Where we test and push you to become protectors of this kingdom. Each of you will step inside of this circle alone. Your goal: wield an elemental bond."
    r "I am not looking for strength, just a connection."

    "Bruh."

    hide r
    show s with moveinright

    s "You're sweating. Try not to explode and take me with you, will you?"

    m "Ha. Very funny. What are you gonna wield, {i}ice{/i}."

    hide s
    hide m 
    show r

    r "Mari."

    hide r
    show m

    "I tense up. Of course I am first."
    "I step forward, bringing the staff the general gave me. With every eye burning the back of my head, my hands begin to tremble."

    if grandpa_opinion == "resentful":
        menu:
            "Fire":
                pass
            "Ice":
                pass
            "Lightening":
                pass
        "I clench my fists and try to command some sort of energy. The staff remains cold in my hands. I grit my teeth, but all I feel is the sting of silence."
        $ opinion_self -= 1

        show r at left

        r "That is enough, Mari. Next."
        $ first_trial_result = "failed"

        hide r

        "Hanging my head in defeat, I retreat to the edge of the circle of students beside Sadi." 

        show s at left

        s "Guess I was right after all. You don't belong here."
        $ sadi_relationship -= 1
        "Sadi stuck her tongue out at me before she was called over to demonstrate her skills."
    else:
        menu:
            "Breathe and focus.":
                "I close my eyes and focus inward. I stand there, listening. The staff hums softly and a bit of heat radiates from it."
                r "Well done Mari."
                "I open my eyes and see the staff has a small flame hovering over weakly."
                m "Woah-"
                r "Next."
                "I retreat to the edge of the circle of students beside Sadi."
                $ first_trial_result = "passed"

                show s with moveinleft

                s "Well, look at you. I guess there's hope for you after all."
                $ sadi_relationship += 1
                "I roll my eyes at her before she was called over to demonstrate her skills."

                $ opinion_self += 1
            "Think on what I wanna do.":
                menu:
                    "Fire":
                        pass
                    "Ice":
                        pass
                    "Lightening":
                        pass
                "I clench my fists and try to command some sort of energy. The staff remains cold in my hands. I grit my teeth, but all I feel is the sting of silence."
                $ opinion_self -= 1

                show r at left

                r "That is enough, Mari. Next."
                $ first_trial_result = "failed"

                hide r

                "Hanging my head in defeat, I retreat to the edge of the circle of students besides Sadi." 

                show s with moveinleft

                s "Guess I was right after all. You don't belong here."
                $ sadi_relationship -= 1
                "Sadi stuck her tongue out at me before she was called over to demonstrate her skills."

    hide m
    show s at center

    "Sadi steps forward. A thin, cool mist coils at her feet. With a confident flick of her wrist, snowflakes begin to swirl—indoors"
    "The room quiets. Even the air feels colder. Some students gasp, arms outstretched to catch the snow."
    "Scoffing, I cross my arms."

    show r at left

    "Excellent Sadi! Everyone better take note. Next."

    hide r

    show s at right
    show m at left

    s "Was that icy enough for you?"

    "Was that a {i}wink{/i}?"

    menu:
        "Actually it was snow not ice.":
            s "Erm actually."
            "She huffs in disapproval and decides to saunters off to other students."
            $ sadi_relationship -= 1
        "That was impressive.":
            if first_trial_result == "passed":
                s "Gotta show you who's on top. I could help you get better, you know."
                $ sadi_relationship += 3

                m "Wait- really? I'd like that."
                "Sadi shrugs, like it's nothing, but there's a hint of warmth in her eyes. She then decides to saunter off to other students."
            else:
                s "I did train all my life, it was why I was able to get through the entrance skill assessment. Not with a name or anything.."

                "Ima pretend I did not hear that last part."
                
                if opinion_self > 1:
                    m "Well, I know I can do it. I refuse to sit in that shadow of his."
                else:
                    "Ugh. I hate how she may be right. Maybe I really don't belong."

    jump warcollegescene4

label warcollegescene4:
    scene bg room
    with fade

    "The room smells like herbs and something slightly burnt. Rows of stone tables are lined with ingredients and glass vials. Cauldrons bubble faintly besides each table."

    "Students fill in the space, whispering amongst each other in apprehension."

    show r at center

    r "Your next trial is my favorite, potions. Your goal here is to make a potion useful for battle. You're being tested on intuition and care."
    r "Heed that last word, mistakes will have... explosive results. Now begin."

    hide r
    show s at right
    show m at left

    s "You better not blow anything up this time, Mari."

    menu:
        "Poke at her.":
            m "Maybe I’ll make a potion that turns you into a frog."
            
            s "Pfft. Bold of you to assume you could make that."
            "We both smile before searching for an empty cauldron and table to work with."
            $ sadi_relationship += 1
        "Snap at her.":
            m "Shouldn't you be focused on your own potion?"

            s "Just making sure you're not secretly planning to poison the class."
            $ sadi_relationship -= 1

    hide s
    hide m
    show m at center

    "I peered into an unoccupied cauldron to find it already boiling water."

    if first_trial_result == "failed":
        "After messing up the first trial, I feel the pressure mounting. My hands hesitate over each herb that lined the stone tables besides me."

    menu:
        "Make a frog potion":
            "I carefully measure out what I felt like I needed. Rosemary, duckfeathers, and a vial of deadflys."

            "The brew shifts to a dull green. The smell of swamp overpowers my nose."

            show r at left

            r "Hm, good work Mari."

            "I look up in surprise and smile at the hint of praise."
            "I let out a breath I didn’t know I was holding. It wasn’t perfect, but it worked. For once, I don’t feel like I’m fumbling through this."

            $ potion_trial_result = "passed"
            $ opinion_self += 1
            $ sadi_helped_potion = "didnot"

        "Experiment a little.":
            "I threw in the first two stalks of green that I saw and stir carefully."

            "The brew shifts to a dirt brown. The smell sharply claw at my nose and I recoil. The brew begins to bubble frantically."

            show r at left

            r "Careful! That mixture is unstable. Step back, you're done."

            "I back up in defeat, trying to ignore the lingering smell of burnt shame. Another failure. Another reason to doubt myself."

            $ potion_trial_result = "failed"
            $ opinion_self -= 1
            $ sadi_helped_potion = "didnot"

        "Ask Sadi.":
            m "Hey, Sadi... what should I do?"

            show s at right
            s "Aw, are you admitting I am better than you?"

            if sadi_relationship >= 2:
                s "Fine. Add a pinch of garlic. Maybe a vial of snail mucus."

                "I follow her advice, and the potion settles into a gentle golden hue. It smells sharp, but not bad."

                show r at left
                r "Collaborative thinking. I like that."

                "I glance at Sadi across from me. For a moment, we weren't rivals or roommates - just two peers. Maybe she is not as cold as she wants me to believe."

                $ potion_trial_result = "passed"
                $ sadi_relationship += 2
                $ opinion_self += 1
                $ sadi_helped_potion = "did"
            else:
                s "Figure it out yourself."

                "She turns away, leaving me flustered. I panic and throw in whatever."

                "The mixture hisses and spills over the rim of the cauldron."

                r "Step back, Mari. You’re done."

                "I back up in defeat, trying to ignore the lingering smell of burnt shame. Another failure. Another reason to doubt myself."

                $ potion_trial_result = "failed"
                $ opinion_self -= 1
                $ sadi_helped_potion = "rahdidnot"

    hide r
    hide s
    hide m

    show m at left
    show s at right

    if potion_trial_result == "passed":
        s "Huh. You didn’t turn us into frogs or make something explode. I’m almost impressed"
        
        m "Told you I’m not hopeless."

        s "I'm just glad I don't have to worry about being blown up in battle cause of you."
        $ sadi_relationship += 1
            
        if sadi_helped_potion == "did":
            m "Thanks for the help though."
            s "Guess I am not so icy after all."
            $ sadi_relationship += 2
        if sadi_helped_potion == "rahdidnot":
            m "Yet you kinda left me to dust."

            s "I thought you didn't want help?"
    else:
        s "Well, that was fun watching you fail."
        menu:
            "Why do you care so much about what I do?":
                s "Because you're the general's granddaughter and it feeds my ego."
                "She walks off with a teasing smirk."

            "Whatever.":
                if opinion_self >= 3:
                    m "I’ll do better next time."

                    s "We’ll see about that."
                else:
                    "I avert my gaze and leave Sadi be. All she does is bring me down."
                
                $ opinion_self -= 1
    jump warcollegescene5

label warcollegescene5:
    scene bg outside
    with fade

    "It has been a few weeks training constantly here at the war college."

    show m at center
    "For the first time since arriving, I start to feel like I belong. Magic became slightly easier through each use."

    if sadi_relationship >= 4:
        "Especially when Sadi starting teaching me her techniques."
    
    show s at right
    
    s "I can't wait to put my skills to use. I am itching to fight a real dragon."

    if dragon_opinion == "questioning":
        m "I still don't get why we're fighting dragons in the first place."

        s "You think too much. We're soldiers."

    if dragon_opinion == "accepting":
        if opinion_self >= 5:
            m "I agree, it'll be cool fighting a dragon in the name of our kingdom."

            s "Oooo how noble."
        else:
            m "Yeah I guess so."

            s "Such lack of enthusiasm, where's that fire?"

    if dragon_opinion == "unsure":
        if opinion_self < 3:
            m "I just hope I won't die."

            if sadi_relationship < 3:
                s "I hope you do."
            else:
                s "That is absolutely depressing."
        "I fall silent, a pit in my stomach when I think of fighting dragons."

    "Then the horns sounded."

    # play sound "horn.wav"

    "A blaring, ancient warhorn cuts through the air."

    show r at left

    r "Everyone inside! NOW!"

    "We freeze. Then chaos breaks loose."

    hide r
    hide s

    "The ground shakes below me as I scramble to gather what was happening."

    show r at left

    r "This is not a drill! The dragons have come to steal from us!"

    hide r

    menu:
        "Run with the others.": 
            "My instincts scream to follow the crowd. I turn on my heel and run."

            $ reaction_to_ambush = "act"

        "Stay and look.": 
            "I hesitate, glancing toward a smoke trail rising in the distance. A shape passes overhead with wings."

            "A dragon. Very much real and very much {i}BIG{/i}."

            $ reaction_to_ambush = "think"

    scene bg hall
    with fade

    "We panickly filed inside the hall. The windows rattle as a distant explosion echoes."

    show s at right
    show m at left

    s "What is happening? The dragons are attacking?!"

    if reaction_to_ambush == "think":
        "Yes, it's the dragons! I saw one flying."

    if reaction_to_ambush == "act":
        "I am not sure, I ran straight here."

    menu:
        "What I feel.":
            m "To be honest, I don't really think the dragons want to fight us."

            s "Why are you saying that {i}now{/i}. Especially we are being attacked right this second."

            m "Think about it. No one is hurt here and - "

            s "Stop...You’re starting to sound like my crazy mother."
            $ sadi_relationship -= 1 
        
        "What I know.":
            m "I just know that we have to fight."

            s "Piece of cake. Just gotta slay some dragons, no big deal."
            "Was that a hint of fear in her voice?"
            $ sadi_relationship += 1 

    "The torches flicker. The general's voice rings out from the front steps."

    show g at center
    g "You’re no longer students. This is real combat. We deploy in 15 minutes. Get your staffs and potions - GO!"

    hide r
    hide s
    hide m

    scene bg dorm_dusk
    with fade

    show m at center

    "Back in my room, I stare at the staff and potions laid out for me. My hands tremble as I slide them into my satchel."

    "I pull out a photo from the satchel and I see me and Ebi. My heart aches at the mere thought of losing him, or him losing me. I tuck it back deeper inside, hoping I can keep him safe."

    if opinion_self >=4:
        "I can do this."
        if grandpa_opinion == "hopeful":
            "Just as he taught me... breathe and focus."
    else:
        "Despite learning so much, I don't feel like it's enough."

    if sadi_relationship >=5:
        show s at left

        "Sadi appears at the doorway, already ready with her gear, arms crossed."

        s "Hey."

        m "Hey."

        "A long beat of silence passed between us."

        s "You ready?"

        m "As I will ever be. Dragons huh."

        s "Yea finally fighting dragons."

        "Another moment of silence passed."

        s "Say um. I got your back out there. I won't let you die if that's what you think."

        m "What? Why cause you'd miss me?"

        s "No. Definitely not. But then I would have to explain to the general his granddaughter got herself roasted. He'd have my head."

        "We both laugh quietly. It didn't last long, but it was real and what I needed."

        m "Don't worry, I got your back as well."
        
        s "Nah, ice queen prevails."
        
        "She smiles softly and leaves without another word."
    else:
        show s at left

        "Sadi appears at the doorway, already ready with her gear, arms crossed."

        s "Don't slow the rest of us down."

        m "Wasn't planning to."

        "She scoffs and walks off. I try to not let it string but it does."

    jump warcollegescene6

label warcollegescene6:
    scene bg battlefield_dusk
    with fade

    "The sun begins to set, as we all march out as one towards whatever the distance had in store for us."

    "Smoke curls into the sky. Magic lights the air in bursts of color as the seasoned soldiers clash with dragons. The sound of shouting and fire echoes across the battleground."
    
    show m at center

    "We rush into the battle with no hesitation nor question. The staff in my hand hums with energy, ready to ignite my fears to flame."

    if dragon_opinion == "questioning":
        "I don't even ask what we're defending. Only told that we have to fight."
        if opinion_self >= 4:
            "Still, my gut twists. We’re far from the Mushroom Kingdom’s borders. Why are the dragons here? What are they even after?"
        else:
            "I shut out the questions that stirred in my mind. I can’t afford to hesitate."

    "A burst of flame knocks a soldier to the ground. I jerk my staff up just in time to deflect a blast with a shaky shield spell. The heat burns my face."

    show dragon1 at right
    with dissolve

    "A dragon dives and slams into the ground in front of me. I marveled seeing a real dragon in front of me. It's sharp ivory knives for teeth. Razor sharp claws. Beady eyes."

    if opinion_self < 3:
        "I freeze for a second too long. The dragon lunges. I lift up my staff, willing it to protect me."

        "The dragon knocks my staff out from my hands and roared at me."

        if sadi_relationship >= 5:
            show s at left

            s "Duck!"

            "A bolt of frost smacks against the dragon’s jaw, knocking it sideways. Sadi rushes in, covering me."

            m "I really can't do this."

            s "Don't worry, I got your back. You can do this."
            $ opinion_self += 1

            "Together, we push the dragon back with spell after spell until it scrambling away. Shortly after, two dragons replace the empty spot."

            hide s

        else:
            "The dragon's claw slashes across my side. I scream, pain blinding. I scramble back as it looms over me — "

            " — until a blast from another soldier knocks it back. I’m left on the ground, trembling, my side bleeding."

            $ mari_injured = True

    elif opinion_self >= 4:
        "I plant my feet and calmly breathe. I meet its charge with a blast of fire. It staggers. I press on with my heart pounding."

        "The dragon whips its tail, knocking me down. When it's shadow begins to loom over me - "

        if sadi_relationship >= 5:
            show s at left

            "A bolt of frost smacks against the dragon's jaw, knocking it sideways. Sadi rushes in, covering me."

            s "Thought you might need backup."

            m "Your timing's a bit off."

            "As I get back to my feet, Sadi fights off the dragon til it retreats."

            s "Told you. Ice queen prevails."
            
            hide s

        else:
            "I channel a stream of water to the dragon's face, buying me time to get back on my feet. Panting and shaky, I managed to finish the fight myself and walk the dragon retreat."

    hide dragon1
    show 2dragons

    "I grip the staff tightly, readying myself against the two dragons."

    "The battle blurs around me—screams, fire, glowing staves. But then—"

    show chubbs at right
    with dissolve

    "A white dragon, larger than the rest, soars down. Its wings beat the smoke aside like wind."

    "It locks eyes with me. I raise my staff—but too late."

    "Its claws curl around my body and lift me into the sky."

    scene bg sky_war with fade

    "Wind whips past my face. We fly higher. I struggle, scream, kick—but the grip is iron."

    "Then it speaks."

    ch "Why are you fighting us?"

    m "...What?"

    ch "You think we want this? That we chose to burn and bleed and run from the skies?"

    if opinion_self >= 4 or sadi_relationship >= 5:
        m "I don’t know what to believe anymore. I was told... dragons are enemies. That’s it."

        ch "Told. But what do you see now?"

        "We land roughly on a cliffside. The dragon lowers me to the ground. Not gently—but not to kill me either."

        ch "I am Chubbs of the Hollow Sky. My kind flees starvation. Your kingdom calls us monsters."

        m "Then talk to them—don’t attack!"

        ch "We tried. They answered with arrows."

        "I hesitate. My staff burns in my hand, but I don’t raise it."

        menu:
            "I believe you.":
                $ mari_believes_dragons = True
                m "There has to be another way."

                ch "Then help me find it, Mari."

            "I don't trust you.":
                $ mari_believes_dragons = False
                m "Maybe you’re lying. Maybe this is another trick."

                ch "Then I’ll defend my kind. And you’ll go down with your lies."

    else:
        m "You're just trying to confuse me. Save your breath."

        ch "Then your blindness is a weapon sharper than your staff."

        "He drops me to the rocky ground. I barely land on my feet."

    scene bg cliffedge_battle
    with fade

    "Chubbs rears back. Magic flares. We fight—alone now. No army. Just truth and fury clashing on the edge of the world."

    return

label chubbs_fight:

    scene bg cliffedge_battle
    with fade

    "Chubbs' wings stretch wide, glowing slightly with an inner magic. His eyes burn—not just with anger, but desperation."

    ch "I don’t want to fight you, Mari. But I won’t let you stand in the way of our survival."

    if mari_believes_dragons:
        m "I don’t want to fight either. But they’ll never listen if I show up empty-handed!"

        ch "Then prove to them I'm not your enemy. Survive this."

        "He lunges—not with full force, but to test me."

    elif mari_believes_dragons is False:
        m "You’re lying. You don’t care who dies—just as long as you get what you want."

        ch "You think this is what we wanted? Then show me what you believe!"

        "He roars and strikes, forcing me into a defensive stance."

    else:
        m "I… I don’t know what to believe."

        ch "Then let your body speak while your mind catches up."

        "The wind howls around us as we clash."

    # FIGHT BEGINS

    "We trade blows—his claws against my spells. I dart and weave, narrowly dodging sweeping strikes. My staff shudders under the force of every block."

    if opinion_self < 3 and mari_injured:
        "Pain blossoms in my side. I gasp, stumbling. He doesn’t press the advantage—he waits."

        ch "Still you rise. Why?"

        m "Because I have to!"

        "I summon a burst of force and launch it, staggering him backward."

    elif opinion_self >= 4:
        "My feet are steady. My strikes land with purpose. I’m not just reacting—I’m adapting."

        ch "You’ve grown strong."

        m "I had to. Everyone expects me to fight. To kill."

        ch "And do you want to?"

        m "..."

    # After a few rounds...

    "The cliff shakes. Fire and smoke rise in the distance. Below us, the battle rages on—but here, it’s silent save for our breath."

    ch "Why are you really fighting, Mari?"

    menu:
        "To protect my people.":
            m "Because if I don’t, more will die. I have to protect my people."

            ch "Even if that means slaughtering mine?"

            m "...I don’t know. But I want to find another way."

        "Because I was told to.":
            m "Because… because it’s what I was trained for. What I’m supposed to do."

            ch "Then you are no warrior—just a weapon."

            "That stings. But maybe he’s right."

        "I’m not sure anymore.":
            m "I don’t know anymore. I came here thinking you were monsters. But now I see—you're just fighting to live."

            ch "Then help me. Let’s end this before more die."

    # END OF DUEL

    if mari_believes_dragons or opinion_self >= 4:
        "I lower my staff slowly."

        m "I won’t fight you anymore."

        ch "Then come with me. We’ll face the truth together."

        "He bows his head slightly, then crouches low. I climb onto his back. Below, the battlefield blurs as we take to the skies."

        $ chubbs_alliance = True

    else:
        "I raise my staff again—but my hands shake."

        ch "Then strike. If you truly believe we’re the enemy, finish this."

        "But I can’t move. Not really."

        "Before I can decide, a cry rises from the valley below. Someone’s in danger."

        ch "We’ll meet again, Mari. Decide who you are before then."

        "He dives off the cliff and vanishes into the smoke."

        $ chubbs_alliance = False

    return
