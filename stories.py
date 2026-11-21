# Story database for "The World in One Day" — Saturday 21 November 2026.
# Every record is one counted story: a real event that happened, or was
# first reported, on 21 November 2026 in some time zone. The renderer
# counts these records and prints the accounting on the masthead, so the
# numbers on the page can never drift from the data.
#
# Selection (v3): 35 counted stories in total — the 27 headlines below
# plus the 8 market figures in NUMBERS. An earlier 59-story cut proved
# too dense to read at a glance, so the weakest two dozen headlines were
# dropped and the freed space went to larger type and larger drawings.
# All 16 drawn stories were kept; the cuts fell on text-only cards, the
# sport strip and the late wire.
#
# tag: CONFIRMED (established by multiple reports), REPORTED (single or
# attributed report), DEVELOPING (still unfolding), FORECAST (dated
# future event the day points to). art: key into art.py's illustrations,
# or None for a text-only card.

STORIES = [
    # ---- Heroes ------------------------------------------------------
    dict(kind="hero", art="missiles", tag="CONFIRMED",
         region="Europe", field="Conflict",
         head="Russia fires 400 drones and 110 missiles at Ukraine; "
              "missiles land in Poland",
         deck="Kyiv's bridges and stations are hit and at least eight die "
              "in the capital; PM Tusk calls the Polish impacts a "
              "deliberate provocation as NATO cries airspace violation.",
         src="AP / France 24 / CBS"),
    dict(kind="hero", art="gavel", tag="CONFIRMED",
         region="Asia", field="Justice",
         head="UN court finds Myanmar committed genocide against "
              "the Rohingya",
         deck="The ICJ's landmark ruling in The Hague holds Myanmar "
              "responsible for the genocide; Naypyidaw and Beijing both "
              "protest a 'biased' judgment.",
         src="AP / Standard Topic"),

    # ---- Lead panels (drawn) ----------------------------------------
    dict(kind="lead", art="chart", tag="CONFIRMED",
         region="North America", field="Money",
         head="AI sell-off tips S&P 500 and Dow into correction",
         deck="Chip and AI names lead a 3.7% US slide; Tokyo's Nikkei "
              "falls 5.06% as even gold and bitcoin are sold.",
         src="One Turn / NYT"),
    dict(kind="lead", art="pill", tag="REPORTED",
         region="Europe", field="Health",
         head="Cancer pill clears tumours in 1 in 12 pancreatic patients",
         deck="A trial of the pill daraxonrasib leaves no cancer visible "
              "on scans in one in 12 patients.",
         src="One Turn"),
    dict(kind="lead", art="flags", tag="CONFIRMED",
         region="Europe", field="Politics",
         head="UK and EU sign biggest post-Brexit deals in Brussels",
         deck="PM Andy Burnham and EU leaders agree three pacts: food "
              "exports, carbon markets and youth mobility.",
         src="One Turn"),
    dict(kind="lead", art="globe", tag="DEVELOPING",
         region="Asia", field="Climate",
         head="COP31 runs into overtime as fossil-fuel text stalls",
         deck="Nearly 200 nations in Antalya pass the deadline without "
              "a deal; green groups slam the draft.",
         src="One Turn / AFP"),
    dict(kind="lead", art="crowd", tag="CONFIRMED",
         region="Europe", field="Society",
         head="Gen Z protests spread across 25 European countries",
         deck="Thousands of students march over living costs, military "
              "spending and the climate.",
         src="One Turn"),
    dict(kind="lead", art="f1", tag="CONFIRMED",
         region="North America", field="Sport",
         head="Antonelli fastest in Vegas, but penalty gives "
              "Verstappen pole",
         deck="The champion's 1:33.893 tops qualifying, yet an engine "
              "penalty drops him to sixth; both Ferraris out in Q2.",
         src="Reuters"),

    # ---- Picture wire (small drawn panels) ---------------------------
    dict(kind="wire", art="seismo", tag="CONFIRMED",
         region="Latin America", field="Disaster",
         head="Magnitude 6.7 earthquake shakes central Peru",
         src="One Turn"),
    dict(kind="wire", art="probe", tag="CONFIRMED",
         region="Space", field="Science",
         head="Voyager 1 is now 24 light-hours from Earth",
         src="One Turn / NASA"),
    dict(kind="wire", art="mercury", tag="CONFIRMED",
         region="Europe", field="Science",
         head="BepiColombo reaches Mercury orbit after eight years",
         src="One Turn / ESA"),
    dict(kind="wire", art="boat", tag="CONFIRMED",
         region="Africa", field="Disaster",
         head="Boat carrying funeral mourners capsizes in Nigeria",
         src="One Turn"),
    dict(kind="wire", art="swim", tag="CONFIRMED",
         region="Middle East", field="Society",
         head="Lewis Pugh swims the Strait of Hormuz for its wildlife",
         src="Standard Topic"),
    dict(kind="wire", art="particle", tag="REPORTED",
         region="Europe", field="Science",
         head="CERN finds first evidence of an ultra-rare particle decay",
         src="One Turn"),
    dict(kind="wire", art="tree", tag="CONFIRMED",
         region="Europe", field="Culture",
         head="Giant Christmas tree raised in St Peter's Square",
         src="One Turn"),
    dict(kind="wire", art="shield", tag="CONFIRMED",
         region="North America", field="Health",
         head="United States loses its measles elimination status",
         src="One Turn"),
]

# ---- Section cards (text, grouped by the section key) ----------------
CARDS = [
    # WORLD
    dict(section="WORLD", tag="DEVELOPING", region="Middle East",
         field="Conflict",
         head="Israeli strikes kill Palestinians in Gaza as West Bank "
              "violence grows", src="AP"),
    dict(section="WORLD", tag="CONFIRMED", region="Europe",
         field="Conflict",
         head="Ukrainian drones hit a Russian fertiliser plant and a "
              "Smolensk industrial site", src="Kyiv reports"),
    dict(section="WORLD", tag="REPORTED", region="Middle East",
         field="Conflict",
         head="Iran says it downed a US MQ-9 drone over the Strait of "
              "Hormuz", src="IRGC via Standard Topic"),
    # POLITICS & MONEY
    dict(section="POLITICS & MONEY", tag="FORECAST", region="Europe",
         field="Politics",
         head="Spain heads to a 29 November election as conservatives "
              "gain ground", src="One Turn"),
    dict(section="POLITICS & MONEY", tag="CONFIRMED", region="Asia",
         field="Politics",
         head="Mongolia's president resigns; elections due within four "
              "months", src="Regional wires"),
    # SCIENCE & SOCIETY
    dict(section="SCIENCE & SOCIETY", tag="CONFIRMED",
         region="North America", field="Justice",
         head="Man convicted of starting the deadly Palisades fire in "
              "Los Angeles", src="One Turn"),
    dict(section="SCIENCE & SOCIETY", tag="CONFIRMED",
         region="North America", field="Justice",
         head="Judge approves Bayer's $7.25 billion Roundup settlement",
         src="One Turn"),
]

# ---- Sport strip ------------------------------------------------------
SPORT = [
    dict(tag="CONFIRMED", region="Europe", field="Sport",
         head="Alcaraz beats Cobolli to stay unbeaten in ATP Finals "
              "group play in Turin"),
    dict(tag="FORECAST", region="North America", field="Sport",
         head="Sunday night in Las Vegas: Verstappen starts the Grand "
              "Prix on pole"),
]

# ---- By the numbers (Friday's close, as reported Saturday) ------------
NUMBERS = [
    ("S&P 500", "6,910", "-3.70%"),
    ("NIKKEI 225", "", "-5.06%"),
    ("FTSE 100", "10,346", "-1.02%"),
    ("GOLD", "", "-3.98%"),
    ("BITCOIN", "", "-4.15%"),
    ("BRENT", "$89.87", "+0.48%"),
    ("US 10-YEAR", "4.91%", ""),
    ("BOVESPA", "166,376", "-0.69%"),
]

# ---- Late wire (one-liners) -------------------------------------------
TICKER = [
    dict(tag="CONFIRMED", region="Asia", field="Politics",
         head="Seoul: ruling party moves to impeach the chief justice"),
    dict(tag="CONFIRMED", region="Africa", field="Energy",
         head="Kenya begins onshore crude drilling in Turkana"),
]

# ---- UTC timeline strip ------------------------------------------------
TIMELINE = [
    ("OVERNIGHT", "Russian barrage on Kyiv"),
    ("05:12 UTC", "Las Vegas qualifying opens"),
    ("MORNING", "ICJ genocide ruling, The Hague"),
    ("MIDDAY", "COP31 passes its deadline"),
    ("AT THE CLOSE", "S&P 500 falls 3.7%"),
]

DATE_CHECK = (
    "DATE CHECK — WHAT WE LEFT OUT, AND WHY: the Las Vegas race itself "
    "(it runs Sunday) · Anthropic's market debut (Thursday's news) · "
    "any COP31 final text (still unwritten) · Spain's election result "
    "(29 November). Not dated 21 November 2026? Not on this page."
)
