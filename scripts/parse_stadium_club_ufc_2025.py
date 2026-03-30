"""
Parser for 2025 Topps Stadium Club UFC.

sport: MMA, league: UFC, season: 2025
Team is None for all fighters (MMA has no teams).
RC-tagged fighters: strip " RC" from name, set is_rookie=True.
Co-Signers: dual-auto cards, split by " / " into co_players.
Triumvirates: 18 cards with 3 entries per fighter.
"""

from __future__ import annotations
import json

SET_NAME = "2025 Topps Stadium Club UFC"
SPORT = "MMA"
SEASON = "2025"
LEAGUE = "UFC"

# ── Name normalization ────────────────────────────────────────────────────────
# Canonical forms (no diacritics) so base/chrome/auto entries merge correctly.

NAME_FIXES = {
    "ariane da silva": "Ariane da Silva",
    "jose aldo": "Jose Aldo",
    "jan blachowicz": "Jan Blachowicz",
    "yair rodriguez": "Yair Rodriguez",
    "mateusz rebecki": "Mateusz Rebecki",
    "natalia cristina da silva": "Natalia Cristina da Silva",
    "benoit saint-denis": "Benoit Saint-Denis",
    "benoit saint denis": "Benoit Saint-Denis",
    "volkan oezdemir": "Volkan Oezdemir",
    "khalil rountree jr.": "Khalil Rountree Jr.",
    "reinier de ridder": "Reinier de Ridder",
    "dricus du plessis": "Dricus du Plessis",
    "maria godinez gonzalez": "Maria Godinez Gonzalez",
}

def fix_name(name: str) -> str:
    key = name.lower().strip()
    if key in NAME_FIXES:
        return NAME_FIXES[key]
    return name.strip()


def parse_rc(name: str) -> tuple[str, bool]:
    """Strip ' RC' suffix and return (clean_name, is_rookie)."""
    if name.endswith(" RC"):
        return name[:-3].strip(), True
    return name, False


# ── Parallels ─────────────────────────────────────────────────────────────────

BASE_PARALLELS = [
    {"name": "Red Foil", "print_run": None},
    {"name": "Black Foil", "print_run": None},
    {"name": "Black and White", "print_run": None},
    {"name": "Gold Foil", "print_run": None},
    {"name": "Member's Only", "print_run": None},
    {"name": "Photographer's Proof", "print_run": None},
    {"name": "Orange Foil", "print_run": None},
    {"name": "Sepia", "print_run": None},
    {"name": "Teal Foil", "print_run": None},
    {"name": "Green Foil", "print_run": 199},
    {"name": "Turquoise Foil", "print_run": 99},
    {"name": "Purple Foil", "print_run": 75},
    {"name": "Blue Foil", "print_run": 50},
    {"name": "Rainbow Foil", "print_run": 25},
    {"name": "First Day Issue", "print_run": 10},
    {"name": "Gold Rainbow Foil", "print_run": 1},
]

CHROME_PARALLELS = [
    {"name": "Refractor", "print_run": None},
    {"name": "Green Refractor", "print_run": None},
    {"name": "Gold Minted Refractor", "print_run": None},
    {"name": "X-Fractor", "print_run": None},
    {"name": "Lava", "print_run": None},
    {"name": "Orange Refractor", "print_run": 99},
    {"name": "Purple Refractor", "print_run": 75},
    {"name": "Gold Refractor", "print_run": 50},
    {"name": "Pearl White Refractor", "print_run": 30},
    {"name": "Superfractor", "print_run": 1},
]

BASE_AUTO_PARALLELS = [
    {"name": "Red", "print_run": 50},
    {"name": "Black", "print_run": 25},
    {"name": "Rainbow", "print_run": 10},
    {"name": "Green", "print_run": 5},
    {"name": "Gold Rainbow", "print_run": 1},
]

CHROME_AUTO_PARALLELS = [
    {"name": "Red", "print_run": 50},
    {"name": "Orange", "print_run": 25},
    {"name": "Superfractor", "print_run": 1},
]

BEAM_TEAM_AUTO_PARALLELS = [
    {"name": "Orange", "print_run": 5},
    {"name": "Gold Rainbow", "print_run": 1},
]

CO_SIGNERS_PARALLELS = [
    {"name": "Gold Rainbow", "print_run": 1},
]

LONE_STAR_PARALLELS = [
    {"name": "Orange", "print_run": 5},
    {"name": "Gold Rainbow", "print_run": 1},
]

POWER_PACKED_AUTO_PARALLELS = [
    {"name": "Orange", "print_run": 5},
    {"name": "Gold Rainbow", "print_run": 1},
]

INSERT_PARALLELS_STANDARD = [
    {"name": "Red", "print_run": None},
    {"name": "Black", "print_run": 99},
    {"name": "Green", "print_run": 50},
    {"name": "Gold Rainbow", "print_run": 1},
]

NO_PARALLELS: list = []

# ── Base Set (200 cards) ──────────────────────────────────────────────────────

BASE_SET_RAW = [
    (1, "Islam Makhachev"), (2, "Grant Dawson"), (3, "Deiveson Figueiredo"),
    (4, "Khabib Nurmagomedov"), (5, "Danny Barlow RC"), (6, "Yan Xiaonan"),
    (7, "Cory Sandhagen"), (8, "Tom Aspinall"), (9, "Rinya Nakamura RC"),
    (10, "Max Holloway"), (11, "Ciryl Gane"), (12, "Mike Breeden RC"),
    (13, "Jose Aldo"), (14, "Alexander Volkanovski"), (15, "Joshua Van RC"),
    (16, "Norma Dumont"), (17, "Curtis Blaydes"), (18, "Manel Kape"),
    (19, "Joanderson Brito RC"), (20, "Sean O'Malley"), (21, "Alex Perez"),
    (22, "Tagir Ulanbekov"), (23, "Ilia Topuria"), (24, "Rodolfo Bellato RC"),
    (25, "Ketlen Vieira"), (26, "Payton Talbott RC"), (27, "Alexandre Pantoja"),
    (28, "Macy Chiasson"), (29, "Jailton Malhadinho"), (30, "Daniel Zellhuber RC"),
    (31, "Marlon Vera"), (32, "Georges St-Pierre"), (33, "Irene Aldana"),
    (34, "Brandon Moreno"), (35, "Modestas Bukauskas RC"), (36, "Charles Oliveira"),
    (37, "Stephen Thompson"), (38, "Raul Rosas"), (39, "Brandon Royval"),
    (40, "Nazim Sadykhov RC"), (41, "Belal Muhammad"), (42, "Matheus Nicolau"),
    (43, "Josh Emmett"), (44, "Jan Blachowicz"), (45, "Said Nurmagomedov"),
    (46, "Jean Silva RC"), (47, "Rose Namajunas"), (48, "Erin Blanchfield"),
    (49, "Eduarda Moura RC"), (50, "Aljamain Sterling"), (51, "Jamahal Hill"),
    (52, "Westin Wilson RC"), (53, "Aleksandar Rakic"), (54, "Carlos Ulberg"),
    (55, "Muhammadjon Naimov RC"), (56, "Manon Fiorot"), (57, "Jack Della Maddalena"),
    (58, "Tatsuro Taira"), (59, "Vinicius Oliveira RC"), (60, "Natalia Cristina da Silva"),
    (61, "Dan Ige"), (62, "Trey Waters RC"), (63, "Casey O'Neill"),
    (64, "Tai Tuivasa"), (65, "Reinier de Ridder RC"), (66, "Johnny Walker"),
    (67, "Kai Kara-France"), (68, "Ariane da Silva"), (69, "Roman Kopylov RC"),
    (70, "Mackenzie Dern"), (71, "Amir Albazi"), (72, "Kai Asakura RC"),
    (73, "Derrick Lewis"), (74, "Khalil Rountree Jr."), (75, "Jonathan Martinez RC"),
    (76, "Nassourdine Imavov"), (77, "Maycee Barber"), (78, "Carlos Prates RC"),
    (79, "Rinat Fakhretdinov"), (80, "Lerone Murphy"), (81, "Shamil Gaziev RC"),
    (82, "Sean Strickland"), (83, "Bo Nickal"), (84, "Adrian Yanez"),
    (85, "Katlyn Cerminara"), (86, "Kamaru Usman"), (87, "Nurullo Aliev RC"),
    (88, "Volkan Oezdemir"), (89, "Joe Pyfer"), (90, "Khamzat Chimaev"),
    (91, "Virna Jandiroba"), (92, "Maria Godinez Gonzalez"), (93, "Ailin Perez RC"),
    (94, "Michel Pereira"), (95, "Themba Gorimbo"), (96, "Robert Whittaker"),
    (97, "Alex Pereira"), (98, "Caio Borralho"), (99, "Marcus McGhee RC"),
    (100, "Jon Jones"), (101, "Iasmin Lucindo"), (102, "Azamat Murzakanov"),
    (103, "Farid Basharat RC"), (104, "Mario Bautista"), (105, "Mauricio Santos RC"),
    (106, "Tabatha Ricci"), (107, "Toshiomi Kazama RC"), (108, "Paulo Costa"),
    (109, "Edson Barboza"), (110, "Yair Rodriguez"), (111, "Brendan Allen"),
    (112, "Hyunsung Park RC"), (113, "Petr Yan"), (114, "Ian Machado Garry"),
    (115, "Aiemann Zahabi"), (116, "Assu Almabayev RC"), (117, "Shavkat Rakhmonov"),
    (118, "Diego Lopes"), (119, "Vicente Luque"), (120, "Trevor Peek RC"),
    (121, "Joaquin Buckley"), (122, "Zhang Weili"), (123, "Alexa Grasso"),
    (124, "Viktoriia Dudakova RC"), (125, "Kayla Harrison"), (126, "Dricus du Plessis"),
    (127, "Nikita Krylov"), (128, "Claudio Ribeiro RC"), (129, "Sean Brady"),
    (130, "Bruno Silva"), (131, "Amanda Lemos"), (132, "Karl Williams RC"),
    (133, "Alexander Volkov"), (134, "Christian Rodriguez"), (135, "Tracy Cortez"),
    (136, "Charles Jourdain RC"), (137, "Umar Nurmagomedov"), (138, "Dustin Poirier"),
    (139, "Colby Covington"), (140, "Nate Landwehr RC"), (141, "Mateusz Gamrot"),
    (142, "Alonzo Menifield"), (143, "Sergei Pavlovich"), (144, "Daniel Marcos RC"),
    (145, "Merab Dvalishvili"), (146, "Israel Adesanya"), (147, "Gilbert Burns"),
    (148, "Melissa Mullins RC"), (149, "Benoit Saint-Denis"), (150, "Yadong Song"),
    (151, "Michael Morales"), (152, "Renato Moicano"), (153, "Victor Henry RC"),
    (154, "Arman Tsarukyan"), (155, "Justin Gaethje"), (156, "Valentina Shevchenko"),
    (157, "Ismael Bonfim RC"), (158, "Mateusz Rebecki"), (159, "Arnold Allen"),
    (160, "Marvin Vettori"), (161, "Waldo Cortes RC"), (162, "Michael Page"),
    (163, "Leon Edwards"), (164, "Gabriel Bonfim RC"), (165, "Yazmin Jauregui"),
    (166, "Manuel Torres"), (167, "Hunter Campbell"), (168, "Morgan Charriere RC"),
    (169, "Roman Dolidze"), (170, "Cody Durden"), (171, "Movsar Evloev"),
    (172, "Vitor Petrino RC"), (173, "Michael Chandler"), (174, "Tatiana Suarez"),
    (175, "Christian Duncan RC"), (176, "Raquel Pennington"), (177, "Magomed Ankalaev"),
    (178, "Jake Matthews"), (179, "Jean Matsumoto RC"), (180, "Brian Ortega"),
    (181, "Tony Ferguson"), (182, "Molly McCann"), (183, "Stephen Erceg RC"),
    (184, "Daniel Hooker"), (185, "Jessica Andrade"), (186, "Esteban Ribovics RC"),
    (187, "Paul Craig"), (188, "Cameron Saaiman"), (189, "Anderson Silva"),
    (190, "Myktybek Orolbai RC"), (191, "Sharabutdin Magomedov"), (192, "Jiri Prochazka"),
    (193, "Jose Mariscal RC"), (194, "Paddy Pimblett"), (195, "Brunno Ferreira"),
    (196, "Miranda Maverick"), (197, "Luana Santos RC"), (198, "Kevin Holland"),
    (199, "Bogdan Guskov RC"), (200, "Conor McGregor"),
]

# ── Base Image Variations (50 cards, #201-250) ───────────────────────────────

IMAGE_VARIATIONS_RAW = [
    (201, "Khabib Nurmagomedov"), (202, "Islam Makhachev"), (203, "Jon Jones"),
    (204, "Tom Aspinall"), (205, "Alexander Volkanovski"), (206, "Ilia Topuria"),
    (207, "Max Holloway"), (208, "Sean O'Malley"), (209, "Alexandre Pantoja"),
    (210, "Georges St-Pierre"), (211, "Charles Oliveira"), (212, "Belal Muhammad"),
    (213, "Conor McGregor"), (214, "Paddy Pimblett"), (215, "Anderson Silva"),
    (216, "Khamzat Chimaev"), (217, "Sean Strickland"), (218, "Bo Nickal"),
    (219, "Alex Pereira"), (220, "Caio Borralho"), (221, "Kayla Harrison"),
    (222, "Dricus du Plessis"), (223, "Umar Nurmagomedov"), (224, "Dustin Poirier"),
    (225, "Shavkat Rakhmonov"), (226, "Diego Lopes"), (227, "Zhang Weili"),
    (228, "Alexa Grasso"), (229, "Merab Dvalishvili"), (230, "Israel Adesanya"),
    (231, "Valentina Shevchenko"), (232, "Ian Machado Garry"), (233, "Arman Tsarukyan"),
    (234, "Justin Gaethje"), (235, "Michael Chandler"), (236, "Tatiana Suarez"),
    (237, "Raquel Pennington"), (238, "Magomed Ankalaev"), (239, "Daniel Hooker"),
    (240, "Jessica Andrade"), (241, "Michael Page"), (242, "Leon Edwards"),
    (243, "Sharabutdin Magomedov"), (244, "Jiri Prochazka"), (245, "Nassourdine Imavov"),
    (246, "Maycee Barber"), (247, "Manon Fiorot"), (248, "Jack Della Maddalena"),
    (249, "Rose Namajunas"), (250, "Erin Blanchfield"),
]

# ── Rookie Design Variations (50 cards, #251-300, all is_rookie) ──────────────

ROOKIE_DESIGN_RAW = [
    (251, "Mike Breeden"), (252, "Danny Barlow"), (253, "Joanderson Brito"),
    (254, "Rodolfo Bellato"), (255, "Daniel Zellhuber"), (256, "Modestas Bukauskas"),
    (257, "Mauricio Santos"), (258, "Eduarda Moura"), (259, "Muhammadjon Naimov"),
    (260, "Trey Waters"), (261, "Roman Kopylov"), (262, "Jonathan Martinez"),
    (263, "Shamil Gaziev"), (264, "Nurullo Aliev"), (265, "Ailin Perez"),
    (266, "Marcus McGhee"), (267, "Farid Basharat"), (268, "Toshiomi Kazama"),
    (269, "Hyunsung Park"), (270, "Assu Almabayev"), (271, "Kai Asakura"),
    (272, "Viktoriia Dudakova"), (273, "Claudio Ribeiro"), (274, "Karl Williams"),
    (275, "Charles Jourdain"), (276, "Nate Landwehr"), (277, "Daniel Marcos"),
    (278, "Melissa Mullins"), (279, "Victor Henry"), (280, "Ismael Bonfim"),
    (281, "Waldo Cortes"), (282, "Gabriel Bonfim"), (283, "Morgan Charriere"),
    (284, "Vitor Petrino"), (285, "Christian Duncan"), (286, "Jean Matsumoto"),
    (287, "Stephen Erceg"), (288, "Esteban Ribovics"), (289, "Myktybek Orolbai"),
    (290, "Jose Mariscal"), (291, "Luana Santos"), (292, "Bogdan Guskov"),
    (293, "Rinya Nakamura"), (294, "Joshua Van"), (295, "Payton Talbott"),
    (296, "Nazim Sadykhov"), (297, "Vinicius Oliveira"), (298, "Jean Silva"),
    (299, "Carlos Prates"), (300, "Reinier de Ridder"),
]

# ── Base Chrome (200 cards, C- prefix, same fighters as base) ─────────────────

CHROME_RAW = [
    (f"C-{num}", name) for num, name in BASE_SET_RAW
]

# ── Base Autographs (96 cards) ────────────────────────────────────────────────

BASE_AUTOS_RAW = [
    ("BCA-ADS", "Ariane da Silva"), ("BCA-AMD", "Alonzo Menifield"),
    ("BCA-ANS", "Amanda Nunes"), ("BCA-AOM", "Alistair Overeem"),
    ("BCA-APA", "Alexandre Pantoja"), ("BCA-APP", "Alex Pereira"),
    ("BCA-APZ", "Alex Perez"), ("BCA-ARC", "Aleksandar Rakic"),
    ("BCA-ATN", "Arman Tsarukyan"), ("BCA-AYZ", "Adrian Yanez"),
    ("BCA-AZI", "Aiemann Zahabi"), ("BCA-BGV", "Bogdan Guskov RC"),
    ("BCA-BJP", "BJ Penn"), ("BCA-CBO", "Caio Borralho"),
    ("BCA-CBS", "Curtis Blaydes"), ("BCA-CCN", "Colby Covington"),
    ("BCA-CDN", "Christian Duncan RC"), ("BCA-CHR", "Chase Hooper"),
    ("BCA-CJN", "Charles Jourdain RC"), ("BCA-CLL", "Chuck Liddell"),
    ("BCA-CML", "Jose Mariscal RC"), ("BCA-COA", "Charles Oliveira"),
    ("BCA-COL", "Casey O'Neill"), ("BCA-CRZ", "Christian Rodriguez"),
    ("BCA-CSA", "Cory Sandhagen"), ("BCA-CSJ", "Chan Sung Jung"),
    ("BCA-CSN", "Chael Sonnen"), ("BCA-DBW", "Danny Barlow RC"),
    ("BCA-DDP", "Dricus du Plessis"), ("BCA-DFO", "Deiveson Figueiredo"),
    ("BCA-DHN", "Dan Henderson"), ("BCA-DHR", "Daniel Hooker"),
    ("BCA-DIG", "Dan Ige"), ("BCA-EBD", "Erin Blanchfield"),
    ("BCA-EMA", "Eduarda Moura RC"), ("BCA-ERS", "Esteban Ribovics RC"),
    ("BCA-FBT", "Farid Basharat RC"), ("BCA-GBS", "Gilbert Burns"),
    ("BCA-IMG", "Ian Machado Garry"), ("BCA-JBO", "Joanderson Brito RC"),
    ("BCA-JBZ", "Jan Blachowicz"), ("BCA-JDM", "Jack Della Maddalena"),
    ("BCA-JJK", "Joanna Jedrzejczyk"), ("BCA-JMA", "Jailton Malhadinho"),
    ("BCA-JMO", "Jean Matsumoto RC"), ("BCA-JMZ", "Jonathan Martinez RC"),
    ("BCA-JPR", "Joe Pyfer"), ("BCA-JPU", "Jens Pulver"),
    ("BCA-JSA", "Jean Silva RC"), ("BCA-JWR", "Johnny Walker"),
    ("BCA-KAA", "Kai Asakura RC"), ("BCA-KCA", "Katlyn Cerminara"),
    ("BCA-KCV", "Khamzat Chimaev"), ("BCA-KHN", "Kayla Harrison"),
    ("BCA-KKF", "Kai Kara-France"), ("BCA-KRJ", "Khalil Rountree Jr."),
    ("BCA-LGZ", "Maria Godinez Gonzalez"), ("BCA-LMA", "Lyoto Machida"),
    ("BCA-LMY", "Lerone Murphy"), ("BCA-MAV", "Magomed Ankalaev"),
    ("BCA-MCN", "Mark Coleman"), ("BCA-MCR", "Michael Chandler"),
    ("BCA-MHS", "Matt Hughes"), ("BCA-MKE", "Manel Kape"),
    ("BCA-MNV", "Muhammadjon Naimov RC"), ("BCA-MOI", "Myktybek Orolbai RC"),
    ("BCA-MPA", "Michel Pereira"), ("BCA-MPE", "Michael Page"),
    ("BCA-MRI", "Mateusz Rebecki"), ("BCA-MRY", "Mauricio Santos RC"),
    ("BCA-NIV", "Nassourdine Imavov"), ("BCA-PPT", "Paddy Pimblett"),
    ("BCA-RBO", "Rodolfo Bellato RC"), ("BCA-RFV", "Rinat Fakhretdinov"),
    ("BCA-RGE", "Royce Gracie"), ("BCA-RKV", "Roman Kopylov RC"),
    ("BCA-RNA", "Rinya Nakamura RC"), ("BCA-RNS", "Rose Namajunas"),
    ("BCA-RRS", "Raul Rosas"), ("BCA-SGV", "Shamil Gaziev RC"),
    ("BCA-SMV", "Sharabutdin Magomedov"), ("BCA-SNV", "Said Nurmagomedov"),
    ("BCA-SOM", "Sean O'Malley"), ("BCA-SRA", "Shogun Rua"),
    ("BCA-STN", "Stephen Thompson"), ("BCA-TGO", "Themba Gorimbo"),
    ("BCA-TSA", "Tim Sylvia"), ("BCA-TUV", "Tagir Ulanbekov"),
    ("BCA-UNV", "Umar Nurmagomedov"), ("BCA-VJA", "Virna Jandiroba"),
    ("BCA-VOA", "Vinicius Oliveira RC"), ("BCA-VSO", "Valentina Shevchenko"),
    ("BCA-WCA", "Waldo Cortes RC"), ("BCA-WSA", "Wanderlei Silva"),
    ("BCA-WWN", "Westin Wilson RC"), ("BCA-YXN", "Yan Xiaonan"),
]

# ── Chrome Autographs (91 cards) ──────────────────────────────────────────────

CHROME_AUTOS_RAW = [
    ("CAS-AAI", "Amir Albazi"), ("CAS-AAN", "Arnold Allen"),
    ("CAS-AAV", "Assu Almabayev RC"), ("CAS-AGO", "Alexa Grasso"),
    ("CAS-APZ", "Ailin Perez RC"), ("CAS-ARN", "Antonio Rodrigo Nogueira"),
    ("CAS-AVI", "Alexander Volkanovski"), ("CAS-AVV", "Alexander Volkov"),
    ("CAS-BFA", "Brunno Ferreira"), ("CAS-BMO", "Brandon Moreno"),
    ("CAS-BOA", "Brian Ortega"), ("CAS-BRN", "Bas Rutten"),
    ("CAS-BSD", "Benoit Saint-Denis"), ("CAS-CDN", "Cody Durden"),
    ("CAS-CGE", "Ciryl Gane"), ("CAS-CSN", "Cameron Saaiman"),
    ("CAS-CUG", "Carlos Ulberg"), ("CAS-DFE", "Don Frye"),
    ("CAS-DLS", "Diego Lopes"), ("CAS-DMS", "Daniel Marcos RC"),
    ("CAS-DPR", "Dustin Poirier"), ("CAS-DZR", "Daniel Zellhuber RC"),
    ("CAS-FGN", "Forrest Griffin"), ("CAS-GBM", "Gabriel Bonfim RC"),
    ("CAS-GSP", "Georges St-Pierre"), ("CAS-HCL", "Hunter Campbell"),
    ("CAS-HSP", "Hyunsung Park RC"), ("CAS-IBM", "Ismael Bonfim RC"),
    ("CAS-ITA", "Ilia Topuria"), ("CAS-JAO", "Jose Aldo"),
    ("CAS-JBY", "Joaquin Buckley"), ("CAS-JDS", "Junior Dos Santos"),
    ("CAS-JGE", "Justin Gaethje"), ("CAS-JHL", "Jamahal Hill"),
    ("CAS-JMS", "Jake Matthews"), ("CAS-JPA", "Julianna Pena"),
    ("CAS-JPR", "Jiri Prochazka"), ("CAS-JPY", "Joe Pyfer"),
    ("CAS-JVN", "Joshua Van RC"), ("CAS-KHD", "Kevin Holland"),
    ("CAS-KSK", "Ken Shamrock"), ("CAS-KVA", "Ketlen Vieira"),
    ("CAS-LES", "Leon Edwards"), ("CAS-LGZ", "Maria Godinez Gonzalez"),
    ("CAS-LSS", "Luana Santos RC"), ("CAS-MBG", "Michael Bisping"),
    ("CAS-MBR", "Maycee Barber"), ("CAS-MBS", "Modestas Bukauskas RC"),
    ("CAS-MDI", "Merab Dvalishvili"), ("CAS-MFT", "Manon Fiorot"),
    ("CAS-MHY", "Max Holloway"), ("CAS-MMC", "Molly McCann"),
    ("CAS-MMG", "Marcus McGhee RC"), ("CAS-MMK", "Miranda Maverick"),
    ("CAS-MMO", "Michael Morales"), ("CAS-MMS", "Melissa Mullins RC"),
    ("CAS-MTE", "Miesha Tate"), ("CAS-MTS", "Manuel Torres"),
    ("CAS-MVI", "Marvin Vettori"), ("CAS-NDT", "Norma Dumont"),
    ("CAS-NLR", "Nate Landwehr RC"), ("CAS-NSV", "Nazim Sadykhov RC"),
    ("CAS-PCA", "Paulo Costa"), ("CAS-PCG", "Paul Craig"),
    ("CAS-PTT", "Payton Talbott RC"), ("CAS-RDR", "Reinier de Ridder RC"),
    ("CAS-RES", "Rashad Evans"), ("CAS-RFN", "Rich Franklin"),
    ("CAS-RLR", "Robbie Lawler"), ("CAS-RPN", "Raquel Pennington"),
    ("CAS-RWR", "Robert Whittaker"), ("CAS-SBY", "Sean Brady"),
    ("CAS-SEG", "Stephen Erceg RC"), ("CAS-SRV", "Shavkat Rakhmonov"),
    ("CAS-SSC", "Serghei Spivac"), ("CAS-SSD", "Sean Strickland"),
    ("CAS-TAL", "Tom Aspinall"), ("CAS-TCZ", "Tracy Cortez"),
    ("CAS-TFN", "Tony Ferguson"), ("CAS-TKA", "Toshiomi Kazama RC"),
    ("CAS-TPK", "Trevor Peek RC"), ("CAS-TRI", "Tabatha Ricci"),
    ("CAS-TTA", "Tatsuro Taira"), ("CAS-TWS", "Trey Waters RC"),
    ("CAS-UFR", "Urijah Faber"), ("CAS-VHY", "Victor Henry RC"),
    ("CAS-VOR", "Volkan Oezdemir"), ("CAS-VPO", "Vitor Petrino RC"),
    ("CAS-YJI", "Yazmin Jauregui"), ("CAS-YSG", "Yadong Song"),
    ("CAS-ZWI", "Zhang Weili"),
]

# ── Beam Team Autographs (25 cards) ──────────────────────────────────────────

BEAM_TEAM_AUTOS_RAW = [
    ("BTA-AG", "Alexa Grasso"), ("BTA-AP", "Alex Pereira"),
    ("BTA-AS", "Anderson Silva"), ("BTA-BN", "Bo Nickal"),
    ("BTA-CM", "Conor McGregor"), ("BTA-CO", "Charles Oliveira"),
    ("BTA-DC", "Daniel Cormier"), ("BTA-DL", "Diego Lopes"),
    ("BTA-IM", "Islam Makhachev"), ("BTA-IT", "Ilia Topuria"),
    ("BTA-JJ", "Jon Jones"), ("BTA-JP", "Julianna Pena"),
    ("BTA-KA", "Kai Asakura RC"), ("BTA-KH", "Kayla Harrison"),
    ("BTA-KN", "Khabib Nurmagomedov"), ("BTA-MH", "Max Holloway"),
    ("BTA-RN", "Rose Namajunas"), ("BTA-SM", "Sean O'Malley"),
    ("BTA-SR", "Shavkat Rakhmonov"), ("BTA-SS", "Sean Strickland"),
    ("BTA-TA", "Tom Aspinall"), ("BTA-UN", "Umar Nurmagomedov"),
    ("BTA-VS", "Valentina Shevchenko"), ("BTA-WS", "Wanderlei Silva"),
    ("BTA-ZW", "Zhang Weili"),
]

# ── Co-Signers (9 cards) ─────────────────────────────────────────────────────

CO_SIGNERS_RAW = [
    ("CSA-AT", "Kai Asakura / Tatsuro Taira"),
    ("CSA-CS", "Sean Strickland / Donald Cerrone"),
    ("CSA-GL", "Alexa Grasso / Diego Lopes"),
    ("CSA-HG", "Max Holloway / Justin Gaethje"),
    ("CSA-JP", "Alex Pereira / Jon Jones"),
    ("CSA-MG", "Ian Machado Garry / Conor McGregor"),
    ("CSA-MN", "Umar Nurmagomedov / Islam Makhachev"),
    ("CSA-PH", "Dustin Poirier / Daniel Hooker"),
    ("CSA-WC", "Hunter Campbell / Dana White"),
]

# ── Lone Star Signatures (29 cards) ──────────────────────────────────────────

LONE_STAR_RAW = [
    ("LSS-AA", "Assu Almabayev RC"), ("LSS-CB", "Caio Borralho"),
    ("LSS-CC", "Colby Covington"), ("LSS-CL", "Chuck Liddell"),
    ("LSS-DC", "Donald Cerrone"), ("LSS-DH", "Daniel Hooker"),
    ("LSS-DL", "Diego Lopes"), ("LSS-DP", "Dricus du Plessis"),
    ("LSS-DZ", "Daniel Zellhuber RC"), ("LSS-EB", "Erin Blanchfield"),
    ("LSS-HP", "Hyunsung Park RC"), ("LSS-IG", "Ian Machado Garry"),
    ("LSS-IL", "Iasmin Lucindo"), ("LSS-JA", "Jessica Andrade"),
    ("LSS-JB", "Jan Blachowicz"), ("LSS-JJ", "Jon Jones"),
    ("LSS-JV", "Joshua Van RC"), ("LSS-KH", "Kevin Holland"),
    ("LSS-KN", "Khabib Nurmagomedov"), ("LSS-MD", "Merab Dvalishvili"),
    ("LSS-PP", "Paddy Pimblett"), ("LSS-PT", "Payton Talbott RC"),
    ("LSS-RD", "Reinier de Ridder RC"), ("LSS-RR", "Raul Rosas"),
    ("LSS-SE", "Stephen Erceg RC"), ("LSS-SG", "Shamil Gaziev RC"),
    ("LSS-TC", "Tracy Cortez"), ("LSS-TR", "Tabatha Ricci"),
    ("LSS-TT", "Tatsuro Taira"),
]

# ── Power Packed Autographs (35 cards) ────────────────────────────────────────

POWER_PACKED_AUTOS_RAW = [
    ("PPA-AA", "Arnold Allen"), ("PPA-AP", "Alexandre Pantoja"),
    ("PPA-AS", "Anderson Silva"), ("PPA-AT", "Arman Tsarukyan"),
    ("PPA-AV", "Alexander Volkanovski"), ("PPA-BD", "Benoit Saint-Denis"),
    ("PPA-BR", "Brandon Royval"), ("PPA-CD", "Christian Duncan RC"),
    ("PPA-CM", "Conor McGregor"), ("PPA-DP", "Dustin Poirier"),
    ("PPA-FM", "Frank Mir"), ("PPA-GS", "Georges St-Pierre"),
    ("PPA-IT", "Ilia Topuria"), ("PPA-JB", "Joanderson Brito RC"),
    ("PPA-JG", "Justin Gaethje"), ("PPA-JM", "Jean Matsumoto RC"),
    ("PPA-JP", "Joe Pyfer"), ("PPA-JS", "Jean Silva RC"),
    ("PPA-JW", "Johnny Walker"), ("PPA-KC", "Khamzat Chimaev"),
    ("PPA-KV", "Ketlen Vieira"), ("PPA-LE", "Leon Edwards"),
    ("PPA-MA", "Magomed Ankalaev"), ("PPA-MB", "Maycee Barber"),
    ("PPA-MC", "Michael Chandler"), ("PPA-MF", "Manon Fiorot"),
    ("PPA-MM", "Michael Morales"), ("PPA-MO", "Myktybek Orolbai RC"),
    ("PPA-RN", "Rinya Nakamura RC"), ("PPA-RP", "Raquel Pennington"),
    ("PPA-RW", "Robert Whittaker"), ("PPA-SC", "Stipe Miocic"),
    ("PPA-SM", "Sharabutdin Magomedov"), ("PPA-TS", "Tatiana Suarez"),
    ("PPA-VO", "Vinicius Oliveira RC"),
]

# ── Hype Machines (20 cards) ──────────────────────────────────────────────────

HYPE_MACHINES_RAW = [
    ("HM-1", "Ilia Topuria"), ("HM-2", "Dustin Poirier"),
    ("HM-3", "Sean O'Malley"), ("HM-4", "Conor McGregor"),
    ("HM-5", "Israel Adesanya"), ("HM-6", "Alexander Volkanovski"),
    ("HM-7", "Valentina Shevchenko"), ("HM-8", "Jon Jones"),
    ("HM-9", "Alex Pereira"), ("HM-10", "Raul Rosas"),
    ("HM-11", "Amanda Nunes"), ("HM-12", "Georges St-Pierre"),
    ("HM-13", "Max Holloway"), ("HM-14", "Colby Covington"),
    ("HM-15", "Jose Aldo"), ("HM-16", "Chan Sung Jung"),
    ("HM-17", "Khamzat Chimaev"), ("HM-18", "Paddy Pimblett"),
    ("HM-19", "Brian Ortega"), ("HM-20", "Charles Oliveira"),
]

# ── Dynasty And Destiny (20 cards) ────────────────────────────────────────────

DYNASTY_RAW = [
    ("DD-1", "Khabib Nurmagomedov"), ("DD-2", "Islam Makhachev"),
    ("DD-3", "Jon Jones"), ("DD-4", "Tom Aspinall"),
    ("DD-5", "Alexander Volkanovski"), ("DD-6", "Ilia Topuria"),
    ("DD-7", "Max Holloway"), ("DD-8", "Sean O'Malley"),
    ("DD-9", "Alexandre Pantoja"), ("DD-10", "Kai Asakura RC"),
    ("DD-11", "Charles Oliveira"), ("DD-12", "Carlos Prates RC"),
    ("DD-13", "Conor McGregor"), ("DD-14", "Paddy Pimblett"),
    ("DD-15", "Anderson Silva"), ("DD-16", "Khamzat Chimaev"),
    ("DD-17", "Sean Strickland"), ("DD-18", "Bo Nickal"),
    ("DD-19", "Alex Pereira"), ("DD-20", "Caio Borralho"),
]

# ── Instavision (10 cards) ────────────────────────────────────────────────────

INSTAVISION_RAW = [
    ("IV-1", "Kayla Harrison"), ("IV-2", "Dricus du Plessis"),
    ("IV-3", "Umar Nurmagomedov"), ("IV-4", "Dustin Poirier"),
    ("IV-5", "Shavkat Rakhmonov"), ("IV-6", "Diego Lopes"),
    ("IV-7", "Zhang Weili"), ("IV-8", "Alexa Grasso"),
    ("IV-9", "Merab Dvalishvili"), ("IV-10", "Israel Adesanya"),
]

# ── Power Packed inserts (20 cards, PD- prefix) ──────────────────────────────

POWER_PACKED_RAW = [
    ("PD-1", "Dricus du Plessis"), ("PD-2", "Caio Borralho"),
    ("PD-3", "Reinier de Ridder RC"), ("PD-4", "Justin Gaethje"),
    ("PD-5", "Michael Chandler"), ("PD-6", "Tatiana Suarez"),
    ("PD-7", "Charles Oliveira"), ("PD-8", "Magomed Ankalaev"),
    ("PD-9", "Carlos Prates RC"), ("PD-10", "Jessica Andrade"),
    ("PD-11", "Stephen Erceg RC"), ("PD-12", "Alexandre Pantoja"),
    ("PD-13", "Sharabutdin Magomedov"), ("PD-14", "Jiri Prochazka"),
    ("PD-15", "Payton Talbott RC"), ("PD-16", "Maycee Barber"),
    ("PD-17", "Paddy Pimblett"), ("PD-18", "Jack Della Maddalena"),
    ("PD-19", "Rose Namajunas"), ("PD-20", "Alex Pereira"),
]

# ── Special Forces (30 cards) ─────────────────────────────────────────────────

SPECIAL_FORCES_RAW = [
    ("SF-1", "Petr Yan"), ("SF-2", "Daniel Zellhuber RC"),
    ("SF-3", "Arman Tsarukyan"), ("SF-4", "Merab Dvalishvili"),
    ("SF-5", "Rinya Nakamura RC"), ("SF-6", "Ian Machado Garry"),
    ("SF-7", "Tom Aspinall"), ("SF-8", "Jean Silva RC"),
    ("SF-9", "Myktybek Orolbai RC"), ("SF-10", "Valentina Shevchenko"),
    ("SF-11", "Ketlen Vieira"), ("SF-12", "Tabatha Ricci"),
    ("SF-13", "Ilia Topuria"), ("SF-14", "Ailin Perez RC"),
    ("SF-15", "Joshua Van RC"), ("SF-16", "Michael Page"),
    ("SF-17", "Islam Makhachev"), ("SF-18", "Hyunsung Park RC"),
    ("SF-19", "Daniel Hooker"), ("SF-20", "Mackenzie Dern"),
    ("SF-21", "Shavkat Rakhmonov"), ("SF-22", "Leon Edwards"),
    ("SF-23", "Sean Strickland"), ("SF-24", "Bo Nickal"),
    ("SF-25", "Joaquin Buckley"), ("SF-26", "Khabib Nurmagomedov"),
    ("SF-27", "Manon Fiorot"), ("SF-28", "Belal Muhammad"),
    ("SF-29", "Raquel Pennington"), ("SF-30", "Nassourdine Imavov"),
]

# ── Beam Team inserts (20 cards) ──────────────────────────────────────────────

BEAM_TEAM_RAW = [
    ("BT-1", "Khamzat Chimaev"), ("BT-2", "Ilia Topuria"),
    ("BT-3", "Carlos Prates RC"), ("BT-4", "Kai Asakura RC"),
    ("BT-5", "Alex Pereira"), ("BT-6", "Rinya Nakamura RC"),
    ("BT-7", "Bo Nickal"), ("BT-8", "Stephen Erceg RC"),
    ("BT-9", "Kayla Harrison"), ("BT-10", "Payton Talbott RC"),
    ("BT-11", "Shavkat Rakhmonov"), ("BT-12", "Zhang Weili"),
    ("BT-13", "Islam Makhachev"), ("BT-14", "Tom Aspinall"),
    ("BT-15", "Valentina Shevchenko"), ("BT-16", "Jon Jones"),
    ("BT-17", "Reinier de Ridder RC"), ("BT-18", "Dustin Poirier"),
    ("BT-19", "Sean O'Malley"), ("BT-20", "Conor McGregor"),
]

# ── Triumvirates (18 cards) ──────────────────────────────────────────────────

TRIUMVIRATES_RAW = [
    ("TV-1", "Islam Makhachev"), ("TV-2", "Islam Makhachev"), ("TV-3", "Islam Makhachev"),
    ("TV-4", "Jon Jones"), ("TV-5", "Jon Jones"), ("TV-6", "Jon Jones"),
    ("TV-7", "Conor McGregor"), ("TV-8", "Conor McGregor"), ("TV-9", "Conor McGregor"),
    ("TV-10", "Sean O'Malley"), ("TV-11", "Sean O'Malley"), ("TV-12", "Sean O'Malley"),
    ("TV-13", "Ilia Topuria"), ("TV-14", "Ilia Topuria"), ("TV-15", "Ilia Topuria"),
    ("TV-16", "Alex Pereira"), ("TV-17", "Alex Pereira"), ("TV-18", "Alex Pereira"),
]


# ── Build sections ────────────────────────────────────────────────────────────

def build_cards(raw: list[tuple], *, force_rookie: bool = False, team: str | None = None) -> list[dict]:
    """Build card dicts from (card_number, name) tuples."""
    cards = []
    for card_num, name in raw:
        clean_name, is_rc = parse_rc(name)
        clean_name = fix_name(clean_name)
        cards.append({
            "card_number": str(card_num),
            "player": clean_name,
            "team": team,
            "is_rookie": force_rookie or is_rc,
            "subset": None,
        })
    return cards


def build_co_signer_cards(raw: list[tuple]) -> list[dict]:
    """Build cards for Co-Signers with co_players field."""
    cards = []
    for card_num, name_pair in raw:
        names = [fix_name(n.strip()) for n in name_pair.split(" / ")]
        # First name is the primary card holder
        primary = names[0]
        primary, is_rc = parse_rc(primary)
        primary = fix_name(primary)
        cards.append({
            "card_number": str(card_num),
            "player": primary,
            "team": None,
            "is_rookie": is_rc,
            "subset": None,
            "co_players": [fix_name(n) for n in names[1:]],
        })
    return cards


def build_section(name: str, cards: list[dict], parallels: list[dict]) -> dict:
    return {
        "insert_set": name,
        "parallels": parallels,
        "cards": cards,
    }


SECTIONS_DEF = [
    ("Base Set", build_cards(BASE_SET_RAW), BASE_PARALLELS),
    ("Base Image Variations", build_cards(IMAGE_VARIATIONS_RAW), NO_PARALLELS),
    ("Rookie Design Variations", build_cards(ROOKIE_DESIGN_RAW, force_rookie=True), NO_PARALLELS),
    ("Base Chrome", build_cards(CHROME_RAW), CHROME_PARALLELS),
    ("Base Autographs", build_cards(BASE_AUTOS_RAW), BASE_AUTO_PARALLELS),
    ("Chrome Autographs", build_cards(CHROME_AUTOS_RAW), CHROME_AUTO_PARALLELS),
    ("Beam Team Autographs", build_cards(BEAM_TEAM_AUTOS_RAW), BEAM_TEAM_AUTO_PARALLELS),
    ("Co-Signers", build_co_signer_cards(CO_SIGNERS_RAW), CO_SIGNERS_PARALLELS),
    ("Lone Star Signatures", build_cards(LONE_STAR_RAW), LONE_STAR_PARALLELS),
    ("Power Packed Autographs", build_cards(POWER_PACKED_AUTOS_RAW), POWER_PACKED_AUTO_PARALLELS),
    ("Hype Machines", build_cards(HYPE_MACHINES_RAW), INSERT_PARALLELS_STANDARD),
    ("Dynasty And Destiny", build_cards(DYNASTY_RAW), INSERT_PARALLELS_STANDARD),
    ("Instavision", build_cards(INSTAVISION_RAW), INSERT_PARALLELS_STANDARD),
    ("Power Packed", build_cards(POWER_PACKED_RAW), INSERT_PARALLELS_STANDARD),
    ("Special Forces", build_cards(SPECIAL_FORCES_RAW), INSERT_PARALLELS_STANDARD),
    ("Beam Team", build_cards(BEAM_TEAM_RAW), NO_PARALLELS),
    ("Triumvirates", build_cards(TRIUMVIRATES_RAW), NO_PARALLELS),
]

sections = [build_section(name, cards, pars) for name, cards, pars in SECTIONS_DEF]

# ── Build players ─────────────────────────────────────────────────────────────

players_map: dict[str, dict] = {}

for section in sections:
    for card in section["cards"]:
        key = card["player"].lower()
        if key not in players_map:
            players_map[key] = {
                "player": card["player"],
                "appearances": [],
                "_insert_sets": set(),
            }
        app = {
            "insert_set": section["insert_set"],
            "card_number": card["card_number"],
            "team": card["team"],
            "is_rookie": card["is_rookie"],
            "subset_tag": None,
            "parallels": section["parallels"],
        }
        if "co_players" in card:
            app["co_players"] = card["co_players"]
        players_map[key]["appearances"].append(app)
        players_map[key]["_insert_sets"].add(section["insert_set"])

# Also add secondary co-signer fighters as players
for section in sections:
    for card in section["cards"]:
        if "co_players" not in card:
            continue
        for co_name in card["co_players"]:
            co_key = co_name.lower()
            if co_key not in players_map:
                players_map[co_key] = {
                    "player": co_name,
                    "appearances": [],
                    "_insert_sets": set(),
                }
            # Add appearance for the co-player too
            players_map[co_key]["appearances"].append({
                "insert_set": section["insert_set"],
                "card_number": card["card_number"],
                "team": None,
                "is_rookie": False,
                "subset_tag": None,
                "parallels": section["parallels"],
            })
            players_map[co_key]["_insert_sets"].add(section["insert_set"])

# Compute stats
players_list = []
for p in sorted(players_map.values(), key=lambda x: x["player"].lower()):
    numbered = []
    for app in p["appearances"]:
        for par in app["parallels"]:
            if par["print_run"] is not None:
                numbered.append(par["print_run"])
    stats = {
        "unique_cards": len(p["appearances"]),
        "total_print_run": sum(numbered),
        "one_of_ones": sum(1 for pr in numbered if pr == 1),
        "insert_sets": len(p["_insert_sets"]),
    }
    # Remove co_players from appearances (seed.ts doesn't expect it in PlayerAppearance)
    clean_appearances = []
    for app in p["appearances"]:
        a = {k: v for k, v in app.items() if k != "co_players"}
        clean_appearances.append(a)
    players_list.append({
        "player": p["player"],
        "appearances": clean_appearances,
        "stats": stats,
    })

# ── Output ────────────────────────────────────────────────────────────────────

# Clean co_players from section cards too (seed.ts uses "player" entries for co-player links)
clean_sections = []
for s in sections:
    clean_cards = []
    for c in s["cards"]:
        cc = {k: v for k, v in c.items() if k != "co_players"}
        clean_cards.append(cc)
    clean_sections.append({
        "insert_set": s["insert_set"],
        "parallels": s["parallels"],
        "cards": clean_cards,
    })

output = {
    "set_name": SET_NAME,
    "sport": SPORT,
    "season": SEASON,
    "league": LEAGUE,
    "sections": clean_sections,
    "players": players_list,
}

total_cards = sum(len(s["cards"]) for s in sections)
unique_players = len(players_list)
auto_names = {"Base Autographs", "Chrome Autographs", "Beam Team Autographs", "Co-Signers", "Lone Star Signatures", "Power Packed Autographs"}
auto_cards = sum(len(s["cards"]) for s in sections if s["insert_set"] in auto_names)
insert_names = {"Hype Machines", "Dynasty And Destiny", "Instavision", "Power Packed", "Special Forces", "Beam Team", "Triumvirates"}
insert_cards = sum(len(s["cards"]) for s in sections if s["insert_set"] in insert_names)

print(f"Set: {SET_NAME}")
print(f"Sections: {len(sections)}")
print(f"Total cards: {total_cards}")
print(f"Unique players: {unique_players}")
print(f"Base set: {len(BASE_SET_RAW)} cards")
print(f"Base Chrome: {len(CHROME_RAW)} cards")
print(f"Image Variations: {len(IMAGE_VARIATIONS_RAW)} cards")
print(f"Rookie Design Variations: {len(ROOKIE_DESIGN_RAW)} cards")
print(f"Autograph sets: {len(auto_names)} ({auto_cards} cards)")
print(f"Insert sets: {len(insert_names)} ({insert_cards} cards)")

out_path = "scripts/stadium_club_ufc_2025_parsed.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nWrote {out_path}")
