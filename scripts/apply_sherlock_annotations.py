#!/usr/bin/env python3
"""Apply LLM-authored annotations to Sherlock Holmes library sections."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LIB = REPO / "content/library/002-adventures-of-sherlock-holmes.json"


def find_span(text: str, snippet: str, start_from: int = 0) -> tuple[int, int]:
    idx = text.find(snippet, start_from)
    if idx == -1:
        raise ValueError(f"Snippet not found from {start_from}: {snippet[:100]!r}")
    return idx, idx + len(snippet)


def build(text: str, items: list[tuple[str, str, str]]) -> list[dict]:
    located: list[tuple[int, str, str, str]] = []
    for snippet, category, note in items:
        start = text.find(snippet)
        if start == -1:
            raise ValueError(f"Snippet not found: {snippet[:100]!r}")
        located.append((start, snippet, category, note))
    located.sort(key=lambda item: item[0])

    anns: list[dict] = []
    search_from = 0
    for _, snippet, category, note in located:
        start = text.find(snippet, search_from)
        if start == -1:
            raise ValueError(f"Snippet not found after offset {search_from}: {snippet[:100]!r}")
        end = start + len(snippet)
        anns.append({"start": start, "end": end, "category": category, "note": note})
        search_from = start + 1
    return anns


ANNOTATIONS: dict[str, list[tuple[str, str, str]]] = {
    "scandal-in-bohemia": [
        ("To Sherlock Holmes she is always _the_ woman.", "structure", "STR: Watson opens by framing the whole case. Irene Adler is named before the plot begins, so the reader knows this story will test Holmes personally."),
        ("most perfect reasoning and observing machine that", "theme", "TH: The story's central contrast is stated early: Holmes excels at logic but rejects emotion, which makes Irene's victory more meaningful."),
        ('"You see, but you do not observe', "theme", "TH: Holmes states his method in plain terms. Observation, not mere seeing, is the rule that will drive every deduction in the case."),
        ("It is a capital mistake to theorise before one has\ndata.", "theme", "TH: Holmes repeats a core series rule: gather facts first. The masked note gives him almost no data, so he refuses to guess."),
        ("Such paper could not\nbe bought under half a crown a packet.", "evidence", "E: Watson's deduction from the note points to wealth and foreign origin. The expensive Bohemian paper supports the royal client's identity."),
        ("If this young person should\nproduce her letters for blackmailing or other purposes, how is she to\nprove their authenticity?", "inference", "INF: Holmes shows that the letters alone may not ruin the King unless Irene acts. That inference raises the stakes of what she might do next."),
        ('It is quite a pretty little problem," said he.', "tone", "TO: Holmes treats royal blackmail as an elegant puzzle. His amused tone contrasts with the King's fear."),
        ("character of a groom out of work.", "structure", "STR: Holmes shifts from talk to undercover work. The groom disguise begins the field investigation at Briony Lodge."),
        ("She lives quietly, sings at concerts, drives\nout at five every day, and returns at seven sharp for dinner.", "evidence", "E: The groom's gossip gives Holmes Irene's routine. These fixed habits become the timetable for the later wedding and fire scenes."),
        ('rocket into the room with a cry of "Fire!"', "structure", "SHIFT: The staged fire forces Irene to reveal where she hides the photograph. The scene turns from surveillance into direct trickery."),
        ('Irene Adler is married," remarked Holmes.', "structure", "SHIFT: Holmes learns Irene married Norton only yesterday. The case pivots from theft to pursuit of someone who may already have escaped."),
        ("Sherlock Holmes staggered back, white with chagrin and\nsurprise.", "tone", "TO: For once Holmes is visibly shaken. The rare loss of composure marks Irene as an opponent unlike his usual criminals."),
        ("You really did it very well", "evidence", "E: Irene's letter proves how Holmes failed and why. She names the fire, the disguises, and the coachman who watched him."),
        ('"This photograph!"', "inference", "INF: Holmes refuses money and asks for the photograph instead. We infer he values respect for Irene's mind more than royal reward."),
        ("woman's wit.", "theme", "TH: Watson closes by naming the theme: intellect defeats even Holmes when the adversary matches his nerve and foresight."),
    ],
    "case-of-identity": [
        ("life is infinitely stranger than\nanything which the mind of man could invent.", "theme", "MI: Holmes opens with the story's premise: everyday life hides plots stranger than fiction."),
        ("there is nothing so\nunnatural as the commonplace.", "theme", "TH: Holmes turns Watson's skepticism around. The case will look ordinary on the surface and prove anything but."),
        ("become of Mr. Hosmer Angel", "evidence", "E: Miss Sutherland states the problem directly: her fiancé vanished on their wedding day. Every clue must explain that disappearance."),
        ('Do you not find," he said, "that with your short sight', "inference", "INF: Holmes already knows details Miss Sutherland never told him. The reader infers he has investigated before she finished speaking."),
        ("Above all, try to let Mr. Hosmer Angel vanish from your\nmemory, as he has done from your life.", "inference", "INF: Holmes hints Hosmer will not return. His advice prepares the reader for a cruel explanation rather than a rescue."),
        ("For all the preposterous hat and the vacuous face, there was something\nnoble in the simple faith of our visitor", "tone", "TO: Watson's sympathy for Miss Sutherland adds moral weight. The tone makes the eventual fraud feel more contemptible."),
        ("a typewriter has really\nquite as much individuality as a man's handwriting.", "theme", "TH: Holmes states the method that will crack the case: mechanical writing leaves repeatable flaws, just like handwriting."),
        ("In each case, not only are the 'e's' slurred and\nthe 'r's' tailless, but you will observe, if you care to use my\nmagnifying lens, that the fourteen other characteristics to which I\nhave alluded are there as well.", "evidence", "E: Holmes compares four letters and finds matching typewriter defects. This physical proof links Hosmer Angel's notes to one machine."),
        ('"I let you know, then, that I have caught him!"', "structure", "SHIFT: Holmes stops searching for a missing man and names the culprit in the room. The story turns from mystery to exposure."),
        ("Windibank sprang out of his chair", "evidence", "E: Windibank's attempt to flee acts like a confession. His panic supports Holmes's claim before the full explanation."),
        ("The law cannot, as you say, touch you", "tone", "TO: Holmes admits Windibank escapes legal punishment, which makes his disgust feel sharper and more personal."),
        ("Hosmer\nAngel must have some strong object for his curious conduct, and it was\nequally clear that the only man who really profited by the incident, as\nfar as we could see, was the stepfather.", "inference", "INF: Holmes reconstructs the motive chain: profit, disguise, and control over Mary. Each isolated fact now supports one conclusion."),
        ("So were the tinted spectacles and the curious\nvoice, which both hinted at a disguise", "evidence", "E: Holmes lists disguise clues—voice, whiskers, spectacles—that kept Mary from recognizing her stepfather as Hosmer."),
        ("You may remember the old\nPersian saying", "theme", "TH: Holmes ends with a bleak theme: some delusions protect the heart, and exposing them may help no one."),
    ],
    "boscombe-valley-mystery": [
        ("simple\ncases which are so extremely difficult.", "theme", "TH: Holmes warns that a case can look simple and still resist solution. That paradox frames the whole Boscombe investigation."),
        ("Singularity is almost invariably a clue.", "theme", "TH: Holmes states a series rule: odd details are not distractions but signposts. The reader should treat strangeness as evidence."),
        ("The more featureless and commonplace a crime is, the more difficult it\nis to bring it home.", "inference", "INF: Holmes flips ordinary police assumptions. Because the scene looks common, only careful reading of small facts will work."),
        ("His frank acceptance of the situation marks him as\neither an innocent man, or else as a man of considerable self-restraint\nand firmness.", "inference", "INF: Holmes reads James McCarthy's behavior against expectation. A guilty man would perform surprise; James does not."),
        ('"Cooee!"', "evidence", "E: The dying man's last word is a concrete clue. Holmes later treats it as proof the meeting was not hostile on McCarthy's side."),
        ("what does the idiot do but get into the clutches of\na barmaid in Bristol and marry her at a registry office?", "evidence", "E: Holmes reveals James's secret marriage. That hidden fact explains why he could not marry Alice Turner and why he acted desperately."),
        ("screening him or her", "inference", "INF: Holmes eliminates one theory: James is not protecting the killer. That narrows the case to an outside attacker."),
        ("The impression of his right foot was always less distinct than his\nleft. He put less weight upon it. Why? Because he limped—he was lame.", "inference", "INF: Holmes turns uneven footprints into a portrait of the killer. Each physical trace builds a left-handed, lame suspect."),
        ("ash of a cigar, which my special knowledge of tobacco ashes enables\nme to pronounce as an Indian cigar.", "evidence", "E: Holmes uses cigar ash as exact proof of who waited by the pond. The detail directly ties to the visitor he expects."),
        ("The blow was struck from immediately", "evidence", "E: Holmes reads the wound location as proof of the attacker's handedness. Medical detail becomes part of the logical chain."),
        ('"Mr. John Turner," cried the hotel waiter', "structure", "SHIFT: Holmes is about to name the killer when Turner himself arrives. The scene shifts from deduction to confession."),
        ("McCarthy was the only man alive who had known dad", "evidence", "E: Turner admits a shared criminal past in Australia. That history gives him motive to kill rather than let blackmail destroy his daughter's future."),
        ("I struck him down with no more compunction than if\nhe had been some foul and venomous beast.", "inference", "INF: Turner's confession shows he acted to protect Alice, not from random rage. The reader infers the murder was a desperate shield."),
        ("Why does fate play\nsuch tricks with poor, helpless worms?", "tone", "TO: Holmes's rare moral grief softens the ending. The tone shows even he sees tragedy in justice, not only puzzle-solving."),
        ("James McCarthy was acquitted at the Assizes on the strength of a number\nof objections which had been drawn out by Holmes", "theme", "TH: Watson closes with partial mercy: Holmes saves an innocent son while keeping a dying man's secret."),
    ],
    "five-orange-pips": [
        ("have their explanations founded rather upon conjecture\nand surmise than on that absolute logical proof which was so dear to\nhim.", "structure", "STR: Watson warns that this case lacks Holmes's usual clean proof. The opening prepares the reader for an unresolved ending."),
        ("treble K which I had\nread in the morning upon the envelope.", "evidence", "E: The same K.K.K. mark appears on the envelope and the burned box. That repeated symbol links the threats into one pattern."),
        ("orange pips, which pattered down upon", "evidence", "E: The five orange pips are the story's central clue object. They announce death the same way the earlier letters did."),
        ("K. K. K.!' he shrieked", "evidence", "E: Elias Openshaw's terror names the Ku Klux Klan and ties the pips to past guilt. His reaction proves the threat is not random."),
        ("Put the papers on the sundial", "structure", "STR: Holmes lays out a plan to trap the senders by using the papers as bait. The structure moves from explanation to attempted counter-stroke."),
        ("Do not think of revenge, or anything of the sort, at present.", "inference", "INF: Holmes tells Openshaw to obey first and leave justice later. That advice shows how dangerous the unseen enemy is."),
        ("No, your secret lies in London. It is there that I shall seek it.", "inference", "INF: Holmes separates the country family from the real base of the conspiracy. The reader infers the enemy is urban and organized."),
        ("the body was eventually recovered.", "structure", "SHIFT: Watson reports John Openshaw's death. The story shifts from client rescue to Holmes's personal failure."),
        ('"That hurts my pride, Watson," he said at last.', "tone", "TO: Holmes rarely admits emotion this openly. His wounded pride shows how seriously he takes a case he did not save in time."),
        ("That he should come to me for help, and that I should send him away to\nhis death—!", "inference", "INF: Holmes blames his own advice for Openshaw's murder. The reader infers the trap worked faster than Holmes expected."),
        ("the _Lone Star_, instantly attracted my\nattention", "evidence", "E: Holmes traces the threatening letters to an American ship in Lloyd's records. The name links the pips to a concrete crew."),
        ("Oh, I have my hand upon him.", "inference", "INF: Holmes believes he can reach the killers through the mail and cable. The reader infers justice is finally within reach."),
        ("murderers of John Openshaw were never to receive the orange pips", "theme", "TH: Watson closes with unfinished justice: logic can identify guilt, but fate and storm can still defeat punishment."),
    ],
    "man-with-the-twisted-lip": [
        ("much addicted to opium", "evidence", "E: The case begins with Isa Whitney's addiction, which pulls Watson out at night. That domestic crisis leads directly to the St. Clair mystery."),
        ("It seems absurdly simple, and yet, somehow I can get nothing to\ngo upon.", "theme", "TH: Holmes admits the case resists him early. The theme is appearance versus hidden identity: everything looks simple and is not."),
        ("returning by the 5:14 from Cannon Street every night.", "evidence", "E: Neville St. Clair's steady commute creates the window of time where he vanishes. Routine becomes a clue."),
        ("opium den", "structure", "STR: Holmes takes Watson into the East End den. The setting shift moves the search from respectable Lee to London's hidden underworld."),
        ("twisted lip which had given the repulsive sneer to the face!", "evidence", "E: Mrs. St. Clair identifies the beggar by his disfigured mouth. The grotesque face is the story's title clue and first answer."),
        ("If I am Mr. Neville St. Clair, then it is obvious that no crime has\nbeen committed, and that, therefore, I am illegally detained.", "inference", "INF: St. Clair reframes the police theory. If he is alive and unharmed, the supposed murder disappears."),
        ("You would have done better to have trusted your wife.", "inference", "INF: Holmes suggests secrecy caused the crisis. The reader infers Mrs. St. Clair might have understood had he confessed sooner."),
        ("I would not have them ashamed of their father.", "tone", "TO: St. Clair's shame drives the plot more than greed does. The emotional tone explains why a respectable man chooses disguise."),
        ("One day my editor wished to\nhave a series of articles upon begging in the metropolis, and I\nvolunteered to supply them.", "evidence", "E: St. Clair explains how he first tried begging for research. That experiment led to the accidental discovery of how much money a beggar can earn."),
        ("reporter on an evening paper in London", "evidence", "E: His former profession matters: he knows observation and performance, skills that make the disguise believable."),
        ("instead of\nbeing identified as Mr. Neville St. Clair, I was arrested as his\nmurderer.", "structure", "SHIFT: St. Clair's confession explains the missing-man panic. The story turns from suspected murder to voluntary disguise."),
        ("Even a wife's eyes could not pierce so complete a disguise.", "inference", "INF: St. Clair's costume works almost perfectly. The reader infers only accident and bad luck exposed him, not careless detection."),
        ("Many times; but what was a fine to me?", "evidence", "E: St. Clair admits repeated arrests for begging. The fines were cheaper than giving up the profitable double life."),
        ('I reached this one," said my friend, "by sitting upon five pillows and\nconsuming an ounce of shag.', "tone", "TO: Holmes jokes about his method after a case built on shame and family fear. The light tone restores calm once danger passes."),
        ("we shall just be in time for breakfast.", "theme", "TH: Holmes ends on domestic normalcy after a night of opium dens and false identity. The theme is how close respectability sits to disguise."),
    ],
    "blue-carbuncle": [
        ("Christmas goose.", "theme", "T: The case begins with a lost goose, not a violent crime. The trivial object will carry the story from comedy to jewel theft."),
        ("The goose, Mr. Holmes! The goose, sir!", "structure", "STR: Peterson's excited arrival with the goose pivots the story. A comic lost bird becomes the center of the investigation."),
        ("a brilliantly\nscintillating blue stone", "evidence", "E: The carbuncle in the goose's crop turns a comic lost-property case into a major theft. This is the pivot evidence."),
        ("Not the Countess of Morcar's blue carbuncle!", "inference", "INF: Watson and Holmes connect the stone to a famous robbery. The reader infers the goose links a street quarrel to a hotel crime."),
        ("loss of a goose, all this seems to be rather a waste of energy.", "inference", "INF: Watson thinks the matter trivial just before the jewel appears. The contrast shows how wrong surface judgments can be."),
        ("though we have so\nhomely a thing as a goose at one end of this chain, we have at the\nother a man who will certainly get seven years' penal servitude", "theme", "TH: Holmes states the story's design: humble clues can lead to serious guilt. The method matters more than the opening mood."),
        ('not _our_ geese', "evidence", "E: The Alpha Inn landlord redirects Holmes to Breckinridge. Each interview narrows the path the goose traveled."),
        ("Breckinridge is his name.", "structure", "STR: The trail moves from pub to market seller. Holmes follows the goose backward through a chain of vendors."),
        ("James Ryder, upper-attendant at the hotel", "evidence", "E: Holmes names the hotel employee tied to the robbery. The goose chain finally reaches a suspect with motive and access."),
        ("How came the stone into the goose, and how came the goose\ninto the open market?", "structure", "SHIFT: Holmes stops chasing clues and demands confession. The question frames the final explanatory scene."),
        ("When Horner had been arrested", "evidence", "E: Ryder admits he stole the gem and panicked after Horner was accused. His confession supplies the missing criminal link."),
        ("there were two barred-tailed ones, and I could never tell\nthem apart.", "inference", "INF: The swapped geese explain how chance, not planning, moved the carbuncle. The absurd mix-up is the story's comic engine."),
        ("I am not retained by the police to supply their deficiencies", "theme", "TH: Holmes releases Ryder because prosecution would not recover the stone. The theme is pragmatic mercy once the puzzle is solved."),
    ],
    "speckled-band": [
        ("none commonplace; for, working as he did rather for the love of his\nart than for the acquirement of wealth", "theme", "TH: Watson frames the case as unusually dark even for Holmes. The opening tells readers to expect real danger, not a puzzle alone."),
        ("manifold wickedness of the human heart.", "tone", "TO: Helen Stoner's fear sets a gothic tone. Her language treats Holmes as a last hope against hidden evil."),
        ("fixed for the wedding, the\nterrible event occurred which has deprived me of my only companion.", "evidence", "E: Julia died just before her wedding. That timing suggests the killer feared marriage would remove her from the house."),
        ("There is no communication between\nthem, but they all open out into the same corridor.", "evidence", "E: Helen maps the bedroom layout. The corridor arrangement later makes the ventilator-and-bell-rope trap physically possible."),
        ("It was the band! The speckled band!'", "evidence", "E: Julia's dying words are the story's central clue phrase. They sound mysterious until Holmes interprets them literally."),
        ('"But have you told me all?"', "inference", "INF: Holmes presses Helen because he already suspects Dr. Roylott. His questions test whether fear is hiding facts."),
        ("An Eley's No. 2 is an excellent argument\nwith gentlemen who can twist steel pokers into knots.", "evidence", "E: Holmes arms himself because Roylott's strength is established fact. The revolver proves he expects violence, not talk."),
        ("It is a nice household", "tone", "TO: Holmes laughs at the baboon in the dark. The dry remark undercuts horror and shows his composure before the night watch."),
        ("Why, it's a dummy", "evidence", "E: Holmes discovers the bell-rope is fake and tied to the ventilator. That detail proves the room was built for murder."),
        ("sit without light. He would see it through the ventilator.", "structure", "STR: Holmes sets the trap by waiting in darkness. The final scene is structured as staged observation, not immediate arrest."),
        ('"It is a swamp adder!" cried Holmes;', "structure", "SHIFT: Holmes names the weapon at the climax. The mysterious 'speckled band' becomes a real snake on the bell-rope."),
        ("recoil upon the violent", "theme", "TH: Holmes states the moral theme: Roylott's own murder device kills him. The violent plan destroys its maker."),
        ("weigh very heavily upon my\nconscience.", "inference", "INF: Holmes accepts partial moral responsibility. The reader infers justice here is accidental rather than cleanly legal."),
    ],
    "engineers-thumb": [
        ("when the facts slowly evolve before your own eyes, and the mystery\nclears gradually away as each new discovery furnishes a step which\nleads on to the complete truth.", "structure", "STR: Watson tells readers how to experience the case: each discovery should arrive in order, not as a newspaper summary."),
        ("absolute secrecy\nis quite essential", "evidence", "E: Colonel Stark's demand for secrecy is the first warning sign. Legitimate employers rarely forbid all mention of the job."),
        ("The passage outside was empty.", "inference", "INF: Stark checks the hall after Hatherley promises silence. We infer he is staging privacy because the work is illegal."),
        ("examine the machine and to let us know what is\nwrong with it.", "evidence", "E: Hatherley is hired to inspect a hydraulic press. The machine will become the attempted-murder weapon, not a repair job."),
        ("green, unhealthy blotches", "inference", "INF: The decaying house signals danger before the trap springs. Setting details warn that the job is not ordinary business."),
        ("with a force which must\nwithin a minute grind me to a shapeless pulp.", "structure", "SHIFT: The closing press turns the repair job into attempted murder. The story's danger becomes physical and immediate."),
        ("my thumb had been cut off and that the blood was pouring", "evidence", "E: Hatherley's mutilation gives the case its title and proves the villains wanted silence, not just labor."),
        ("That circle is drawn at a radius of ten\nmiles from the village.", "evidence", "E: Holmes maps the carriage radius to locate the hideout. Geometry turns confused memory into a searchable area."),
        ("Six out and six back. Nothing simpler.", "inference", "INF: Holmes proves the carriage distance was half what Hatherley thought. That calculation locates the real house within walking distance."),
        ("This is where we shall find them.", "inference", "INF: Holmes places the gang at the center of the radius, not along the roads Hatherley remembers. Memory under anesthesia misled everyone else."),
        ("crushed in the press, set fire to the wooden walls", "evidence", "E: Holmes reads the fire as accidental revenge from the broken lamp. Physical evidence closes the loop on the trap house."),
        ('Experience," said Holmes, laughing', "theme", "TH: Holmes ends with dry humor after horror and loss. The theme is that even painful cases can become lessons in observation."),
    ],
    "noble-bachelor": [
        ("The Lord St. Simon marriage, and its curious termination", "structure", "STR: Watson announces a social scandal already fading from gossip. The opening frames a mystery about disappearance, not murder."),
        ("It is just possible, however, that that also may not be wanting in this\nnew investigation.", "inference", "INF: Holmes hints the noble title is less important than the puzzle itself. Class spectacle may distract from simpler facts."),
        ("Hatty Doran, the only daughter of\nAloysius Doran.", "evidence", "E: The bride's American name and mining fortune explain why London society cares. Money and status drive the marriage plot."),
        ("witness, if only as a check to my own\nmemory.", "tone", "TO: Holmes wants Watson present for social cases too. The remark shows how carefully he documents unusual behavior."),
        ("Because you have just as good a chance of finding this lady in the one\nas in the other.", "inference", "INF: Holmes rejects the police theory that disappearance equals death. The reader should look for voluntary flight instead."),
        ("Flora Millar, the lady who had caused the disturbance", "evidence", "E: Flora's public quarrel ties her to the wedding morning. She becomes an early suspect because of social conflict, not murder."),
        ("I saw it in a paper", "evidence", "E: Francis M. Norton says he learned the wedding from a newspaper. That public notice enabled the old lover to reappear."),
        ("Frank took my wedding-clothes and\nthings and made a bundle of them", "structure", "SHIFT: Hatty explains she fled with her former husband. The missing bride reappears through confession, not rescue."),
        ("I was wrong and that Frank was right", "theme", "TH: Hatty states the moral choice: she prefers an honest past love to a noble marriage built on rank and money."),
        ("intimate personal affairs in this public manner.", "tone", "TO: Lord St. Simon's cold reply shows wounded pride more than affection. The tone reveals why the marriage failed socially, not criminally."),
        ("perhaps you would not be very\ngracious either, if, after all the trouble of wooing and wedding, you\nfound yourself deprived in an instant of wife and of fortune.", "inference", "INF: Holmes asks Watson to read St. Simon with sympathy. The reader infers the scandal is social embarrassment, not crime."),
        ("the only problem we have still\nto solve is how to while away these bleak autumnal evenings.", "theme", "TH: Holmes ends lightly after a case with no villain. The theme is that some mysteries dissolve into human choice, not prosecution."),
    ],
    "beryl-coronet": [
        ("here is a madman coming along", "tone", "TO: Watson first reads Holder as madness, not distress. The opening tone shows how extreme grief can look like insanity."),
        ("Beryl Coronet?'", "theme", "T: The title jewel names the object everyone will chase. A royal loan worth far more than money concentrates every character's motive."),
        ("She is my right hand. I do not know what I could do without her.", "evidence", "E: Holder praises Mary so highly that the reader stores her as trustworthy. That setup makes the later accusation against Arthur sharper."),
        ("Oh, any old key will fit that bureau.", "inference", "INF: Arthur's casual remark about the bureau suggests weak security. We infer the coronet was never as safe as Holder believed."),
        ("I saw Arthur with the coronet\nin his hands", "evidence", "E: Holder's eyewitness report is the strongest apparent proof against his son. The case turns on interpreting that moment."),
        ("infer that she may have gone out to tell her sweetheart", "inference", "INF: Holmes tests a theory about the maid and her lover. Even false paths show how he reads household relationships."),
        ("And he is a man with a wooden leg?", "evidence", "E: Holmes extracts the wooden-leg detail from footprints in snow. That physical fact redirects blame away from Arthur alone."),
        ("Why, you are like a magician", "tone", "TO: Mary's shock at Holmes's deductions adds suspense. The tone marks him closing in on hidden knowledge she did not expect exposed."),
        ("your son, finding that he had the coronet in his\nhands, rushed back", "inference", "INF: Holmes reconstructs Arthur's act as rescue, not robbery. The same visual evidence supports opposite moral readings."),
        ("He took the more chivalrous\nview, however, and preserved her secret.", "theme", "TH: Holmes names the story's moral center: Arthur protected Mary instead of clearing himself, and his father misread silence as guilt."),
        ("what a blind fool I have been!", "tone", "TO: Holder's remorse shifts the emotional tone from accusation to reconciliation. The father finally reads character correctly."),
        ("went in the shape of a loafer to Sir George's house", "structure", "STR: Holmes reopens the case through undercover work outdoors. The structure moves from indoor panic to physical reconstruction."),
        ("You may go to any expense which you think necessary.", "evidence", "E: Holmes buys cast-off shoes and pays informants. The case is solved partly by quiet expense, not only by deduction in the parlor."),
        ("A day which has saved England from a great public scandal", "theme", "TH: Holder's gratitude states the stakes: family honor and national reputation, not just a missing gem."),
    ],
    "copper-beeches": [
        ("Crime is common. Logic is rare.", "theme", "TH: Holmes states the collection's ethic again: readers should watch reasoning, not sensational crime alone."),
        ("The Copper Beeches", "theme", "T: The house name becomes the story's destination and symbol. A pleasant country home will hide imprisonment and fraud."),
        ("I must remain firm upon this", "evidence", "E: Rucastle insists Violet Hunter cut her hair. That demand begins the pattern of making her resemble someone else."),
        ("sister of mine apply for.", "inference", "INF: Holmes warns Miss Hunter despite approving her choice. The reader infers danger from the salary and odd rules together."),
        ("I concealed a piece of the glass in my handkerchief.", "structure", "STR: Violet uses a mirror trick to spy behind her. The investigation structure gives the client agency, not only Holmes."),
        ("there was a man standing in the Southampton\nRoad, a small bearded man in a grey suit, who seemed to be looking in\nmy direction.", "evidence", "E: Violet sees a watcher outside while she reads by the window. That surveillance links the house to someone beyond the family."),
        ("She said nothing, but I am convinced\nthat she had divined that I had a mirror in my hand", "inference", "INF: Mrs. Rucastle notices Violet's trick without speaking. We infer the household constantly monitors her behavior."),
        ("imprisoned in this chamber.\nThat is obvious. As to who this prisoner is, I have no doubt that it is\nthe daughter, Miss Alice Rucastle", "inference", "INF: Holmes deduces Alice is the prisoner from Violet's observations. The missing daughter and copied appearance now connect."),
        ("Carlo, my mastiff.", "evidence", "E: The mastiff's behavior shows Alice still lives nearby. The dog's loyalty supports the secret-captive theory."),
        ("Mr. Rucastle then, I presume, took to this system of\nimprisonment?", "evidence", "E: Holmes explains Rucastle kept Alice isolated to control her fortune and marriage. The motive turns family cruelty into plot."),
        ("Have you managed it?", "structure", "SHIFT: Holmes arrives for the rescue at dusk. The story shifts from Violet's undercover observations to direct action."),
        ("prisoner gone.", "structure", "SHIFT: The locked room is empty. The climax immediately complicates the rescue with a new flight through the skylight."),
        ('"I have my revolver," said I.', "evidence", "E: The rescue turns violent when Rucastle releases the dog. Holmes and Watson must act physically, not only deduce."),
        ("And thus was solved the mystery of the sinister house with the copper\nbeeches in front of the door.", "theme", "TH: Watson closes by naming the solved mystery and its human cost. Logic plus client courage broke a household built on control."),
    ],
}


def apply() -> None:
    data = json.loads(LIB.read_text(encoding="utf-8"))
    for sec in data["sections"]:
        sid = sec["id"]
        if sid not in ANNOTATIONS:
            continue
        sec["annotations"] = build(sec["text"], ANNOTATIONS[sid])
        print(f"{sid}: {len(sec['annotations'])} annotations")
    LIB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    apply()
