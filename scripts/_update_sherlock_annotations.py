#!/usr/bin/env python3
"""Update Sherlock Holmes story annotations (LLM-authored content, script only locates/writes)."""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LIB = REPO / "content/library/002-adventures-of-sherlock-holmes.json"

SKIP = {"red-headed-league"}

# Each entry: (quote, category, note, occurrence=0)
STORY_ANNOTATIONS: dict[str, list[tuple]] = {
    "scandal-in-bohemia": [
        (
            "To Sherlock Holmes she is always _the_ woman. I have seldom heard him\nmention her under any other name.",
            "theme",
            "TH: Watson opens with the story's lasting theme: Irene Adler is the one woman who outranked every other in Holmes's mind.",
        ),
        (
            "He was, I take it, the most perfect reasoning and observing machine that\nthe world has seen, but as a lover he would have placed himself in a\nfalse position.",
            "theme",
            "MI: Holmes is defined as pure intellect; emotion would corrupt his method, yet this case will test that claim.",
        ),
        (
            '"I have no data yet. It is a capital mistake to theorise before one has\ndata. Insensibly one begins to twist facts to suit theories, instead of\ntheories to suit facts."',
            "structure",
            "STR: Holmes states his investigative rule before the masked client arrives: gather data first, then build theory.",
        ),
        (
            '"The paper was made in Bohemia," I said.\n\n"Precisely. And the man who wrote the note is a German.',
            "evidence",
            "E: Watermark and grammar prove the anonymous note comes from a German writer linked to Bohemia, narrowing who the client may be.",
        ),
        (
            '"There is the writing."\n\n"Pooh, pooh! Forgery."\n\n"My private note-paper."\n\n"Stolen."',
            "evidence",
            "E: Holmes quickly shows why the King's compromising letters are dangerously authentic, not easily disowned.",
        ),
        (
            '"Because she has said that she would send it on the day when the\nbetrothal was publicly proclaimed. That will be next Monday."',
            "inference",
            "INF: Irene's planned timing tells Holmes she still holds the photograph and has set a deadline tied to the royal marriage.",
        ),
        (
            '"Well, I found my plans very seriously menaced. It looked as if the\npair might take an immediate departure, and so necessitate very prompt\nand energetic measures on my part.',
            "structure",
            "SHIFT: Irene's sudden marriage to Norton forces Holmes to act before she flees or hides the photograph elsewhere.",
        ),
        (
            '"You must not interfere,\ncome what may. You understand?"\n\n"I am to be neutral?"\n\n"To do nothing whatever. There will probably be some small\nunpleasantness.',
            "structure",
            "STR: Holmes lays out the staged quarrel-and-fire plan that will trick Irene into revealing where the photograph is hidden.",
        ),
        (
            "I never felt more heartily ashamed of\nmyself in my life than when I saw the beautiful creature against whom I\nwas conspiring, or the grace and kindliness with which she waited upon\nthe injured man.",
            "tone",
            "TO: Watson's guilt contrasts with Holmes's tactical coldness, showing the human cost of the deception.",
        ),
        (
            '"When a woman thinks that her house is on fire,\nher instinct is at once to rush to the thing which she values most.',
            "evidence",
            "E: Holmes explains the psychological bait behind the false alarm: crisis reveals what someone protects most.",
        ),
        (
            "The\nphotograph is in a recess behind a sliding panel just above the right\nbell-pull. She was there in an instant, and I caught a glimpse of it as\nshe half drew it out.",
            "inference",
            "INF: Irene's reflex under fire confirms Holmes's theory that she keeps the photograph in her own house, not with a banker or lawyer.",
        ),
        (
            '"Irene Adler is married," remarked Holmes.\n\n"Married! When?"\n\n"Yesterday."',
            "structure",
            "SHIFT: The morning call turns into a race: marriage may change Irene's motives and daily habits overnight.",
        ),
        (
            '"MY DEAR MR. SHERLOCK HOLMES,—You really did it very well. You took\n    me in completely. Until after the alarm of fire, I had not a\n    suspicion.',
            "evidence",
            "E: Irene's letter proves she matched Holmes move for move, recognized his disguise, and fled before he could recover the photograph.",
        ),
        (
            "And that was how a great scandal threatened to affect the kingdom of\nBohemia, and how the best plans of Mr. Sherlock Holmes were beaten by a\nwoman's wit.",
            "theme",
            "TH: Watson closes by naming the outcome: intellect alone loses to a rival who combines wit, nerve, and self-protection.",
        ),
    ],
    "case-of-identity": [
        (
            '"life is infinitely stranger than\nanything which the mind of man could invent.',
            "theme",
            "TH: Holmes frames the story's premise: real life hides bizarre plots beneath ordinary surfaces.",
        ),
        (
            "Depend upon it, there is nothing so\nunnatural as the commonplace.",
            "theme",
            "MI: The case will turn on a fraud disguised as everyday romance, not on a sensational crime.",
        ),
        (
            "The details are\nfamiliar to me, but I have not yet heard the name of the client. I\nshould be glad to know it.",
            "structure",
            "STR: Holmes shifts from abstract debate to a concrete client narrative, the usual Watson frame for a case.",
        ),
        (
            '"It is a little difficult to know what to do, Mr. Holmes," said she,\n"because no one else has ever been in the same position."',
            "evidence",
            "E: Miss Sutherland's typed correspondence with Hosmer Angel is the first hard clue that courtship happened mostly on paper.",
        ),
        (
            "He was a strange, mysterious, elusive, and yet lovable man, and I\nnever saw him save on the four occasions when he called upon my\nfather and myself at Lee.",
            "inference",
            "INF: She never met her fiancé alone and only at home, which suggests the suitor controlled access and visibility.",
        ),
        (
            '"Not invisible but unnoticed, Watson. You did not know where to look,\nand so you missed all that was important.',
            "structure",
            "STR: Holmes contrasts Watson's description of clothing with what trained observation should extract from sleeves, nails, and wear.",
        ),
        (
            '"I knew that my own stepfather was in France, and that for ten days at\nleast we should be free from his interference."',
            "evidence",
            "E: The stepfather's absence on the wedding day is the opening the impostor needs, linking timing to Windibank's control.",
        ),
        (
            "so were the tinted spectacles and the curious\nvoice, which both hinted at a disguise, as did the bushy whiskers.",
            "inference",
            "INF: Holmes reads Angel's odd voice and appearance as deliberate concealment, not romantic eccentricity.",
        ),
        (
            "My\nsuspicions were all confirmed by his peculiar action in typewriting his\nsignature, which, of course, inferred that his handwriting was so\nfamiliar to her that she would recognise even the smallest sample of\nit.",
            "evidence",
            "E: The typewritten signature is proof someone feared recognition through ordinary handwriting.",
        ),
        (
            '"There\'s a cold-blooded scoundrel!" said Holmes, laughing, as he threw\nhimself down into his chair once more.',
            "structure",
            "SHIFT: Windibank's flight confirms the trap; the comic chase ends in Holmes's moral verdict on the stepfather.",
        ),
        (
            "it was\nequally clear that the only man who really profited by the incident, as\nfar as we could see, was the stepfather.",
            "inference",
            "INF: Profit points to motive: keeping Miss Sutherland's income at home by preventing marriage.",
        ),
        (
            "I sent it to\nthe firm, with a request that they would inform me whether it answered\nto the description of any of their travellers.",
            "evidence",
            "E: Holmes verifies disguise by stripping false features from a printed description and matching them to Windibank's employer.",
        ),
    ],
    "boscombe-valley-mystery": [
        (
            '"Have you a couple of days to spare? Have just been wired for from the\nwest of England in connection with Boscombe Valley tragedy.',
            "structure",
            "STR: The telegram pulls Watson into a country murder inquiry away from ordinary domestic life.",
        ),
        (
            "The London papers\nare full of it. I presume that there is no doubt that the son murdered\nthe father?",
            "theme",
            "TH: Public opinion assumes patricide at the Boscombe Pool, but the story will test whether appearances match guilt.",
        ),
        (
            '"Rache,"\n\n"Good!" said Holmes, laughing. "It is the second time that I have heard\nthat word to-day. I have no doubt that it was written by the dead man,\nand that he meant to write Rachel, but was interrupted before he could\nfinish.',
            "evidence",
            "E: Holmes rejects the obvious German revenge reading of 'Rache' and treats the word as a misleading clue.",
        ),
        (
            "I had examined the\npool and the surrounding ground with great care, and I had formed a\npretty clear idea of what had occurred.",
            "inference",
            "INF: Holmes's site inspection implies a third person at the pool, not a simple quarrel ending in murder by the son.",
        ),
        (
            "what does the idiot do but get into the clutches of\na barmaid in Bristol and marry her at a registry office?",
            "structure",
            "STR: The hidden marriage explains why young McCarthy cannot marry Miss Turner despite loving her.",
        ),
        (
            "I was inclined to think at one time that he knew who had\ndone it and was screening him or her, but I am convinced now that he is\nas puzzled as everyone else.",
            "inference",
            "INF: The son's silence looks like guilt, but Holmes infers confusion and secret shame rather than murderous knowledge.",
        ),
        (
            "Circumstantial evidence is a very tricky thing. It may seem to point\nvery straight to one thing, but if you shift your own point of view a\nlittle, you may find it pointing in an equally uncompromising manner to\nsomething entirely different.",
            "theme",
            "MI: Holmes warns that the same facts can support opposite conclusions until the hidden motive appears.",
        ),
        (
            '"Deeply as I\nhave sinned, I have led a life of martyrdom to atone for it. But that\nmy girl should be entangled in the same meshes which held me was more\nthan I could suffer. I struck him down',
            "evidence",
            "E: Old Turner's confession supplies motive: he killed McCarthy to stop blackmail over his daughter's marriage prospects.",
        ),
        (
            '"Well, it is not for me to judge you," said Holmes as the old man\nsigned the statement which had been drawn out. "I pray that we may\nnever be exposed to such a temptation."',
            "tone",
            "TO: Holmes's sympathy is unusually personal here; he recognizes desperate parental protection, not mere villainy.",
        ),
        (
            "If McCarthy is condemned I shall be\nforced to use it. If not, it shall never be seen by mortal eye",
            "inference",
            "INF: Holmes will suppress the confession to free the son unless justice absolutely requires revealing it.",
        ),
        (
            "He\nhad gone out with a very determined purpose, and he had not returned\nuntil nearly midnight.",
            "evidence",
            "E: McCarthy's final walk to the pool, arranged by message, sets up the staged meeting that ends in violence.",
        ),
        (
            "Lestrade\nwas coming up the path with a very grave face.",
            "structure",
            "SHIFT: Official police pressure tightens just before Holmes extracts the true account from Turner.",
        ),
    ],
    "five-orange-pips": [
        (
            "There is, however, one of these last which was so remarkable in\nits details and so startling in its results that I am tempted to give\nsome account of it",
            "theme",
            "TH: Watson warns that this case mixes partial mystery with unusually stark consequences.",
        ),
        (
            "Inside I found five little dried orange pips and\na piece of paper with the letters 'K. K. K.' upon it",
            "evidence",
            "E: The first death warning arrives as five orange pips and initials, not as a direct threat in words.",
        ),
        (
            '"K. K. K.!\' he shrieked. \'My God, my God, my sins have overtaken me!\'',
            "inference",
            "INF: Openshaw's uncle reacts as if the pips revive a buried past, suggesting a long-feared secret society.",
        ),
        (
            '"4th. Hudson came. Same old platform.\n\n"7th. Set the pips on McCauley, Paramore, and John Swain of St.\nAugustine."',
            "evidence",
            "E: The torn diary page links Hudson, the pips, and named victims, turning symbols into a record of methodical persecution.",
        ),
        (
            '"You must put\nthis piece of paper which you have shown us into the brass box which\nyou have described. You must also put in a note to say that all the\nothers were burned by your uncle, and that the last one remains."',
            "structure",
            "STR: Holmes's urgent instruction shows the only counter-move he trusts against the society's ritual warning.",
        ),
        (
            "It is a little time before the poison takes effect, but in the end it\nis sure.",
            "inference",
            "INF: Holmes infers murder by means that leave little trace, which explains why the victims seemed to die mysteriously.",
        ),
        (
            '"It is really two days since you had the letter. We should have acted\nbefore this.',
            "tone",
            "TO: Holmes's impatience marks the cost of delay; the client arrives after the window for safety has narrowed.",
        ),
        (
            "Within an hour\nwe had reached the spot where the body had been found.",
            "structure",
            "SHIFT: Openshaw's death moves the case from prevention to pursuit of his killers.",
        ),
        (
            "Of these, one, the _Lone Star_, instantly attracted my\nattention, since, although it was reported as having cleared from\nLondon, the name is that which is given to one of the states of the\nUnion.",
            "evidence",
            "E: Lloyd's registers and the ship name Lone Star give Holmes an American trail tied to the murder night.",
        ),
        (
            "I know, also, that they were all three away from the ship last\nnight.",
            "inference",
            "INF: Only three native-born Americans were ashore when Openshaw died, narrowing suspects aboard the Lone Star.",
        ),
        (
            "By\nthe time that their sailing-ship reaches Savannah the mail-boat will\nhave carried this letter, and the cable will have informed the police\nof Savannah",
            "structure",
            "STR: Holmes switches from deduction to action, wiring ahead to intercept the killers abroad.",
        ),
        (
            "And\nso ended the strange case of the five orange pips, one of the most\nunique in my friend's experience, and one which, as he often remarked,\nshowed how helpless even he could be when the blow fell before he could\nstrike.",
            "theme",
            "TH: The ending stresses incomplete justice: Holmes's logic arrives too late to save Openshaw.",
        ),
    ],
    "man-with-the-twisted-lip": [
        (
            "The\nhabit grew upon him, as I understand, from some foolish freak when he\nwas at college",
            "theme",
            "T: Opium addiction frames the case: respectability, poverty, and hidden lives collide in London's underworld.",
        ),
        (
            '"I didn\'t know what to do, so I came straight to you." That was always\nthe way. Folk who were in grief came to my wife',
            "structure",
            "STR: Domestic distress enters through Mrs. Whitney, shifting Watson from doctor at home to Holmes's investigation.",
        ),
        (
            "On the window-sill was a bloodstain and beside it several scattered\ncoins and a man's coarse sleeve-link.",
            "evidence",
            "E: Blood on the sill and coins in the coat suggest violence and a hasty attempt to sink evidence in the Thames.",
        ),
        (
            "Boone, as I have told you, was arrested and taken to the station, but\nit could not be shown that there had ever before been anything against\nhim.",
            "inference",
            "INF: The beggar's clean record makes murder less likely and raises the question of mistaken identity.",
        ),
        (
            "what\nNeville St. Clair was doing in the opium den, what happened to him when\nthere, where is he now, and what Hugh Boone had to do with his\ndisappearance—are all as far from a solution as ever.",
            "theme",
            "MI: Holmes admits the case looks simple yet resists explanation, setting up the hidden-double-life reveal.",
        ),
        (
            "Swiftly I threw off\nmy clothes, pulled on those of a beggar, and put on my pigments and\nwig.",
            "structure",
            "SHIFT: St. Clair's confession reverses the plot: the missing man and the beggar are the same person.",
        ),
        (
            "I found that I made more in a day as a beggar than I could do in a\nmonth by my profession.",
            "evidence",
            "E: St. Clair confesses that disguise paid better than honest journalism, explaining why he kept the secret.",
        ),
        (
            "I hurled it out of the window, and it\ndisappeared into the Thames. The other clothes would have followed, but\nat that moment there was a rush of constables up the stair",
            "inference",
            "INF: Weighting the coat with coppers was meant to hide the respectable clothes that would expose his disguise.",
        ),
        (
            '"That note only reached her yesterday," said Holmes.\n\n"Good God! What a week she must have spent!"',
            "tone",
            "TO: The delayed note turns comic misunderstanding into real marital suffering.",
        ),
        (
            "I was determined to preserve my disguise as long as possible, and hence my\npreference for a dirty face.",
            "evidence",
            "E: St. Clair kept playing Hugh Boone even after arrest because exposure would destroy family and income.",
        ),
        (
            "Mrs. St. Clair had fainted at the\nsight of the blood upon the window.",
            "inference",
            "INF: Her collapse shows she read the scene as fatal violence, which is exactly what the planted blood was meant to suggest.",
        ),
        (
            '"Get out!" said he.\n\n"What, sir! Oh, Heaven bless you!"\n\n"No more words. Get out!"',
            "structure",
            "STR: Holmes ends not with prosecution but release, closing the case through mercy rather than court.",
        ),
    ],
    "blue-carbuncle": [
        (
            '"The matter is a perfectly trivial one"—he jerked his thumb in the\ndirection of the old hat—"but there are points in connection with it\nwhich are not entirely devoid of interest and even of instruction."',
            "theme",
            "TH: Holmes frames a comic lost-hat episode as a chain of deduction, not a major crime at first.",
        ),
        (
            '"You see, but you do not observe. The distinction is clear."',
            "evidence",
            "E: Holmes reads Henry Baker's identity, habits, and decline from the hat alone, proving observation beats guessing.",
        ),
        (
            "A carbuncle, then, of a\nconsiderable size and value was missing from the hotel where this man\nhad lodged.",
            "structure",
            "SHIFT: The goose ceases to be a joke when the stolen jewel appears in its crop.",
        ),
        (
            "There is the Alpha Inn, near the Museum—we are to be found in the Museum itself during the\nday, you understand. This year our good host, Windigate by name,\ninstituted a goose club",
            "evidence",
            "E: The goose club trail links Baker's bird to a specific inn and distribution chain Holmes can follow.",
        ),
        (
            "Breckinridge, of Covent Garden.",
            "inference",
            "INF: The dealer's refusal to name buyers blocks the trail, forcing Holmes to lure the thief rather than chase records.",
        ),
        (
            "Bring back this goose,\nMr. Baker, at eight o'clock to-night, and I will give you another bird\nof the same value if you can tell me where it came from.",
            "structure",
            "STR: Holmes's advertisement turns passive inventory into bait for the man who knows which goose holds the stone.",
        ),
        (
            "My heart turned to water, for\nthere was no sign of the stone, and I knew that some terrible mistake\nhad occurred.",
            "tone",
            "TO: Ryder's panic when the wrong goose is opened shows guilt before he speaks a full confession.",
        ),
        (
            "'Yes, Jem; there were two barred-tailed ones, and I could never tell\nthem apart.'",
            "evidence",
            "E: Two identical geese explain how the carbuncle-bearing bird was swapped away from Ryder's chosen one.",
        ),
        (
            "I had a friend\nnamed Maudsley, who was at the hotel, and who knew all about the stone.\nHe had planned the robbery",
            "inference",
            "INF: Ryder did not mastermind the theft; fear and convenience led him to hide the gem in a goose bound for market.",
        ),
        (
            '"Get out!" said he.',
            "structure",
            "STR: Holmes dismisses Ryder instead of handing him to the police, making mercy the story's final move.",
        ),
        (
            "After all, Watson," said Holmes, reaching up his hand for his clay pipe,\n"I am not retained by the police to supply their deficiencies.",
            "theme",
            "TH: Holmes separates justice from prosecution: Christmas charity outweighs jailing a terrified small thief.",
        ),
        (
            "Amid the action and reaction of so dense a swarm of humanity,\nevery possible combination of events may be expected to take place, and\nmany a little problem will be presented which may be striking and\nbizarre without being criminal.",
            "theme",
            "MI: The opening claim holds: coincidence and oddity need not equal felony.",
        ),
    ],
    "speckled-band": [
        (
            "Of all these varied cases, however, I cannot recall any\nwhich presented more singular features than that which was associated\nwith the well-known Surrey family of the Roylotts of Stoke Moran.",
            "theme",
            "TH: Watson signals a gothic household mystery where family power and violence sit at the center.",
        ),
        (
            '"It is not cold which makes me shiver," said the woman, and with a\nconvulsive movement she raised her veil.\n\n"It is fear, Mr. Holmes. It is terror."',
            "tone",
            "TO: Helen Stoner's terror establishes immediate danger before Holmes knows the mechanism.",
        ),
        (
            "It was the band! The speckled band!"',
            "evidence",
            "E: Julia's dying words are the story's central clue, though their meaning stays hidden until the end.",
        ),
        (
            "He had no friends at all save the wandering gypsies, and he would\naccept in return the hospitality of their tents, wandering away\nsometimes for weeks on end.",
            "inference",
            "INF: Roylott's gypsy camp and exotic pets misdirect suspicion toward outsiders instead of the stepfather.",
        ),
        (
            "An Eley's No. 2 is an excellent argument\nwith gentlemen who can twist steel pokers into knots.",
            "structure",
            "STR: Holmes arms himself because he expects physical danger, not a mere interview at Stoke Moran.",
        ),
        (
            "To me at least\nthere was a strange contrast between the sweet promise of the spring\nand this sinister quest upon which we were engaged.",
            "tone",
            "TO: Spring beauty against murderous purpose heightens the case's gothic tension.",
        ),
        (
            "the bell-rope hung down beside the bed, and the\nfringe of it lay upon the pillow. The bed itself was clamped to the\nfloor.",
            "evidence",
            "E: The dummy bell-pull, fixed bed, and ventilator are physical proof the room was engineered as a trap.",
        ),
        (
            "The idea of a snake instantly occurred to me, and when I coupled it\nwith my knowledge that the doctor was furnished with a supply of\ncreatures from India, I felt that I was probably on the right track.",
            "inference",
            "INF: Holmes links Indian animals, whistle signals, and untraceable poison to a snake sent through the ventilator.",
        ),
        (
            "The metallic clang heard by Miss Stoner was\nobviously caused by her stepfather hastily closing the door of his safe\nupon its terrible occupant.",
            "evidence",
            "E: Milk, safe, and whipcord confirm the snake's training and storage, explaining the nightly metallic sound.",
        ),
        (
            "We must sit without a light or the snake may\nwarn its master that we are there.",
            "structure",
            "STR: The night vigil shifts the story from explanation to live confrontation in Helen's bedroom.",
        ),
        (
            "He hurled the snake away into the darkness and\nclearly heard it strike against the wall with a dull thud.",
            "structure",
            "SHIFT: Holmes turns the murder weapon back on Roylott, ending the threat in one violent reversal.",
        ),
        (
            "Of all the\nqueer things that I have heard, this is the queerest, and I have heard\nmany strange ones in my time.",
            "inference",
            "INF: The 'speckled band' is literally the swamp adder, not gypsy clothing or metaphor alone.",
        ),
        (
            "Violence does, in\ntruth, recoil upon the violent, and the schemer falls into the pit\nwhich he digs for another.",
            "theme",
            "TH: Holmes states the moral outcome: Roylott's own trap destroys him.",
        ),
    ],
    "engineers-thumb": [
        (
            "The story has, I believe, been told more than once in the\nnewspapers, but, like all such narratives, its effect is much less\nstriking when set forth _en bloc_ in a single half-column of print than\nwhen the facts slowly evolve before your own eyes",
            "structure",
            "STR: Watson promises gradual revelation, matching how each discovery advances the mystery.",
        ),
        (
            "A stranger entered the\nroom and offered me fifty guineas if I would spend a night at his house\nand repair a hydraulic press which had been injured.",
            "theme",
            "TH: The case begins as paid technical work but will expose criminal industry hidden behind respectability.",
        ),
        (
            "Who were these German people, and\nwhat were they doing living in this strange, out-of-the-way place?",
            "inference",
            "INF: Isolation, secrecy, and nationality raise Hatherley's unease before any attack occurs.",
        ),
        (
            "'I would go,' said she, trying hard, as it seemed to me, to speak\ncalmly; 'I would go. I should not stay here. There is no good for you\nto do.'",
            "evidence",
            "E: The woman's whispered warning is the first direct clue that Hatherley is in real danger, not merely odd company.",
        ),
        (
            "He pressed the\nlever, and the press came down with a thud. I yelled with pain, but the\nthud of the press drowned my cries.",
            "structure",
            "SHIFT: The repair job becomes assault when Hatherley's thumb is caught and severed.",
        ),
        (
            "There can be no question that it was your oil-lamp which, when it was\ncrushed in the press, set fire to the wooden walls",
            "inference",
            "INF: Holmes explains the fire as an accidental by-product of the chase, not the criminals' original plan.",
        ),
        (
            "Large masses of nickel and of tin\nwere discovered stored in an out-house, but no coins were to be found",
            "evidence",
            "E: Metal stock and destroyed machinery support counterfeiting, explaining why the press mattered and why witnesses had to be silenced.",
        ),
        (
            "He had evidently been carried out\nthrough the kitchen door and so round into the lane.",
            "evidence",
            "E: Mould impressions show Hatherley was moved while unconscious, proving organized removal not random violence.",
        ),
        (
            "And Holmes' fears came to be realised, for from that day to this no\nword has ever been heard either of the beautiful woman, the sinister\nGerman, or the morose Englishman.",
            "theme",
            "TH: Unlike many Holmes tales, this one ends with escape rather than capture: ingenuity fails to locate the gang.",
        ),
        (
            "I had\nobserved that the press was stained with blood in several places, and\nthat a human thumb had been found upon the window-sill.",
            "inference",
            "INF: Blood on the press and the severed thumb confirm mutilation meant to terrorize or disable the witness.",
        ),
        (
            "It was\nwith a sinking heart that I heard Hatherley's story, for I knew only too\nwell what a terrible master he served, and how dangerous it was to\ncross his path.",
            "tone",
            "TO: Colonel Stark's reputation precedes him, lending dread before Holmes even investigates.",
        ),
        (
            "save some twisted cylinders and\niron piping, not a trace remained of the machinery which had cost our\nunfortunate acquaintance so dearly.",
            "structure",
            "STR: Fire destroys the site, erasing evidence and forcing Holmes to reconstruct the crime from fragments.",
        ),
    ],
    "noble-bachelor": [
        (
            "The Lord St. Simon marriage, and its curious termination, have long\nceased to be a subject of interest in those exalted circles",
            "theme",
            "T: Society treats the scandal as gossip, but Watson promises the fuller reasoning behind its strange ending.",
        ),
        (
            "she\nsuddenly stopped, looked at him with a strange expression, and threw\nhimself into his arms. Lord St. Simon was, as I understand, a little\nstartled by this, but he was a man of the world, and he shook her off\nwith some little show of impatience.",
            "evidence",
            "E: The bride's abrupt change at the altar foreshadows flight rather than ordinary wedding nerves.",
        ),
        (
            "she\nhad suddenly turned and walked out of the room, leaving her bouquet on\nthe table.",
            "structure",
            "SHIFT: The missing bride at breakfast turns a society wedding into an investigation.",
        ),
        (
            '"I have solved it."\n\n"Eh? What was that?"\n\n"I say that I have solved it."',
            "inference",
            "INF: Holmes's confidence before questioning St. Simon signals that social clues already outrank the peer's bewilderment.",
        ),
        (
            "Circumstantial evidence is occasionally\nvery convincing, as when you find a trout in the milk, to quote\nThoreau's example.",
            "evidence",
            "E: Holmes treats small mismatches—like a trout in milk—as proof when they fit a pattern.",
        ),
        (
            "claim-jumping—which in miners'\nparlance means taking possession of that which another person has a\nprior claim to—the whole situation became absolutely clear.",
            "inference",
            "INF: The American idiom reveals the bride returned to a prior claim, not to abduction.",
        ),
        (
            "By the select prices. Eight shillings for a bed and eightpence for a\nglass of sherry pointed to one of the most expensive hotels.",
            "evidence",
            "E: Hotel charges let Holmes narrow where Francis H. Moulton could afford to stay in London.",
        ),
        (
            "His letters were\nto be forwarded to 226 Gordon Square; so thither I travelled, and being\nfortunate enough to find the loving couple at home",
            "structure",
            "STR: The trail ends not in crime but reunion: Holmes locates bride and former husband together.",
        ),
        (
            "She was brought up in America and was\nreported to have died there, so that her husband thought himself free\nand married again.",
            "theme",
            "MI: The 'disappearance' is really conflicting marriages and mistaken death, not aristocratic kidnapping.",
        ),
        (
            "I ventured to give\nthem some paternal advice and to point out to them that it would be\nbetter in every way that they should make their position a little\nclearer both to the general public and to Lord St. Simon in particular.",
            "tone",
            "TO: Holmes's dry 'paternal advice' undercuts noble outrage with calm social practicality.",
        ),
        (
            "I had formed my conclusions as to the case before\nour client came into the room.",
            "structure",
            "STR: Holmes narrates backward from solution, teaching how pre-existing parallel cases accelerate reading.",
        ),
        (
            "Lord St. Simon shook his head. \"I am afraid that it will take wiser\nheads than yours or mine,\" he remarked",
            "inference",
            "INF: St. Simon's class pride blinds him to evidence Holmes already considers obvious.",
        ),
    ],
    "beryl-coronet": [
        (
            '"Here is a madman coming along. It seems rather sad that\nhis relatives should allow him to come out alone."',
            "theme",
            "T: Holder looks frantic before he speaks, signaling a family crisis tied to wealth and reputation.",
        ),
        (
            "The Beryl Coronet—one of the most\nprecious public possessions of the empire—has been nearly stolen and\nyet the thief has not been apprehended.",
            "theme",
            "MI: A national treasure in private hands raises stakes beyond ordinary theft: scandal, not just loss.",
        ),
        (
            "How could I help suspecting him, when I actually saw him with the\ncoronet in his hands?",
            "evidence",
            "E: Arthur holding the damaged coronet is the incriminating surface fact Holmes must explain away.",
        ),
        (
            "Arthur's silence suggests protecting someone",
            "inference",
            "INF: Arthur accepts suspicion rather than explain, which points to loyalty or guilt for another person's act.",
        ),
    ],
    "copper-beeches": [
        (
            '"To the man who loves art for its own sake," remarked Sherlock Holmes,\ntossing aside the advertisement sheet of _The Daily Telegraph_, "it is\nfrequently in its least important and lowliest manifestations that the\nkeenest pleasure is to be derived."',
            "theme",
            "TH: Holmes praises small odd cases because they display pure deduction better than famous trials.",
        ),
    ],
}


def find_span(text: str, quote: str, occurrence: int = 0) -> tuple[int, int]:
    start = 0
    idx = -1
    for _ in range(occurrence + 1):
        idx = text.find(quote, start)
        if idx == -1:
            raise ValueError(f"Quote not found (occ={occurrence}): {quote[:100]!r}")
        start = idx + 1
    return idx, idx + len(quote)


def build_annotation(text: str, item: tuple) -> dict:
    if len(item) == 4:
        quote, category, note, occ = item
    else:
        quote, category, note = item
        occ = 0
    start, end = find_span(text, quote, occ)
    return {"start": start, "end": end, "category": category, "note": note}


def main() -> int:
    data = json.loads(LIB.read_text(encoding="utf-8"))
    updated = []
    for sec in data["sections"]:
        sid = sec["id"]
        if sid not in STORY_ANNOTATIONS:
            continue
        text = sec["text"]
        anns = [build_annotation(text, item) for item in STORY_ANNOTATIONS[sid]]
        anns.sort(key=lambda a: a["start"])
        sec["annotations"] = anns
        updated.append((sid, len(anns)))
    LIB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for sid, n in updated:
        print(f"{sid}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
