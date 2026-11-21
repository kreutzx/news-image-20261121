# Story database for "The World in One Day" — Saturday 21 November 2026.
# Every record is one counted story: a real event that happened, or was
# first reported, on 21 November 2026 in some time zone. The renderer
# counts these records and prints the accounting on the masthead, so the
# numbers on the page can never drift from the data.
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
    dict(section="WORLD", tag="CONFIRMED", region="Latin America",
         field="Conflict",
         head="Salvadoran troops in Haiti lose soldiers to explosives",
         src="One Turn"),
    dict(section="WORLD", tag="REPORTED", region="Middle East",
         field="Conflict",
         head="Iran says it downed a US MQ-9 drone over the Strait of "
              "Hormuz", src="IRGC via Standard Topic"),
    dict(section="WORLD", tag="CONFIRMED", region="Europe",
         field="Politics",
         head="Estonia moves to close its border crossings with Russia",
         src="One Turn"),
    dict(section="WORLD", tag="REPORTED", region="Middle East",
         field="Justice",
         head="Syria captures a former general accused of a 2014 "
              "massacre", src="Regional wires"),
    dict(section="WORLD", tag="CONFIRMED", region="Middle East",
         field="Conflict",
         head="Saudi-led coalition intercepts Houthi missiles aimed at "
              "Riyadh", src="One Turn"),
    # POLITICS & MONEY
    dict(section="POLITICS & MONEY", tag="REPORTED", region="Asia",
         field="Politics",
         head="After Shenzhen, Trump defends Putin ties; Zelensky "
              "condemns the 'friend' remark", src="NYT / wires"),
    dict(section="POLITICS & MONEY", tag="FORECAST", region="Europe",
         field="Politics",
         head="Spain heads to a 29 November election as conservatives "
              "gain ground", src="One Turn"),
    dict(section="POLITICS & MONEY", tag="CONFIRMED", region="Asia",
         field="Politics",
         head="Mongolia's president resigns; elections due within four "
              "months", src="Regional wires"),
    dict(section="POLITICS & MONEY", tag="CONFIRMED", region="Europe",
         field="Politics",
         head="EU approves 1 billion euros in defence aid for Ukraine; "
              "UK pledges 1,000 drones", src="EU Council / MoD"),
    dict(section="POLITICS & MONEY", tag="REPORTED",
         region="North America", field="Technology",
         head="FBI criminal database reportedly hacked as US outages "
              "continue", src="CNN via One Turn"),
    dict(section="POLITICS & MONEY", tag="CONFIRMED",
         region="Latin America", field="Money",
         head="Argentina's country risk tops 1,000 points as bonds "
              "slump", src="One Turn"),
    dict(section="POLITICS & MONEY", tag="DEVELOPING",
         region="North America", field="Technology",
         head="YouTube nears a multibillion-dollar settlement with US "
              "schools", src="One Turn"),
    # SCIENCE & SOCIETY
    dict(section="SCIENCE & SOCIETY", tag="CONFIRMED",
         region="North America", field="Justice",
         head="Man convicted of starting the deadly Palisades fire in "
              "Los Angeles", src="One Turn"),
    dict(section="SCIENCE & SOCIETY", tag="CONFIRMED",
         region="North America", field="Justice",
         head="Judge approves Bayer's $7.25 billion Roundup settlement",
         src="One Turn"),
    dict(section="SCIENCE & SOCIETY", tag="CONFIRMED", region="Africa",
         field="Justice",
         head="Tanzanian opposition leader Tundu Lissu convicted of "
              "sedition", src="One Turn"),
    dict(section="SCIENCE & SOCIETY", tag="CONFIRMED", region="Europe",
         field="Society",
         head="UN cuts its food-aid target despite a looming starvation "
              "threat", src="UN wires"),
    dict(section="SCIENCE & SOCIETY", tag="CONFIRMED", region="Africa",
         field="Health",
         head="Uganda restricts gatherings and travel over an Ebola "
              "threat", src="One Turn"),
    dict(section="SCIENCE & SOCIETY", tag="CONFIRMED", region="Space",
         field="Science",
         head="Curiosity rover photographs twilight clouds drifting "
              "over Mars", src="One Turn"),
    dict(section="SCIENCE & SOCIETY", tag="CONFIRMED",
         region="North America", field="Science",
         head="Blue sucker fish found to live well beyond 100 years",
         src="One Turn"),
]

# ---- Sport strip ------------------------------------------------------
SPORT = [
    dict(tag="CONFIRMED", region="Europe", field="Sport",
         head="Alcaraz beats Cobolli to stay unbeaten in ATP Finals "
              "group play in Turin"),
    dict(tag="CONFIRMED", region="North America", field="Sport",
         head="A Lim Kim leads the LPGA finale after a hole-in-one in "
              "Florida"),
    dict(tag="CONFIRMED", region="Asia", field="Sport",
         head="Choi Min-jeong cruises at the short-track World Tour "
              "stop in Seoul"),
    dict(tag="CONFIRMED", region="Europe", field="Sport",
         head="Mao Shimada leads the Finlandia Trophy after the short "
              "program"),
    dict(tag="CONFIRMED", region="North America", field="Sport",
         head="Washington Spirit reach the NWSL Championship final"),
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
    dict(tag="FORECAST", region="Asia", field="Politics",
         head="Nepal PM Balendra Shah to make his first visit to India"),
    dict(tag="REPORTED", region="Europe", field="Politics",
         head="Trump tells Europe to defund Ukraine after the Putin "
              "summit"),
    dict(tag="REPORTED", region="Europe", field="Money",
         head="Nordic police flag Revolut in a Russia-linked laundering "
              "probe"),
    dict(tag="CONFIRMED", region="Africa", field="Energy",
         head="Kenya begins onshore crude drilling in Turkana"),
    dict(tag="REPORTED", region="North America", field="Technology",
         head="Trump vows tariffs for US firms building data centres "
              "abroad"),
    dict(tag="REPORTED", region="North America", field="Justice",
         head="$22.5M haul in what police call a staggering train heist"),
    dict(tag="CONFIRMED", region="Oceania", field="Climate",
         head="US sells deep-sea mining leases off American Samoa"),
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
    "(it runs Sunday) · Anthropic's stock-market debut (that was "
    "Thursday's news) · any COP31 final text (still unwritten at press "
    "time) · Spain's election result (voting is 29 November). If it is "
    "not dated 21 November 2026, it is not on this page."
)
