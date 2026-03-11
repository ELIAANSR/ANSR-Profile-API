#!/usr/bin/env python3
"""ANSR Profile — Premium PDF Report Generator FINAL
All Alexandre feedback applied. 17 pages. Dual radar. Real QR. Expert interpretation."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
import math

W, H = A4
M = 25 * mm
CW = W - 2*M

# Colors
DARK = HexColor("#1A1714")
IVORY = HexColor("#FAF5EE")
CHARCOAL = HexColor("#3A3530")
ACCENT = HexColor("#C4896A")
MUTED = HexColor("#B0A494")
DIM = HexColor("#7A7068")

PROF_COLORS = {
    "sunfire": HexColor("#D4845A"), "velvetblade": HexColor("#9B7A8F"),
    "eclipse": HexColor("#6B7A8B"), "summerstorm": HexColor("#8B6B5C"),
    "heartwood": HexColor("#7A8B5B"), "newmoon": HexColor("#5B7A7A"),
}

DIM_KEYS = ["alertness","sensitivity","vitality","connection","performance","aliveness"]
DIM_LABELS = ["Alertness","Sensitivity","Vitality","Connection","Performance","Aliveness"]

# ═══════════════════════════════════════
# FULL PROFILE DESCRIPTIONS (5 paragraphs each)
# Pattern · Mechanism · Cost · Strength · Blind Spot
# ═══════════════════════════════════════
FULL_DESCRIPTIONS = {
    "sunfire": [
        "From the outside, you are a force. You make decisions faster than most people form opinions. You carry more responsibility than a team of ten and you never drop a ball. People describe you as unstoppable, driven, magnetic. They don't use the word tired — because you don't let them see it.",
        "What's actually happening is neurological. Your sympathetic nervous system — the fight-or-flight branch — has become your permanent operating mode. Adrenaline and cortisol, designed for short bursts of emergency activation, are now your baseline chemistry. Your body doesn't know how to come down because it hasn't been down in years. Stillness doesn't feel like rest — it feels like falling.",
        "The cost is invisible but compounding. Your sleep is shallow or broken. Your body sends signals — tension, fatigue, illness — that you override with willpower. Your relationships have adapted to your unavailability. Beauty, pleasure, and sensory experience have been deprioritised so completely that they no longer register as needs. You eat to fuel, not to taste. You move to perform, not to feel. The bandwidth of your experience has narrowed to a single channel: output.",
        "But here is what the Sunfire pattern also tells us: your capacity is extraordinary. The energy your system produces is real — it's not manufactured from nothing. You have a nervous system with enormous range. The fire isn't the problem. The inability to come down from it is. The activation that makes you exceptional at 2pm is the same activation that wakes you at 3am.",
        "Your blind spot is this: you have confused rest with collapse. Because the only way your system currently comes down is through exhaustion or illness, you've concluded that rest is weakness. It's not. It's a skill your nervous system was never taught — and it's the single intervention that would change everything about how you feel, sleep, and sustain what you've built.",
        "If you\u2019ve seen Blue Jasmine, you\u2019ve watched your pattern on screen. Cate Blanchett\u2019s Jasmine burns magnificent \u2014 the fire, the performance, the relentless forward motion. And she cannot come down. When the structure collapses, she has no off switch. She keeps performing in an empty room. The difference between you and Jasmine is this: you\u2019re reading this report. Your system found its way here before the structure broke."
    ],
    "velvetblade": [
        "Your composure is impeccable. The clothes, the poise, the measured warmth that makes everyone feel you're fully present while keeping them at exactly the distance your nervous system requires. You've mastered the art of controlled proximity — close enough to be trusted, far enough to remain untouched.",
        "This is not a personality trait. It's a nervous system strategy. Your system learned early — or learned through sustained professional pressure — that vulnerability is expensive. Feeling deeply in a world that rewards composure became a liability. So your nervous system built a filter: sensory and emotional inputs arrive, but they're processed through a layer of aesthetic distance. You see beauty but don't feel it land in your body. You hear compliments but they don't reach your chest. You curate exquisite environments that regulate everyone around you — except you.",
        "The cost of the Velvet Blade is the most dangerous kind: invisible. From the outside, you look like the most composed person in the room. From the inside, you're sealed. The last time you cried from beauty — not from exhaustion, not from frustration, but from being genuinely moved — may be a memory you can't locate. Physical closeness has become something you manage rather than experience. Your sensitivity, which was once one of your greatest assets, now lives behind glass.",
        "What the Velvet Blade pattern preserved is worth naming: your standards. Your eye for beauty. Your capacity to create environments, experiences, and relationships of extraordinary quality. The blade didn't destroy your sensitivity — it protected it. The elegance isn't a mask. It's a real part of you. But it was never supposed to be the only part anyone — including you — could access.",
        "Your blind spot: you believe the armour IS the person. That without the composure, the poise, the controlled elegance, there's nothing strong enough to withstand the world. The practices for your pattern don't ask you to dismantle the armour. They bypass it — finding doorways through the body, through the senses, through channels your system forgot to guard.",
        "If you\u2019ve seen The Devil Wears Prada, you know your pattern by name. Meryl Streep\u2019s Miranda Priestly is the Velvet Blade at its most refined. The composure never slips. Everyone is kept at exactly the right distance. The one moment we see her without armour \u2014 no makeup, marriage ending \u2014 she seals it back up in thirty seconds. The difference: you\u2019re here because you felt the seal tightening. Your blade is real. So is the woman it\u2019s protecting."
    ],
    "eclipse": [
        "Something bright has been covered over. You function. You deliver. You show up every morning, execute at a high level, and nobody around you would use the word 'struggling.' But the inner experience of being alive has gone flat. Food has less taste. Music you once loved plays without landing. Weekends feel identical to weekdays. Beauty exists around you but it's behind glass — you can see it, name it, even appreciate it intellectually, but it doesn't reach your body.",
        "Your nervous system made an intelligent decision. Faced with sustained pressure it couldn't escape — professional demands, relational strain, years of overriding your own needs — it turned down the volume on everything. This is dorsal vagal withdrawal: the oldest survival mechanism in the autonomic nervous system. When fight-or-flight can't resolve the threat, the system conserves. Sensation, emotion, desire, pleasure — these are the first channels to go because they're not essential for functional survival. What remains is execution without experience.",
        "The cost is existential. You can describe your life in accurate detail but you can't feel it. Achievement lands as a fact, not a feeling. Relationships continue on competence and routine but the warmth has thinned. You may have noticed that your memory has changed — not cognitively, but experientially. Days blur together because nothing creates the emotional punctuation that makes moments distinct. You're not depressed in the clinical sense. You're in conservation mode. And conservation mode was designed to be temporary.",
        "What the Eclipse preserved is the most important thing: the light itself. The brightness your system covered over isn't destroyed — it's protected. Your sensitivity, your capacity for beauty, your ability to feel and connect — these are in storage, not in ruin. The nervous system is conservative: it doesn't discard what it might need again. It archives it. Every woman with an Eclipse pattern who begins sensory rehabilitation discovers the same thing: the volume comes back. Slowly. But it comes back.",
        "Your blind spot: you've normalised the flatness. Because it arrived gradually — not as a crisis but as a slow fade — you may have concluded that this is just what life feels like at your age, at your level, at this stage. It's not. The flatness is a nervous system state, not a life sentence. And it responds to specific, sensory intervention faster than most women expect.",
        "If you\u2019ve seen Big Little Lies, you\u2019ve watched your pattern in Nicole Kidman\u2019s Celeste. Perfect house. Perfect children. Perfect face. She sits in her ocean-view living room and the beauty doesn\u2019t reach her. Everything is curated. Nothing is felt. The difference: conservation mode was designed to be temporary. You\u2019re reading this because your system is ready for the light to come back."
    ],
    "summerstorm": [
        "You feel everything. The tension in a room before anyone speaks. The beauty of a sky that nobody else stopped to notice. The pain of a stranger on the metro. The energy shift when someone lies. Your nervous system is a high-fidelity receiver — it picks up signals most people's systems filtered out years ago.",
        "This is not anxiety, though it's been called that. And it's not weakness, though the professional world has treated it that way. What you have is a nervous system with exceptional sensitivity — a wider bandwidth of experience than most people will ever access. In polyvagal terms, your neuroception (the unconscious detection of safety and threat) is highly calibrated. You don't just think about danger or beauty — you feel it in your body before your mind has words for it.",
        "The problem isn't the sensitivity. It's the absence of a container. Your system absorbs everything — beauty, pain, tension, stimulation — and has no reliable mechanism for releasing what isn't yours. The result is overwhelm that arrives without warning, emotional flooding that doesn't match the apparent trigger, and a constant background hum of overstimulation that makes you retreat, isolate, or shut down. You may have been told you're 'too much.' You're not too much. You're uncontained.",
        "What the Summer Storm preserves is rare and valuable: the capacity to feel the world at full resolution. Most women in high-pressure leadership have lost this. Their systems traded sensitivity for survival. Yours didn't. You still feel spaces. You still feel people. You still feel beauty. In a regulated state, this sensitivity is an extraordinary leadership asset — you read rooms, anticipate problems, and create experiences others can't because you sense at a level they can't access.",
        "Your blind spot: you've been managing your sensitivity instead of building a container for it. Every coping mechanism you've developed — withdrawing, controlling your environment, limiting stimulation — is about reducing the input. The practices for your pattern do the opposite: they build the container so the input doesn't flood. Your sensitivity stays. Your overwhelm doesn't.",
        "If you\u2019ve seen A Star Is Born, you\u2019ve watched your pattern in Lady Gaga\u2019s Ally. Raw, unfiltered sensitivity. She feels the music in her body before she has words for it. The talent is enormous and has no container. The bathroom scene where she writes on her arm \u2014 that\u2019s the sensitivity looking for edges. The difference: you don\u2019t need less feeling. You need the container these practices will build."
    ],
    "heartwood": [
        "You are the person everyone calls. Not for advice — for presence. When the team is falling apart, you hold it together. When a friend is in crisis, you're the first message she sends. When the family needs organising, coordinating, carrying — you don't wait to be asked. You show up. You've always shown up.",
        "The Heartwood pattern is the nervous system expression of one-directional care. Your system learned — through family dynamics, professional culture, or the specific demands of your role — that giving is safe and receiving is dangerous. The neurological mechanism is subtle: the circuits that activate when you care for others (ventral vagal, social engagement) are fully online. The circuits that would allow you to receive care, let down your guard, and be held — those have been gradually suppressed. Not because they're broken. Because they were never exercised.",
        "The cost is the most generous form of depletion: nobody notices it, including you. You create beautiful experiences for everyone around you. You curate environments, manage emotions, hold space, give gifts, remember details. And the care flows in one direction. Out. Never in. Compliments bounce off. Help feels like failure. Being taken care of triggers anxiety rather than relief. Your nervous system has been running a giving pattern so long that receiving has become physiologically uncomfortable.",
        "What the Heartwood preserves is the deepest kind of strength: the ability to sustain others. This isn't codependency — it's a genuine, powerful capacity for care. The problem isn't that you give. It's that the giving has become the only channel through which your nervous system knows how to engage. You've built your identity, your relationships, and your professional value around being the one who holds everything up. And nobody thinks to check on the heartwood.",
        "Your blind spot: you believe that needing is the opposite of strength. That the moment you stop holding, everything falls. That receiving would somehow diminish the extraordinary giving you do. It won't. The beauty and care you create for others is the exact medicine your own nervous system is missing. Redirecting even a fraction of it inward isn't selfish. It's the only way to sustain what you've built.",
        "If you\u2019ve seen Volver, you\u2019ve watched your pattern in Pen\u00e9lope Cruz\u2019s Raimunda. She holds the family. She holds the secret. She holds the restaurant, the daughter, the dead. The care flows one direction. Almod\u00f3var gave her every burden and never let anyone check on her. The difference: you\u2019re here because some part of you knows the holding has to include you."
    ],
    "newmoon": [
        "Something is shifting. It's not dramatic — not a breakdown, not a crisis. More like a direction. A quiet, persistent knowing that the way you've been living isn't the way you want to keep living. The sensitivity is flickering back on. You're noticing things you haven't noticed in years — a colour, a feeling, a desire that has no productive justification.",
        "The New Moon pattern means your nervous system is in active transition. The old strategies — the ones that kept you performing through sustained pressure — are loosening their grip. This might feel like instability, but it's not. In polyvagal terms, your system is moving from a fixed state (sympathetic or dorsal) toward greater flexibility. The moments of feeling — even when they're uncomfortable — are evidence that your ventral vagal pathway is re-engaging.",
        "You might be experiencing a paradox: you feel more and simultaneously feel more confused. Emotions that were muted are surfacing at inconvenient times. Desires that were archived are demanding attention. The life that was 'fine' is suddenly not enough — not because it got worse, but because your capacity to feel what was always missing has returned. This is not regression. This is emergence.",
        "What the New Moon tells us is that your nervous system is ready for something most women in sustained pressure never reach: genuine reorganisation. Not more coping. Not better management. An actual shift in how your system processes safety, beauty, and aliveness. The patterns that brought you here served you. They kept you functional when your system needed to conserve. But they were always temporary — and your system knows it.",
        "Your blind spot: the temptation to turn this emergence into another project. To optimise the shift. To set goals for your awakening. To announce the change before it's strong enough to withstand the world's opinion. The New Moon is delicate. It needs protection, not acceleration. The practices for your pattern don't force change — they protect what's already stirring and let your nervous system show you the pace.",
        "If you\u2019ve seen Eat, Pray, Love, you\u2019ve watched your pattern in Julia Roberts\u2019s Elizabeth. The old life isn\u2019t wrong \u2014 it\u2019s just not hers anymore. Something is pulling her toward she-doesn\u2019t-know-what. The emergence is messy, beautiful, and fragile. The difference: you don\u2019t need to leave everything. You need to protect what\u2019s stirring until it\u2019s strong enough to reshape what stays."
    ],
}

# ═══════════════════════════════════════
# HOPE PARAGRAPHS (Rose Gold accent border)
# ═══════════════════════════════════════
HOPE_TEXTS = {
    "sunfire": "The fire doesn't need to go out. It needs a hearth. Your system has extraordinary capacity — what it's missing is the ability to come down without collapsing. That's not weakness. It's the one skill your nervous system was never taught.",
    "velvetblade": "The woman underneath the elegance is still breathing. The practices that reach her don't ask you to dismantle the armour. They bypass it — through the body, through the senses, through doorways your system forgot to guard.",
    "eclipse": "The light didn't leave. Your system protected it by covering it over. The path back is not through force — it's through the body's oldest safety signals: warmth, gentle touch, micro-sensory experiences. One small beautiful thing at a time. Your system doesn't need to be fixed. It needs to be told, through sensation, that the emergency is over.",
    "summerstorm": "You don't need less feeling. You need a container strong enough to hold what you feel. The practices for your pattern don't numb your sensitivity — they give it structure. A nervous system container that lets your extraordinary capacity become a leadership advantage instead of the thing that drains you.",
    "heartwood": "The beauty and care you create for others is the exact medicine your own nervous system is missing. Redirecting even a fraction of it inward is not selfish. It's the beginning of sustainability. It's the only way to continue being the woman who holds everything up — without the everything including you.",
    "newmoon": "What's stirring in you is not a crisis. It's an emergence. Your nervous system is beginning to remember what it turned off. The practices for your pattern don't force the change — they protect it. They give the thawing somewhere safe to happen, at the pace your system needs."
}

# ═══════════════════════════════════════
# DUAL-PROFILE DESCRIPTIONS (30 combos)
# ═══════════════════════════════════════
DUAL_DESCS = {
    ("velvetblade","heartwood"): "The armour is impeccable. The composure never slips. But underneath the elegance, there's a woman who holds everything up for everyone around her \u2014 and lets nothing back in. The blade keeps the world at arm's length. The heartwood keeps giving from behind the glass. The combination is the most invisible form of depletion: she looks like she has everything together while running on a deficit nobody sees.",
    ("velvetblade","sunfire"): "Composed on the surface, relentless underneath. The elegance masks an engine that never stops. She controls how close anyone gets \u2014 but she can't control the drive that keeps her performing long after her body begged her to stop.",
    ("velvetblade","eclipse"): "The armour still gleams but there's less and less behind it. She curates beauty for others while feeling increasingly little herself. The blade that once protected her sensitivity now keeps her sealed from the very experiences that could bring her back.",
    ("velvetblade","summerstorm"): "Impeccable on the outside, overwhelmed underneath. She feels everything but shows nothing. The composure is real \u2014 and so is the flooding behind it. The most exhausting combination: managing the world's perception while absorbing its energy.",
    ("velvetblade","newmoon"): "The armour is starting to crack \u2014 not from pressure, but from the inside. Something underneath the elegance is waking up, pushing against the composure she's maintained for years. She's not breaking down. She's breaking open.",
    ("sunfire","velvetblade"): "Burns at full intensity but with impeccable control. She performs at extraordinary levels while maintaining an elegance that makes it look effortless. The fire is real. The ease is not.",
    ("sunfire","heartwood"): "Drives herself relentlessly and gives what's left to everyone around her. Her energy is extraordinary \u2014 but it flows outward in every direction, and the source is running dry.",
    ("sunfire","eclipse"): "The fire is still burning but the light is fading. She pushes harder and feels less. Achievement still arrives but satisfaction doesn't. The intensity that once felt like power now feels like the only thing keeping the emptiness at bay.",
    ("sunfire","summerstorm"): "Burns hot and feels everything. The intensity of her drive meets the intensity of her sensitivity \u2014 and neither has a container. She oscillates between relentless performance and overwhelming emotion.",
    ("sunfire","newmoon"): "The fire that drove her for years is becoming something else. Not dying \u2014 transforming. She can feel the shift but she can't stop performing long enough to understand it.",
    ("eclipse","sunfire"): "Flat on the surface, still burning underneath. She's gone quiet but the drive hasn't stopped \u2014 it's just lost its object. The most disorienting combination: an engine running at full speed with nowhere to go.",
    ("eclipse","velvetblade"): "The flatness has an elegance to it. She's composed and contained \u2014 but the containment isn't style anymore, it's numbness. The beauty she curates around her is a memory of what she used to feel.",
    ("eclipse","heartwood"): "Still giving, barely feeling. The care continues on autopilot but the warmth behind it has thinned. She holds others together while quietly going flat inside.",
    ("eclipse","summerstorm"): "The sensitivity didn't die \u2014 it went underground. She looks shut down but there are moments when feeling erupts from beneath the flatness with startling force. Then it retreats again.",
    ("eclipse","newmoon"): "The eclipse is beginning to thin. There are moments \u2014 a colour, a feeling, a sudden unexplained emotion \u2014 where light breaks through the flatness. She's not coming back to who she was. She's becoming who she's never been.",
    ("summerstorm","velvetblade"): "Feels everything but shows nothing. The sensitivity is enormous \u2014 and completely hidden. She's built an elegant container around her overwhelm that nobody can see through.",
    ("summerstorm","heartwood"): "Absorbs everyone's pain and holds it. She feels the room, feels the team, feels her family \u2014 and carries all of it. Her sensitivity serves others at the cost of flooding herself.",
    ("summerstorm","sunfire"): "Intense in every direction. She feels at full volume and performs at full volume \u2014 and the two exhaust each other. The sensitivity fuels the drive. The drive overwhelms the sensitivity.",
    ("summerstorm","eclipse"): "The sensitivity comes and goes. Some days she feels everything at full force. Other days the system shuts it all down to survive. She never knows which version of herself will show up.",
    ("summerstorm","newmoon"): "Her extraordinary sensitivity is beginning to find its purpose. What used to flood her is becoming a compass \u2014 pointing toward something she can't name yet but can feel pulling.",
    ("heartwood","velvetblade"): "Holds everything up with impeccable grace. She gives, she carries, she curates beautiful experiences for others \u2014 and behind the elegance, she's running on empty.",
    ("heartwood","sunfire"): "Gives with relentless intensity. She doesn't just hold \u2014 she drives while holding. The combination produces a woman who carries more than anyone and never slows down.",
    ("heartwood","eclipse"): "Still giving, barely feeling. The care continues on autopilot but the warmth behind it has thinned. She holds others together while quietly going flat inside.",
    ("heartwood","summerstorm"): "Holds everyone while feeling everything. She absorbs their pain and carries their weight \u2014 and her sensitivity makes every burden heavier. The most generous and most overwhelmed combination.",
    ("heartwood","newmoon"): "Something in the giving is shifting. She's beginning to notice the cost. Beginning to wonder what it would feel like to receive. The heartwood is learning to ask a dangerous question: what about me?",
    ("newmoon","velvetblade"): "The shift is happening behind an elegant exterior. Nobody sees the transition because her composure is still perfect. But inside, everything is rearranging.",
    ("newmoon","sunfire"): "The emergence has energy. She's not just thawing \u2014 she's igniting. The new direction has a drive behind it that surprises even her.",
    ("newmoon","heartwood"): "The shift is toward herself. After years of giving, her nervous system is redirecting attention inward. The most tender combination: a woman learning to hold herself.",
    ("newmoon","eclipse"): "Light is returning through the cracks. The new moon is lifting an eclipse that's been in place for years. What she feels is disorienting \u2014 because she hasn't felt anything this clearly in a long time.",
    ("newmoon","summerstorm"): "The sensitivity is flooding back in. She's feeling things she hasn't felt in years and it's overwhelming and beautiful at the same time. The emergence is intense.",
}

def get_dual_desc(primary, secondary):
    key = (primary, secondary)
    if key in DUAL_DESCS:
        return DUAL_DESCS[key]
    return f"Your nervous system runs two patterns simultaneously: {PROFILES_BASIC[primary]['name']} as the dominant strategy, with {PROFILES_BASIC[secondary]['name']} surfacing under extreme pressure. This combination shapes how you crash, how you recover, and what brings you back."

PROFILES_BASIC = {
    "sunfire": {"name": "Sunfire", "tag": "Burns magnificent and unsustainable.", "short": "Locked in activation. She performs at extraordinary levels \u2014 makes decisions faster than most people form opinions, carries more than a team of ten, never drops a ball. Her body never comes down. Rest feels like failure. Stillness triggers anxiety. The 3am wake-ups, the jaw tension, the exercise that feels compulsive rather than joyful \u2014 these are a nervous system running on cortisol as a baseline, not a boost. If you\u2019ve seen Blue Jasmine, you\u2019ve seen her pattern. Cate Blanchett\u2019s Jasmine burns magnificent. The fire is real. The inability to come down is what destroys."},
    "velvetblade": {"name": "Velvet Blade", "tag": "Elegant and dangerous. The danger is to yourself.", "short": "Armour made of elegance. She controls proximity with precision \u2014 warm enough to be trusted, distant enough to remain untouched. The clothes, the poise, the curated spaces. She sees beauty but doesn\u2019t feel it land in her body. Compliments arrive but don\u2019t reach her chest. The last time she cried from beauty \u2014 not exhaustion \u2014 is a memory she can\u2019t locate. Meryl Streep as Miranda Priestly in The Devil Wears Prada. The composure never slips. The one moment we see her without armour, she seals it back up in thirty seconds."},
    "eclipse": {"name": "Eclipse", "tag": "The light didn't leave. Something moved in front of it.", "short": "Everything has gone flat. She functions, delivers, shows up \u2014 but sensation, beauty, and pleasure have been turned down to survive. Food has less taste. Music doesn\u2019t move her. Weekends feel identical to weekdays. She can describe her life in accurate detail but she can\u2019t feel it. Achievement lands as fact, not feeling. Not depressed \u2014 in conservation mode. Nicole Kidman as Celeste in Big Little Lies. Perfect house, perfect children, perfect face. She sits in her ocean-view living room and the beauty doesn\u2019t reach her."},
    "summerstorm": {"name": "Summer Storm", "tag": "You feel everything. That's not the problem.", "short": "Sensitivity at full volume without a container. She absorbs everything \u2014 the tension in a room before anyone speaks, the beauty of a sky nobody stopped to notice, the pain of a stranger on the metro. The world comes in too fast and too loud. Not too much. Uncontained. She may have been told she\u2019s \u2018too sensitive.\u2019 She\u2019s not. She\u2019s uncontained. Lady Gaga as Ally in A Star Is Born. Raw, unfiltered sensitivity. She feels the music in her body before she has words. The talent is enormous and has no container."},
    "heartwood": {"name": "Heartwood", "tag": "The one who holds everything up. The one nobody thinks to check on.", "short": "The care flows one direction. Out. Never in. She gives, organises, carries, shows up. She creates beautiful experiences for everyone around her. Compliments bounce off. Help feels like failure. Being taken care of triggers anxiety rather than relief. Her system has been running a giving pattern so long that receiving has become physiologically uncomfortable. Pen\u00e9lope Cruz as Raimunda in Volver. She holds the family, the secret, the restaurant, the daughter. Nobody asks what it costs her."},
    "newmoon": {"name": "New Moon", "tag": "Invisible \u2014 but already pulling the tide.", "short": "Something is shifting. Not dramatic \u2014 more like a direction. The old patterns are loosening their grip. She\u2019s noticing things she hasn\u2019t noticed in years \u2014 a colour, a feeling, a desire that has no productive justification. The sensitivity is flickering back on. This is the most delicate moment. The shift is genuine but fragile. Julia Roberts as Elizabeth in Eat, Pray, Love. The old life isn\u2019t wrong \u2014 it\u2019s just not hers anymore."},
}

PRACTICES = {
    "sunfire": [("The Extended Exhale", "Breathe in for 4 counts, out for 8. The extended exhale activates the vagal brake \u2014 the parasympathetic mechanism that slows your system down. This isn't a breathing exercise. It's a neurological intervention: the exhale phase directly stimulates the ventral vagus nerve, reducing heart rate and cortisol in under 90 seconds. Do this for 2 minutes before sleep. Your body will resist it \u2014 the acceleration will feel like restlessness, like you should be doing something. That resistance is the Sunfire pattern talking. Breathe through it."),("Deliberate Deceleration", "Choose one daily transition \u2014 arriving home, finishing a meal, ending a call \u2014 and add 30 seconds of deliberate stillness. Not rest. Stillness. Your nervous system has been trained to interpret the gap between tasks as a threat. This practice teaches it that the space between demands is safe. The first week will feel unbearable. By the third week, your system will begin to crave it. That craving is your body remembering what regulation feels like."),("Warm Descent", "Before sleep, hold something warm \u2014 a cup, a heated cloth, your own hands pressed against your chest. Warmth activates thermoreceptors that signal safety directly to the hypothalamus, bypassing cognitive resistance. For a Sunfire system that can't think its way to calm, this is the back door. The warmth tells your autonomic nervous system what no amount of willpower can: the day is over. You are safe. You can come down now.")],
    "velvetblade": [("The Unguarded Minute", "Once a day, let your face go completely soft. Unclench the jaw. Let the eyes unfocus. Release the forehead. This isn't relaxation \u2014 it's neuroanatomy. The muscles of your face are directly wired to your vagal nerve through cranial nerves V and VII. When the face softens, the nervous system receives a safety signal that bypasses your cognitive armour entirely. For the Velvet Blade, the face is where the composure lives. Releasing it \u2014 even for 60 seconds, even alone \u2014 creates a crack in the aesthetic distance your system has built. One minute. No audience. No mirror. Just the face your nervous system forgot it was holding."),("Receive Without Composing", "The next time something beautiful appears \u2014 a sky, a sound, a moment \u2014 do not compose a response. Do not frame it. Do not find the words. Just let it land in your body without your mind organising the experience. Your Velvet Blade pattern processes beauty through an aesthetic filter: you see it, name it, curate it \u2014 and in doing so, you manage it rather than feel it. This practice bypasses the filter. It's the difference between observing beauty and being moved by it. When you feel something land in your chest rather than your mind, the blade is lifting."),("The Unperformed Moment", "Find 5 minutes alone where you are not performing for anyone \u2014 including yourself. No optimising. No reflecting. No mental narration. Just being, without an audience. For your pattern, this is the most challenging practice because the Velvet Blade performs even in solitude \u2014 composing thoughts, maintaining an internal aesthetic, curating the experience of being alone. Five minutes of genuinely unperformed existence interrupts the deepest layer of the pattern. Your nervous system needs to learn that you exist when nobody \u2014 not even you \u2014 is watching.")],
    "eclipse": [("The Warm Anchor", "Place your hand on your own chest or stomach. Hold it there for 90 seconds. This activates C-tactile afferent nerves \u2014 specialised fibres that process gentle touch and send safety signals directly to the insular cortex, the brain region responsible for interoception (awareness of your body from the inside). For an Eclipse system that has turned down internal sensation, this practice re-teaches the body that it exists and that it's safe to feel. Start here. Every day. The flatness didn't arrive in a day. It leaves the same way \u2014 through small, repeated sensory signals that your system can't ignore."),("One Beautiful Thing", "Each morning, find one thing that's beautiful. Not profound. Not Instagram-worthy. Just beautiful. A colour. A sound. A texture. Notice it with your body, not your mind. Name where in your body you feel it \u2014 chest, throat, hands. This is micro-sensory rehabilitation: you are rebuilding the neural pathways between aesthetic experience and physical sensation that your system shut down during conservation. The goal isn't to feel overwhelmed by beauty. It's to feel anything at all \u2014 and to notice that you felt it."),("The Slow Return", "Your system turned the volume down gradually. It comes back the same way. Do not force feeling. Do not chase sensation. Do not set goals for your emotional awakening. The Eclipse pattern responds to gentleness, not intensity. When a moment of feeling arrives \u2014 however small, however brief \u2014 don't grab it. Let it be. Let it leave. Notice that it came. That noticing is the practice. Your nervous system is learning that sensation is safe again. Every moment of feeling that arrives and leaves without crisis teaches it to let more through next time.")],
    "summerstorm": [("The Container", "When overwhelm arrives, place both hands on your sternum. Press gently. Breathe into the pressure of your own hands. This creates a physical boundary \u2014 a literal container for the sensation. You're not stopping the feeling. You're giving it edges. For the Summer Storm, sensation arrives without boundaries: it floods, it fills, it overwhelms. The hands on the chest create a tactile boundary that your nervous system can use to contain what it's processing. The pressure activates mechanoreceptors that signal containment to the insula. Your sensitivity stays. The flooding stops."),("Sensory Boundaries", "Before entering a stimulating environment \u2014 a meeting, a dinner, a crowded space \u2014 set a physical intention: place your hand briefly on your own arm or wrist. This micro-gesture tells your nervous system: 'I am here. I am separate. I will feel what is mine and release what is not.' Your Summer Storm pattern absorbs other people's states because your neuroception (unconscious safety scanning) runs at high resolution. This practice doesn't lower the resolution. It draws a line between your signal and others'. You can feel the room without carrying it home."),("Structured Beauty", "Seek aesthetic experiences with a deliberate beginning and end \u2014 a single song, a 10-minute walk, one page of a book, one painting. Open-ended beauty floods a Summer Storm system because there's no container, no edge, no natural stopping point. Contained beauty \u2014 beauty with a frame \u2014 lets your sensitivity receive the experience fully without the overwhelm of infinity. This is why galleries work and nature sometimes doesn't: the frame provides the containment your nervous system needs. Build frames around your beauty. Your sensitivity will thank you.")],
    "heartwood": [("The First Beautiful Thing That's Yours", "Tomorrow morning, before you do anything for anyone else, give yourself one beautiful experience. A cup of tea held with full attention. A song with your eyes closed. Two minutes of sky. This isn't self-care \u2014 it's nervous system rewiring. Your Heartwood pattern has the giving circuits fully online and the receiving circuits suppressed. Every morning that begins with output reinforces the pattern. One small beautiful experience that belongs to you \u2014 before the giving begins \u2014 teaches your system that receiving is physiologically safe. The resistance you feel is the pattern. The practice is doing it anyway."),("Receive Without Reciprocating", "The next time someone offers you something \u2014 a compliment, help, a gift, a meal they cooked \u2014 receive it without giving anything back. Don't deflect. Don't minimise. Don't immediately reciprocate. Just let it in. Notice what your body does: the tension in your shoulders, the impulse to say 'you didn't have to,' the anxiety that rises when you owe someone. That anxiety is your nervous system interpreting receiving as debt. This practice teaches it that receiving is not a transaction. It's a sensation. Let it be uncomfortable. The discomfort is the Heartwood rewiring."),("The Boundary of Beauty", "Create one space in your home that is only for you. Not shared. Not functional. Not for hosting, not for work, not for the family. Beautiful. A corner with a candle. A shelf with objects that move you. A chair by a window. This space exists because you deserve beauty, not because someone else needs it. For the Heartwood, every beautiful thing you create is for others. This practice creates one exception \u2014 one space where the beauty flows inward. When you sit in that space, you are practising the thing your nervous system has never learned: receiving what you give to everyone else.")],
    "newmoon": [("The Question Beneath The Question", "When you feel an impulse \u2014 to change something, to move toward something, to quit something \u2014 pause and ask: what is my nervous system actually asking for right now? Don't answer immediately. Let the question sit for 24 hours. The New Moon pattern generates impulses that feel urgent because your system is waking up after a long period of suppression. Not every impulse is a direction. Some are just the nervous system testing its range. The practice is learning to distinguish between a genuine signal and the noise of emergence. If the impulse is still there tomorrow, it's signal."),("Follow Beauty as Compass", "For one week, notice what draws you. Not what you should want \u2014 what your body actually moves toward. A colour. A texture. A person. A direction. A type of music you haven't listened to in years. Beauty is your nervous system's way of pointing toward what it needs for restoration. For the New Moon, these attractions are not random and not frivolous \u2014 they're your system's earliest signals of what the next version of your life might look like. Don't act on them yet. Just notice. Collect the data. The pattern will become visible."),("Protect the Stirring", "What's emerging in you is fragile. Do not turn it into a plan. Do not set goals for your transformation. Do not announce the change on social media or at dinner with friends. Let it be inarticulate and private until it's strong enough to withstand the world's opinion. The New Moon is the most delicate moment in the nervous system cycle \u2014 the system is open, sensitive, and suggestible. External input at this stage can either support or hijack the emergence. Your practice is protection: silence, privacy, and the discipline to let something be unfinished.")],
}

SENSORY_MAP = {
    "V": ("Light & Space", "Your nervous system responds most powerfully to visual openness \u2014 natural light, horizons, open sky, uncluttered space. Your eyes are your primary regulation organ. When your visual field opens, your nervous system follows. This is why a room with a view calms you, why clutter agitates you, and why the first thing you need after sustained pressure is space.", "Your answers consistently pointed toward visual regulation \u2014 you responded most strongly to questions about open space, natural light, and visual beauty. Your system doesn't just appreciate visual openness; it depends on it for safety and restoration."),
    "A": ("Sound & Voice", "Your nervous system restores most effectively through auditory experience \u2014 music, the human voice, specific frequencies, and silence. The auditory system shares direct neural links with the vagus nerve through the middle ear muscles. When you hear certain frequencies \u2014 particularly the prosodic range of the human voice \u2014 your nervous system receives one of its strongest safety signals. This is why the right music changes your breathing and why a trusted voice calms you faster than any thought.", "Your responses mapped clearly to auditory regulation. When your system seeks safety, it reaches for sound \u2014 music, voice, or deliberate silence \u2014 before any other channel. This is supported by polyvagal research showing the auditory pathway is one of the most direct routes to vagal activation."),
    "M": ("Water & Warmth", "Your nervous system restores most effectively through thermal and aquatic sensation \u2014 showers, baths, the sea, rain, warmth against skin. This is one of the body's oldest safety signals. The autonomic nervous system processes water and warmth as evidence that the emergency is over. This is why a bath does what willpower can't, and why warm hands on your chest at night settle something no thought can reach.", "Your responses revealed a consistent pattern: warmth and water are your nervous system's primary language for safety. When asked about what restores you, your body pointed toward thermal and aquatic sensation before anything else."),
    "S": ("Touch & Texture", "Your nervous system finds its way back through tactile sensation \u2014 weight, fabric, stone, warmth in the hands. Your skin is your largest sensory organ and your body uses it to ground, contain, and regulate. When you touch something with deliberate attention, your system receives a safety signal that bypasses thought entirely. This is why a heavy blanket calms you and why holding a warm cup changes your breathing.", "Your responses mapped clearly to tactile regulation. When your system seeks safety, it reaches for texture, weight, and physical contact before any other channel. This isn't preference \u2014 it's your body's most efficient pathway back to itself."),
    "O": ("Scent & Breath", "Your nervous system restores most effectively through olfactory experience \u2014 essential oils, earth after rain, wood, coffee, the scent of someone safe. The olfactory bulb is unique among sensory organs: it connects directly to the amygdala and hippocampus, bypassing the thalamic relay that other senses require. This means scent reaches your emotional and memory centres before your conscious mind can intervene. This is why a familiar scent can change your entire state in seconds.", "Your responses pointed consistently toward olfactory regulation. Your system uses scent as its primary doorway to safety and memory. This is one of the most ancient and direct sensory pathways \u2014 scent was the first sense to evolve and remains the most emotionally immediate."),
    "D": ("Signal Lost", "Your nervous system has lost reliable access to sensory regulation. No single channel consistently brings you back to yourself. This isn't failure \u2014 it's deep depletion. Your sensory channels aren't broken; they're dormant. The practices in your restoration path are designed to rebuild these channels one at a time, starting with the simplest and most direct: warmth and touch.", "Your responses didn't converge on a single sensory channel. This tells us your system's regulatory pathways have been suppressed by sustained pressure. The good news: these channels don't disappear. They go dormant. Rebuilding starts with the most primitive \u2014 warmth and touch."),
}

ALL_SENSORY_CHANNELS = [
    ("V", "Light & Space", "Visual openness \u2014 horizons, natural light, uncluttered space. The eyes as a primary regulation organ, telling the nervous system the world is safe and spacious."),
    ("A", "Sound & Voice", "Auditory regulation \u2014 music, prosody, silence, the human voice at specific frequencies. The auditory system shares direct neural links with the vagus nerve, making sound one of the fastest pathways to nervous system safety."),
    ("M", "Water & Warmth", "Thermal and aquatic sensation \u2014 showers, baths, the sea, warmth against skin. One of the body's oldest safety signals, processing heat and water as evidence the emergency is over."),
    ("S", "Touch & Texture", "Tactile regulation \u2014 weight, fabric, stone, warmth in the hands. The skin as the largest sensory organ, receiving safety signals that bypass thought entirely."),
    ("O", "Scent & Breath", "Olfactory regulation \u2014 essential oils, earth after rain, wood, coffee, skin. The olfactory bulb connects directly to the amygdala and hippocampus, bypassing conscious processing to reach memory and emotion instantly."),
    ("D", "Signal Lost", "No reliable sensory channel. Not failure \u2014 deep depletion. The channels are dormant, not broken. Rebuilding starts with the most primitive: warmth and direct physical contact."),
]

DIM_INSIGHTS = {
    "alertness": {
        "Contracted": "Your nervous system is in deep survival mode. The sympathetic activation has become your baseline \u2014 not a response to specific threats, but a permanent state of readiness. Your body has forgotten what genuine safety feels like. The jaw clenches. The shoulders brace. The 3am wake-ups aren't anxiety \u2014 they're a system that doesn't know how to stand down.\n\nThis level of activation was designed for emergencies. Your body is treating your entire life as one. The adrenaline that served you in a crisis meeting or a difficult transition never switched off \u2014 it became the floor beneath everything you do. The result is a baseline tension so constant you no longer feel it as tension. You feel it as normal.\n\nThe way back is not through relaxation techniques. Your system doesn't trust relaxation. It needs proof \u2014 physical, sensory proof \u2014 that the emergency is genuinely over. The practices in your restoration path work with the body's safety architecture, not against your mind's resistance.",
        "Compressed": "Your system runs hot but you've learned to manage it. The activation is constant but controlled \u2014 you function well under pressure because your body never fully leaves pressure mode. You've normalised a level of tension that most people would find unbearable. This is both your superpower and your debt.\n\nThe compression shows up in ways you've stopped noticing: the jaw that tightens in meetings, the shoulders that rise toward your ears by mid-afternoon, the sleep that takes too long to arrive and never goes deep enough. These aren't stress symptoms. They're evidence that your nervous system has accepted a permanently elevated baseline. You've adapted to the pressure \u2014 but adaptation is not the same as regulation.\n\nThe leverage point is this: your system can still come down. Unlike the contracted band, your capacity for regulation isn't lost \u2014 it's just not being exercised. Small, deliberate moments of deactivation throughout your day can teach your system that the space between demands is not a threat. Your body is waiting for permission to stand down. It needs the permission to come through sensation, not through thought.",
        "Emerging": "Your nervous system can still find calm \u2014 but it takes the right conditions and deliberate effort. The capacity for regulation is there. It needs to be practiced, not just hoped for. The moments when your body actually lets go are data: they tell you what your system needs.\n\nYou're in the most responsive band for change. Your alertness system hasn't been pushed into permanent overdrive, and it hasn't shut down. What you have is a system that remembers regulation but doesn't default to it. The architecture is intact \u2014 the habit isn't. This means your practices will produce noticeable results faster than you might expect.\n\nPay attention to what's already working. The moments when your shoulders drop, when your breathing deepens, when your body genuinely softens \u2014 these aren't random. They're your nervous system showing you its preferred pathway back to safety. Build on those moments deliberately.",
        "Open": "Your alertness system is well-regulated. You can activate when needed and return to baseline when the demand passes. This is a genuine strength and an increasingly rare one among women in high-performance environments. Protect it.\n\nA regulated alertness system means your body trusts that pressure is temporary. You can rise to meet demands without your nervous system interpreting every challenge as a threat. You sleep because your body knows how to stand down. You focus because your attention isn't being hijacked by background vigilance.\n\nThis dimension is your anchor. When other dimensions are under pressure, your regulated alertness gives your system a stable foundation to work from. Don't take it for granted \u2014 it's the product of either natural resilience or practices you've already built. Continue what's working."
    },
    "sensitivity": {
        "Contracted": "Your sensory bandwidth has narrowed significantly. Beauty, taste, touch, music \u2014 these inputs arrive at your senses but they don't land in your body. Your nervous system turned down the volume on aesthetic experience to conserve energy for survival. The result is a life that looks complete but feels muted.\n\nThis isn't a choice you made. It's a neurological strategy your system implemented without asking. When resources are scarce and demands are high, the brain deprioritises everything that isn't essential for functional survival. Aesthetic experience, sensory pleasure, the ability to be moved by beauty \u2014 these are the first channels to close because they're not required to keep you performing. What remains is execution without texture.\n\nThe path back to sensitivity begins with the simplest possible sensory inputs \u2014 not overwhelming beauty, but micro-doses. The warmth of a cup. The texture of fabric. The weight of a blanket. Your channels aren't destroyed. They're dormant. And they respond to gentle, repeated activation faster than most women expect.",
        "Compressed": "You still sense the world but through a filter. Strong experiences get through \u2014 a powerful sunset, an overwhelming piece of music. But subtle beauty \u2014 the warmth of light on a wall, the texture of fabric, the taste of your morning coffee \u2014 passes without registration. You know things are beautiful without feeling the beauty.\n\nThe filter is your nervous system's compromise. It couldn't afford to shut down sensation entirely \u2014 you need some sensory input to navigate your life. But it turned the sensitivity dial down low enough that only high-intensity experiences break through. The result is a world that feels slightly grey. Not colourless. Just... less.\n\nYour sensory channels are intact but throttled. The practices for this band don't require dramatic intervention. They require deliberate attention to subtle sensation. When you slow down enough to notice texture, temperature, light \u2014 not just see them but feel them in your body \u2014 the filter thins. The bandwidth widens. The practice is simple. The discipline is in the slowing.",
        "Emerging": "Your sensitivity is coming back online. There are moments when beauty breaks through unexpectedly \u2014 and when it does, you feel how much you've been missing. Those moments aren't random. They're your nervous system reopening channels it shut down. They're evidence that restoration is happening.\n\nYou're in a particularly interesting position: the sensitivity is available but not stable. Some days the world has colour and texture and warmth. Other days the filter is back. This inconsistency is not a setback \u2014 it's the signature of a system in transition. The capacity for full sensation is there. It's building strength.\n\nYour practice now is to protect and extend the moments when sensation is alive. Not to force them. Not to chase them. But to create the conditions that let them arrive more frequently. Slow mornings. Deliberate beauty. Sensory experiences chosen for depth, not productivity. Your system is showing you the way back. Follow it.",
        "Open": "Your aesthetic and sensory channels are alive. Beauty reaches your body, not just your mind. Music moves you. Taste delights you. Touch soothes you. This is rare among women under sustained professional pressure \u2014 and it's the foundation of everything ANSR builds on.\n\nYour open sensitivity means your nervous system has preserved its full bandwidth of experience. This is both a gift and a responsibility. Your capacity to feel beauty is also a capacity to feel pain, overwhelm, and the weight of environments that don't match your sensitivity. Protect this channel by choosing your sensory environment deliberately.\n\nThis dimension is likely a core part of your identity \u2014 you've always been someone who notices, who feels, who responds to beauty. The ANSR framework treats this not as a personality trait but as a nervous system asset. When your other dimensions are under pressure, your sensitivity is the channel through which restoration reaches you."
    },
    "vitality": {
        "Contracted": "Your body is in deep restoration deficit. Sleep doesn't restore. Rest doesn't reach. Your system is spending more than it's rebuilding every single day, and the debt has been compounding for months or years. The signals your body sends \u2014 persistent fatigue, recurring illness, tension that never resolves \u2014 are not problems to solve. They're your body's language for 'stop.'\n\nVitality at this level means your parasympathetic nervous system \u2014 the branch responsible for repair, digestion, sleep, and restoration \u2014 has been chronically suppressed. Your body knows how to activate. It has forgotten how to rebuild. This is why rest doesn't feel restful: the restoration circuits aren't engaging even when you stop moving.\n\nThe practices for contracted vitality are not about more rest. They're about teaching your body to use rest. The autonomic nervous system needs specific sensory signals \u2014 warmth, gentle pressure, slow breathing, safety \u2014 to shift from spending mode to rebuilding mode. Without those signals, lying down is just horizontal exhaustion.",
        "Compressed": "You manage your energy but you're managing a declining resource. The tank refills to 60%, never 100%. You've adjusted your expectations downward so gradually that you've forgotten what genuine vitality feels like. You call this 'realistic.' Your nervous system calls it rationing.\n\nThe compression in your vitality system is like a slow leak. You're not in crisis \u2014 you function, you deliver, you show up. But the reserves are thin. Recovery takes longer than it used to. Illness visits more often. The gap between what your body can sustain and what your life demands is narrowing, and you've been closing it with willpower.\n\nThe opportunity at this level is significant: your restoration system isn't offline, it's throttled. With deliberate sensory intervention \u2014 practices that activate the parasympathetic branch specifically \u2014 you can shift from rationing to genuine rebuilding. The tank can fill higher. But it needs targeted input, not just time off.",
        "Emerging": "Your body's restoration capacity is returning. There are days when you wake genuinely rested, moments when energy feels real rather than manufactured. These are not random good days \u2014 they're evidence that your system remembers how to rebuild. Build on them deliberately.\n\nEmerging vitality means your parasympathetic system is coming back online. The repair circuits are firing. Sleep is beginning to restore rather than just pause. Your body is starting to trust that it's safe to rebuild rather than just survive. This is the turning point \u2014 the moment when compounding shifts from negative to positive.\n\nYour practice now is consistency. The moments of genuine vitality are showing you what works for your specific system. Pay attention to what preceded the good days \u2014 what you ate, how you slept, what sensory experiences you had. Your body is giving you a restoration blueprint. Follow it.",
        "Open": "Your vitality system is functioning well. Your body recovers from exertion. Your energy has rhythm \u2014 it rises and falls with natural cycles rather than being forced by caffeine and willpower. You know the difference between genuine rest and collapse. This is your foundation.\n\nOpen vitality means your parasympathetic nervous system is doing its job: repairing, restoring, rebuilding. Your sleep architecture is intact. Your body processes stress and returns to baseline. This is increasingly rare and extraordinarily valuable.\n\nProtect this dimension. It's the engine room of everything else. When vitality is open, your other dimensions have the resources they need to regulate. When it closes, everything else follows. The practices that maintain your vitality \u2014 whatever they are \u2014 are non-negotiable."
    },
    "connection": {
        "Contracted": "You've withdrawn from genuine connection to conserve energy. Not deliberately \u2014 your nervous system made the decision for you. You show up in relationships, you fulfil your roles, you say the right things. But the felt experience of being truly with someone \u2014 present, open, receiving \u2014 has thinned to almost nothing. Care flows out. Nothing flows in.\n\nConnection at this level means your social engagement system \u2014 the ventral vagal pathway that allows you to co-regulate with other humans \u2014 has been significantly suppressed. You can perform connection. You can simulate warmth. But the physiological experience of being met, held, and received by another person is no longer available to your body.\n\nThis is not an emotional problem. It's a nervous system state. The circuits for genuine connection are intact but offline. They respond to safety, not effort. The practices for contracted connection don't ask you to try harder in relationships. They create the physiological conditions under which your system can begin to receive again.",
        "Compressed": "You're present in relationships but not fully available. Part of you is always behind glass \u2014 observing, managing, performing the right responses. The people closest to you may have noticed before you did. There's a gap between how connected you appear and how connected you feel.\n\nCompressed connection means your social engagement system is online but throttled. You can connect \u2014 but it takes energy, and the connection doesn't fully nourish you. You leave conversations feeling engaged but not filled. You show up for people but come home still empty. The give is working. The receive is blocked.\n\nThe leverage point for compressed connection is not more socialising. It's the quality of presence in the connections you already have. One moment of genuine receiving \u2014 a compliment that lands, a touch that reaches, a conversation where you stop managing the other person's experience \u2014 does more for your system than a week of performed connection.",
        "Emerging": "Connection is still available to you \u2014 but it requires conditions your current life rarely provides. When those conditions appear \u2014 a specific person, a particular moment of safety \u2014 you feel how much you've been missing. Those moments are not nostalgia. They're your nervous system showing you what it needs.\n\nEmerging connection means your social engagement system is functional but conditional. It comes online under the right circumstances \u2014 and those circumstances are telling you something important about what your nervous system requires for genuine connection: safety, presence, and someone who can hold space without needing you to perform.\n\nYour practice is to create more of those conditions \u2014 not more relationships, but more moments of genuine receiving within the relationships you have. Follow the connections that nourish rather than deplete. Your body knows the difference even when your mind doesn't.",
        "Open": "Your capacity for genuine connection is intact. You can receive care, be seen in your vulnerability, and stay present when it matters. You let people in \u2014 not everyone, but the right ones. This is a resource both for your own regulation and for the people around you.\n\nOpen connection means your ventral vagal social engagement system is fully functional. You co-regulate naturally \u2014 your presence calms others, and being with certain people calms you. This is the foundation of relational health and an increasingly rare capacity among women under sustained professional pressure.\n\nThis dimension is likely one of your greatest assets \u2014 and potentially one of your greatest costs if not protected. Open connection means you feel others deeply. Guard this channel by choosing your relational environment deliberately. Not everyone deserves access to your open system."
    },
    "performance": {
        "Contracted": "Your work has become the only thing that still produces feeling. Achievement is your last remaining source of aliveness \u2014 not because you love what you do, but because your nervous system shut down every other channel. The identity you've built is indistinguishable from your output. If the title were removed tomorrow, you would not know who you are.\n\nContracted performance doesn't mean you're failing. It means performance has consumed everything else. Your system routes all remaining energy into output because that's the only channel that still provides feedback. Beauty, connection, pleasure, rest \u2014 these have been deprioritised so completely that work is the last thing standing.\n\nThe practices for contracted performance are counterintuitive: they don't address work at all. They rebuild the other channels \u2014 sensation, connection, aliveness \u2014 so that your identity has somewhere else to stand. When the other dimensions come back online, your relationship with performance naturally recalibrates. Not less achievement. Less dependence on it.",
        "Compressed": "You perform at a high level but the cost is escalating invisibly. The mask is getting heavier. The gap between who you are at work and who you are underneath is widening. You're excellent at what you do \u2014 and you stopped loving it a long time ago.\n\nCompressed performance means your professional identity is intact but your relationship with it has shifted. There's a growing distance between the person who shows up to work and the person who exists underneath. You may not have told anyone. You may not have fully admitted it to yourself. But the cost of performing is rising, and the return is diminishing.\n\nThe leverage point is not changing what you do. It's reconnecting why you do it. When performance is driven by purpose rather than habit or fear, the same output costs less energy. The practices for this band reconnect your work to meaning \u2014 not through reflection, but through the body. When you feel aligned, you perform from a different place entirely.",
        "Emerging": "You're beginning to question the relationship between your identity and your output. That questioning isn't a crisis \u2014 it's the beginning of a healthier relationship with work and with yourself. You can feel the distinction between performing from purpose and performing from habit.\n\nEmerging performance means you're in the process of separating who you are from what you produce. This is uncomfortable but necessary. The discomfort you're feeling is the gap between the identity you built under pressure and the identity that's trying to emerge. Don't close that gap too quickly. Sit in it.\n\nYour practice is to notice when you're performing from purpose versus performing from pattern. The body knows the difference even when the calendar doesn't. Purpose feels energising even when difficult. Pattern feels draining even when successful. Let your body be the compass.",
        "Open": "Your relationship with work feels sustainable and aligned. You can perform without losing yourself in the performance. Purpose drives you, not fear or habit. You bring the same person to work that you bring everywhere else. This alignment is rare and valuable.\n\nOpen performance means your professional output is connected to your deeper identity rather than substituting for it. You work hard because the work matters \u2014 not because stopping would leave you with nothing. This distinction is the difference between a career that sustains you and one that consumes you.\n\nProtect this alignment. It's easy to lose under sustained external pressure. When demands escalate, the temptation is to disconnect from purpose and switch to survival-mode output. The practices that keep you aligned \u2014 whatever they are \u2014 are not luxuries. They're the mechanism that keeps your performance sustainable."
    },
    "aliveness": {
        "Contracted": "The experience of being alive \u2014 joy that arrives without achievement, desire that has no productive justification, beauty that stops you in your tracks \u2014 has gone quiet. You function. You achieve. But the feeling that your life belongs to you, that it's yours to experience and not just to manage, has faded. This is not depression. This is a nervous system that forgot to tell you the emergency is over.\n\nContracted aliveness is the deepest cost of sustained pressure. It means your system has shut down the channels that make life feel like yours. Beauty, desire, spontaneity, wonder \u2014 these require a nervous system that feels safe enough to play, to waste time, to want things that serve no purpose. Your system doesn't feel safe enough for that.\n\nThe return of aliveness is the ultimate goal of every ANSR practice. Not productivity. Not resilience. Not coping. The felt experience of being alive. It begins with the smallest possible sensory pleasures and builds from there. Your system doesn't need to be fixed. It needs to be told \u2014 through sensation, not words \u2014 that the emergency is over and beauty is safe again.",
        "Compressed": "Aliveness visits in flashes \u2014 a sunset that catches you, a conversation that opens something, a rare moment of unstructured stillness where you feel yourself arrive. You recognise it when it comes. You just can't hold it or find it deliberately. The moments are real. They're not enough.\n\nCompressed aliveness means the capacity is there but unstable. Your system can produce the experience of genuine aliveness \u2014 but only under specific conditions, and only briefly. The rest of the time, life happens to you rather than through you. You're present but not arrived.\n\nThe practice for compressed aliveness is not to chase the moments but to create the conditions. What was happening the last time you felt genuinely alive? Not performing-alive. Not succeeding-alive. Just... alive. That answer contains your restoration blueprint. Follow it.",
        "Emerging": "Something is stirring. Not dramatic \u2014 more like a direction. A desire without a plan. A feeling without a name. Your system is beginning to remember what it turned off, and the remembering feels both exciting and frightening. This stirring is fragile and important. Do not optimise it.\n\nEmerging aliveness is the most delicate and promising state in the ANSR framework. It means your nervous system is crossing the threshold from conservation to exploration. The impulses you're feeling \u2014 to change something, to move toward something, to want something you can't justify \u2014 are not midlife crisis signals. They're your system telling you it's ready to come back online.\n\nProtect this emergence. Don't turn it into a project. Don't set goals for your aliveness. Don't announce the shift before it's strong enough to withstand scrutiny. The New Moon doesn't need a spotlight. It needs darkness and time.",
        "Open": "You feel alive \u2014 not just productive, not just successful, but alive. Beauty moves your body. Joy arrives without reason. Your life feels like yours. This is the goal of every practice in the ANSR framework \u2014 not performance, not productivity, but this. Protect it fiercely.\n\nOpen aliveness is the rarest state among women in sustained high-performance environments. It means your nervous system has preserved \u2014 or restored \u2014 the capacity for wonder, desire, and beauty that most people traded for survival long ago. You feel your life. You don't just manage it.\n\nThis is your most precious resource. Everything in the ANSR framework points toward this dimension. When aliveness is open, every other dimension has access to the energy and meaning it needs. Guard it. Feed it. Build your life around protecting the conditions that keep this channel alive."
    },
}

def calc_profile_pct(scores, primary_key, secondary_key):
    s = scores
    weights = {}
    weights["sunfire"] = (10-s["alertness"])*2 + s["performance"] + (10-s["vitality"])
    weights["velvetblade"] = (10-s["sensitivity"])*2 + s["alertness"] + (10-s["connection"])
    weights["eclipse"] = (10-s["sensitivity"]) + (10-s["vitality"]) + (10-s["aliveness"]) + (10-s["connection"])
    weights["summerstorm"] = s["sensitivity"]*2 + (10-s["alertness"]) + (10-s["vitality"])
    weights["heartwood"] = (10-s["connection"])*2 + (10-s["aliveness"]) + s["performance"]*0.5
    avg = sum(s.values()) / 6
    weights["newmoon"] = (15 if abs(avg-5.5) < 2 else 5) + (5 if s["sensitivity"] > 5 else 0) + (5 if s["aliveness"] > 5 else 0)
    pw = weights.get(primary_key, 10)
    sw = weights.get(secondary_key, 5)
    total = pw + sw
    if total == 0: return 70, 30
    primary_pct = round(pw / total * 100)
    primary_pct = max(55, min(85, primary_pct))
    return primary_pct, 100 - primary_pct

def get_band(score):
    if score <= 2.5: return "Contracted"
    if score <= 5: return "Compressed"
    if score <= 7.5: return "Emerging"
    return "Open"

def get_band_color(score):
    if score <= 2.5: return HexColor("#B46E5A")
    if score <= 5: return HexColor("#B49664")
    if score <= 7.5: return HexColor("#8CAA82")
    return HexColor("#64A08C")

# ═══════════════════════════════════════
# EXPERT RADAR INTERPRETATION
# ═══════════════════════════════════════
def get_radar_interpretation(scores, primary_key, secondary_key, ppct, spct):
    """Generate 2-3 paragraphs of expert-level radar interpretation."""
    prof = PROFILES_BASIC[primary_key]
    sec = PROFILES_BASIC[secondary_key]
    srt = sorted([(l,k,scores[k]) for l,k in zip(DIM_LABELS, DIM_KEYS)], key=lambda x:-x[2])
    avg = sum(scores.values()) / 6
    rng = srt[0][2] - srt[-1][2]
    
    # Find clusters
    high_dims = [(l,s) for l,_,s in srt if s >= 5]
    low_dims = [(l,s) for l,_,s in srt if s < 5]
    
    # Paragraph 1: Overall shape
    if rng > 4:
        shape_desc = f"Your ANSR map shows a pronounced asymmetry \u2014 a {rng:.1f}-point spread between your strongest dimension ({srt[0][0]}, {srt[0][2]:.1f}) and your most depleted ({srt[-1][0]}, {srt[-1][2]:.1f}). This is not a balanced decline. Your nervous system has preserved certain capacities while sacrificing others. The shape tells a story: under sustained pressure, your system protected {srt[0][0].lower()} at the expense of {srt[-1][0].lower()}. This trade-off is characteristic of the {prof['name']} pattern \u2014 and it reveals both where your resilience lives and where the cost has accumulated."
    elif rng > 2:
        shape_desc = f"Your map shows a moderately uneven pattern with a {rng:.1f}-point range. {srt[0][0]} ({srt[0][2]:.1f}) remains your strongest resource while {srt[-1][0]} ({srt[-1][2]:.1f}) has taken the most pressure. The shape suggests your nervous system is selectively rationing \u2014 maintaining some channels while compressing others. This is typical of the {prof['name']} pattern, where certain capacities are preserved because they serve the primary survival strategy."
    else:
        shape_desc = f"Your map shows a relatively even pattern \u2014 a {rng:.1f}-point spread across all six dimensions. This uniformity is itself significant. Rather than sacrificing specific channels, your system has compressed evenly. An overall average of {avg:.1f}/10 across a flat shape suggests systemic rather than targeted depletion."
    
    # Paragraph 2: How the two profiles interact on the radar
    # Construct the "secondary shape" conceptually
    sec_interpretation = ""
    if secondary_key == "heartwood":
        sec_interpretation = f"The Heartwood undertone ({spct}%) surfaces in your connection and aliveness scores. Connection at {scores['connection']:.1f} and aliveness at {scores['aliveness']:.1f} together tell the Heartwood story: the giving circuits are still firing, but the receiving circuits have gone quiet. When your {prof['name']} pattern can no longer hold, it's the Heartwood that catches you \u2014 defaulting to care for others as the only remaining way to feel useful. The gap between your performance score and your connection score is where the undertone lives."
    elif secondary_key == "sunfire":
        sec_interpretation = f"The Sunfire undertone ({spct}%) shows in the tension between your performance score ({scores['performance']:.1f}) and your vitality ({scores['vitality']:.1f}). The drive hasn't stopped \u2014 it's still there, pushing beneath your primary pattern. When your {prof['name']} strategy loosens, the Sunfire surfaces: more activation, more output, more intensity. The undertone is the engine your system falls back on when the primary strategy can't hold."
    elif secondary_key == "eclipse":
        sec_interpretation = f"The Eclipse undertone ({spct}%) is visible in the lower dimensions of your map \u2014 sensitivity ({scores['sensitivity']:.1f}) and aliveness ({scores['aliveness']:.1f}) in particular. These scores suggest that beneath your {prof['name']} pattern, a conservation mechanism is at work: your system is quietly turning down the volume on sensory and emotional experience. When your primary strategy falters, the Eclipse catches you \u2014 and the world goes flatter."
    elif secondary_key == "velvetblade":
        sec_interpretation = f"The Velvet Blade undertone ({spct}%) shows in the relationship between your sensitivity ({scores['sensitivity']:.1f}) and your performance ({scores['performance']:.1f}). The aesthetic distance \u2014 the filter between you and what you feel \u2014 is there beneath your primary pattern. When your {prof['name']} strategy loosens, the Blade steps in: composure, control, the elegant management of proximity. The undertone protects you. It also seals you."
    elif secondary_key == "summerstorm":
        sec_interpretation = f"The Summer Storm undertone ({spct}%) lives in the gap between your sensitivity and your capacity to contain it. When your {prof['name']} pattern can no longer hold, the Storm surfaces: sensation floods in without a container. The undertone explains the moments when your composure breaks \u2014 not from weakness, but from the sheer volume of what your system is actually processing beneath the surface."
    elif secondary_key == "newmoon":
        sec_interpretation = f"The New Moon undertone ({spct}%) shows in the emerging scores on your map. There are dimensions beginning to shift \u2014 not dramatically, but directionally. The undertone tells us your nervous system is in early transition. Beneath your {prof['name']} pattern, something is stirring. The question isn't whether change is coming. It's whether your system gets the support it needs to make the transition safely."
    
    # Paragraph 3: Leverage point
    # Find the dimension closest to a band boundary that could tip
    leverage = None
    for l,k,s in srt:
        for boundary in [2.5, 5.0, 7.5]:
            if abs(s - boundary) < 1.0 and s < boundary:
                leverage = (l, k, s, boundary, get_band(boundary + 0.1))
                break
        if leverage: break
    
    if leverage:
        lev_text = f"Your leverage point is {leverage[0]}. At {leverage[2]:.1f}, it's closest to the {leverage[4]} threshold ({leverage[3]:.1f}). This is the dimension where targeted practice will produce the most noticeable shift. When {leverage[0].lower()} moves, it changes the shape of your entire map \u2014 because nervous system dimensions don't operate in isolation. A shift in {leverage[0].lower()} will create movement in connection, aliveness, and sensitivity. Start here."
    else:
        lev_text = f"Your leverage point is {srt[-1][0].lower()} \u2014 not because it's the weakest, but because it's the dimension where your system has the most to recover. When the most depleted channel begins to open, it shifts the pressure across every other dimension. Your {srt[0][0].lower()} is already strong. Your {srt[-1][0].lower()} is where the intervention will be felt."
    
    return shape_desc, sec_interpretation, lev_text


# ═══════════════════════════════════════
# MAIN PDF GENERATOR
# ═══════════════════════════════════════
def generate_pdf(user_name, primary_key, secondary_key, scores, sensory_type, output_path, date_str="10 March 2026"):
    # Defensive validation — bulletproof against bad data
    if primary_key not in PROFILES_BASIC:
        primary_key = "newmoon"
    if secondary_key not in PROFILES_BASIC:
        secondary_key = "heartwood" if primary_key != "heartwood" else "eclipse"
    if primary_key == secondary_key:
        secondary_key = [k for k in PROFILES_BASIC if k != primary_key][0]
    for dk in DIM_KEYS:
        if dk not in scores:
            scores[dk] = 5.0
        scores[dk] = max(0, min(10, float(scores.get(dk, 5.0))))
    if sensory_type not in ["V","A","M","S","O","D"]:
        sensory_type = "D"
    
    prof = PROFILES_BASIC[primary_key]
    sec = PROFILES_BASIC[secondary_key]
    pCol = PROF_COLORS[primary_key]
    sCol = PROF_COLORS[secondary_key]
    desc_paras = FULL_DESCRIPTIONS[primary_key]
    practices = PRACTICES[primary_key]
    sensory = SENSORY_MAP.get(sensory_type, SENSORY_MAP["D"])
    ppct, spct = calc_profile_pct(scores, primary_key, secondary_key)
    
    c = canvas.Canvas(output_path, pagesize=A4)
    
    def safe_text(text):
        return text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    
    def wrap(text, x, y, mw, font="Times-Roman", size=10.5, color=CHARCOAL, leading=15.5, align=TA_LEFT):
        style = ParagraphStyle('w', fontName=font, fontSize=size, textColor=color, leading=leading, alignment=align)
        p = Paragraph(safe_text(text), style)
        w, h = p.wrap(mw, 800)
        p.drawOn(c, x, max(y - h, 8*mm))
        return y - h - 3
    
    def darkBg():
        c.setFillColor(DARK); c.rect(0,0,W,H,fill=1,stroke=0)
    def lightBg():
        c.setFillColor(IVORY); c.rect(0,0,W,H,fill=1,stroke=0)
    def foot(n):
        c.setFont("Times-Roman",7);c.setFillColor(DIM)
        c.drawString(M,12*mm,f"ANSR\u2122 Profile \u00b7 {user_name}")
        c.drawRightString(W-M,12*mm,str(n))
    def accentLine(y):
        c.setStrokeColor(ACCENT);c.setLineWidth(0.3);c.line(M,y,M+35*mm,y)
    
    page_num = 1
    
    # ════════════════════════════════════
    # P1: COVER (LOCKED — do not change)
    # ════════════════════════════════════
    darkBg()
    c.setFont("Times-Roman",18);c.setFillColor(IVORY)
    c.drawCentredString(W/2, H-80*mm, "E L I A")
    c.setStrokeColor(IVORY);c.setLineWidth(0.3);c.line(W/2-15*mm,H-90*mm,W/2+15*mm,H-90*mm)
    c.setFont("Times-Roman",36);c.setFillColor(pCol)
    c.drawCentredString(W/2, H-130*mm, prof["name"])
    c.setFont("Times-Italic",13);c.setFillColor(IVORY)
    c.drawCentredString(W/2, H-142*mm, f"with {sec['name']} undertone")
    c.setFont("Times-Roman",13);c.setFillColor(IVORY)
    c.drawCentredString(W/2, H-195*mm, "Your Nervous System Pattern")
    c.setFont("Times-Roman",10)
    c.drawCentredString(W/2, H-210*mm, user_name)
    c.drawCentredString(W/2, H-220*mm, date_str)
    c.setFont("Times-Roman",8)
    c.drawCentredString(W/2, H-258*mm, "ANSR\u2122")
    c.setFont("Times-Roman",7)
    c.drawCentredString(W/2, H-268*mm, "\u00a9 ELIA / Uskale SA")
    c.showPage(); page_num += 1

    # ════════════════════════════════════
    # P2: SHARE CARD — DUAL profile description
    # ════════════════════════════════════
    darkBg()
    c.setFont("Times-Roman",11);c.setFillColor(ACCENT)
    c.drawCentredString(W/2, H-55*mm, "Your ANSR Signature")
    c.setFont("Times-Roman",32);c.setFillColor(pCol)
    c.drawCentredString(W/2, H-78*mm, prof["name"])
    c.setFont("Times-Italic",13);c.setFillColor(IVORY)
    c.drawCentredString(W/2, H-91*mm, prof["tag"])
    # Percentage split
    c.setFont("Times-Roman",11);c.setFillColor(MUTED)
    c.drawCentredString(W/2, H-106*mm, f"with {sec['name']} undertone \u00b7 {ppct}% / {spct}%")
    # Thin accent line
    c.setStrokeColor(ACCENT);c.setLineWidth(0.3);c.line(W/2-20*mm,H-116*mm,W/2+20*mm,H-116*mm)
    # Dual profile description — centered italic
    dual_desc = get_dual_desc(primary_key, secondary_key)
    style = ParagraphStyle('share', fontName='Times-Italic', fontSize=11, textColor=MUTED, leading=16.5, alignment=TA_CENTER)
    p = Paragraph(safe_text(dual_desc), style)
    pw, ph = p.wrap(135*mm, 200)
    p.drawOn(c, (W-135*mm)/2, H-126*mm-ph)
    # Screenshot CTA
    c.setFont("Times-Bold",9);c.setFillColor(IVORY)
    c.drawCentredString(W/2, H-230*mm, "Screenshot this page. Send it to the woman who comes to mind.")
    c.setFont("Times-Roman",7);c.setFillColor(DIM)
    c.drawCentredString(W/2, H-268*mm, "Take the free ANSR Pulse: ansr-pulse.vercel.app")
    c.showPage(); page_num += 1

    # ════════════════════════════════════
    # P3-4: HOW TO READ THIS REPORT (2 pages)
    # ════════════════════════════════════
    lightBg()
    c.setFont("Times-Roman",9);c.setFillColor(ACCENT);c.drawString(M,H-M-5*mm,"Before You Read")
    c.setFont("Times-Roman",22);c.setFillColor(CHARCOAL);c.drawString(M,H-M-20*mm,"How to Read This Report")
    accentLine(H-M-26*mm)
    y = H-M-38*mm
    
    # Section 1: What this is
    c.setFont("Times-Roman",12);c.setFillColor(ACCENT);c.drawString(M,y,"What This Report Is");y -= 8*mm
    y = wrap("This is not a personality test. It is not a diagnosis. It is a map of how your nervous system is currently managing the demands on it \u2014 which channels it has preserved, which it has compressed, and where it is showing signs of change.", M, y, CW)
    y -= 4
    y = wrap("Every score reflects a strategy your system adopted under pressure. Low scores are not failures. They are evidence of intelligent conservation \u2014 your system protecting what it could by quieting what it couldn't sustain. High scores are not achievements. They are channels your system kept open because they served its survival strategy.", M, y, CW)
    y -= 4
    y = wrap("The patterns you see here are not permanent. They are current. The nervous system is plastic \u2014 it changes in response to specific sensory input. That is what the practices in this report are designed to provide.", M, y, CW)
    y -= 16
    
    # Section 2: The Four Bands
    c.setFont("Times-Roman",12);c.setFillColor(ACCENT);c.drawString(M,y,"The Four Bands");y -= 8*mm
    y = wrap("Your six dimension scores each fall into one of four bands. These are not grades. They are descriptions of what your nervous system is doing in each area.", M, y, CW)
    y -= 6
    for bname, bdesc in [
        ("Contracted (0 \u2014 2.5)", "Your system has significantly reduced this capacity to conserve energy. Deep conservation \u2014 not damage. The channel is dormant, not broken."),
        ("Compressed (2.5 \u2014 5)", "Your system is rationing this capacity. It works, but at reduced bandwidth. This is the most common band for women in sustained leadership pressure."),
        ("Emerging (5 \u2014 7.5)", "This capacity is returning or has been partially preserved. The inconsistency you may feel is itself a sign of transition."),
        ("Open (7.5 \u2014 10)", "This channel is fully available. This is your resource \u2014 the dimension from which restoration of the others can begin. Protect it."),
    ]:
        c.setFont("Times-Bold",9.5);c.setFillColor(CHARCOAL);c.drawString(M+4*mm,y,bname)
        y -= 5*mm
        y = wrap(bdesc, M+4*mm, y, CW-4*mm, size=9.5, leading=13)
        y -= 6
    
    foot(page_num);c.showPage(); page_num += 1
    
    # Page 4: How to read dual profile + sensory + practices
    lightBg()
    c.setFont("Times-Roman",9);c.setFillColor(ACCENT);c.drawString(M,H-M-5*mm,"Before You Read")
    y = H-M-18*mm
    
    # Section 3: Dual Profile
    c.setFont("Times-Roman",12);c.setFillColor(ACCENT);c.drawString(M,y,"How to Read the Dual Profile");y -= 8*mm
    y = wrap(f"Your primary pattern \u2014 {prof['name']} \u2014 is the dominant strategy your nervous system uses daily. It accounts for roughly {ppct}% of your nervous system behaviour. Your undertone \u2014 {sec['name']} \u2014 is what surfaces when the primary can no longer hold. Under extreme fatigue or emotional pressure, your system shifts from the primary to the undertone.", M, y, CW)
    y -= 4
    y = wrap(f"The combination matters more than either pattern alone. A {prof['name']} with a {sec['name']} undertone crashes differently, recovers differently, and needs different practices than a {prof['name']} with a different undertone. The practices in this report are matched to your specific combination.", M, y, CW)
    y -= 4
    y = wrap("When you read the ANSR Map, notice the gap between your two highest dimensions and your two lowest. That gap tells you where your system is spending and where it is conserving. The dimensions closest to the 5.0 threshold are your leverage points \u2014 small changes there produce the largest shifts in how you feel.", M, y, CW)
    y -= 16
    
    # Section 4: Sensory Signature
    c.setFont("Times-Roman",12);c.setFillColor(ACCENT);c.drawString(M,y,"Your Sensory Signature");y -= 8*mm
    y = wrap("Your sensory signature is not a preference. It is the channel through which your nervous system most efficiently processes safety signals. When you use this channel deliberately \u2014 not as entertainment but as intervention \u2014 your system shifts from spending mode to restoration mode faster than through any other input.", M, y, CW)
    y -= 16
    
    # Section 5: How to use the practices
    c.setFont("Times-Roman",12);c.setFillColor(ACCENT);c.drawString(M,y,"How to Use the Practices");y -= 8*mm
    y = wrap("The three practices in your Restoration Path are sequenced intentionally. Practice 1 is the entry point \u2014 less than two minutes, no preparation. Start here. Do it daily for one week before adding anything else. Practice 2 expands the first, asking slightly more of your system. Add it in week two. Practice 3 touches the core of your pattern. Arrive when your system is ready.", M, y, CW)
    y -= 4
    y = wrap("The most important instruction: do not turn these practices into a performance. The moment you optimise them, track them, or judge yourself for missing a day, your nervous system reads that as more pressure, not less. These practices work through surrender, not discipline.", M, y, CW)
    y -= 16
    
    # Section 6: What to do first
    c.setFont("Times-Roman",12);c.setFillColor(ACCENT);c.drawString(M,y,"What to Do First");y -= 8*mm
    y = wrap("Read your Primary Profile description slowly. Notice which sentences your body responds to. Then find your leverage point on the ANSR Map \u2014 the dimension closest to 5.0. Start Practice 1 tomorrow. Just that. Nothing else. Return to this report in one week. The second reading will land differently. Your system will be ready to hear what it couldn't absorb the first time.", M, y, CW)
    
    foot(page_num);c.showPage(); page_num += 1

    # ════════════════════════════════════
    # P5: YOUR PRIMARY PROFILE — all 5 paragraphs + hope on ONE page
    # ════════════════════════════════════
    lightBg()
    c.setFont("Times-Roman",9);c.setFillColor(ACCENT);c.drawString(M,H-M-5*mm,"Your Primary Profile")
    c.setFont("Times-Roman",26);c.setFillColor(pCol);c.drawString(M,H-M-20*mm,prof["name"])
    c.setFont("Times-Italic",11);c.setFillColor(MUTED);c.drawString(M,H-M-29*mm,prof["tag"])
    accentLine(H-M-34*mm)
    y = H-M-43*mm
    # All 6 paragraphs (5 original + movie reference) — compact leading
    for i, para in enumerate(desc_paras):
        if y < 45*mm:
            # Overflow to next page if needed
            foot(page_num); c.showPage(); page_num += 1; lightBg()
            c.setFont("Times-Roman",9);c.setFillColor(ACCENT);c.drawString(M,H-M-5*mm,"Your Primary Profile (continued)")
            y = H-M-18*mm
        # Movie paragraph (last one) gets italic treatment
        if i == len(desc_paras) - 1:
            y -= 4
            y = wrap(para, M, y, CW, size=9.5, leading=13, font="Times-Italic", color=MUTED)
        else:
            y = wrap(para, M, y, CW, size=9.3, leading=12.8)
        y -= 4
    # Hope paragraph with Rose Gold accent border
    y -= 4
    hope = HOPE_TEXTS.get(primary_key, "")
    style_hope = ParagraphStyle('hope', fontName='Times-Italic', fontSize=9.5, textColor=ACCENT, leading=13.5, alignment=TA_LEFT)
    p_hope = Paragraph(safe_text(hope), style_hope)
    pw_h, ph_h = p_hope.wrap(CW-10*mm, 200)
    c.setFillColor(ACCENT);c.rect(M, y-ph_h-1, 1.2*mm, ph_h+2, fill=1, stroke=0)
    p_hope.drawOn(c, M+6*mm, y-ph_h)
    foot(page_num); c.showPage(); page_num += 1

    # ════════════════════════════════════
    # P5: YOUR UNDERTONE — dedicated page
    # ════════════════════════════════════
    lightBg()
    c.setFont("Times-Roman",9);c.setFillColor(ACCENT);c.drawString(M,H-M-5*mm,"Your Undertone")
    c.setFont("Times-Roman",24);c.setFillColor(CHARCOAL);c.drawString(M,H-M-22*mm,sec["name"])
    c.setFont("Times-Italic",12);c.setFillColor(MUTED);c.drawString(M,H-M-32*mm,sec["tag"])
    accentLine(H-M-38*mm)
    y = H-M-50*mm
    # Percentage
    c.setFont("Times-Roman",11);c.setFillColor(ACCENT)
    c.drawString(M, y, f"Your pattern: {ppct}% {prof['name']} \u00b7 {spct}% {sec['name']}")
    y -= 12*mm
    # Primary explanation
    y = wrap(f"Your primary pattern \u2014 {prof['name']} \u2014 is the dominant strategy your nervous system uses to manage sustained pressure. It's the pattern most visible in your daily life, your work, and your relationships. It accounts for approximately {ppct}% of your nervous system behaviour.", M, y, CW)
    y -= 6
    y = wrap(f"Your undertone \u2014 {sec['name']} \u2014 is the shadow pattern. It accounts for approximately {spct}% of your behaviour and surfaces under extreme pressure, fatigue, or when your primary strategy can no longer hold. Under sustained stress, your {prof['name']} pattern gives way to {sec['name']} characteristics.", M, y, CW)
    y -= 6
    y = wrap(f"This specific combination \u2014 {prof['name']} with {sec['name']} undertone \u2014 shapes everything: how you crash, how you recover, what sensory experiences regulate you, and which practices will work for your particular nervous system. A {prof['name']} with a different undertone would need different practices.", M, y, CW)
    # SPACE before secondary heading
    y -= 14*mm
    # Secondary profile heading
    c.setFont("Times-Roman",15);c.setFillColor(sCol)
    c.drawString(M, y, f"The {sec['name']} Pattern")
    y -= 9*mm
    # 2 paragraphs of secondary description in CHARCOAL (not muted)
    sec_descs = FULL_DESCRIPTIONS.get(secondary_key, [""])
    for para in sec_descs[:2]:
        y = wrap(para, M, y, CW, font="Times-Roman", color=CHARCOAL)
        y -= 5
        if y < 25*mm: break
    foot(page_num);c.showPage(); page_num += 1

    # ════════════════════════════════════
    # P6: ANSR MAP — DUAL Radar
    # ════════════════════════════════════
    lightBg()
    c.setFont("Times-Roman",9);c.setFillColor(ACCENT)
    c.drawString(M, H-M-5*mm, f"{user_name}\u2019s ANSR Map")
    
    cx, cy, radius = W/2, H-105*mm, 45*mm
    angles = [(math.pi*2*i/6)-math.pi/2 for i in range(6)]
    
    # Grid
    for r_s in [0.25,0.5,0.75,1.0]:
        pts = [(cx+math.cos(a)*radius*r_s, cy+math.sin(a)*radius*r_s) for a in angles]
        path = c.beginPath();path.moveTo(pts[0][0],pts[0][1])
        for pt in pts[1:]:path.lineTo(pt[0],pt[1])
        path.close();c.setStrokeColor(HexColor("#C8C3BC"));c.setLineWidth(0.15);c.drawPath(path,fill=0,stroke=1)
    for a in angles:
        c.setStrokeColor(HexColor("#D2CDC6"));c.setLineWidth(0.1);c.line(cx,cy,cx+math.cos(a)*radius,cy+math.sin(a)*radius)
    
    # Labels
    c.setFont("Times-Roman",8);c.setFillColor(CHARCOAL)
    for i,(lbl,key) in enumerate(zip(DIM_LABELS,DIM_KEYS)):
        a=angles[i];lx=cx+math.cos(a)*(radius+8*mm);ly=cy+math.sin(a)*(radius+8*mm)
        txt=f"{lbl} {scores[key]:.1f}"
        if math.cos(a)>0.3:c.drawString(lx-2*mm,ly,txt)
        elif math.cos(a)<-0.3:c.drawRightString(lx+2*mm,ly,txt)
        else:c.drawCentredString(lx,ly,txt)
    
    # SECONDARY shape (outline/dashed) — draw first so primary overlays
    # Use the "ideal" scores for the secondary profile type as a reference shape
    sec_ideal = _get_profile_reference_shape(secondary_key)
    dp_sec = [(cx+math.cos(angles[i])*radius*max(sec_ideal[k]/10,0.05),cy+math.sin(angles[i])*radius*max(sec_ideal[k]/10,0.05)) for i,k in enumerate(DIM_KEYS)]
    c.saveState()
    c.setDash(3,3)
    c.setStrokeColor(sCol);c.setLineWidth(0.7)
    path_s=c.beginPath();path_s.moveTo(dp_sec[0][0],dp_sec[0][1])
    for pt in dp_sec[1:]:path_s.lineTo(pt[0],pt[1])
    path_s.close();c.drawPath(path_s,fill=0,stroke=1)
    c.restoreState()
    for pt in dp_sec:c.setFillColor(sCol);c.circle(pt[0],pt[1],0.8*mm,fill=1,stroke=0)
    
    # PRIMARY shape (filled)
    dp = [(cx+math.cos(angles[i])*radius*max(scores[k]/10,0.05),cy+math.sin(angles[i])*radius*max(scores[k]/10,0.05)) for i,k in enumerate(DIM_KEYS)]
    path=c.beginPath();path.moveTo(dp[0][0],dp[0][1])
    for pt in dp[1:]:path.lineTo(pt[0],pt[1])
    path.close()
    c.saveState();c.setFillColor(Color(pCol.red,pCol.green,pCol.blue,alpha=0.15));c.drawPath(path,fill=1,stroke=0);c.restoreState()
    c.setStrokeColor(pCol);c.setLineWidth(0.8)
    ol=c.beginPath();ol.moveTo(dp[0][0],dp[0][1])
    for pt in dp[1:]:ol.lineTo(pt[0],pt[1])
    ol.close();c.drawPath(ol,fill=0,stroke=1)
    for pt in dp:c.setFillColor(pCol);c.circle(pt[0],pt[1],1.2*mm,fill=1,stroke=0)
    c.setFillColor(ACCENT);c.circle(cx,cy,1*mm,fill=1,stroke=0)
    
    # Legend
    leg_y = cy - radius - 10*mm
    c.setFont("Times-Roman",7);c.setFillColor(pCol)
    c.rect(M, leg_y+1, 8*mm, 2, fill=1, stroke=0)
    c.drawString(M+10*mm, leg_y, f"Your scores ({prof['name']})")
    c.setFillColor(sCol)
    c.saveState();c.setDash(3,3);c.setStrokeColor(sCol);c.setLineWidth(0.5);c.line(M, leg_y-6*mm+1, M+8*mm, leg_y-6*mm+1);c.restoreState()
    c.drawString(M+10*mm, leg_y-7*mm, f"{sec['name']} reference pattern")
    
    # Expert interpretation — 2-3 paragraphs
    y = leg_y - 16*mm
    p1, p2, p3 = get_radar_interpretation(scores, primary_key, secondary_key, ppct, spct)
    y = wrap(p1, M, y, CW, size=10, leading=14.5)
    y -= 4
    y = wrap(p2, M, y, CW, size=10, leading=14.5)
    y -= 4
    if y > 30*mm:
        y = wrap(p3, M, y, CW, size=10, leading=14.5)
    
    foot(page_num);c.showPage(); page_num += 1

    # ════════════════════════════════════
    # P7-12: SIX DIMENSION PAGES — ranked by score (strength → weakness)
    # ════════════════════════════════════
    dim_ranked = sorted(zip(DIM_KEYS, DIM_LABELS), key=lambda x: -scores[x[0]])
    for idx,(dk,dl) in enumerate(dim_ranked):
        lightBg()
        sc = scores[dk]
        band = get_band(sc)
        insight = DIM_INSIGHTS.get(dk,{}).get(band,"")
        if not insight:
            insight = f"Your {dl.lower()} score is {sc:.1f}/10."
        
        c.setFont("Times-Roman",9);c.setFillColor(ACCENT);c.drawString(M,H-M-5*mm,f"Dimension {idx+1} of 6")
        c.setFont("Times-Roman",24);c.setFillColor(CHARCOAL);c.drawString(M,H-M-20*mm,dl)
        c.setFont("Times-Roman",12);c.setFillColor(MUTED);c.drawRightString(W-M,H-M-15*mm,f"{sc:.1f} / 10")
        c.setFont("Times-Roman",10);c.setFillColor(get_band_color(sc));c.drawRightString(W-M,H-M-23*mm,band)
        
        # Progress bar
        by = H-M-30*mm
        c.setFillColor(HexColor("#E6E1DA"));c.rect(M,by,CW,3*mm,fill=1,stroke=0)
        c.setFillColor(ACCENT);c.rect(M,by,CW*max(sc/10,0.03),3*mm,fill=1,stroke=0)
        accentLine(by-5*mm)
        
        # Full insight text (multi-paragraph, split by \n\n)
        y = by - 15*mm
        paras = insight.split('\n\n')
        for pi, para in enumerate(paras):
            y = wrap(para, M, y, CW, size=10, leading=14.5)
            y -= 5
            if y < 50*mm and pi < len(paras)-1:
                break  # Don't overflow, truncate gracefully
        
        # Band scale at bottom
        y = min(y - 8, 70*mm)
        c.setFont("Times-Roman",8)
        for rng,bl,desc in [("0 \u2014 2.5","Contracted","Deep depletion"),("2.5 \u2014 5","Compressed","Narrowing, partial awareness"),("5 \u2014 7.5","Emerging","Capacity returning"),("7.5 \u2014 10","Open","Healthy, regulated")]:
            is_current = bl == band
            c.setFillColor(CHARCOAL if is_current else DIM)
            c.setFont("Times-Bold" if is_current else "Times-Roman", 8)
            arrow = "  \u2190" if is_current else ""
            c.drawString(M,y,f"{rng}  {bl} \u2014 {desc}{arrow}")
            y -= 5*mm
        
        foot(page_num);c.showPage(); page_num += 1

    # ════════════════════════════════════
    # P13: SENSORY SIGNATURE — clean luxury layout
    # ════════════════════════════════════
    lightBg()
    c.setFont("Times-Roman",9);c.setFillColor(ACCENT);c.drawString(M,H-M-5*mm,"Your Sensory Signature")
    c.setFont("Times-Roman",24);c.setFillColor(pCol);c.drawString(M,H-M-22*mm,sensory[0])
    accentLine(H-M-28*mm)
    y = H-M-40*mm
    # Main description
    y = wrap(sensory[1], M, y, CW, size=10, leading=14.5)
    y -= 5
    # WHY she landed on this channel
    y = wrap(sensory[2], M, y, CW, size=10, leading=14.5, font="Times-Italic", color=MUTED)
    y -= 5
    y = wrap("Your sensory signature is the channel through which your nervous system most effectively restores itself. It's not a preference \u2014 it's a physiological pathway. When you use this channel deliberately, restoration happens faster and deeper than through willpower, rest, or distraction alone.", M, y, CW, size=10, leading=14.5)
    y -= 14
    # Short accent line divider
    c.setStrokeColor(ACCENT);c.setLineWidth(0.3);c.line(M,y,M+25*mm,y)
    y -= 12*mm
    # Section heading
    c.setFont("Times-Roman",11);c.setFillColor(CHARCOAL)
    c.drawString(M, y, "The Six Sensory Channels")
    y -= 10*mm
    # Clean uniform list — ALL titles in charcoal, ALL descriptions in charcoal, her channel bold
    for idx, (ch_code, ch_name, ch_desc) in enumerate(ALL_SENSORY_CHANNELS):
        is_hers = ch_code == sensory_type
        num = f"{idx+1}. "
        # Channel name — all in charcoal, hers is bold, numbered
        if is_hers:
            c.setFont("Times-Bold",10);c.setFillColor(CHARCOAL)
            c.drawString(M, y, f"{num}{ch_name}")
            tw = c.stringWidth(f"{num}{ch_name}", "Times-Bold", 10)
            c.setFont("Times-Italic",8);c.setFillColor(ACCENT)
            c.drawString(M + tw + 3*mm, y + 0.3, "your channel")
        else:
            c.setFont("Times-Roman",10);c.setFillColor(CHARCOAL)
            c.drawString(M, y, f"{num}{ch_name}")
        y -= 5*mm
        # Description — all in charcoal, same size
        y = wrap(ch_desc, M, y, CW, size=8.5, leading=11.5, color=CHARCOAL)
        y -= 7*mm  # Generous gap between channels
    
    foot(page_num);c.showPage(); page_num += 1

    # ════════════════════════════════════
    # P13-14: RESTORATION — expanded practices, may span 2 pages
    # ════════════════════════════════════
    lightBg()
    c.setFont("Times-Roman",9);c.setFillColor(ACCENT);c.drawString(M,H-M-5*mm,"Your Restoration Path")
    c.setFont("Times-Roman",22);c.setFillColor(CHARCOAL);c.drawString(M,H-M-20*mm,"Nervous System Restoration")
    accentLine(H-M-26*mm)
    y = H-M-36*mm
    y = wrap("Restoring a nervous system that has been in survival mode requires a specific sequence of sensory interventions \u2014 not information, not insight, but physical experiences that teach your body a new baseline. These three practices are matched to your dual-profile combination.", M, y, CW, size=10, leading=14.5)
    y -= 14
    rest_page = page_num
    for i,(name,desc) in enumerate(practices):
        # Check if we need a new page (need ~70mm for title + paragraph)
        if y < 70*mm:
            foot(rest_page);c.showPage();lightBg()
            rest_page += 1
            c.setFont("Times-Roman",9);c.setFillColor(ACCENT);c.drawString(M,H-M-5*mm,"Your Restoration Path (continued)")
            y = H-M-18*mm
        y -= 6
        c.setFont("Times-Roman",12);c.setFillColor(ACCENT);c.drawString(M,y,f"{i+1}. {name}")
        y -= 8*mm
        y = wrap(desc, M, y, CW, size=9.5, leading=13.5)
        y -= 12
    foot(rest_page);c.showPage(); page_num = rest_page + 1

    # ════════════════════════════════════
    # P14-15: THE SIX PROFILES — may span 2 pages with expanded descriptions
    # ════════════════════════════════════
    lightBg()
    c.setFont("Times-Roman",9);c.setFillColor(ACCENT);c.drawString(M,H-M-5*mm,"The Six ANSR Profiles")
    c.setFont("Times-Roman",16);c.setFillColor(CHARCOAL)
    c.drawString(M,H-M-17*mm,"Know the patterns. See the people around you.")
    accentLine(H-M-22*mm)
    y = H-M-32*mm
    six_page = page_num
    profiles_order = ["sunfire","velvetblade","eclipse","summerstorm","heartwood","newmoon"]
    for i,pk in enumerate(profiles_order):
        pb = PROFILES_BASIC[pk]
        is_hers = pk == primary_key
        
        # Check if we need a new page
        if y < 55*mm:
            foot(six_page);c.showPage();lightBg()
            six_page += 1
            c.setFont("Times-Roman",9);c.setFillColor(ACCENT);c.drawString(M,H-M-5*mm,"The Six ANSR Profiles")
            y = H-M-18*mm
        
        # Profile name in its color
        if is_hers:
            c.setFont("Times-Bold",11);c.setFillColor(PROF_COLORS[pk])
            c.drawString(M, y, pb["name"])
            tw = c.stringWidth(pb["name"], "Times-Bold", 11)
            c.setFont("Times-Italic",8);c.setFillColor(ACCENT)
            c.drawString(M + tw + 3*mm, y + 0.5, "you")
        else:
            c.setFont("Times-Roman",11);c.setFillColor(PROF_COLORS[pk])
            c.drawString(M, y, pb["name"])
        y -= 4.5*mm
        
        # Tagline — same line energy, italic
        c.setFont("Times-Italic",8.5);c.setFillColor(MUTED)
        c.drawString(M, y, pb["tag"])
        y -= 5*mm
        
        # Short description — compact
        y = wrap(pb["short"], M, y, CW, size=8, leading=11, color=CHARCOAL)
        y -= 8*mm
    
    foot(six_page);c.showPage(); page_num = six_page + 1

    # ════════════════════════════════════
    # P17: THE BRIDGE — upsells + REAL QR CODE
    # ════════════════════════════════════
    lightBg()
    c.setFont("Times-Roman",9);c.setFillColor(ACCENT);c.drawString(M,H-M-5*mm,"What Comes Next")
    c.setFont("Times-Roman",22);c.setFillColor(CHARCOAL);c.drawString(M,H-M-20*mm,"Two Paths Forward")
    accentLine(H-M-26*mm)
    y = H-M-38*mm
    y = wrap("Your ANSR Profile has shown you the pattern. The practices above are your starting point. For women ready to go deeper, two paths continue from here:", M, y, CW)
    y -= 12
    c.setFont("Times-Roman",13);c.setFillColor(ACCENT);c.drawString(M,y,"The Aesthetic Reset \u2014 \u20ac197");y -= 7*mm
    y = wrap("A structured nervous system restoration programme designed for your specific ANSR profile. The practices build on each other in sequence. Self-guided. At your own pace. The container your practices need.", M, y, CW);y -= 12
    c.setFont("Times-Roman",13);c.setFillColor(ACCENT);c.drawString(M,y,"ANSR Profile Interpretation \u2014 \u20ac350");y -= 7*mm
    y = wrap("A private 90-minute session with Alexandre Olive. Not coaching. A premium reading of your complete dual-profile \u2014 what the report couldn't fully convey. One decision point. One 90-day stabilisation plan. Limited to 20 sessions.", M, y, CW);y -= 12
    c.setFont("Times-Italic",10.5);c.setFillColor(MUTED)
    y = wrap("Your nervous system found its way here. Trust what brought you.", M, y, CW, font="Times-Italic", color=MUTED);y -= 14
    c.setStrokeColor(ACCENT);c.setLineWidth(0.2);c.line(M,y,W-M,y)
    
    # Push the ANSR Pulse section to a fixed lower position
    y = 105*mm
    c.setFont("Times-Roman",10);c.setFillColor(CHARCOAL)
    c.drawCentredString(W/2, y, "Know a woman who needs to see her pattern?")
    y -= 8*mm
    c.setFont("Times-Roman",9);c.setFillColor(ACCENT)
    c.drawCentredString(W/2, y, "The ANSR Pulse is free")
    y -= 12*mm
    
    # REAL QR CODE — centered
    qr = QrCodeWidget("https://ansr-pulse.vercel.app")
    qr.barWidth = 30*mm
    qr.barHeight = 30*mm
    qr.barLevel = 'M'
    d = Drawing(30*mm, 30*mm)
    d.add(qr)
    qr_x = (W - 30*mm) / 2
    qr_y = y - 30*mm
    renderPDF.draw(d, c, qr_x, qr_y)
    
    c.setFont("Times-Roman",8);c.setFillColor(DIM)
    c.drawCentredString(W/2, qr_y - 5*mm, "Scan to take the free ANSR Pulse")
    c.drawCentredString(W/2, qr_y - 10*mm, "ansr-pulse.vercel.app")
    
    # Footer branding
    c.setFont("Times-Roman",10);c.setFillColor(CHARCOAL);c.drawCentredString(W/2, 35*mm, "E L I A")
    c.setFont("Times-Italic",8);c.setFillColor(MUTED);c.drawCentredString(W/2, 29*mm, "Beauty That Heals")
    c.setFont("Times-Roman",7);c.setFillColor(DIM);c.drawCentredString(W/2, 20*mm, "ANSR\u2122 \u00b7 \u00a9 ELIA / Uskale SA \u00b7 Personal development purposes only")
    c.showPage()
    
    c.save()
    return True


def _get_profile_reference_shape(profile_key):
    """Return a 'typical' score shape for each profile to use as secondary radar overlay."""
    shapes = {
        "sunfire": {"alertness": 2.5, "sensitivity": 4.0, "vitality": 3.5, "connection": 4.5, "performance": 8.0, "aliveness": 3.5},
        "velvetblade": {"alertness": 5.0, "sensitivity": 3.0, "vitality": 5.0, "connection": 3.0, "performance": 6.5, "aliveness": 4.0},
        "eclipse": {"alertness": 4.0, "sensitivity": 2.5, "vitality": 3.0, "connection": 3.0, "performance": 5.5, "aliveness": 2.5},
        "summerstorm": {"alertness": 3.5, "sensitivity": 7.5, "vitality": 4.0, "connection": 5.0, "performance": 4.5, "aliveness": 5.5},
        "heartwood": {"alertness": 5.0, "sensitivity": 5.0, "vitality": 4.5, "connection": 3.0, "performance": 6.0, "aliveness": 3.5},
        "newmoon": {"alertness": 4.5, "sensitivity": 5.5, "vitality": 5.0, "connection": 4.5, "performance": 5.0, "aliveness": 5.5},
    }
    return shapes.get(profile_key, {"alertness": 5, "sensitivity": 5, "vitality": 5, "connection": 5, "performance": 5, "aliveness": 5})


# ═══════════════════════════════════════
# GENERATE SAMPLE
# ═══════════════════════════════════════
if __name__ == "__main__":
    scores = {"alertness": 4.3, "sensitivity": 3.1, "vitality": 5.7, "connection": 2.8, "performance": 6.4, "aliveness": 4.0}
    output = "/mnt/user-data/outputs/ANSR-Profile-FINAL.pdf"
    generate_pdf("Isabelle Durand", "velvetblade", "heartwood", scores, "S", output, "10 March 2026")
    ppct, spct = calc_profile_pct(scores, "velvetblade", "heartwood")
    print(f"Generated: {output}")
    print(f"Profile split: {ppct}% Velvet Blade / {spct}% Heartwood")
