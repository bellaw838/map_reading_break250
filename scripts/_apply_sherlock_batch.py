#!/usr/bin/env python3
"""Apply LLM-authored annotations to 11 Sherlock stories (not red-headed-league)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LIB = REPO / "content/library/002-adventures-of-sherlock-holmes.json"

OFFICIAL = re.compile(r"^(T:|MI:|TH:|E:|RSN:|INF:|TO:|M:|WC:|STR:|PF:|SHIFT:)")

STORY_ANNOTATIONS: dict[str, list[tuple[str, str, str]]] = {
    "scandal-in-bohemia": [
        (
            "To Sherlock Holmes she is always _the_ woman.",
            "structure",
            "STR: Watson opens by naming Irene Adler before the plot begins, so the reader knows this case will test Holmes personally rather than follow a routine puzzle.",
        ),
        (
            "the most perfect reasoning and observing machine that",
            "theme",
            "TH: Holmes is defined as pure logic without love, which makes Irene's later victory a challenge to his whole method, not just a lost case.",
        ),
        (
            "You see, but you do not observe.",
            "theme",
            "TH: Holmes states the story's method in plain terms: careful observation, not casual seeing, will drive every deduction in the case.",
        ),
        (
            "It is a capital mistake to theorise before one has\ndata.",
            "evidence",
            "E: Holmes refuses to guess about the masked note until he has facts, proving that even urgent royal business must wait on evidence.",
        ),
        (
            "Such paper could not\nbe bought under half a crown a packet.",
            "evidence",
            "E: Watson's deduction from the expensive Bohemian paper supports the idea that the client is wealthy and foreign, which fits the King in disguise.",
        ),
        (
            "European history.",
            "theme",
            "TH: The King frames the stakes as dynastic scandal and a threatened royal marriage, so the photograph is a political weapon, not a private grudge.",
        ),
        (
            "If this young person should\nproduce her letters for blackmailing or other purposes, how is she to\nprove their authentici",
            "inference",
            "INF: Holmes shows that the letters alone may not ruin the King unless Irene acts, which raises the real question of what she plans to do with the photograph.",
        ),
        (
            "It is quite a pretty little problem,\" said he.",
            "tone",
            "TO: Holmes treats royal blackmail as an elegant puzzle, and his amused tone contrasts sharply with the King's fear.",
        ),
        (
            "character of a groom out of work.",
            "structure",
            "STR: Holmes shifts from talk to undercover work; the groom disguise begins the field investigation at Briony Lodge.",
        ),
        (
            "She lives quietly, sings at concerts, drives\nout at five every day, and returns at seven sharp for dinner.",
            "evidence",
            "E: The groom's gossip gives Holmes Irene's fixed routine, which becomes the timetable for the wedding rush and the evening trap.",
        ),
        (
            "secure tying up of Irene Adler, spinster, to Godfrey Norton,\nbachelor.",
            "structure",
            "SHIFT: Holmes is pulled into an emergency wedding, and the case pivots when Irene marries Norton before Holmes can recover the photograph.",
        ),
        (
            "raise the cry of fire.",
            "structure",
            "STR: Holmes plans a staged fire to force Irene to reveal where she hides the photograph, turning surveillance into direct trickery.",
        ),
        (
            "When a woman thinks that her house is on fire,\nher instinct is at once to rush to the thing which she values most.",
            "evidence",
            "RSN: Holmes explains why the false alarm works: panic makes Irene expose the hiding place, linking the trick to human instinct rather than luck.",
        ),
        (
            "Irene Adler is married,\" remarked Holmes.",
            "structure",
            "SHIFT: Holmes learns Irene married Norton only yesterday, so the chase shifts from theft to pursuit of someone who may already have escaped.",
        ),
        (
            "Sherlock Holmes staggered back, white with chagrin and\nsurprise.",
            "tone",
            "TO: For once Holmes is visibly shaken; the rare loss of composure marks Irene as an opponent unlike his usual criminals.",
        ),
        (
            "You really did it very well",
            "evidence",
            "E: Irene's letter proves how Holmes failed and why: she names the fire, the disguises, and the coachman who watched him.",
        ),
        (
            "woman's wit.",
            "theme",
            "TH: Watson closes by naming the theme: intellect and nerve can defeat even Holmes when the adversary matches his foresight.",
        ),
    ],
    "case-of-identity": [
        (
            "life is infinitely stranger than\nanything which the mind of man could invent.",
            "theme",
            "MI: Holmes opens with the story's premise: everyday life hides plots stranger than fiction if one knows where to look.",
        ),
        (
            "there is nothing so\nunnatural as the commonplace.",
            "theme",
            "TH: Holmes turns Watson's skepticism around: the case will look ordinary on the surface but prove anything but common.",
        ),
        (
            "Oscillation upon the pavement always means an\n_affaire de cœur_.",
            "inference",
            "INF: Holmes reads Miss Sutherland's nervous pacing as a love problem, not anger, before she speaks a word.",
        ),
        (
            "trying to do so much typewriting?",
            "evidence",
            "E: Holmes deduces typewriting before Miss Sutherland explains her work, showing how small physical marks can prove a client's daily habits.",
        ),
        (
            "there was no one there! The cabman said that he could not\nimagine what had become of him",
            "evidence",
            "E: Hosmer Angel vanishes from the wedding cab; this is the central mystery event that every later clue must explain.",
        ),
        (
            "was always to remember that I was pledged to him, and that he would\nclaim his pledge sooner or later",
            "evidence",
            "E: Hosmer's strange vows on the wedding morning suggest he planned a permanent break, not a sudden accident.",
        ),
        (
            "the signature is typewritten. Look at the neat\nlittle 'Hosmer Angel' at the bottom.",
            "evidence",
            "E: A typewritten signature is the first strong proof that Hosmer Angel is a disguise, because a real suitor would sign by hand.",
        ),
        (
            "I let you know, then, that I have caught him!",
            "structure",
            "STR: Holmes locks the door and springs the trap, shifting the scene from interview to confrontation with Windibank.",
        ),
        (
            "as cruel and selfish and heartless a trick in a petty\nway as ever came before me.",
            "theme",
            "TH: Holmes names the motive: Windibank staged a fake romance to keep his stepdaughter's income and prevent her marrying anyone else.",
        ),
        (
            "disguised himself, covered those keen eyes with tinted glasses, masked\nthe face with a moustache and a pair of bushy whiskers",
            "structure",
            "STR: Holmes reconstructs the full hoax: Windibank played Hosmer Angel himself, which explains why the two men were never seen together.",
        ),
        (
            "stepping in at one door of a four-wheeler and out at the other.",
            "inference",
            "INF: Holmes explains the vanishing trick at the church, completing the chain from disguise to staged disappearance.",
        ),
        (
            "There's a cold-blooded scoundrel!",
            "tone",
            "TO: Holmes' amused contempt turns to open rage when Windibank escapes legal punishment, showing how much the cruelty disgusts him.",
        ),
        (
            "whoso snatches a delusion from a woman.",
            "theme",
            "TH: Holmes decides not to tell Mary the truth, closing on the theme that some comforting illusions are too painful to destroy.",
        ),
    ],
    "boscombe-valley-mystery": [
        (
            "Singularity is almost invariably a clue.",
            "theme",
            "TH: Holmes states a series rule: odd details are not distractions but signposts, especially when a case looks deceptively simple.",
        ),
        (
            "they have established a\nvery serious case against the son of the murdered man.",
            "evidence",
            "E: The official case already points at James McCarthy, so Holmes must work against a seemingly obvious suspect.",
        ),
        (
            "The men had\nknown each other in the colonies",
            "theme",
            "TH: The Australia connection hints that colonial past guilt, not present quarrel alone, may explain the murder.",
        ),
        (
            "which may have been by no means obvious to Mr. Lestrade",
            "inference",
            "INF: Holmes flips ordinary police assumptions: because the scene looks common, officers miss what a careful reader should question.",
        ),
        (
            "McCarthy the elder using\nvery strong language",
            "evidence",
            "E: Witnesses report a violent quarrel at the pool, establishing time, place, and tone of the meeting that ended in death.",
        ),
        (
            "BALLARAT.",
            "evidence",
            "E: Holmes finds the unfinished word on the ground, linking the dying man's message to the Australian past shared by Turner and McCarthy.",
        ),
        (
            "person whom McCarthy expected to meet him\nat Boscombe Pool",
            "inference",
            "INF: Holmes infers McCarthy came to the pool by appointment, so the killer was someone he knew and waited for.",
        ),
        (
            "clearing James McCarthy,\" said Holmes.",
            "structure",
            "SHIFT: Holmes announces he can exonerate the son, shifting the investigation from proving guilt to uncovering hidden history.",
        ),
        (
            "Turner, of the Hall, is so ill that his life is despaired of.",
            "structure",
            "SHIFT: Turner's approaching death forces the hidden confession before the trial, tightening the story's clock.",
        ),
        (
            "He was a devil incarnate.",
            "evidence",
            "E: Turner's confession reveals the old blackmail: McCarthy knew a colonial crime and used it to extort money and force a marriage.",
        ),
        (
            "have his cursed stock mixed with mine",
            "theme",
            "TH: The murder grows from class pride and old guilt: Turner killed to stop his daughter marrying McCarthy's son after years of extortion.",
        ),
        (
            "I am afraid that my colleague has\nbeen a little quick in forming his conclusions",
            "tone",
            "TO: Holmes' dry mockery of Lestrade shows his contempt for conclusions drawn too quickly from surface evidence.",
        ),
    ],
    "five-orange-pips": [
        (
            "points in\nconnection with it which never have been, and probably never will be,\nentirely cleared up.",
            "structure",
            "STR: Watson warns that this case lacks Holmes's usual clean proof, preparing the reader for justice deferred.",
        ),
        (
            "five little dried orange pips, which pattered down upon",
            "evidence",
            "E: The five orange pips are the story's central clue object; they announce death before any explanation arrives.",
        ),
        (
            "'K. K. K.!' he shrieked",
            "evidence",
            "E: Elias Openshaw's terror names the Ku Klux Klan and ties the pips to past guilt, not random malice.",
        ),
        (
            "It is K. K. K.,' said I.",
            "inference",
            "INF: The initials connect the warning to a secret society, so the reader infers organized revenge rather than a local crime.",
        ),
        (
            "Ku Klux Klan.",
            "evidence",
            "E: Holmes' encyclopedia entry explains the Klan's methods, proving how pips functioned as a death summons in the American past.",
        ),
        (
            "sailing-ship.",
            "structure",
            "STR: Holmes traces the warnings to a vessel, shifting the search from London rooms to men who can only strike by mail and sea.",
        ),
        (
            "K. K. K. ceases to be",
            "inference",
            "RSN: Holmes reasons that if he finds the ship he finds the senders, because the society uses the same delivery route for every warning.",
        ),
        (
            "wind cried and sobbed like a\nchild in the chimney.",
            "tone",
            "M: The storm outside mirrors the case's dread and creates a gloomy mood before the client even tells his story.",
        ),
        (
            "John Openshaw, and whose",
            "structure",
            "SHIFT: Openshaw's death ends the active case before Holmes can intercept the ship, turning triumph into failure.",
        ),
        (
            "murderers of John Openshaw were never to receive the orange pips which",
            "theme",
            "TH: Holmes fails to save Openshaw or punish the killers in time, so the theme becomes justice delayed and incomplete.",
        ),
        (
            "beaten four times",
            "inference",
            "INF: Holmes' rare admission of defeat lets the reader infer how deeply this failure wounds his pride.",
        ),
    ],
    "man-with-the-twisted-lip": [
        (
            "much addicted to opium.",
            "evidence",
            "E: The case begins with Isa Whitney's addiction, which pulls Watson into the East End at night and leads him to Holmes in disguise.",
        ),
        (
            "opium den in the farthest",
            "structure",
            "STR: Holmes takes Watson into the opium den, and the setting shift moves the search from respectable home to hidden underworld.",
        ),
        (
            "murder-trap on the whole riverside, and I fear that Neville St. Clair",
            "theme",
            "TH: The story's puzzle is appearance versus disappearance: a respectable family man seems to have been swallowed by a criminal den.",
        ),
        (
            "clothes of Mr. Neville St. Clair, with the exception of his coat.",
            "evidence",
            "E: St. Clair's clothes in the den without his body suggest either murder or a deliberate change of identity.",
        ),
        (
            "blood were to be seen upon the windowsill, and",
            "inference",
            "INF: The blood points to violence, but Holmes will show it can also fit a hidden escape rather than death.",
        ),
        (
            "Let me introduce you,\" he shouted, \"to Mr. Neville St. Clair, of Lee,",
            "structure",
            "SHIFT: Holmes reveals St. Clair alive in the same room, pivoting the case from suspected murder to explained disappearance.",
        ),
        (
            "twisted lip which had given the repulsive sneer to the face!",
            "evidence",
            "E: The twisted lip links the beggar Boone to Neville St. Clair, proving one man has been living two identities.",
        ),
        (
            "professional beggar, though in order to\navoid the police regulations he pretends to a small trade in wax\nvestas.",
            "theme",
            "TH: St. Clair confesses he begged in disguise because it paid far more than honest office work, so respectability hid economic desperation.",
        ),
        (
            "Even a wife's eyes could not pierce so complete a disguise.",
            "inference",
            "INF: St. Clair's own account shows how thoroughly performance can hide truth even from intimate observers.",
        ),
        (
            "If I am Mr. Neville St. Clair, then it is obvious that no crime has",
            "tone",
            "TO: St. Clair's calm claim that no real crime occurred sets a relieved, explanatory tone after the case's dark opening.",
        ),
    ],
    "blue-carbuncle": [
        (
            "The matter is a perfectly trivial one",
            "theme",
            "T: The case begins with a lost goose, not a violent crime; the trivial object will lead to a royal jewel.",
        ),
        (
            "No, no. No crime,\" said Sherlock Holmes, laughing.",
            "inference",
            "INF: Watson expects a deadly story, but Holmes denies crime at the start; the contrast prepares the reader for a comic-to-serious turn.",
        ),
        (
            "See what my wife found in its crop!",
            "structure",
            "SHIFT: Peterson's excited arrival with the goose pivots the story from a comic lost-bird puzzle to a major theft.",
        ),
        (
            "Not the Countess of Morcar's blue carbuncle!",
            "evidence",
            "E: The stolen gem names the real stakes and connects the goose to a recent hotel robbery.",
        ),
        (
            "from a rifled jewel-case at one end to the crop of a\ngoose in Tottenham Court Road at the other.",
            "structure",
            "STR: Holmes maps the chain he must follow, showing how the story will move from luxury crime to street-level clue.",
        ),
        (
            "instituted a goose club",
            "evidence",
            "E: The goose club trail gives Holmes a practical path from Baker's bird back through sellers to the thief.",
        ),
        (
            "my real name is James Ryder.",
            "inference",
            "INF: The nervous man at the goose seller reveals himself under pressure, confirming Holmes' suspicion of the hotel attendant.",
        ),
        (
            "The game's up, Ryder,\" said Holmes quietly.",
            "structure",
            "STR: Holmes confronts Ryder with the stone, moving the story into confession and explanation.",
        ),
        (
            "I would take my goose now, and in it I would carry my",
            "evidence",
            "E: Ryder explains how he hid the carbuncle inside a goose, supplying the missing link between theft and Peterson's bird.",
        ),
        (
            "Sold out of geese, I see,\" continued Holmes, pointing at the bare",
            "inference",
            "INF: Holmes uses the empty coop to pressure Breckinridge, showing how a small commercial detail can break open the goose chain.",
        ),
        (
            "commuting a felony",
            "tone",
            "TO: Holmes lets Ryder flee rather than face prison, giving the ending a merciful tone unusual for a jewel thief.",
        ),
    ],
    "speckled-band": [
        (
            "none commonplace; for, working as he did rather for the love of his\nart than for the acquirement of wealth",
            "theme",
            "TH: Watson frames the case as unusually dark even for Holmes, telling the reader to expect gothic danger, not a polite puzzle.",
        ),
        (
            "It is fear, Mr. Holmes. It is terror.",
            "tone",
            "TO: Helen Stoner's language sets a gothic tone and treats Holmes as a last refuge from something she cannot name safely.",
        ),
        (
            "within\na fortnight of the day which had been fixed for the wedding, the",
            "evidence",
            "E: Julia died just before her wedding, so the timing suggests the killer feared marriage would remove her from the house.",
        ),
        (
            "It was the band! The speckled band!",
            "evidence",
            "E: Julia's dying words supply the story's central clue phrase, which Holmes must decode literally rather than figuratively.",
        ),
        (
            "You are screening your stepfather.",
            "inference",
            "INF: Holmes sees Helen protecting Roylott, so the reader infers the danger lies inside the family home, not outside it.",
        ),
        (
            "bell-ropes, and ventilators which do not ventilate.",
            "structure",
            "STR: Holmes lists fake fixtures in the house, signaling that the building itself is the murder weapon.",
        ),
        (
            "We must sit without light. He would see it through the ventilator.",
            "structure",
            "STR: The night vigil begins; Holmes turns the sisters' bedroom into a trap and waits for the killer's method to reappear.",
        ),
        (
            "low, clear whistle, but the sudden glare flashing into my weary eyes",
            "structure",
            "SHIFT: The whistle and lamp light mark the attack moment, confirming Holmes' prediction that the ventilator is the entry point.",
        ),
        (
            "It is a swamp adder!",
            "evidence",
            "E: Holmes identifies the snake, turning the 'speckled band' from metaphor to literal cause of death.",
        ),
        (
            "The idea of a snake instantly occurred to me",
            "inference",
            "RSN: Holmes walks through the clue chain—whistle, ventilator, milk, safe—to show how each odd detail pointed to a trained snake.",
        ),
        (
            "indirectly responsible for Dr. Grimesby Roylott's\ndeath",
            "theme",
            "TH: Holmes closes by accepting moral responsibility for Roylott's death, so the story's cost is not only solved mystery but human consequence.",
        ),
    ],
    "engineers-thumb": [
        (
            "the lapse of two years has hardly served\nto weaken the effect",
            "structure",
            "STR: Watson tells readers how to experience the case: each discovery should arrive with shock because he withholds the outcome at first.",
        ),
        (
            "absolute secrecy\nis quite essential",
            "evidence",
            "E: Colonel Stark's demand for secrecy is the first warning sign; legitimate employers do not isolate engineers in hidden houses.",
        ),
        (
            "pressing my hand in a cold, dank grasp",
            "inference",
            "INF: Stark's cold, damp handshake and furtive manner suggest an unhealthy, hidden operation rather than ordinary repair work.",
        ),
        (
            "'we have our own process. We compress the",
            "evidence",
            "E: Stark's vague explanation of the press hints at illegal metal work, preparing the reader for counterfeiting rather than factory repair.",
        ),
        (
            "actually within the hydraulic press, and it\nwould be a particularly unpleasant thing for us if anyone were to turn\nit on",
            "evidence",
            "E: Hatherley is trapped inside the press, the story's physical climax and proof that the employers mean to kill him.",
        ),
        (
            "my thumb had been cut off",
            "structure",
            "SHIFT: Hatherley's escape with a severed thumb turns the tale from suspicious job to violent crime and pursuit.",
        ),
        (
            "your oil-lamp which, when it was\ncrushed in the press, set fire to the wooden walls",
            "evidence",
            "E: Holmes explains the fire as evidence destruction: the lamp burst in the press and burned the counterfeiting site.",
        ),
        (
            "human thumb upon a window-sill of the second floor.",
            "inference",
            "INF: The bloody thumb found by firemen corroborates Hatherley's story and shows how close he came to being crushed.",
        ),
        (
            "Colonel Lysander Stark sprang out",
            "inference",
            "INF: The name and setup are fake; the laundered labels and hidden press identify a temporary counterfeiting den, not a real colonel's home.",
        ),
        (
            "I have lost a fifty-guinea fee, and what have I gained?",
            "tone",
            "TO: Holmes ends with wry acceptance of unpaid work, giving the story a rueful tone after violent adventure.",
        ),
    ],
    "noble-bachelor": [
        (
            "The Lord St. Simon marriage, and its curious termination, have long\nceased to be a subject of interest",
            "structure",
            "STR: Watson announces a faded social scandal, framing the case as manners and reputation rather than violent crime.",
        ),
        (
            "Miss Hatty Doran, the only daughter of\nAloysius Doran",
            "evidence",
            "E: The bride's American name and mining fortune explain why London society cares about the match and why fortune hunters gather.",
        ),
        (
            "Flora Millar, the lady who had caused the disturbance",
            "inference",
            "INF: Holmes hints that the ex-mistress is too obvious a suspect, steering the reader away from the first apparent explanation.",
        ),
        (
            "She walked into the breakfast-room.",
            "evidence",
            "E: Hatty enters breakfast normally before vanishing, so the mystery is sudden choice, not struggle or abduction.",
        ),
        (
            "This dress does implicate Miss Flora Millar.",
            "structure",
            "STR: Holmes uses the abandoned dress to test police theory, showing how a clue can point convincingly to the wrong person.",
        ),
        (
            "allow me to introduce you to Mr. and Mrs.\nFrancis Hay Moulton.",
            "structure",
            "SHIFT: The missing bride reappears with her first husband alive, pivoting the case from kidnapping to prior marriage.",
        ),
        (
            "Frank was really dead. Then Lord St. Simon came to 'Frisco",
            "theme",
            "TH: Hatty explains she believed her first husband dead and would have kept the noble marriage if Frank had not returned.",
        ),
        (
            "process of exclusion, at the idea that she might have seen an American.",
            "inference",
            "INF: Holmes narrows the cause of Hatty's change of mind to a prior American tie, which leads logically to Frank Moulton.",
        ),
        (
            "we may judge Lord St. Simon very mercifully",
            "theme",
            "TH: Holmes closes by reframing the 'curious termination' as human complication rather than crime, urging sympathy over gossip.",
        ),
    ],
    "beryl-coronet": [
        (
            "here is a madman coming along",
            "tone",
            "TO: Watson first reads Holder as madness, not distress; the opening tone shows how extreme wealth and fear can look like insanity.",
        ),
        (
            "Beryl Coronet?",
            "theme",
            "T: The beryll coronet's name and value define the object everyone will chase and explain why Holder accepts such dangerous responsibility.",
        ),
        (
            "my little Mary, who has a woman's quick insight",
            "evidence",
            "E: Holder praises Mary so highly that the reader stores her as trustworthy, which makes Holmes' later reversal more surprising.",
        ),
        (
            "you villain! you thief! How dare you touch that\ncoronet?",
            "evidence",
            "E: Holder catches Arthur with the damaged coronet, creating the obvious but misleading appearance of guilt.",
        ),
        (
            "Arthur's. Sir George Burnwell has been several times lately.",
            "inference",
            "INF: Holmes notices Burnwell's visits and Arthur's shoes, inferring that the noble thief, not the son, fits the physical evidence.",
        ),
        (
            "three gems",
            "evidence",
            "E: The broken corner proves force was used, letting Holmes test whether Arthur could have snapped the setting without noise.",
        ),
        (
            "Burnwell and your niece Mary. They have now fled together.",
            "structure",
            "SHIFT: Holmes reveals Mary as conspirator, pivoting the case from fraternal theft to lover betrayal.",
        ),
        (
            "My Mary? Impossible!",
            "tone",
            "TO: Holder's shock captures the emotional cost of the solution: the people he trusted most engineered the crime.",
        ),
        (
            "Arthur caught\nhim, and there was a struggle between them",
            "evidence",
            "E: Arthur fought Burnwell to protect the coronet, so his possession of the jewels proves bravery and misunderstanding, not theft.",
        ),
        (
            "what a blind fool I have been",
            "theme",
            "TH: Holder's anguished self-reproach shows how trust in Mary blinded him, reinforcing the story's warning about misplaced confidence.",
        ),
    ],
    "copper-beeches": [
        (
            "deduction and of logical synthesis which I have made my special\nprovince.",
            "theme",
            "TH: Holmes states the collection's ethic again: readers should watch reasoning, because trivial job conditions may hide a crime.",
        ),
        (
            "Copper Beeches, five miles on\nthe far side of Winchester.",
            "theme",
            "T: The house name becomes the story's destination and symbol: a pleasant country home masking imprisonment and control.",
        ),
        (
            "Or to cut your hair quite short before you come to us?",
            "evidence",
            "E: Rucastle insists Violet Hunter cut her hair, beginning the pattern of odd demands that mimic his imprisoned stepdaughter.",
        ),
        (
            "leaned back in his chair and laughed\nhis eyes into his head again.",
            "evidence",
            "E: Rucastle laughs at the idea of a child who whips her nurse, an early clue that cruelty runs in the household.",
        ),
        (
            "was my coil of hair.",
            "inference",
            "INF: Violet finds her own hair locked in a drawer, inferring someone is impersonating her or the missing daughter.",
        ),
        (
            "Miss Alice Rucastle, if I remember right, who was said to\nhave gone to America",
            "inference",
            "INF: Holmes connects the cut hair, locked room, and cruel child to Alice, inferring she is a prisoner, not an emigrant.",
        ),
        (
            "abnormally cruel, merely for cruelty's\nsake",
            "inference",
            "RSN: Holmes argues from the child's cruelty to the parents' character, showing how family behavior exposes the household's real nature.",
        ),
        (
            "at the Copper Beeches by seven o'clock, my friend and I.",
            "structure",
            "STR: Holmes plans the rescue for the evening when the Rucastles leave, structuring the climax as a timed break-in.",
        ),
        (
            "Someone has loosed the dog.",
            "structure",
            "SHIFT: Toller releases the mastiff, turning the rescue into immediate physical danger.",
        ),
        (
            "Mr. Rucastle survived, but was always a\nbroken man",
            "theme",
            "TH: The ending shows the cost of control: Rucastle is ruined, Alice freed, and Violet saved because Holmes read the job's odd terms as evidence.",
        ),
    ],
}


def find_span(text: str, snippet: str, start_from: int = 0) -> tuple[int, int]:
    idx = text.find(snippet, start_from)
    if idx == -1:
        raise ValueError(f"Snippet not found: {snippet[:80]!r}...")
    return idx, idx + len(snippet)


def build_annotations(text: str, items: list[tuple[str, str, str]]) -> list[dict]:
    anns: list[dict] = []
    for snippet, category, note in items:
        start, end = find_span(text, snippet, 0)
        if not OFFICIAL.match(note):
            raise ValueError(f"Bad note prefix: {note[:40]!r}")
        anns.append({"start": start, "end": end, "category": category, "note": note})
    anns.sort(key=lambda x: x["start"])
    return anns


def main() -> None:
    data = json.loads(LIB.read_text(encoding="utf-8"))
    skip = {"red-headed-league"}
    updated: dict[str, int] = {}

    for sec in data["sections"]:
        sid = sec["id"]
        if sid not in STORY_ANNOTATIONS:
            if sid not in skip:
                print(f"WARN: no annotations defined for {sid}", file=sys.stderr)
            continue
        text = sec["text"]
        anns = build_annotations(text, STORY_ANNOTATIONS[sid])
        sec["annotations"] = anns
        updated[sid] = len(anns)
        print(f"Patched {sid}: {len(anns)} annotations")

    LIB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\nCounts:")
    for sid, count in updated.items():
        print(f"  {sid}: {count}")


if __name__ == "__main__":
    main()
