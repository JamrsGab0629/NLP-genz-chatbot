# INTENT_DATABASE: Maps expected conversational contexts to example phrases
INTENT_DATABASE = {
    "algorithm": [
        "how does the feed algorithm work",
        "we need to fix the recommendation algorithm for the app",
        "pushing viral content on the feed algorithm"
    ],
    "feature": [
        "what new features should we add to the social media app",
        "building the direct messaging and story feature",
        "adding a live streaming feature for creators"
    ],
    "design": [
        "the user interface ui design looks a bit mid",
        "we need a cleaner dark mode aesthetic for the app design",
        "improving the mobile app ux and layout"
    ],
    "post": [
        "how users create and publish video posts",
        "should we allow long text posts or just reels",
        "engagement rates on image and video posts"
    ],
    "profile": [
        "customizing user profile pages and bios",
        "showing follower counts and stats on profiles"
    ],
    "backend": [
        "setting up the backend server and api endpoints",
        "handling user authentication and server logic",
        "connecting routes on the backend"
    ],
    "database": [
        "configuring the database to store user posts",
        "sql or nosql database for managing user data",
        "database schema design for comments and likes"
    ],
    "frontend": [
        "building the frontend client interface views",
        "frontend mobile app navigation and routing",
        "styling the frontend screens to look clean"
    ]
}

# GEN_Z_SLANG: Maps response categories to slang-infused messages
GEN_Z_SLANG = {
    "algorithm": [
        "No cap, our feed algorithm needs to push more viral short-form content.",
        "Bet, the algorithm is cooking right now. Users are gonna love the FYP!"
    ],
    "feature": [
        "That feature is straight fire, no cap! Let's prioritize building it.",
        "Adding that would defs give our app major creator rizz and be a huge W."
    ],
    "design": [
        "The UI design is looking a bit mid right now, we gotta make it slay.",
        "Bet, let's keep the dark mode aesthetic clean and modern, no cap."
    ],
    "post": [
        "Posting videos and reels is going to get us insane engagement.",
        "Cap or no cap, do you think text posts will actually take off on our app?"
    ],
    "profile": [
        "User profiles definitely need a custom bio section and follower stats, obviously.",
        "That profile layout is giving clean aesthetics, total slay."
    ],
    "backend": [
        "No cap, a solid backend architecture keeps the app from crashing. Major W!",
        "The backend server is cooking clean APIs right now, bet."
    ],
    "database": [
        "Setting up the database tables securely is straight fire, no cap.",
        "Bet, that database structure is totally optimized for scalability."
    ],
    "frontend": [
        "The frontend UI layout is giving total clean aesthetics, absolute slay.",
        "No cap, a smooth frontend user experience makes the app go viral."
    ],
    "general": [
        "No cap, that social media project idea sounds solid. Tell me more about it!",
        "That's a major W for the roadmap. What else are we adding?"
    ],
    "scope_violation": [
        "That sounds kind of sus... let's stick to talking about our social media project, bet?",
        "No cap, I only want to talk about the social media app right now. What's the next feature?"
    ],
    "easter_egg_dumbel": [
        "Ohh the dumbel is lifting all our heavy backend logic right now, no cap!"
    ]
}

# GEN_Z_KEYWORDS: Slang terms to detect in user inputs
GEN_Z_KEYWORDS = ["bet", "no cap", "cap", "slay", "rizz", "sus", "mid", "fire", "w"]
