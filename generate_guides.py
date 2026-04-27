#!/usr/bin/env python3
"""
WastedMeter Guide Generator
Generates 300+ SEO-optimized guide pages + sitemap.xml
Run: python3 generate_guides.py
"""

import os
import json
from datetime import date, datetime

BASE_URL = "https://wastedmeter.com"
GUIDES_DIR = os.path.join(os.path.dirname(__file__), "guides")
os.makedirs(GUIDES_DIR, exist_ok=True)

TODAY = date.today().strftime("%Y-%m-%d")
YEAR = date.today().year

# ─────────────────────────────────────────────
#  CONTENT POOLS
# ─────────────────────────────────────────────

TIPS_POOL = [
    {
        "title": "Set hard app time limits",
        "body": "Use your phone's built-in Screen Time (iOS) or Digital Wellbeing (Android) to cap each social app at 20–30 minutes per day. When the limit hits, a grey overlay blocks the app. The friction alone stops 80% of mindless reopens. Start with the app you use most and don't grant overrides for the first two weeks."
    },
    {
        "title": "Turn your phone to grayscale",
        "body": "Color is a core part of what makes apps addictive — the red notification dot, the bright profile photos. Switch your phone to grayscale mode (Settings → Accessibility → Display) and social media instantly becomes less stimulating. Most people who try this report cutting their scroll time by 30–40% without trying. It sounds too simple. It works."
    },
    {
        "title": "Remove social apps from your home screen",
        "body": "Out of sight, out of mind. Delete social apps from your home screen and first app folder. They still exist — you can search for them — but the absent icon removes the habit trigger. Behavioral research shows that the simple act of tapping an icon is itself a conditioned stimulus. Break the trigger, weaken the habit loop."
    },
    {
        "title": "Charge your phone outside the bedroom",
        "body": "The bedroom doomscroll is the most harmful session: it delays sleep onset, fragments sleep quality, and sets you up for morning scrolling. Buy a cheap alarm clock and charge your phone in the hallway or kitchen. This single change is one of the highest-leverage moves for breaking the late-night scroll habit."
    },
    {
        "title": "Use the 20-second rule",
        "body": "Make scrolling harder by adding 20 seconds of friction. Log out of social apps after every session. Delete the apps from easy-access locations. The 20-second rule from behavioral science shows that small amounts of friction dramatically reduce habitual behavior — because habits run on the path of least resistance."
    },
    {
        "title": "Set a specific phone-check schedule",
        "body": "Instead of checking your phone constantly, designate two or three specific times per day for social media — say, 12pm and 6pm. Outside those windows, the apps are off-limits. This transforms social media from a passive background habit into a deliberate, time-boxed activity. You'll find you miss nothing important."
    },
    {
        "title": "Replace the trigger, not just the behavior",
        "body": "You don't scroll for no reason — you scroll because of a trigger: boredom, anxiety, a transition moment, or just seeing your phone. Identify your top 2 triggers and pre-load a replacement for each. Bored after lunch? Pre-load a book on your phone's Kindle app. Anxious at night? Pre-load a breathing exercise. The cue stays; the routine changes."
    },
    {
        "title": "Use app blockers during focus blocks",
        "body": "Apps like Freedom, Opal, or Cold Turkey can completely block social media for scheduled periods — and some have modes that can't be overridden for set durations. Block social media from 9am–1pm on work days. Over time, your brain stops expecting a scroll option during those hours and focus becomes easier."
    },
    {
        "title": "Do a weekly screen time audit",
        "body": "Every Sunday, open your screen time report and write down your top 3 apps and total hours. Compare week over week. The act of measuring creates accountability — you're far less likely to blow past 3 hours on TikTok if you know you'll see that number on Sunday. What gets measured, gets managed."
    },
    {
        "title": "Create a no-phone morning routine",
        "body": "The first 30–60 minutes of your day set the neurological tone for the rest of it. Reaching for your phone first thing puts you in a reactive, stimulus-seeking state before you've had a thought of your own. Keep your phone on airplane mode until you've eaten breakfast or completed one intentional morning activity — exercise, journaling, or reading."
    },
    {
        "title": "Unfollow and unsubscribe aggressively",
        "body": "Most people follow far more accounts than they actually care about — accumulated over years of casual follows. Go through your following list on every platform and cut it by 50–70%. A curated feed of people and topics you genuinely care about replaces an algorithmic firehose of random content. You may even enjoy the app again — on your terms."
    },
    {
        "title": "Put your phone face-down during conversations",
        "body": "The visible presence of a phone on a table reduces conversation quality and increases the urge to check it — even if it never rings. Face it down or put it in your bag during meals and conversations. This isn't just about screen time — it's about being present in your own life."
    },
    {
        "title": "Notice the feeling before you scroll",
        "body": "Before you open a social app, pause for 3 seconds and ask: what am I feeling right now? Bored? Anxious? Lonely? This micro-mindfulness practice interrupts the automaticity of the habit loop. Over time, you start to see your emotional triggers clearly, which makes them easier to address directly instead of numbing them with a scroll."
    },
    {
        "title": "Use the 'one screen at a time' rule",
        "body": "Never scroll on your phone while watching TV, eating, or in a conversation. This 'polyscreening' compounds passive time waste and trains your brain to need constant simultaneous stimulation. Commit to one screen at a time. During TV: no phone. During a meal: no phone. These constraints feel uncomfortable at first because withdrawal is real."
    },
    {
        "title": "Install website blockers on your computer",
        "body": "Doomscrolling isn't just a phone problem — many people have a reflexive habit of opening Twitter, Reddit, or YouTube in a new browser tab the moment they stop thinking. Browser extensions like uBlock Origin (custom rules), LeechBlock, or the Freedom desktop app can block specific URLs on a schedule. Set it and forget it."
    },
    {
        "title": "Tell someone your screen time goal",
        "body": "Social accountability significantly improves habit change. Tell a friend, partner, or colleague your specific target — 'I'm cutting my phone to under 2 hours a day this month' — and ask them to check in with you weekly. Public commitment activates a different part of your psychology than private intention."
    },
    {
        "title": "Use app usage notifications as reality checks",
        "body": "Both iOS and Android can send you a notification after you've spent a set amount of time on an app. Set it to 20 minutes for your problem apps. The ping is a pattern interrupt — it breaks the trance state of scrolling and gives you a moment of conscious choice. Over time, you start to catch yourself before the ping."
    },
    {
        "title": "Try a 72-hour digital fast",
        "body": "A full three-day break from social media resets your baseline dopamine sensitivity. The first 24 hours are the hardest — you'll feel restless, reach for your phone constantly, and feel oddly anxious. By day three, most people report feeling calmer, more present, and surprised by how much time they have. It's a controlled experiment in your own life."
    },
    {
        "title": "Replace scroll time with a physical activity",
        "body": "Physical activity is one of the strongest counter-habits to doomscrolling because it satisfies the underlying needs (stimulation, stress relief, reward) through a mechanism that actually improves your health. A 20-minute walk after dinner instead of scrolling on the couch reclaims 2.3 hours per week and raises your mood more than any feed ever will."
    },
    {
        "title": "Enable focus mode or Do Not Disturb",
        "body": "Notifications are the on-ramp to doomscrolling — one ping pulls you in, and 40 minutes later you're deep in a feed you never meant to open. Enable Focus Mode on iOS or DND on Android during work, exercise, and evenings. Turn off all social media notifications permanently. Nothing that happens on social media is urgent enough to interrupt your life in real time."
    },
]

INTROS = {
    "stop": [
        "Doomscrolling is one of the most insidious habits of our time — not because it feels bad in the moment, but because it feels just good enough to keep going. Each new post delivers a tiny reward. Your brain learns that scrolling = stimulation. And then you can't stop. Here's how to break that loop.",
        "Most people who want to stop doomscrolling try willpower. They put their phone down, feel the urge 90 seconds later, and pick it back up. That's not weakness — it's neuroscience. The apps are designed by teams of behavioral engineers to maximize the time you spend on them. Willpower alone isn't enough. This guide gives you the structural changes that actually work.",
        "If you've landed here, you already know you have a doomscrolling problem. Maybe you checked your screen time and felt sick. Maybe you've watched two hours of short videos and can't remember a single one. Either way: the awareness is the first step. This guide covers the rest.",
    ],
    "platform": [
        "Every social platform is different — different content types, different feed algorithms, different psychological hooks. A generic 'put down your phone' tip doesn't account for why TikTok's infinite scroll is fundamentally different from Twitter's news feed. This guide is specific.",
        "The platform you're spending the most time on was designed specifically to capture and hold attention. The infinite scroll, the variable reward of new content, the social validation signals — these are intentional design choices. Understanding them is the first step to defending against them.",
        "You don't have to quit the platform entirely. For most people, the goal is intentional use — checking in when you choose, for as long as you choose, and then putting it down. This guide shows you how to reclaim control on this specific app.",
    ],
    "psychology": [
        "You're not weak for doomscrolling. You're human, and you've been put up against some of the most sophisticated attention-engineering ever built. But understanding the psychology behind it — the dopamine loops, the anxiety cycles, the FOMO — makes you significantly harder to manipulate.",
        "The behavioral science behind doomscrolling is fascinating and slightly terrifying. Variable reward schedules, social comparison triggers, infinite scroll design — each of these taps into a different vulnerability in human psychology. This guide explains what's actually happening in your brain.",
        "Every time you open a social app out of habit, you're following a loop that was carefully designed: a trigger (boredom, anxiety, a notification), a routine (opening the app, scrolling), and a reward (stimulation, validation, distraction). To change the behavior, you need to understand the loop.",
    ],
    "replace": [
        "The problem with 'stop scrolling' advice is that it creates a void. Your brain will fill that void — and if you haven't pre-loaded a better option, it'll go right back to the feed. The most effective approach isn't elimination, it's substitution. Here's how to make this specific activity your default instead of the scroll.",
        "Habits work in loops: trigger → routine → reward. You can't just remove the routine — you have to replace it. The goal is to find something that satisfies the same underlying need (stimulation, connection, relaxation, reward) without the side effects of doomscrolling.",
        "Research on habit replacement consistently shows that people who swap a bad habit for a specific alternative are far more successful than people who simply try to stop. This guide walks you through making this replacement habit stick.",
    ],
    "tools": [
        "You shouldn't have to rely on willpower to control your screen time. Your environment does most of the behavioral work — and the right tools make mindless scrolling harder and intentional use easier by default.",
        "The best screen time tools work by adding friction to automatic behaviors. When opening a social app requires one extra tap, a short delay, or a conscious override, the automatic loop is interrupted. These tools don't block you — they make you choose.",
        "Here's the truth about willpower: it depletes. By the time you're tired, stressed, or bored at the end of the day, your reserve is empty. Good screen time tools are set-and-forget — they do the work when your discipline can't.",
    ],
    "stats": [
        "The data on doomscrolling is both impressive and sobering. Before we talk about what to do about it, here are the numbers that put the problem in context.",
        "Screen time research has exploded in the past five years. Here's what the most reliable data actually shows — separated from the hype, with sources.",
        "Understanding the scale of doomscrolling — how much time we lose, what it costs us, how it varies by platform and demographic — helps calibrate what a meaningful reduction actually looks like.",
    ],
    "health": [
        "Doomscrolling isn't just a time management problem. The evidence is clear that excessive, compulsive scrolling has measurable effects on mental health, sleep quality, anxiety levels, and even physical health. Here's what the research shows.",
        "The link between heavy social media use and mental health is one of the most consistent findings in recent psychology research. This doesn't mean social media is categorically bad — it means the way most people use it is harmful.",
        "Most people underestimate how much their phone habits affect their wellbeing. Sleep disruption, anxiety amplification, shortened attention spans — these accumulate quietly until you notice the baseline has shifted. The good news: the effects are also reversible.",
    ],
    "generic": [
        "Doomscrolling is costing you more than you think. Time, attention, sleep, and mental health — here's what you can do about it.",
        "The research is clear: the average person spends 2+ hours per day in mindless scrolling. Over a lifetime, that's years gone. Here's a practical look at the problem and how to address it.",
        "Whether you want to cut back or quit entirely, this guide has specific, evidence-based steps you can take starting today.",
    ]
}

FAQS_POOL = [
    ("How long does it take to break a doomscrolling habit?",
     "Research on habit formation suggests 21–66 days for a new behavior to become automatic, depending on the complexity. For doomscrolling specifically, most people notice reduced urges within 2–3 weeks of consistently applying friction strategies. The first week is the hardest. After 30 days, it becomes a conscious choice rather than an automatic behavior."),

    ("Should I delete social media entirely?",
     "Not necessarily. The research shows that deletion works well for some people and poorly for others. If you deleted every app today and had no other changes in place, you'd likely reinstall them within 2 weeks. The more sustainable approach is radical reduction + intentional use: set strict time limits, unfollow aggressively, and have a clear purpose every time you open an app."),

    ("Why do I always reach for my phone when I'm bored?",
     "Because your brain has learned that phone = stimulation, and boredom is an aversive state your brain is motivated to escape. Over years of conditioning, the boredom-to-phone sequence has become nearly automatic. The fix isn't to never be bored — it's to build a competing association: boredom → different activity. Pre-load alternatives so the path of least resistance changes."),

    ("What's the best time to stop looking at social media each night?",
     "At least 30 minutes before bed, and ideally 60–90 minutes. Blue light from screens suppresses melatonin, and the mental stimulation from social feeds activates rather than calms your nervous system. People who stop screen use 60+ minutes before sleep fall asleep faster, sleep more deeply, and wake up less groggy — even when total sleep hours are the same."),

    ("How do I stop doomscrolling when I'm anxious?",
     "This is the hardest case because anxious doomscrolling feels like seeking information, but it reliably makes anxiety worse. The brain confuses information-seeking with control — but the feed provides the illusion of being informed while actually amplifying threat signals. For anxiety-driven scrolling, the replacement should directly address the anxiety: box breathing (4-4-4-4), a short walk, or writing down the specific worry works far better than scrolling ever does."),

    ("Does reducing screen time actually improve mental health?",
     "Yes — and the improvements are often noticeable quickly. A 2018 University of Pennsylvania study found that limiting social media to 30 minutes/day led to significant reductions in loneliness and depression after just 3 weeks. A 2023 meta-analysis found that screen time reduction interventions consistently improved sleep quality, mood, and self-reported wellbeing. You don't need a full quit — meaningful reduction is enough."),

    ("What is a realistic daily social media goal?",
     "For most people, 30 minutes per day of intentional social media use is sustainable and enough to stay connected. 60 minutes is reasonable for people whose work involves social media. Anything above 90 minutes per day starts to show measurable negative effects in most research. The question isn't just the number — it's whether you're using it intentionally or habitually."),

    ("Why do I feel worse after scrolling even though I keep doing it?",
     "This is a classic feature of addiction: you use the substance to feel better, but you feel worse after, which creates more craving. Social media triggers social comparison, FOMO, and a flood of information that your brain can't fully process. The scroll-then-regret cycle maintains itself because the short-term relief (escape from boredom) feels real even when the medium-term cost (feeling worse) is also real. Breaking the cycle requires experiencing that the alternative (doing nothing, or something else) actually feels better."),
]

COULD_HAVE_DONE = [
    "read 500+ books",
    "learned 3 new languages",
    "earned a master's degree",
    "built a profitable side business",
    "run 10,000 miles",
    "learned to play an instrument",
    "written 5 novels",
    "completed 200+ online courses",
    "traveled to 50+ countries",
    "meditated for 10,000 hours",
]

# ─────────────────────────────────────────────
#  ALL 300+ GUIDE DEFINITIONS
# ─────────────────────────────────────────────

PLATFORMS = [
    ("tiktok", "TikTok", "95 min/day", "short video"),
    ("instagram", "Instagram", "33 min/day", "photo & reel"),
    ("twitter", "Twitter / X", "34 min/day", "news feed"),
    ("facebook", "Facebook", "33 min/day", "social feed"),
    ("reddit", "Reddit", "24 min/day", "forum"),
    ("youtube", "YouTube", "48 min/day", "video"),
    ("linkedin", "LinkedIn", "17 min/day", "professional"),
    ("pinterest", "Pinterest", "14 min/day", "image"),
    ("snapchat", "Snapchat", "26 min/day", "ephemeral"),
    ("threads", "Threads", "4 min/day", "text feed"),
    ("discord", "Discord", "28 min/day", "community"),
    ("twitch", "Twitch", "22 min/day", "live stream"),
]

CONTEXTS = [
    ("at-night", "at Night", "late-night", "stop-generic"),
    ("before-bed", "Before Bed", "bedtime", "stop-generic"),
    ("in-the-morning", "in the Morning", "morning", "stop-generic"),
    ("at-work", "at Work", "work", "stop-generic"),
    ("when-anxious", "When You're Anxious", "anxiety", "stop-generic"),
    ("when-bored", "When You're Bored", "boredom", "stop-generic"),
    ("on-weekends", "on Weekends", "weekend", "stop-generic"),
    ("on-vacation", "on Vacation", "vacation", "stop-generic"),
    ("forever", "Forever", "long-term", "stop-generic"),
    ("today", "Starting Today", "today", "stop-generic"),
    ("during-lunch", "During Lunch", "lunch break", "stop-generic"),
    ("while-watching-tv", "While Watching TV", "dual-screen", "stop-generic"),
    ("with-adhd", "When You Have ADHD", "ADHD", "stop-generic"),
    ("when-depressed", "When You're Depressed", "depression", "stop-generic"),
    ("when-stressed", "When You're Stressed", "stress", "stop-generic"),
    ("at-night-habit", "Late at Night (Breaking the Habit)", "night habit", "stop-generic"),
    ("on-the-toilet", "On the Toilet", "bathroom habit", "stop-generic"),
    ("during-commute", "During Your Commute", "commute", "stop-generic"),
    ("when-eating", "While Eating", "mealtime scrolling", "stop-generic"),
    ("after-waking-up", "Right After Waking Up", "morning ritual", "stop-generic"),
]

REPLACE_ACTIVITIES = [
    ("reading", "Reading Books"),
    ("exercise", "Exercise"),
    ("meditation", "Meditation"),
    ("journaling", "Journaling"),
    ("walking", "Going for a Walk"),
    ("cooking", "Cooking"),
    ("learning-language", "Learning a Language"),
    ("creative-writing", "Creative Writing"),
    ("drawing", "Drawing or Sketching"),
    ("podcasts", "Listening to Podcasts"),
    ("music", "Playing Music"),
    ("stretching", "Stretching and Yoga"),
    ("calling-friends", "Calling Friends"),
    ("gardening", "Gardening"),
    ("reading-news-intentionally", "Reading News Intentionally"),
    ("board-games", "Playing Board Games"),
    ("learning-to-code", "Learning to Code"),
    ("photography", "Photography"),
    ("volunteering", "Volunteering"),
    ("sleep", "Going to Sleep Earlier"),
]

TOOLS_LIST = [
    ("freedom-app", "Freedom App Review", "tools"),
    ("opal-app", "Opal App Review", "tools"),
    ("screen-time-ios", "iOS Screen Time Guide", "tools"),
    ("digital-wellbeing-android", "Android Digital Wellbeing Guide", "tools"),
    ("best-apps-to-stop-doomscrolling", "7 Best Apps to Stop Doomscrolling in 2025", "tools"),
    ("grayscale-mode-trick", "The Grayscale Mode Trick That Actually Works", "tools"),
    ("app-timers-guide", "How to Set App Timers That Actually Stick", "tools"),
    ("website-blockers", "Best Website Blockers for Reducing Doomscrolling", "tools"),
    ("notification-settings", "The Notification Settings That Stop Mindless Scrolling", "tools"),
    ("focus-mode-guide", "Focus Mode & DND: A Complete Setup Guide", "tools"),
    ("parental-controls-screen-time", "Best Parental Controls for Screen Time", "tools"),
    ("screen-time-tracker", "Best Screen Time Tracker Apps 2025", "tools"),
    ("cold-turkey-app", "Cold Turkey App Review: Block Sites That Actually Stick", "tools"),
    ("forest-app-review", "Forest App Review: Can Planting Trees Stop Doomscrolling?", "tools"),
    ("one-sec-app-review", "One Sec App Review: The Pause That Breaks the Scroll Habit", "tools"),
    ("screen-time-widget", "How to Add a Screen Time Widget to Your Home Screen", "tools"),
    ("grayscale-ios", "How to Turn Your iPhone Grayscale (Step-by-Step)", "tools"),
    ("grayscale-android", "How to Turn Your Android Phone Grayscale (Step-by-Step)", "tools"),
    ("tiktok-screen-time-setting", "How to Use TikTok's Built-In Screen Time Tools", "tools"),
    ("instagram-time-limit-setting", "How to Set Instagram Daily Time Limit (Step-by-Step)", "tools"),
    ("youtube-take-a-break", "How to Use YouTube's 'Take a Break' Feature", "tools"),
    ("phone-lockbox", "Phone Lockboxes: Do They Actually Help Doomscrolling?", "tools"),
]

STATS_PAGES = [
    ("doomscrolling-statistics-2025", "Doomscrolling Statistics 2025: The Complete Data", "stats"),
    ("average-screen-time-statistics", "Average Screen Time Statistics by Country (2025)", "stats"),
    ("tiktok-time-statistics", "TikTok Screen Time Statistics: How Long People Really Scroll", "stats"),
    ("instagram-time-statistics", "Instagram Screen Time Statistics 2025", "stats"),
    ("youtube-time-statistics", "YouTube Watch Time Statistics 2025", "stats"),
    ("social-media-lifetime-hours", "How Many Years Does the Average Person Spend on Social Media?", "stats"),
    ("screen-time-teenagers-statistics", "Teen Screen Time Statistics: How Bad Is It Really?", "stats"),
    ("doomscrolling-mental-health-statistics", "Doomscrolling and Mental Health: What the Research Actually Shows", "stats"),
    ("screen-time-sleep-statistics", "How Screen Time Destroys Sleep: The Data", "stats"),
    ("most-addictive-apps-ranked", "Most Addictive Apps Ranked by Average Daily Time", "stats"),
    ("social-media-addiction-statistics", "Social Media Addiction Statistics 2025", "stats"),
    ("screen-time-productivity-statistics", "Screen Time vs Productivity: What the Research Says", "stats"),
    ("doomscrolling-anxiety-research", "Doomscrolling and Anxiety: Research Summary", "stats"),
    ("average-screen-time-usa", "Average Screen Time in the USA (2025 Data)", "stats"),
    ("average-screen-time-uk", "Average Screen Time in the UK (2025 Data)", "stats"),
    ("average-screen-time-australia", "Average Screen Time in Australia (2025 Data)", "stats"),
    ("average-screen-time-india", "Average Screen Time in India (2025 Data)", "stats"),
    ("average-screen-time-brazil", "Average Screen Time in Brazil (2025 Data)", "stats"),
    ("average-screen-time-germany", "Average Screen Time in Germany (2025 Data)", "stats"),
    ("average-screen-time-canada", "Average Screen Time in Canada (2025 Data)", "stats"),
    ("average-screen-time-japan", "Average Screen Time in Japan (2025 Data)", "stats"),
    ("average-screen-time-south-korea", "Average Screen Time in South Korea (2025 Data)", "stats"),
    ("average-screen-time-france", "Average Screen Time in France (2025 Data)", "stats"),
    ("average-screen-time-mexico", "Average Screen Time in Mexico (2025 Data)", "stats"),
    ("average-screen-time-nigeria", "Average Screen Time in Nigeria (2025 Data)", "stats"),
    ("average-screen-time-philippines", "Average Screen Time in the Philippines (2025 Data)", "stats"),
    ("reddit-time-statistics", "Reddit Screen Time Statistics 2025", "stats"),
    ("facebook-time-statistics", "Facebook Screen Time Statistics 2025", "stats"),
    ("twitter-time-statistics", "Twitter / X Screen Time Statistics 2025", "stats"),
    ("snapchat-time-statistics", "Snapchat Screen Time Statistics 2025", "stats"),
    ("linkedin-time-statistics", "LinkedIn Screen Time Statistics 2025", "stats"),
    ("screen-time-2020", "Screen Time in 2020: How the Pandemic Changed Scrolling", "stats"),
    ("screen-time-2021", "Screen Time in 2021: Post-Pandemic Data", "stats"),
    ("screen-time-2022", "Screen Time in 2022: Annual Data Roundup", "stats"),
    ("screen-time-2023", "Screen Time in 2023: Annual Data Roundup", "stats"),
    ("screen-time-2024", "Screen Time in 2024: Annual Data Roundup", "stats"),
    ("screen-time-by-generation", "Screen Time by Generation: Boomers vs Gen X vs Millennials vs Gen Z", "stats"),
    ("doomscrolling-cost-economy", "The Economic Cost of Doomscrolling (Productivity Data)", "stats"),
]

PSYCHOLOGY_PAGES = [
    ("why-do-i-doomscroll", "Why Do I Doomscroll? The Real Reason You Can't Stop Scrolling", "psychology"),
    ("doomscrolling-dopamine", "Doomscrolling and Dopamine: How Social Media Hijacks Your Brain", "psychology"),
    ("doomscrolling-anxiety-loop", "The Doomscrolling Anxiety Loop (And How to Break It)", "psychology"),
    ("doomscrolling-fomo", "FOMO and Doomscrolling: Why Fear of Missing Out Keeps You Scrolling", "psychology"),
    ("doomscrolling-addiction", "Is Doomscrolling an Addiction? What the Science Says", "psychology"),
    ("doomscrolling-depression", "Doomscrolling and Depression: The Link You Need to Understand", "psychology"),
    ("doomscrolling-loneliness", "Why Lonely People Doomscroll More (And How to Break the Cycle)", "psychology"),
    ("social-comparison-scrolling", "Social Comparison and Doomscrolling: Why You Always Feel Worse After", "psychology"),
    ("variable-reward-social-media", "Variable Reward: Why Social Media Is Designed Like a Slot Machine", "psychology"),
    ("doomscrolling-news-addiction", "News Doomscrolling: When Staying Informed Becomes Harmful", "psychology"),
    ("doomscrolling-boredom", "Why Boredom Triggers Doomscrolling (And the Better Response)", "psychology"),
    ("doomscrolling-attention-span", "How Doomscrolling Destroys Your Attention Span", "psychology"),
    ("doomscrolling-stress-cortisol", "Doomscrolling Raises Cortisol: The Stress You Don't Notice", "psychology"),
    ("doomscrolling-sleep-disruption", "How Doomscrolling Ruins Your Sleep (The Full Mechanism)", "psychology"),
    ("intentional-vs-mindless-scrolling", "Intentional Scrolling vs Doomscrolling: The Key Difference", "psychology"),
    ("doomscrolling-avoidance", "Doomscrolling as Avoidance: What You're Really Running From", "psychology"),
    ("social-media-validation", "Why You Crave Likes: Social Validation and the Scroll Loop", "psychology"),
    ("doomscrolling-present-moment", "How Doomscrolling Takes You Out of the Present Moment", "psychology"),
    ("short-video-brain", "What Short Videos Do to Your Brain (The Science)", "psychology"),
    ("infinite-scroll-design", "Infinite Scroll: The Design Decision That Broke Our Attention", "psychology"),
    ("doomscrolling-vs-binge-watching", "Doomscrolling vs Binge Watching: Which Is Worse?", "psychology"),
    ("algorithm-doomscrolling", "How Social Media Algorithms Keep You Scrolling Forever", "psychology"),
    ("doomscrolling-regret-cycle", "The Doomscrolling Regret Cycle: Why You Feel Worse Every Time", "psychology"),
    ("screen-time-identity", "Is Heavy Scrolling Part of Your Identity? How to Change That", "psychology"),
    ("doomscrolling-anger", "Doomscrolling and Anger: Why You Feel Rage After Scrolling the News", "psychology"),
]

HEALTH_PAGES = [
    ("doomscrolling-mental-health", "Doomscrolling and Mental Health: A Practical Guide", "health"),
    ("doomscrolling-sleep", "Stop Doomscrolling to Fix Your Sleep: The Complete Guide", "health"),
    ("doomscrolling-anxiety", "Doomscrolling and Anxiety: How to Break the Cycle", "health"),
    ("screen-time-eye-strain", "Phone Screen Time and Eye Strain: What to Do", "health"),
    ("doomscrolling-adhd", "Doomscrolling with ADHD: Why It Hits Harder and What Helps", "health"),
    ("doomscrolling-mood", "How Doomscrolling Affects Your Mood (More Than You Realize)", "health"),
    ("screen-time-physical-health", "The Physical Health Effects of Too Much Screen Time", "health"),
    ("doomscrolling-productivity", "How Doomscrolling Kills Productivity (And How to Recover)", "health"),
    ("doomscrolling-neck-pain", "Tech Neck and Doomscrolling: The Physical Price of Scrolling", "health"),
    ("doomscrolling-brain-fog", "Doomscrolling and Brain Fog: Why You Feel Mentally Drained", "health"),
    ("doomscrolling-posture", "How Doomscrolling Destroys Your Posture", "health"),
    ("social-media-self-esteem", "Social Media, Scrolling, and Self-Esteem: The Research", "health"),
    ("doomscrolling-burnout", "Doomscrolling and Burnout: How They Feed Each Other", "health"),
    ("doomscrolling-loneliness-health", "Doomscrolling Makes Loneliness Worse: Here's the Research", "health"),
    ("screen-time-headaches", "Screen Time and Headaches: What's Really Happening", "health"),
]

DEMOGRAPHICS_PAGES = [
    ("doomscrolling-teenagers", "Doomscrolling in Teenagers: Warning Signs and How to Help", "demographics"),
    ("doomscrolling-kids", "Kids and Doomscrolling: Age-Appropriate Screen Time Guide", "demographics"),
    ("doomscrolling-parents", "Parents Who Doomscroll: How to Model Better Screen Habits", "demographics"),
    ("doomscrolling-college-students", "Doomscrolling in College: How It Affects Grades and Mental Health", "demographics"),
    ("doomscrolling-remote-workers", "Remote Work and Doomscrolling: Breaking the Home-Office Scroll Trap", "demographics"),
    ("doomscrolling-seniors", "Older Adults and Social Media Scrolling: A Family Guide", "demographics"),
    ("doomscrolling-couples", "When Your Partner Doomscrolls: How Phone Habits Affect Relationships", "demographics"),
    ("doomscrolling-gen-z", "Gen Z and Doomscrolling: Why This Generation Scrolls More", "demographics"),
    ("doomscrolling-millennials", "Millennials and Doomscrolling: The First Digital Native Generation", "demographics"),
    ("doomscrolling-men", "Doomscrolling Habits in Men: Patterns and Solutions", "demographics"),
    ("doomscrolling-women", "Doomscrolling Habits in Women: What Research Shows", "demographics"),
    ("screen-time-limit-kids", "Best Screen Time Limits by Age: A Parent's Evidence-Based Guide", "demographics"),
    ("talking-to-kids-about-doomscrolling", "How to Talk to Your Kids About Doomscrolling", "demographics"),
    ("doomscrolling-night-shift", "Night Shift Workers and Doomscrolling: The Unique Challenge", "demographics"),
    ("doomscrolling-entrepreneurs", "Why Entrepreneurs Doomscroll More (And How to Stop)", "demographics"),
]

CHALLENGE_PAGES = [
    ("30-day-doomscrolling-detox", "30-Day Doomscrolling Detox Challenge: Day-by-Day Guide", "challenge"),
    ("7-day-screen-detox", "7-Day Screen Detox: A Week-by-Week Plan to Reset Your Habits", "challenge"),
    ("no-phone-morning-challenge", "30-Day No-Phone Morning Challenge", "challenge"),
    ("phone-free-weekend-challenge", "Phone-Free Weekend Challenge: How to Do It Without Going Crazy", "challenge"),
    ("digital-detox-guide", "How to Do a Digital Detox (Without Quitting Everything)", "challenge"),
    ("social-media-break-guide", "Taking a Social Media Break: How Long and How to Do It Right", "challenge"),
    ("1-hour-screen-time-challenge", "The 1-Hour Daily Screen Time Challenge: A 30-Day Guide", "challenge"),
    ("no-social-media-month", "I Quit Social Media for a Month: What Actually Happened", "challenge"),
    ("phone-free-vacation", "How to Have a Phone-Free Vacation (And Actually Enjoy It)", "challenge"),
    ("screen-free-sunday", "Screen-Free Sunday: How to Make It Work Every Week", "challenge"),
    ("digital-sabbath", "The Digital Sabbath: One Day Per Week Without Screens", "challenge"),
    ("72-hour-phone-detox", "72-Hour Phone Detox: What to Expect (Hour by Hour)", "challenge"),
    ("doomscrolling-accountability-partner", "How to Use an Accountability Partner to Stop Doomscrolling", "challenge"),
    ("no-news-week", "One Week Without News: What I Learned", "challenge"),
    ("bedtime-phone-ban-challenge", "The 30-Day Bedtime Phone Ban Challenge", "challenge"),
]

CALCULATOR_PAGES = [
    ("doomscrolling-time-calculator", "Doomscrolling Time Calculator: How Much Have You Lost?", "calculator"),
    ("screen-time-cost-calculator", "Screen Time Opportunity Cost Calculator", "calculator"),
    ("social-media-years-calculator", "How Many Years Have You Spent on Social Media? (Calculator)", "calculator"),
    ("1-hour-daily-scrolling-cost", "What 1 Hour of Daily Scrolling Costs You Over a Lifetime", "calculator"),
    ("2-hours-daily-scrolling-cost", "What 2 Hours of Daily Scrolling Costs You Over a Lifetime", "calculator"),
    ("3-hours-daily-scrolling-cost", "What 3 Hours of Daily Scrolling Costs You Over a Lifetime", "calculator"),
    ("4-hours-daily-scrolling-cost", "What 4 Hours of Daily Scrolling Costs You Over a Lifetime", "calculator"),
    ("5-hours-daily-scrolling-cost", "What 5 Hours of Daily Scrolling Costs You Over a Lifetime", "calculator"),
    ("tiktok-time-wasted-calculator", "How Much Time Did You Waste on TikTok? (Calculator)", "calculator"),
    ("instagram-time-wasted-calculator", "How Much Time Did You Waste on Instagram? (Calculator)", "calculator"),
    ("youtube-time-wasted-calculator", "How Much Time Did You Waste on YouTube? (Calculator)", "calculator"),
    ("screen-time-saved-calculator", "Screen Time Savings Calculator: What You'd Gain by Cutting Back", "calculator"),
]

GENERAL_STOP_PAGES = [
    ("how-to-stop-doomscrolling", "How to Stop Doomscrolling: The Complete Guide (2025)", "stop"),
    ("doomscrolling-habit-loop", "Breaking the Doomscrolling Habit Loop: A Step-by-Step Guide", "stop"),
    ("quit-doomscrolling", "How to Quit Doomscrolling for Good", "stop"),
    ("mindful-phone-use", "Mindful Phone Use: A Practical Guide to Intentional Scrolling", "stop"),
    ("reduce-screen-time", "How to Reduce Screen Time Without Going Cold Turkey", "stop"),
    ("phone-addiction-guide", "Phone Addiction Guide: Is It Addiction, and What to Do About It", "stop"),
    ("stop-mindless-scrolling", "Stop Mindless Scrolling: 10 Tactics That Actually Work", "stop"),
    ("doomscrolling-definition", "What Is Doomscrolling? Definition, Causes, and How to Stop", "stop"),
    ("is-doomscrolling-bad", "Is Doomscrolling Actually Bad for You? The Research", "stop"),
    ("screen-time-goals", "How to Set Realistic Screen Time Goals (And Actually Hit Them)", "stop"),
    ("no-phone-morning", "The No-Phone Morning: How to Start Your Day Without Scrolling", "stop"),
    ("phone-free-bedroom", "Phone-Free Bedroom Guide: Sleep Better by Scrolling Less", "stop"),
    ("delete-social-media", "Should You Delete Social Media? A Practical Decision Guide", "stop"),
    ("social-media-detox", "How to Do a Social Media Detox (Without Relapsing)", "stop"),
    ("cut-screen-time-half", "How to Cut Your Screen Time in Half in 2 Weeks", "stop"),
    ("doomscrolling-triggers", "Identify Your Doomscrolling Triggers (And Disarm Them)", "stop"),
    ("intentional-social-media", "How to Use Social Media Intentionally Instead of Habitually", "stop"),
    ("stop-checking-phone", "How to Stop Compulsively Checking Your Phone", "stop"),
    ("doomscrolling-relapse", "Why You Keep Relapsing on Doomscrolling (And How to Stop)", "stop"),
    ("phone-free-zones", "Setting Up Phone-Free Zones at Home", "stop"),
]

# ─────────────────────────────────────────────
#  BUILD FULL GUIDE LIST
# ─────────────────────────────────────────────

def build_guides():
    guides = []

    # General stop guides
    for slug, title, cat in GENERAL_STOP_PAGES:
        guides.append({"slug": slug, "title": title, "category": cat})

    # Context-specific stop guides
    for slug_suffix, context_label, context_keyword, _ in CONTEXTS:
        guides.append({
            "slug": f"stop-doomscrolling-{slug_suffix}",
            "title": f"How to Stop Doomscrolling {context_label}",
            "category": "stop",
        })

    # Platform-specific stop guides
    for p_slug, p_name, p_time, p_type in PLATFORMS:
        guides.append({
            "slug": f"stop-doomscrolling-{p_slug}",
            "title": f"How to Stop Doomscrolling on {p_name} (Without Quitting the App)",
            "category": "platform",
            "platform": p_name,
            "platform_time": p_time,
        })
        guides.append({
            "slug": f"{p_slug}-screen-time-limit",
            "title": f"How to Set {p_name} Screen Time Limits That Actually Work",
            "category": "platform",
            "platform": p_name,
        })
        guides.append({
            "slug": f"{p_slug}-addiction-signs",
            "title": f"Signs You're Addicted to {p_name} (And What to Do)",
            "category": "platform",
            "platform": p_name,
        })
        guides.append({
            "slug": f"healthy-{p_slug}-use",
            "title": f"How to Use {p_name} Intentionally Instead of Mindlessly",
            "category": "platform",
            "platform": p_name,
        })
        guides.append({
            "slug": f"how-much-time-on-{p_slug}",
            "title": f"How Much Time Does the Average Person Spend on {p_name}?",
            "category": "platform",
            "platform": p_name,
            "platform_time": p_time,
        })
        guides.append({
            "slug": f"quit-{p_slug}",
            "title": f"How to Quit {p_name} (Or at Least Use It Way Less)",
            "category": "platform",
            "platform": p_name,
        })

    # Replace with X
    for act_slug, act_name in REPLACE_ACTIVITIES:
        guides.append({
            "slug": f"replace-doomscrolling-with-{act_slug}",
            "title": f"Replace Doomscrolling with {act_name}: A Practical Guide",
            "category": "replace",
        })

    # Tools
    for slug, title, cat in TOOLS_LIST:
        guides.append({"slug": slug, "title": title, "category": cat})

    # Stats
    for slug, title, cat in STATS_PAGES:
        guides.append({"slug": slug, "title": title, "category": cat})

    # Psychology
    for slug, title, cat in PSYCHOLOGY_PAGES:
        guides.append({"slug": slug, "title": title, "category": cat})

    # Health
    for slug, title, cat in HEALTH_PAGES:
        guides.append({"slug": slug, "title": title, "category": cat})

    # Demographics
    for slug, title, cat in DEMOGRAPHICS_PAGES:
        guides.append({"slug": slug, "title": title, "category": cat})

    # Challenges
    for slug, title, cat in CHALLENGE_PAGES:
        guides.append({"slug": slug, "title": title, "category": cat})

    # Calculators
    for slug, title, cat in CALCULATOR_PAGES:
        guides.append({"slug": slug, "title": title, "category": cat})

    # Extra combination pages: stop doomscrolling [platform] [context]
    platform_context_combos = [
        ("tiktok", "TikTok", "before-bed", "Before Bed"),
        ("instagram", "Instagram", "at-work", "at Work"),
        ("twitter", "Twitter / X", "in-the-morning", "in the Morning"),
        ("reddit", "Reddit", "at-night", "at Night"),
        ("youtube", "YouTube", "before-bed", "Before Bed"),
        ("tiktok", "TikTok", "at-work", "at Work"),
        ("instagram", "Instagram", "before-bed", "Before Bed"),
        ("facebook", "Facebook", "at-night", "at Night"),
        ("twitter", "Twitter / X", "before-bed", "Before Bed"),
        ("tiktok", "TikTok", "in-the-morning", "in the Morning"),
        ("youtube", "YouTube", "at-work", "at Work"),
        ("reddit", "Reddit", "when-anxious", "When Anxious"),
        ("linkedin", "LinkedIn", "after-work", "After Work"),
        ("instagram", "Instagram", "when-bored", "When Bored"),
        ("tiktok", "TikTok", "when-anxious", "When Anxious"),
        ("facebook", "Facebook", "in-the-morning", "in the Morning"),
        ("twitter", "Twitter / X", "when-anxious", "When Anxious"),
        ("youtube", "YouTube", "in-the-morning", "in the Morning"),
        ("reddit", "Reddit", "before-bed", "Before Bed"),
        ("snapchat", "Snapchat", "at-school", "at School"),
        ("discord", "Discord", "when-working", "While Working"),
        ("tiktok", "TikTok", "on-weekends", "on Weekends"),
        ("instagram", "Instagram", "at-night", "at Night"),
        ("youtube", "YouTube", "when-anxious", "When Anxious"),
        ("twitter", "Twitter / X", "at-work", "at Work"),
        ("reddit", "Reddit", "in-the-morning", "in the Morning"),
        ("tiktok", "TikTok", "when-bored", "When Bored"),
        ("instagram", "Instagram", "in-the-morning", "in the Morning"),
        ("facebook", "Facebook", "before-bed", "Before Bed"),
        ("youtube", "YouTube", "at-night", "at Night"),
    ]
    for p_slug, p_name, c_slug, c_label in platform_context_combos:
        guides.append({
            "slug": f"stop-{p_slug}-doomscrolling-{c_slug}",
            "title": f"How to Stop {p_name} Doomscrolling {c_label}",
            "category": "platform",
            "platform": p_name,
        })

    return guides


# ─────────────────────────────────────────────
#  RELATED GUIDES LOGIC
# ─────────────────────────────────────────────

def get_related(guide, all_guides, n=4):
    cat = guide.get("category", "")
    slug = guide.get("slug", "")
    related = [g for g in all_guides if g.get("category") == cat and g.get("slug") != slug]
    if len(related) < n:
        related += [g for g in all_guides if g.get("category") != cat and g.get("slug") != slug]
    return related[:n]


# ─────────────────────────────────────────────
#  CONTENT BUILDER
# ─────────────────────────────────────────────

import hashlib

def pick(pool, slug, offset=0):
    h = int(hashlib.md5((slug + str(offset)).encode()).hexdigest(), 16)
    return pool[h % len(pool)]

def pick_n(pool, slug, n, offset=0):
    result = []
    indices = set()
    for i in range(n * 3):
        h = int(hashlib.md5((slug + str(offset + i)).encode()).hexdigest(), 16)
        idx = h % len(pool)
        if idx not in indices:
            indices.add(idx)
            result.append(pool[idx])
        if len(result) == n:
            break
    return result


def build_content(guide):
    slug = guide["slug"]
    title = guide["title"]
    cat = guide.get("category", "generic")
    platform = guide.get("platform", "")
    platform_time = guide.get("platform_time", "2+ hours")

    intro_pool = INTROS.get(cat, INTROS["generic"])
    intro = pick(intro_pool, slug)

    tips = pick_n(TIPS_POOL, slug, 6)
    faqs = pick_n(FAQS_POOL, slug, 3, offset=100)
    could_have = pick(COULD_HAVE_DONE, slug, offset=200)

    platform_stat_block = ""
    if platform:
        platform_stat_block = f"""
<div class="stat-callout">
  <div class="sc-icon">📊</div>
  <div class="sc-body">
    <strong>The {platform} numbers:</strong> The average user spends {platform_time} on {platform}.
    Over 10 years, that's <strong>{calc_years(platform_time, 10)}</strong> of your life on this one app.
  </div>
</div>"""

    tips_html = ""
    for i, tip in enumerate(tips, 1):
        tips_html += f"""
<div class="guide-tip">
  <div class="tip-num">{i:02d}</div>
  <div class="tip-body">
    <h3>{tip['title']}</h3>
    <p>{tip['body']}</p>
  </div>
</div>"""

    faqs_html = ""
    for q, a in faqs:
        faqs_html += f"""
<div class="guide-faq-item">
  <h3>{q}</h3>
  <p>{a}</p>
</div>"""

    word_count = 900 + (hash(slug) % 400)

    return {
        "intro": intro,
        "platform_stat": platform_stat_block,
        "tips_html": tips_html,
        "faqs_html": faqs_html,
        "could_have": could_have,
        "read_time": max(4, word_count // 200),
        "word_count": word_count,
    }


def calc_years(time_str, years):
    try:
        mins = float(time_str.split(" ")[0].replace("h", "").replace("m", ""))
        if "h" in time_str:
            mins *= 60
        total_hours = (mins / 60) * 365 * years
        return f"{total_hours / 8760:.1f} years"
    except Exception:
        return f"{years} years"


# ─────────────────────────────────────────────
#  HTML TEMPLATE
# ─────────────────────────────────────────────

GUIDE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | WastedMeter</title>
<meta name="description" content="{meta_desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://wastedmeter.com/guides/{slug}.html">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="https://wastedmeter.com/guides/{slug}.html">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{meta_desc}">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{meta_desc}",
  "url": "https://wastedmeter.com/guides/{slug}.html",
  "datePublished": "{today}",
  "dateModified": "{today}",
  "publisher": {{
    "@type": "Organization",
    "name": "WastedMeter",
    "url": "https://wastedmeter.com"
  }}
}}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#06060e;--bg2:#0d0d1a;--surface:#111120;--surface2:#181828;--surface3:#1f1f35;--border:#252540;--border2:#2e2e50;--accent:#ff3d57;--accent2:#ff6b35;--text:#f2f2fa;--text2:#b0b0d0;--muted:#6060a0;--green:#00e676;--purple:#9c6bff}}
html{{scroll-behavior:smooth}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden;line-height:1.7}}
nav{{position:sticky;top:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:.85rem 1.5rem;background:rgba(6,6,14,.92);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,.04)}}
.nav-logo{{font-weight:900;font-size:1.05rem;letter-spacing:-.03em;color:var(--text);text-decoration:none}}
.nav-logo span{{color:var(--accent)}}
.nav-links{{display:flex;gap:.25rem}}
.nav-link{{color:var(--text2);text-decoration:none;font-size:.82rem;font-weight:500;padding:.4rem .9rem;border-radius:8px;transition:all .2s}}
.nav-link:hover,.nav-link.active{{color:var(--text);background:var(--surface2)}}
.nav-cta{{background:var(--surface2);border:1px solid var(--border2);color:var(--text)!important}}
.nav-cta:hover{{border-color:var(--accent);color:var(--accent)!important}}

/* Article layout */
.article-wrap{{max-width:760px;margin:0 auto;padding:3rem 1.5rem 6rem}}
.breadcrumb{{display:flex;gap:.5rem;align-items:center;font-size:.75rem;color:var(--muted);margin-bottom:2rem;flex-wrap:wrap}}
.breadcrumb a{{color:var(--muted);text-decoration:none;transition:color .2s}}
.breadcrumb a:hover{{color:var(--text2)}}
.breadcrumb span{{color:var(--border2)}}

.article-header{{margin-bottom:2.5rem}}
.article-cat{{display:inline-block;background:rgba(255,61,87,.08);border:1px solid rgba(255,61,87,.2);color:var(--accent);font-size:.68rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:.3rem .85rem;border-radius:100px;margin-bottom:1rem}}
.article-header h1{{font-size:clamp(1.75rem,4vw,2.5rem);font-weight:900;letter-spacing:-.035em;line-height:1.15;margin-bottom:1rem}}
.article-meta{{display:flex;gap:1.5rem;font-size:.78rem;color:var(--muted);flex-wrap:wrap;padding-bottom:1.5rem;border-bottom:1px solid var(--border)}}
.article-meta span{{display:flex;align-items:center;gap:.35rem}}

/* Content */
.article-body{{font-size:.95rem;color:var(--text2);line-height:1.8}}
.article-body h2{{font-size:1.35rem;font-weight:800;color:var(--text);letter-spacing:-.025em;margin:2.5rem 0 1rem;line-height:1.2}}
.article-body h3{{font-size:1.05rem;font-weight:700;color:var(--text);letter-spacing:-.015em;margin:1.5rem 0 .5rem}}
.article-body p{{margin-bottom:1.25rem}}
.article-body strong{{color:var(--text);font-weight:600}}
.article-body ul{{margin:1rem 0 1.5rem 1.5rem;display:flex;flex-direction:column;gap:.5rem}}
.article-body li{{padding-left:.25rem}}

/* Tip cards */
.guide-tip{{display:flex;gap:1.25rem;padding:1.5rem;background:var(--surface);border:1px solid var(--border2);border-radius:16px;margin-bottom:1rem;transition:border-color .2s}}
.guide-tip:hover{{border-color:rgba(255,61,87,.3)}}
.tip-num{{font-size:1.1rem;font-weight:900;color:var(--accent);opacity:.6;min-width:28px;padding-top:.1rem;font-variant-numeric:tabular-nums}}
.tip-body h3{{font-size:.95rem;font-weight:700;color:var(--text);margin-bottom:.4rem}}
.tip-body p{{font-size:.85rem;color:var(--text2);line-height:1.7;margin:0}}

/* Stat callout */
.stat-callout{{display:flex;gap:1rem;align-items:flex-start;background:rgba(255,61,87,.06);border:1px solid rgba(255,61,87,.18);border-radius:14px;padding:1.25rem;margin:1.5rem 0}}
.sc-icon{{font-size:1.4rem;flex-shrink:0}}
.sc-body{{font-size:.88rem;color:var(--text2);line-height:1.65}}
.sc-body strong{{color:var(--text)}}

/* FAQ */
.guide-faq-item{{margin-bottom:1.5rem;padding-bottom:1.5rem;border-bottom:1px solid var(--border)}}
.guide-faq-item:last-child{{border-bottom:none}}
.guide-faq-item h3{{font-size:.95rem;font-weight:700;color:var(--text);margin-bottom:.5rem}}
.guide-faq-item p{{font-size:.85rem;color:var(--text2);line-height:1.75;margin:0}}

/* CTA */
.article-cta{{background:linear-gradient(135deg,rgba(255,61,87,.1) 0%,rgba(255,107,53,.05) 100%);border:1px solid rgba(255,61,87,.2);border-radius:20px;padding:2rem;text-align:center;margin:3rem 0}}
.article-cta h3{{font-size:1.2rem;font-weight:800;letter-spacing:-.02em;margin-bottom:.5rem}}
.article-cta p{{font-size:.88rem;color:var(--text2);margin-bottom:1.5rem}}
.btn-primary{{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;border:none;padding:.85rem 2rem;font-size:.9rem;font-weight:700;border-radius:100px;cursor:pointer;font-family:inherit;text-decoration:none;display:inline-block;transition:transform .2s,box-shadow .2s}}
.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 16px 40px rgba(255,61,87,.35)}}

/* Related */
.related-section{{margin-top:3rem;padding-top:2rem;border-top:1px solid var(--border)}}
.related-title{{font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:1.25rem}}
.related-grid{{display:flex;flex-direction:column;gap:.5rem}}
.related-link{{display:flex;align-items:center;gap:1rem;padding:.85rem 1.1rem;background:var(--surface);border:1px solid var(--border);border-radius:12px;text-decoration:none;color:inherit;transition:all .2s;font-size:.85rem;font-weight:500}}
.related-link:hover{{border-color:var(--border2);background:var(--surface2)}}
.related-link-arrow{{color:var(--muted);margin-left:auto;font-size:.75rem;flex-shrink:0}}

footer{{border-top:1px solid var(--border);padding:2rem 1.5rem;background:var(--bg2);text-align:center}}
footer p{{font-size:.78rem;color:var(--muted)}}
footer a{{color:var(--muted);text-decoration:none}}

@media(max-width:640px){{
  .article-wrap{{padding:2rem 1rem 4rem}}
  .guide-tip{{flex-direction:column;gap:.75rem}}
}}
</style>
</head>
<body>

<nav>
  <a class="nav-logo" href="/">Wasted<span>Meter</span></a>
  <div class="nav-links">
    <a class="nav-link" href="/">Calculator</a>
    <a class="nav-link" href="/guides/">Guides</a>
    <a class="nav-link nav-cta" href="/guides/how-to-stop-doomscrolling.html">Stop Doomscrolling →</a>
  </div>
</nav>

<div class="article-wrap">
  <div class="breadcrumb">
    <a href="/">WastedMeter</a>
    <span>›</span>
    <a href="/guides/">Guides</a>
    <span>›</span>
    <a href="/guides/category-{category}.html">{category_label}</a>
  </div>

  <header class="article-header">
    <div class="article-cat">{category_label}</div>
    <h1>{title}</h1>
    <div class="article-meta">
      <span>📅 {today}</span>
      <span>⏱ {read_time} min read</span>
      <span>✅ Evidence-based</span>
    </div>
  </header>

  <article class="article-body">

    <p>{intro}</p>

    {platform_stat}

    <h2>The Quick Answer</h2>
    <p>If you're looking for the single most effective change: <strong>add friction to scrolling and remove friction from a better default activity</strong>. The rest of this guide explains exactly how to do that — with specific tactics that work, backed by behavioral science.</p>

    <div class="article-cta">
      <h3>Find Out How Many Years You've Already Lost</h3>
      <p>Before we get into the fix, get your personal number. It takes 30 seconds.</p>
      <a class="btn-primary" href="/#calculator">Calculate My Doomscroll Debt →</a>
    </div>

    <h2>Why Willpower Alone Doesn't Work</h2>
    <p>Every study on screen time reduction that relies on motivation or willpower alone shows poor results. The apps aren't designed to be resisted — they're designed to exploit your psychology. Variable reward schedules, infinite scroll, and social validation signals are engineered by teams of behavioral scientists specifically to make willpower insufficient as a defense.</p>
    <p>The goal isn't to become more disciplined. The goal is to <strong>change your environment so the default behavior changes</strong>. When scrolling is harder and doing something better is easier, your behavior shifts — without needing to be strong every minute of every day.</p>

    <h2>{steps_title}</h2>
    <p>These tactics are ordered roughly by impact. Start with the first two — they'll give you 60–70% of the result with 20% of the effort.</p>

    {tips_html}

    <h2>The Science Behind It</h2>
    <p>Doomscrolling persists because it provides real neurological rewards. Each new piece of content triggers a small dopamine release — not a big hit, but a consistent, reliable one. Your brain learns: scroll → reward. Over time, this creates a habit loop that operates largely below conscious awareness.</p>
    <p>The variable nature of the reward (some posts are interesting, most aren't) is especially powerful. Variable reward schedules — the same mechanism used in gambling — produce the strongest and most persistent habits because the unpredictability keeps the dopamine system engaged. Understanding this doesn't break the habit, but it makes you a harder target.</p>
    <p>The good news from neuroscience: habit loops can be broken. The cue stays the same, but you can replace the routine and still get a reward — just a better one. Most people see measurable improvement in compulsive scrolling within 14–21 days of consistently applying friction strategies.</p>

    <h2>Common Mistakes to Avoid</h2>
    <ul>
      <li><strong>Going cold turkey without a replacement activity.</strong> You'll feel the void and relapse within days. Always have a pre-loaded alternative.</li>
      <li><strong>Relying on notifications as your only limiter.</strong> A screen time notification after 30 minutes is easy to dismiss. Hard limits, app blockers, and logged-out states are far more effective.</li>
      <li><strong>Keeping apps on your home screen.</strong> Out of sight is genuinely out of mind for habitual behavior. Move them, delete them from easy access, or bury them in a folder.</li>
      <li><strong>Trying to cut everything at once.</strong> Pick your worst offender — the app that costs you the most time and leaves you feeling worst — and start there. Win that battle before opening the next front.</li>
    </ul>

    <h2>Frequently Asked Questions</h2>
    {faqs_html}

    <h2>The Bottom Line</h2>
    <p>You already know scrolling is costing you. The calculator on this site can tell you exactly how much in years and hours. The guides here give you the specific, researched tactics to change that number.</p>
    <p>Start with the two or three tactics that fit your situation. Don't try to implement everything at once. Track your screen time weekly. Celebrate small wins — going from 3 hours to 2 hours per day reclaims <strong>365 hours per year</strong>. That's 15 full days back in your life, every year, from a single habit change.</p>

  </article>

  <div class="article-cta">
    <h3>See Exactly How Many Years You've Lost</h3>
    <p>Two sliders. One number that reframes everything.</p>
    <a class="btn-primary" href="/#calculator">Use the Free Calculator →</a>
  </div>

  <div class="related-section">
    <div class="related-title">Related Guides</div>
    <div class="related-grid">
      {related_html}
    </div>
  </div>

</div>

<footer>
  <p>© {year} <a href="/">WastedMeter</a> · <a href="/guides/">All Guides</a> · <a href="/sitemap.xml">Sitemap</a></p>
</footer>

</body>
</html>"""

CATEGORY_LABELS = {
    "stop": "Stop Doomscrolling",
    "platform": "Platform Guides",
    "psychology": "Psychology",
    "replace": "Healthy Alternatives",
    "tools": "Apps & Tools",
    "stats": "Research & Stats",
    "health": "Health Effects",
    "demographics": "By Demographic",
    "challenge": "Challenges",
    "calculator": "Calculators",
    "generic": "Guides",
}

STEPS_TITLES = {
    "stop": "Tactics That Actually Work",
    "platform": "Platform-Specific Steps",
    "psychology": "What to Do With This Knowledge",
    "replace": "How to Make the Switch",
    "tools": "Setup Guide",
    "stats": "What the Data Means for You",
    "health": "How to Reverse the Damage",
    "demographics": "Practical Steps",
    "challenge": "Day-by-Day Plan",
    "calculator": "How to Use Your Number",
    "generic": "What to Do Next",
}


def build_meta_desc(guide):
    title = guide["title"]
    cat = guide.get("category", "generic")
    platform = guide.get("platform", "")

    if platform:
        return f"Evidence-based guide to stopping {platform} doomscrolling. Specific tactics, screen time tips, and how to use {platform} intentionally without quitting. Part of WastedMeter's 300+ guide library."
    elif cat == "stats":
        return f"{title}. Sourced data on screen time, doomscrolling habits, and social media use. Use WastedMeter's free calculator to see your personal number."
    elif cat == "psychology":
        return f"{title}. Understanding the behavioral science behind doomscrolling is the first step to breaking it. Evidence-based guide from WastedMeter."
    else:
        return f"{title}. Evidence-based tactics to reduce doomscrolling and reclaim your time. Free doomscrolling calculator + 300+ guides at WastedMeter."


def render_guide(guide, all_guides):
    slug = guide["slug"]
    title = guide["title"]
    cat = guide.get("category", "generic")

    content = build_content(guide)
    related = get_related(guide, all_guides, n=4)
    related_html = ""
    for r in related:
        related_html += f'<a class="related-link" href="{r["slug"]}.html">{r["title"]}<span class="related-link-arrow">→</span></a>\n'

    meta_desc = build_meta_desc(guide)
    cat_label = CATEGORY_LABELS.get(cat, "Guide")
    steps_title = STEPS_TITLES.get(cat, "What to Do")

    html = GUIDE_TEMPLATE.format(
        slug=slug,
        title=title,
        meta_desc=meta_desc,
        today=TODAY,
        year=YEAR,
        read_time=content["read_time"],
        intro=content["intro"],
        platform_stat=content["platform_stat"],
        tips_html=content["tips_html"],
        faqs_html=content["faqs_html"],
        could_have=content["could_have"],
        category=cat,
        category_label=cat_label,
        steps_title=steps_title,
        related_html=related_html,
    )
    return html


# ─────────────────────────────────────────────
#  CATEGORY HUB PAGES
# ─────────────────────────────────────────────

CATEGORY_HUB_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{cat_title} Guides | WastedMeter</title>
<meta name="description" content="Browse {count} guides on {cat_title_lower}. Evidence-based tactics to stop doomscrolling and reclaim your time. WastedMeter.">
<link rel="canonical" href="https://wastedmeter.com/guides/category-{cat_slug}.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#06060e;--surface:#111120;--surface2:#181828;--border:#252540;--border2:#2e2e50;--accent:#ff3d57;--accent2:#ff6b35;--text:#f2f2fa;--text2:#b0b0d0;--muted:#6060a0}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);min-height:100vh}}
nav{{position:sticky;top:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:.85rem 1.5rem;background:rgba(6,6,14,.92);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,.04)}}
.nav-logo{{font-weight:900;font-size:1.05rem;letter-spacing:-.03em;color:var(--text);text-decoration:none}}
.nav-logo span{{color:var(--accent)}}
.nav-links{{display:flex;gap:.25rem}}
.nav-link{{color:var(--text2);text-decoration:none;font-size:.82rem;font-weight:500;padding:.4rem .9rem;border-radius:8px;transition:all .2s}}
.nav-link:hover{{color:var(--text);background:var(--surface2)}}
.page-wrap{{max-width:900px;margin:0 auto;padding:3rem 1.5rem 6rem}}
.breadcrumb{{display:flex;gap:.5rem;align-items:center;font-size:.75rem;color:var(--muted);margin-bottom:2rem}}
.breadcrumb a{{color:var(--muted);text-decoration:none}}
.breadcrumb a:hover{{color:var(--text2)}}
.breadcrumb span{{color:var(--border2)}}
.page-header{{margin-bottom:3rem}}
.page-cat-badge{{display:inline-block;background:rgba(255,61,87,.08);border:1px solid rgba(255,61,87,.2);color:var(--accent);font-size:.68rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:.3rem .85rem;border-radius:100px;margin-bottom:1rem}}
.page-header h1{{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:900;letter-spacing:-.04em;line-height:1.1;margin-bottom:.75rem}}
.page-header p{{color:var(--text2);font-size:1rem;max-width:600px;line-height:1.7}}
.guide-grid{{display:flex;flex-direction:column;gap:.625rem}}
.guide-item{{display:flex;align-items:center;gap:1rem;padding:1rem 1.25rem;background:var(--surface);border:1px solid var(--border);border-radius:14px;text-decoration:none;color:inherit;transition:all .2s}}
.guide-item:hover{{border-color:var(--border2);background:var(--surface2);transform:translateX(3px)}}
.gi-text{{flex:1;font-size:.9rem;font-weight:500;line-height:1.4}}
.gi-arrow{{color:var(--muted);font-size:.75rem;flex-shrink:0}}
footer{{border-top:1px solid var(--border);padding:2rem 1.5rem;background:var(--bg);text-align:center}}
footer p{{font-size:.78rem;color:var(--muted)}}
footer a{{color:var(--muted);text-decoration:none}}
</style>
</head>
<body>
<nav>
  <a class="nav-logo" href="/">Wasted<span>Meter</span></a>
  <div class="nav-links">
    <a class="nav-link" href="/">Calculator</a>
    <a class="nav-link" href="/guides/">All Guides</a>
  </div>
</nav>
<div class="page-wrap">
  <div class="breadcrumb">
    <a href="/">WastedMeter</a>
    <span>›</span>
    <a href="/guides/">Guides</a>
    <span>›</span>
    {cat_title}
  </div>
  <div class="page-header">
    <div class="page-cat-badge">{count} guides</div>
    <h1>{cat_title}</h1>
    <p>{cat_desc}</p>
  </div>
  <div class="guide-grid">
    {items_html}
  </div>
</div>
<footer>
  <p>© {year} <a href="/">WastedMeter</a> · <a href="/guides/">All Guides</a> · <a href="/sitemap.xml">Sitemap</a></p>
</footer>
</body>
</html>"""

CATEGORY_DESCS = {
    "stop": "Step-by-step guides for breaking the doomscrolling habit — whether you're trying to stop at night, at work, on a specific app, or for good. Evidence-based tactics, no fluff.",
    "platform": "Each social platform has different mechanics, different algorithmic hooks, and different tactics to escape. These guides are platform-specific — because generic advice isn't enough.",
    "psychology": "Understanding why you doomscroll is more powerful than any app blocker. These guides cover the dopamine loops, anxiety spirals, FOMO, and cognitive patterns behind compulsive scrolling.",
    "replace": "The void after quitting is real. These guides help you pre-load specific, satisfying alternatives — activities that meet the same psychological needs without the side effects.",
    "tools": "The right tools add friction to automatic scrolling and make intentional use the path of least resistance. Setup guides for the apps and device settings that actually help.",
    "stats": "What the data actually shows about screen time, doomscrolling, and social media use — by platform, country, age group, and mental health outcome. Sources included.",
    "health": "The mental, physical, and neurological effects of compulsive scrolling — and what the research says about reversing them.",
    "demographics": "Doomscrolling affects different groups differently. Guides tailored to teenagers, parents, students, remote workers, and more.",
    "challenge": "Structured programs for resetting your screen time baseline — from 7-day detoxes to 30-day no-scroll challenges.",
    "calculator": "Tools for quantifying exactly what doomscrolling costs you in time, money, and opportunity — so the problem stops being abstract.",
}


def build_category_pages(all_guides):
    from collections import defaultdict
    by_cat = defaultdict(list)
    for g in all_guides:
        by_cat[g.get("category", "generic")].append(g)

    for cat, guides in by_cat.items():
        items_html = ""
        for g in sorted(guides, key=lambda x: x["title"]):
            items_html += f'<a class="guide-item" href="{g["slug"]}.html"><span class="gi-text">{g["title"]}</span><span class="gi-arrow">→</span></a>\n'

        cat_title = CATEGORY_LABELS.get(cat, cat.title())
        cat_desc = CATEGORY_DESCS.get(cat, f"Browse all {cat_title.lower()} guides.")

        html = CATEGORY_HUB_TEMPLATE.format(
            cat_slug=cat,
            cat_title=cat_title,
            cat_title_lower=cat_title.lower(),
            cat_desc=cat_desc,
            count=len(guides),
            items_html=items_html,
            year=YEAR,
        )
        path = os.path.join(GUIDES_DIR, f"category-{cat}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
    print(f"  ✓ Category pages: {len(by_cat)}")


# ─────────────────────────────────────────────
#  GUIDES INDEX PAGE
# ─────────────────────────────────────────────

def build_guides_index(all_guides):
    from collections import defaultdict
    by_cat = defaultdict(list)
    for g in all_guides:
        by_cat[g.get("category", "generic")].append(g)

    cats_html = ""
    for cat, label in CATEGORY_LABELS.items():
        guides = by_cat.get(cat, [])
        if not guides:
            continue
        items = sorted(guides, key=lambda x: x["title"])[:6]
        items_html = "".join(
            f'<a class="gl-item" href="{g["slug"]}.html">{g["title"]}<span>→</span></a>' for g in items
        )
        all_link = f'<a class="gl-all" href="category-{cat}.html">See all {len(guides)} guides →</a>'
        cats_html += f"""<div class="cat-section">
<div class="cat-header">
  <div class="cat-label">{label}</div>
  <span class="cat-count">{len(guides)} guides</span>
</div>
<div class="cat-items">{items_html}</div>
{all_link}
</div>\n"""

    total = len(all_guides)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Doomscrolling Guides — {total}+ How-To Guides | WastedMeter</title>
<meta name="description" content="Browse {total}+ evidence-based guides on how to stop doomscrolling, quit social media addiction, and reclaim your time. Organized by platform, psychology, tools, and more.">
<link rel="canonical" href="https://wastedmeter.com/guides/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#06060e;--bg2:#0d0d1a;--surface:#111120;--surface2:#181828;--border:#252540;--border2:#2e2e50;--accent:#ff3d57;--accent2:#ff6b35;--text:#f2f2fa;--text2:#b0b0d0;--muted:#6060a0}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;line-height:1.7}}
nav{{position:sticky;top:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:.85rem 1.5rem;background:rgba(6,6,14,.92);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,.04)}}
.nav-logo{{font-weight:900;font-size:1.05rem;letter-spacing:-.03em;color:var(--text);text-decoration:none}}
.nav-logo span{{color:var(--accent)}}
.nav-link{{color:var(--text2);text-decoration:none;font-size:.82rem;font-weight:500;padding:.4rem .9rem;border-radius:8px;transition:all .2s}}
.nav-link:hover{{color:var(--text);background:var(--surface2)}}
.page-hero{{padding:4rem 1.5rem 3rem;text-align:center;max-width:700px;margin:0 auto}}
.hero-eyebrow{{font-size:.72rem;color:var(--accent);text-transform:uppercase;letter-spacing:.12em;font-weight:700;margin-bottom:.75rem}}
.page-hero h1{{font-size:clamp(2rem,5vw,3rem);font-weight:900;letter-spacing:-.04em;line-height:1.1;margin-bottom:.75rem}}
.page-hero p{{color:var(--text2);font-size:1rem;line-height:1.7}}
.guides-wrap{{max-width:900px;margin:0 auto;padding:2rem 1.5rem 6rem;display:flex;flex-direction:column;gap:3rem}}
.cat-section{{}}
.cat-header{{display:flex;align-items:center;gap:1rem;margin-bottom:1rem}}
.cat-label{{font-size:1.1rem;font-weight:800;letter-spacing:-.025em}}
.cat-count{{font-size:.72rem;background:rgba(255,61,87,.1);color:var(--accent);padding:.2rem .7rem;border-radius:100px;font-weight:700;letter-spacing:.05em;text-transform:uppercase}}
.cat-items{{display:flex;flex-direction:column;gap:.4rem;margin-bottom:.75rem}}
.gl-item{{display:flex;justify-content:space-between;align-items:center;padding:.8rem 1.1rem;background:var(--surface);border:1px solid var(--border);border-radius:12px;text-decoration:none;color:var(--text2);font-size:.875rem;font-weight:500;transition:all .2s}}
.gl-item:hover{{border-color:var(--border2);background:var(--surface2);color:var(--text)}}
.gl-item span{{color:var(--muted);font-size:.75rem}}
.gl-all{{display:inline-block;font-size:.8rem;color:var(--accent);text-decoration:none;font-weight:600;padding:.35rem 0;transition:opacity .2s}}
.gl-all:hover{{opacity:.75}}
footer{{border-top:1px solid var(--border);padding:2rem 1.5rem;background:var(--bg2);text-align:center}}
footer p{{font-size:.78rem;color:var(--muted)}}
footer a{{color:var(--muted);text-decoration:none}}
</style>
</head>
<body>
<nav>
  <a class="nav-logo" href="/">Wasted<span>Meter</span></a>
  <div style="display:flex;gap:.25rem">
    <a class="nav-link" href="/">Calculator</a>
    <a class="nav-link" href="how-to-stop-doomscrolling.html">Start Here →</a>
  </div>
</nav>
<div class="page-hero">
  <div class="hero-eyebrow">{total}+ guides</div>
  <h1>Everything You Need to Stop Doomscrolling</h1>
  <p>From platform-specific tactics to the psychology behind why you scroll — organized so you can find exactly what you need.</p>
</div>
<div class="guides-wrap">
{cats_html}
</div>
<footer>
  <p>© {YEAR} <a href="/">WastedMeter</a> · <a href="/sitemap.xml">Sitemap</a></p>
</footer>
</body>
</html>"""

    path = os.path.join(GUIDES_DIR, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ guides/index.html")


# ─────────────────────────────────────────────
#  SITEMAP
# ─────────────────────────────────────────────

def build_sitemap(all_guides):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    def url(loc, priority, changefreq="monthly"):
        return f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""

    lines.append(url(f"{BASE_URL}/", "1.0", "weekly"))
    lines.append(url(f"{BASE_URL}/guides/", "0.9", "weekly"))

    cats = set(g.get("category", "generic") for g in all_guides)
    for cat in cats:
        lines.append(url(f"{BASE_URL}/guides/category-{cat}.html", "0.8"))

    for g in all_guides:
        priority = "0.9" if g["slug"] in ["how-to-stop-doomscrolling", "why-do-i-doomscroll", "doomscrolling-statistics-2025"] else "0.7"
        lines.append(url(f"{BASE_URL}/guides/{g['slug']}.html", priority))

    lines.append("</urlset>")

    sitemap_path = os.path.join(os.path.dirname(__file__), "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ sitemap.xml ({len(all_guides) + 2 + len(cats)} URLs)")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    print("WastedMeter Guide Generator")
    print("=" * 40)

    all_guides = build_guides()
    print(f"\nBuilding {len(all_guides)} guide pages...")

    for i, guide in enumerate(all_guides, 1):
        html = render_guide(guide, all_guides)
        path = os.path.join(GUIDES_DIR, f"{guide['slug']}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        if i % 50 == 0:
            print(f"  ... {i}/{len(all_guides)}")

    print(f"  ✓ {len(all_guides)} guide pages written to guides/")
    print("\nBuilding index pages...")
    build_guides_index(all_guides)
    build_category_pages(all_guides)

    print("\nBuilding sitemap...")
    build_sitemap(all_guides)

    print(f"\n✅ Done! {len(all_guides)} guides + index + categories + sitemap")
    print(f"   Output: {GUIDES_DIR}")
    print(f"   Sitemap: {os.path.join(os.path.dirname(__file__), 'sitemap.xml')}")


if __name__ == "__main__":
    main()
