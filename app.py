from flask import Flask, render_template, request, jsonify
from difflib import get_close_matches
import random

app = Flask(__name__)

music_data = {
    "happy": [
        {"name": "Happy - Pharrell Williams", "img": "https://img.youtube.com/vi/ZbZSe6N_BXs/0.jpg", "link": "https://www.youtube.com/watch?v=ZbZSe6N_BXs"},
        {"name": "Uptown Funk - Mark Ronson ft. Bruno Mars", "img": "https://img.youtube.com/vi/OPf0YbXqDm0/0.jpg", "link": "https://www.youtube.com/watch?v=OPf0YbXqDm0"},
        {"name": "Can't Stop the Feeling! - Justin Timberlake", "img": "https://img.youtube.com/vi/ru0K8uYEZWw/0.jpg", "link": "https://www.youtube.com/watch?v=ru0K8uYEZWw"},
        {"name": "Happiness - Red Velvet", "img": "https://img.youtube.com/vi/JFgv8bKfxEs/0.jpg", "link": "https://www.youtube.com/watch?v=JFgv8bKfxEs"},
        {"name": "Heart Shaker - TWICE", "img": "https://img.youtube.com/vi/rRzxEiBLQCA/0.jpg", "link": "https://www.youtube.com/watch?v=rRzxEiBLQCA"},
        {"name": "Nonstop - Oh My Girl", "img": "https://img.youtube.com/vi/iDjQSdN_ig8/0.jpg", "link": "https://www.youtube.com/watch?v=iDjQSdN_ig8"},
{"name": "Dynamite - BTS", "img": "https://img.youtube.com/vi/gdZLi9oWNZg/0.jpg", "link": "https://www.youtube.com/watch?v=gdZLi9oWNZg"},
{"name": "Cheer Up - TWICE", "img": "https://img.youtube.com/vi/c7rCyll5AeY/0.jpg", "link": "https://www.youtube.com/watch?v=c7rCyll5AeY"},
{"name": "Gallan Goodiyaan - Dil Dhadakne Do", "img": "https://img.youtube.com/vi/jCEdTq3j-0U/0.jpg", "link": "https://www.youtube.com/watch?v=jCEdTq3j-0U"},
{"name": "Badtameez Dil - Yeh Jawaani Hai Deewani", "img": "https://img.youtube.com/vi/II2EO3Nw4m0/0.jpg", "link": "https://www.youtube.com/watch?v=II2EO3Nw4m0"},
{"name": "Feel Special - TWICE", "img": "https://img.youtube.com/vi/3ymwOvzhwHs/0.jpg", "link": "https://www.youtube.com/watch?v=3ymwOvzhwHs"},

{"name": "Red Flavor - Red Velvet", "img": "https://img.youtube.com/vi/WyiIGEHQP8o/0.jpg", "link": "https://www.youtube.com/watch?v=WyiIGEHQP8o"},

{"name": "Shine - Pentagon", "img": "https://img.youtube.com/vi/Nu2yQ1zYDYU/0.jpg", "link": "https://www.youtube.com/watch?v=Nu2yQ1zYDYU"},

{"name": "Very Very Very - I.O.I", "img": "https://img.youtube.com/vi/GdxvD7r58ng/0.jpg", "link": "https://www.youtube.com/watch?v=GdxvD7r58ng"},
{"name": "In Bloom - ZEROBASEONE", "img": "https://img.youtube.com/vi/trzeUClQIIg/0.jpg", "link": "https://www.youtube.com/watch?v=trzeUClQIIg"}
],

    "sad": [
        {"name": "Someone Like You - Adele", "img": "https://img.youtube.com/vi/hLQl3WQQoQ0/0.jpg", "link": "https://www.youtube.com/watch?v=hLQl3WQQoQ0"},
        {"name": "Fix You - Coldplay", "img": "https://img.youtube.com/vi/k4V3Mo61fJM/0.jpg", "link": "https://www.youtube.com/watch?v=k4V3Mo61fJM"},
        {"name": "Let Her Go - Passenger", "img": "https://img.youtube.com/vi/RBumgq5yVrA/0.jpg", "link": "https://www.youtube.com/watch?v=RBumgq5yVrA"},
        {"name": "Intezaar – Arijit Singh", "img": "https://i.ytimg.com/vi/Fj9IrJ8pPzc/maxresdefault.jpg", "link": "https://www.youtube.com/watch?v=Fj9IrJ8pPzc"},
        {"name": "Blue and Grey - BTS", "img": "https://img.youtube.com/vi/amnspvOH-EE/0.jpg", "link": "https://www.youtube.com/watch?v=amnspvOH-EE"},
        {"name": "My Sea - IU", "img": "https://img.youtube.com/vi/TqIAndOnd74/0.jpg", "link": "https://www.youtube.com/watch?v=TqIAndOnd74"},
{"name": "Love Poem - IU", "img": "https://img.youtube.com/vi/OcVmaIlHZ1o/0.jpg", "link": "https://www.youtube.com/watch?v=OcVmaIlHZ1o"},

{"name": "Spring Day - BTS", "img": "https://img.youtube.com/vi/xEeFrLSkMm8/0.jpg", "link": "https://www.youtube.com/watch?v=xEeFrLSkMm8"},

{"name": "Channa Mereya - Arijit Singh", "img": "https://img.youtube.com/vi/284Ov7ysmfA/0.jpg", "link": "https://www.youtube.com/watch?v=284Ov7ysmfA"},

{"name": "Agar Tum Saath Ho - Alka Yagnik & Arijit Singh", "img": "https://img.youtube.com/vi/sK7riqg2mr4/0.jpg", "link": "https://www.youtube.com/watch?v=sK7riqg2mr4"},
{"name": "I Need Somebody - DAY6", "img": "https://img.youtube.com/vi/j-TcFt2OVSw/0.jpg", "link": "https://www.youtube.com/watch?v=j-TcFt2OVSw"},

{"name": "Eyes, Nose, Lips - Taeyang", "img": "https://img.youtube.com/vi/UwuAPyOImoI/0.jpg", "link": "https://www.youtube.com/watch?v=UwuAPyOImoI"},

{"name": "Stay With Me - Chanyeol & Punch", "img": "https://img.youtube.com/vi/pcKR0LPwoYs/0.jpg", "link": "https://www.youtube.com/watch?v=pcKR0LPwoYs"},

{"name": "Lonely - Jonghyun ft. Taeyeon", "img": "https://img.youtube.com/vi/NpTpEsE9G8c/0.jpg", "link": "https://www.youtube.com/watch?v=NpTpEsE9G8c"},
{"name": "Good Night - ZEROBASEONE", "img": "https://i.ytimg.com/vi/Z0ZyceO05s4/maxresdefault.jpg", "link": "https://www.youtube.com/watch?v=Z0ZyceO05s4"}
    ],

    "gym": [
        {"name": "Stronger - Kanye West", "img": "https://img.youtube.com/vi/PsO6ZnUZI0g/0.jpg", "link": "https://www.youtube.com/watch?v=PsO6ZnUZI0g"},
        {"name": "Till I Collapse - Eminem", "img": "https://img.youtube.com/vi/ytQ5CYE1VZw/0.jpg", "link": "https://www.youtube.com/watch?v=ytQ5CYE1VZw"},
        {"name": "Jump - BLACKPINK", "img": "https://i.ytimg.com/vi/CgCVZdcKcqY/maxresdefault.jpg", "link": "https://www.youtube.com/watch?v=CgCVZdcKcqY"},
        {"name": "Magnetic - ILLIT", "img": "https://img.youtube.com/vi/Vk5-c_v4gMU/0.jpg", "link": "https://www.youtube.com/watch?v=Vk5-c_v4gMU"},
        {"name": "Believer - Imagine Dragons", "img": "https://img.youtube.com/vi/7wtfhZwyrcc/0.jpg", "link": "https://www.youtube.com/watch?v=7wtfhZwyrcc"},
{"name": "How You Like That - BLACKPINK", "img": "https://img.youtube.com/vi/ioNng23DkIM/0.jpg", "link": "https://www.youtube.com/watch?v=ioNng23DkIM"},

{"name": "MIC Drop (Steve Aoki Remix) - BTS", "img": "https://img.youtube.com/vi/kTlv5_Bs8aw/0.jpg", "link": "https://www.youtube.com/watch?v=kTlv5_Bs8aw"},

{"name": "Malang (Title Track) - Ved Sharma", "img": "https://img.youtube.com/vi/KBIq11mNB0I/0.jpg", "link": "https://www.youtube.com/watch?v=KBIq11mNB0I"},

{"name": "Ghungroo - Arijit Singh & Shilpa Rao", "img": "https://img.youtube.com/vi/qFkNATtc3mc/0.jpg", "link": "https://www.youtube.com/watch?v=qFkNATtc3mc"},

{"name": "Jai Jai Shivshankar - Vishal Dadlani & Benny Dayal", "img": "https://i.ytimg.com/vi/0kfLTq57_Y0/maxresdefault.jpg", "link": "https://www.youtube.com/watch?v=0kfLTq57_Y0"},
{"name": "God's Menu - Stray Kids", "img": "https://img.youtube.com/vi/TQTlCHxyuu8/0.jpg", "link": "https://www.youtube.com/watch?v=TQTlCHxyuu8"},

{"name": "Kill This Love - BLACKPINK", "img": "https://img.youtube.com/vi/2S24-y0Ij3Y/0.jpg", "link": "https://www.youtube.com/watch?v=2S24-y0Ij3Y"},

{"name": "CRUSH - ZEROBASEONE", "img": "https://img.youtube.com/vi/AZoZbtI67Yk/0.jpg", "link": "https://www.youtube.com/watch?v=AZoZbtI67Yk"},

{"name": "Wonderland - ATEEZ", "img": "https://img.youtube.com/vi/Z_BhMhZpAug/0.jpg", "link": "https://www.youtube.com/watch?v=Z_BhMhZpAug"},

{"name": "BOOMBAYAH - BLACKPINK", "img": "https://img.youtube.com/vi/bwmSjveL3Lc/0.jpg", "link": "https://www.youtube.com/watch?v=bwmSjveL3Lc"}
    ],

    "study": [
        {"name": "Lo-fi Beats", "img": "https://img.youtube.com/vi/jfKfPfyJRdk/0.jpg", "link": "https://www.youtube.com/watch?v=jfKfPfyJRdk"},
        {"name": "Weightless", "img": "https://img.youtube.com/vi/UfcAVejslrU/0.jpg", "link": "https://www.youtube.com/watch?v=UfcAVejslrU"},
        {"name": "Clair de Lune - Debussy", "img": "https://img.youtube.com/vi/CvFH_6DNRCY/0.jpg", "link": "https://www.youtube.com/watch?v=CvFH_6DNRCY"}
    ],

    "romantic": [
    {
        "name": "Perfect - Ed Sheeran",
        "img": "https://img.youtube.com/vi/2Vv-BfVoq4g/0.jpg",
        "link": "https://www.youtube.com/watch?v=2Vv-BfVoq4g"
    },
    {
        "name": "All of Me - John Legend",
        "img": "https://img.youtube.com/vi/450p7goxZqg/0.jpg",
        "link": "https://www.youtube.com/watch?v=450p7goxZqg"
    },
    {
        "name": "Tum Hi Ho - Arijit Singh",
        "img": "https://img.youtube.com/vi/IJq0yyWug1k/0.jpg",
        "link": "https://www.youtube.com/watch?v=IJq0yyWug1k"
    },
    {
        "name": "Apna Bana Le - Arijit Singh",
        "img": "https://img.youtube.com/vi/ElZfdU54Cp8/0.jpg",
        "link": "https://www.youtube.com/watch?v=ElZfdU54Cp8"
    },
    {
        "name": "Ve Kamleya - Arijit Singh, Shreya Ghoshal",
        "img": "https://img.youtube.com/vi/YxWlaYCA8MU/0.jpg",
        "link": "https://www.youtube.com/watch?v=YxWlaYCA8MU"
    },
    {
        "name": "Love Wins All - IU",
        "img": "https://img.youtube.com/vi/JleoAppaxi0/0.jpg",
        "link": "https://www.youtube.com/watch?v=JleoAppaxi0"
    },

{"name": "Boy With Luv - BTS ft. Halsey", "img": "https://img.youtube.com/vi/XsX3ATc3FbA/0.jpg", "link": "https://www.youtube.com/watch?v=XsX3ATc3FbA"},

{"name": "Raabta - Arijit Singh", "img": "https://img.youtube.com/vi/zlt38OOqwDc/0.jpg", "link": "https://www.youtube.com/watch?v=zlt38OOqwDc"},
{"name": "Saiyaara - Shreya Ghoshal", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS778ZoqfGTR_kW3Atp1608_IIHuVarwRBlGQ&s", "link": "https://www.youtube.com/watch?v=asG7cwxi1sA"},

{"name": "My Universe - BTS & Coldplay", "img": "https://img.youtube.com/vi/3YqPKLZF_WU/0.jpg", "link": "https://www.youtube.com/watch?v=3YqPKLZF_WU"},

{"name": "Love Shot - EXO", "img": "https://img.youtube.com/vi/pSudEWBAYRE/0.jpg", "link": "https://www.youtube.com/watch?v=pSudEWBAYRE"},

{"name": "Heart Attack - Chuu (LOONA)", "img": "https://img.youtube.com/vi/BVVfMFS3mgc/0.jpg", "link": "https://www.youtube.com/watch?v=BVVfMFS3mgc"},
{"name": "Serendipity - BTS (Jimin)", "img": "https://img.youtube.com/vi/gSsCZJM6OG0/0.jpg", "link": "https://www.youtube.com/watch?v=gSsCZJM6OG0"},
{"name": "Only - Lee Hi", "img": "https://img.youtube.com/vi/KmOVNVZEP9o/0.jpg", "link": "https://www.youtube.com/watch?v=KmOVNVZEP9o"},
{"name": "Melting Point - ZEROBASEONE", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQTzIymKx0q0DlK7TeFxTQ885_lgMsiBA5QlQ&s", "link": "https://www.youtube.com/watch?v=LK7ca_PWEoY"}

],

   "party": [
    {
        "name": "Levitating - Dua Lipa",
        "img": "https://img.youtube.com/vi/TUVcZfQe-Kw/0.jpg",
        "link": "https://www.youtube.com/watch?v=TUVcZfQe-Kw"
    },
    {
        "name": "Shape of You - Ed Sheeran",
        "img": "https://img.youtube.com/vi/JGwWNGJdvx8/0.jpg",
        "link": "https://www.youtube.com/watch?v=JGwWNGJdvx8"
    },
    {
        "name": "Kala Chashma - Amar Arshi, Badshah, Neha Kakkar",
        "img": "https://img.youtube.com/vi/k4yXQkG2s1E/0.jpg",
        "link": "https://www.youtube.com/watch?v=k4yXQkG2s1E"
    },
    {"name": "London Thumakda - Labh Janjua, Sonu Kakkar, Neha Kakkar", "img": "https://img.youtube.com/vi/udra3Mfw2oo/0.jpg", "link": "https://www.youtube.com/watch?v=udra3Mfw2oo"},
    {
        "name": "APT. - ROSE & Bruno Mars",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDE4cb-0HcU2msXPfFtJdP87zlxIG_ObWBlA&s",
        "link": "https://www.youtube.com/watch?v=ekr2nIex040"
    },
    {
        "name": "Bang Bang Bang - BIGBANG",
        "img": "https://img.youtube.com/vi/2ips2mM7Zqw/0.jpg",
        "link": "https://www.youtube.com/watch?v=2ips2mM7Zqw"
    },
    {
        "name": "Gangnam Style - PSY",
        "img": "https://img.youtube.com/vi/9bZkp7q19f0/0.jpg",
        "link": "https://www.youtube.com/watch?v=9bZkp7q19f0"
    },
    {
        "name": "New Kidz on the Block - ZEROBASEONE",
        "img": "https://i.ytimg.com/vi/AO6BlpKi3G0/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCkTtKckW888TW_DCiPXc0IkyOwuw",
        "link": "https://www.youtube.com/watch?v=WaPTuK8uyWE"
    },
{"name": "Dynamite - BTS", "img": "https://img.youtube.com/vi/gdZLi9oWNZg/0.jpg", "link": "https://www.youtube.com/watch?v=gdZLi9oWNZg"},

{"name": "Nashe Si Chadh Gayi - Arijit Singh", "img": "https://img.youtube.com/vi/WKbwopSXLWU/0.jpg", "link": "https://www.youtube.com/watch?v=WKbwopSXLWU"},
{"name": "God's Menu - Stray Kids", "img": "https://img.youtube.com/vi/TQTlCHxyuu8/0.jpg", "link": "https://www.youtube.com/watch?v=TQTlCHxyuu8"},

{"name": "Wannabe - ITZY", "img": "https://img.youtube.com/vi/fE2h3lGlOsk/0.jpg", "link": "https://www.youtube.com/watch?v=fE2h3lGlOsk"},

{"name": "HOT - SEVENTEEN", "img": "https://img.youtube.com/vi/gRnuFC4Ualw/0.jpg", "link": "https://www.youtube.com/watch?v=gRnuFC4Ualw"},
{"name": "Kar Gayi Chull - Badshah, Neha Kakkar", "img": "https://img.youtube.com/vi/NTHz9ephYTw/0.jpg", "link": "https://www.youtube.com/watch?v=NTHz9ephYTw"},

{"name": "Ghungroo - Arijit Singh, Shilpa Rao", "img": "https://img.youtube.com/vi/qFkNATtc3mc/0.jpg", "link": "https://www.youtube.com/watch?v=qFkNATtc3mc"}

],

    "chill": [
    {
        "name": "Sunflower - Post Malone",
        "img": "https://img.youtube.com/vi/ApXoWvfEYVU/0.jpg",
        "link": "https://www.youtube.com/watch?v=ApXoWvfEYVU"
    },
    {
        "name": "Stay - Justin Bieber",
        "img": "https://img.youtube.com/vi/kTJczUoc26U/0.jpg",
        "link": "https://www.youtube.com/watch?v=kTJczUoc26U"
    },
    {
        "name": "Heat Waves - Glass Animals",
        "img": "https://img.youtube.com/vi/mRD0-GxqHVo/0.jpg",
        "link": "https://www.youtube.com/watch?v=mRD0-GxqHVo"
    },
    {
        "name": "Tum Se Hi - Mohit Chauhan",
        "img": "https://img.youtube.com/vi/mt9xg0mmt28/0.jpg",
        "link": "https://www.youtube.com/watch?v=mt9xg0mmt28"
    },
    {
        "name": "Love You Zindagi - Amit Trivedi",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTRtbzPD6BFJQjhPKcXXvB3S1TLVG_GYcnQOw&s",
        "link": "https://www.youtube.com/watch?v=nBcKS3dhe5U"
    },
    {
        "name": "Moh Moh Ke Dhaage - Papon & Monali Thakur",
        "img": "https://i.ytimg.com/vi/X4rEsj4z7MY/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCig1n2IMtnmZl8QldLEcvn9yws8Q",
        "link": "https://www.youtube.com/watch?v=X4rEsj4z7MY"
    },
    {
        "name": "Mikrokosmos - BTS",
        "img": "https://img.youtube.com/vi/Fw7C6IsDYgI/0.jpg",
        "link": "https://www.youtube.com/watch?v=Fw7C6IsDYgI"
    },
{"name": "Spring Day - BTS", "img": "https://img.youtube.com/vi/xEeFrLSkMm8/0.jpg", "link": "https://www.youtube.com/watch?v=xEeFrLSkMm8"},

{"name": "Through the Night - IU", "img": "https://img.youtube.com/vi/BzYnNdJhZQw/0.jpg", "link": "https://www.youtube.com/watch?v=BzYnNdJhZQw"},

{"name": "Sham - Aisha", "img": "https://i.ytimg.com/vi/vNSwdLu_ieI/sddefault.jpg", "link": "https://www.youtube.com/watch?v=vNSwdLu_ieI"},
{"name": "Love Talk - WayV", "img": "https://img.youtube.com/vi/N5qWjQ9j6l0/0.jpg", "link": "https://www.youtube.com/watch?v=N5qWjQ9j6l0"},

{"name": "Instagram - DEAN", "img": "https://img.youtube.com/vi/wKyMIrBClYw/0.jpg", "link": "https://www.youtube.com/watch?v=wKyMIrBClYw"},

{"name": "Palette - IU ft. G-Dragon", "img": "https://img.youtube.com/vi/d9IxdwEFk1c/0.jpg", "link": "https://www.youtube.com/watch?v=d9IxdwEFk1c"},

{"name": "Some - Bolbbalgan4", "img": "https://img.youtube.com/vi/hZmoMyFXDoI/0.jpg", "link": "https://www.youtube.com/watch?v=hZmoMyFXDoI"},

{"name": "Dayfly - SUGA, Heize", "img": "https://img.youtube.com/vi/Z3W0jKcv1SU/0.jpg", "link": "https://www.youtube.com/watch?v=Z3W0jKcv1SU"}
],

    "angry": [
    {
        "name": "Numb - Linkin Park",
        "img": "https://img.youtube.com/vi/kXYiU_JCYtU/0.jpg",
        "link": "https://www.youtube.com/watch?v=kXYiU_JCYtU"
    },
    {
        "name": "Believer - Imagine Dragons",
        "img": "https://img.youtube.com/vi/7wtfhZwyrcc/0.jpg",
        "link": "https://www.youtube.com/watch?v=7wtfhZwyrcc"
    },
    {
        "name": "Stronger - Kanye West",
        "img": "https://img.youtube.com/vi/PsO6ZnUZI0g/0.jpg",
        "link": "https://www.youtube.com/watch?v=PsO6ZnUZI0g"
    },
    {
        "name": "Daechwita - Agust D",
        "img": "https://img.youtube.com/vi/qGjAWJ2zWWI/0.jpg",
        "link": "https://www.youtube.com/watch?v=qGjAWJ2zWWI"
    },
    {
        "name": "Kill This Love - BLACKPINK",
        "img": "https://img.youtube.com/vi/2S24-y0Ij3Y/0.jpg",
        "link": "https://www.youtube.com/watch?v=2S24-y0Ij3Y"
    },
    {
        "name": "Saadda Haq - Mohit Chauhan",
        "img": "https://i.ytimg.com/vi/y47Bg9RP2dM/hqdefault.jpg",
        "link": "https://www.youtube.com/watch?v=y47Bg9RP2dM"
    },
    {
        "name": "Kar Har Maidaan Fateh - Sukhwinder Singh, Shreya Ghoshal",
        "img": "https://i.ytimg.com/vi/t6MeeKrDIlM/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBGE1q9vDHmkgWahe4uEARNq7wj5A",
        "link": "https://www.youtube.com/watch?v=t6MeeKrDIlM"
    },
{"name": "Not Today - BTS", "img": "https://img.youtube.com/vi/9DwzBICPhdM/0.jpg", "link": "https://www.youtube.com/watch?v=9DwzBICPhdM"},

{"name": "Zinda - Siddharth Mahadevan", "img": "https://i.ytimg.com/vi/r2LiGO_aiMk/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBaMp2fHuxOy4CaWamDPZH8rYQuvg", "link": "https://www.youtube.com/watch?v=r2LiGO_aiMk"},
{"name": "Malang (Title Track) - Ved Sharma", "img": "https://img.youtube.com/vi/KBIq11mNB0I/0.jpg", "link": "https://www.youtube.com/watch?v=KBIq11mNB0I"},
{"name": "Fire - BTS", "img": "https://img.youtube.com/vi/ALj5MKjy2BU/0.jpg", "link": "https://www.youtube.com/watch?v=ALj5MKjy2BU"},

{"name": "Thunderous - Stray Kids", "img": "https://img.youtube.com/vi/EaswWiwMVs8/0.jpg", "link": "https://www.youtube.com/watch?v=EaswWiwMVs8"},

{"name": "Guerrilla - ATEEZ", "img": "https://img.youtube.com/vi/2HcVZm_4qAI/0.jpg", "link": "https://www.youtube.com/watch?v=2HcVZm_4qAI"},

{"name": "Savage - aespa", "img": "https://img.youtube.com/vi/WPdWvnAAurg/0.jpg", "link": "https://www.youtube.com/watch?v=WPdWvnAAurg"},
{"name": "Sultan (Title Track) - Sultan", "img": "https://img.youtube.com/vi/wPxqcq6Byq0/0.jpg", "link": "https://www.youtube.com/watch?v=wPxqcq6Byq0"}
],


    "sleep": [
    {
        "name": "Weightless - Ambient",
        "img": "https://img.youtube.com/vi/UfcAVejslrU/0.jpg",
        "link": "https://www.youtube.com/watch?v=UfcAVejslrU"
    },
    {
        "name": "Night Rain Sounds",
        "img": "https://img.youtube.com/vi/1ZYbU82GVz4/0.jpg",
        "link": "https://www.youtube.com/watch?v=1ZYbU82GVz4"
    },
    {
        "name": "Deep Sleep Music",
        "img": "https://img.youtube.com/vi/lFcSrYw-ARY/0.jpg",
        "link": "https://www.youtube.com/watch?v=lFcSrYw-ARY"
    },
    {
        "name": "Agar Tum Saath Ho - Alka Yagnik & Arijit Singh",
        "img": "https://img.youtube.com/vi/sK7riqg2mr4/0.jpg",
        "link": "https://www.youtube.com/watch?v=sK7riqg2mr4"
    },
    {
        "name": "Raabta (Slowed & Reverb) - Arijit Singh",
        "img": "https://i.ytimg.com/vi/YnzNWdSwNTE/maxresdefault.jpg",
        "link": "https://www.youtube.com/watch?v=YnzNWdSwNTE"
    },
    {
        "name": "Lag Ja Gale - Lata Mangeshkar",
        "img": "https://img.youtube.com/vi/TFr6G5zveS8/0.jpg",
        "link": "https://www.youtube.com/watch?v=TFr6G5zveS8"
    },
    {
        "name": "Still With You - Jungkook",
        "img": "https://img.youtube.com/vi/djKdPZiJdvA/0.jpg",
        "link": "https://www.youtube.com/watch?v=djKdPZiJdvA"
    },
    {
        "name": "00:00 (Zero O'Clock) - BTS",
        "img": "https://img.youtube.com/vi/Nr3ot5gSvkM/0.jpg",
        "link": "https://www.youtube.com/watch?v=Nr3ot5gSvkM"
    },
    {
        "name": "Through The Night - IU",
        "img": "https://img.youtube.com/vi/BzYnNdJhZQw/0.jpg",
        "link": "https://www.youtube.com/watch?v=BzYnNdJhZQw"
    },
{"name": "Khairiyat - Arijit Singh", "img": "https://img.youtube.com/vi/hoNb6HuNmU0/0.jpg", "link": "https://www.youtube.com/watch?v=hoNb6HuNmU0"},
{"name": "Always - ZEROBASEONE", "img": "https://i.ytimg.com/vi/4DgrwVhMskA/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBqS4-pecwNyG-SHENVvQQi5RjxBg", "link": "https://www.youtube.com/watch?v=g9uSuKs_MN4"},

{"name": "Sweet Night - V", "img": "https://img.youtube.com/vi/N5ShoQimivM/0.jpg", "link": "https://www.youtube.com/watch?v=N5ShoQimivM"},

{"name": "Good Night - CHEN", "img": "https://img.youtube.com/vi/dN-wG4dKzCE/0.jpg", "link": "https://www.youtube.com/watch?v=dN-wG4dKzCE"},

{"name": "All About You - TAEYEON", "img": "https://i.ytimg.com/vi/y9dpVNRSA6k/mqdefault.jpg", "link": "https://www.youtube.com/watch?v=y9dpVNRSA6k"},

{"name": "밤편지 (Dear Name) - IU", "img": "https://img.youtube.com/vi/8zsYZFvKniw/0.jpg", "link": "https://www.youtube.com/watch?v=8zsYZFvKniw"}
]
}
def detect_mood(text):
    text = text.lower()

    mood_map = {
        "happy": ["happy", "joy", "excited", "good", "great"],
        "sad": ["sad", "depressed", "cry", "heartbroken", "low"],
        "gym": ["gym", "workout", "energy", "power"],
        "study": ["study", "focus", "concentrate"],
        "romantic": ["love", "romantic", "crush"],
        "party": ["party", "dance", "fun"],
        "chill": ["chill", "relax", "calm"],
        "angry": ["angry", "mad", "rage"],
        "sleep": ["sleep", "tired", "night"]
    }

    for mood, keywords in mood_map.items():
        if any(word in text for word in keywords):
            return mood

  
    all_keywords = []
    keyword_to_mood = {}

    for mood, keywords in mood_map.items():
        for word in keywords:
            all_keywords.append(word)
            keyword_to_mood[word] = mood

    matches = get_close_matches(text, all_keywords, n=1, cutoff=0.6)

    if matches:
        return keyword_to_mood[matches[0]]

    
    return None
def get_songs(user_input):
    if not user_input:
        return "<div class='card'>Please select a mood</div>"

    user_input = user_input.lower()

    if user_input in songs:
        result = ""

        
        for song in random.sample(songs[user_input], 2):
            result += f"""
            <div class='card'>
                <img src="{song['img']}" width="100%" style="border-radius:10px;">
                <br><br>
                <b>{song['name']}</b><br>
                <a href="{song['link']}" target="_blank">▶ Play</a>
            </div>
            """

        return result

    return "<div class='card'>Invalid mood</div>"



@app.route("/", methods=["GET", "POST"])
def home():
    songs = []
    mood = None

    if request.method == "POST":
        mood = request.form.get("mood")
        songs = music_data.get(mood, [])

    return render_template("index.html", songs=songs, mood=mood)


@app.route("/get_songs", methods=["POST"])
def get_songs():
    user_text = request.json.get("mood")

    detected_mood = detect_mood(user_text)

   
    if not detected_mood:
        from difflib import get_close_matches

        all_keywords = []
        for mood, keywords in {
            "happy": ["happy", "joy", "excited", "good", "great"],
            "sad": ["sad", "depressed", "cry", "heartbroken", "low"],
            "gym": ["gym", "workout", "energy", "power"],
            "study": ["study", "focus", "concentrate"],
            "romantic": ["love", "romantic", "crush"],
            "party": ["party", "dance", "fun"],
            "chill": ["chill", "relax", "calm"],
            "angry": ["angry", "mad", "rage"],
            "sleep": ["sleep", "tired", "night"]
        }.items():
            all_keywords.extend(keywords)

        matches = get_close_matches(user_text.lower(), all_keywords, n=1, cutoff=0.6)

        return jsonify({
            "error": "unknown",
            "suggestion": matches[0] if matches else None
        })

   
    songs = music_data.get(detected_mood, [])
    return jsonify(songs)


if __name__ == "__main__":
    app.run(debug=True)
