#!/bin/bash
#bash script to read JSON data and populate MongoDB with activities based on weather conditions

JSON_DATA='{
  "weather_conditions": {
    "sunny": {
      "outdoor_activities": [
        "Hiking through the nearest nature trail",
        "Beach volleyball with friends",
        "Picnic in the park",
        "Biking through scenic routes",
        "Going to the zoo and making friends with a giraffe",
        "Frisbee with a twist - blindfolded Frisbee!",
        "Organize a water balloon fight",
        "Outdoor yoga session",
        "Flying a kite shaped like your favorite superhero",
        "Build a sandcastle and crown yourself king/queen",
        "Stargazing in the evening",
        "Pretend you'\''re a tourist in your own city and take selfies at every landmark"
      ],
      "indoor_activities": [
        "Sunlit painting session by the window",
        "Cooking a sunny-themed meal - think tropical fruits!",
        "Organize an indoor treasure hunt",
        "Try baking your own bread from scratch",
        "Create DIY sun-catchers to hang in your window",
        "Make a summer playlist and have a solo dance party",
        "Host a board game marathon",
        "Watch travel documentaries to inspire future sunny vacations",
        "Host a virtual beach party with friends",
        "Indoor badminton with balloons",
        "Practice your best beach impressions while wearing a Hawaiian shirt"
      ]
    },
    "rainy": {
      "outdoor_activities": [
        "Jumping in puddles like you'\''re 5 again",
        "Go for a rain-soaked hike bring your raincoat!",
        "Photography walk with a focus on capturing raindrops",
        "Splash around in rain boots - splash competition, anyone?",
        "Set up a slip-and-slide in your backyard",
        "Play soccer in the mud - embrace the mess",
        "Collect rainwater for your plants",
        "Start an impromptu rain dance party in your yard",
        "Visit a waterfall they'\''re extra stunning in the rain",
        "Fishing in the rain - it'\''s peaceful, trust me",
        "Try to make the biggest paper boat and see if it floats in the puddles"
      ],
      "indoor_activities": [
        "Curl up with a good book and a warm drink",
        "Watch movies or binge-watch a series in cozy blankets",
        "Have a rainy day art session - watercolor to match the mood",
        "Build a pillow fort and pretend it'\''s your fortress",
        "Host a homemade pizza night",
        "Learn a new card game",
        "Write a short story about the most ridiculous rainy adventure",
        "Create DIY bath bombs and enjoy a relaxing bath",
        "Do an indoor scavenger hunt",
        "Have a cozy tea party with stuffed animals - formal attire required",
        "Make paper boats and race them in the sink"
      ]
    },
    "snowy": {
      "outdoor_activities": [
        "Build a snowman - or snowdog, or snowdragon!",
        "Snowball fight - winner gets hot cocoa",
        "Create snow angels and compare your angelic abilities",
        "Go sledding down the nearest hill",
        "Try ice skating on a frozen pond",
        "Build a snow fort for ultimate defense in snowball warfare",
        "Go for a snowy walk in the forest and channel your inner explorer",
        "Organize a snow sculpture competition",
        "Take up snowshoeing",
        "Make snow ice cream - yes, it'\''s a thing!",
        "Try to catch snowflakes on your tongue and see who can catch the most!"
      ],
      "indoor_activities": [
        "Watch holiday movies regardless of the season",
        "Bake cookies shaped like snowflakes",
        "Knit yourself a ridiculously oversized scarf",
        "Host a hot chocolate taste-testing competition",
        "Try your hand at making homemade marshmallows",
        "DIY a gingerbread house, then eat it immediately",
        "Have an indoor snowball fight with rolled-up socks",
        "Start a winter-themed puzzle",
        "Make paper snowflakes and hang them around the house",
        "Write and perform your own winter-themed comedy sketch",
        "Have a snow-themed karaoke night singing winter classics"
      ]
    },
    "windy": {
      "outdoor_activities": [
        "Fly the biggest kite you can find - or make",
        "Wind surfing at a nearby lake",
        "Take a dramatic walk with your scarf blowing in the wind",
        "Create a wind-powered obstacle course",
        "Do a windy-day photoshoot - hair flying everywhere",
        "Set up a sailboat on a small lake",
        "Test paper airplanes in the wind",
        "Start a leaf-chasing race",
        "Have an outdoor wind chime concert",
        "Build a mini wind turbine with household items",
        "Try to take a selfie with your hair blowing everywhere – new style alert!"
      ],
      "indoor_activities": [
        "Make paper pinwheels and see how they spin",
        "Host a movie night with wind-themed films - Twister, anyone?",
        "Craft a wind-sock and hang it outside to watch it blow",
        "Learn how to whistle like the wind",
        "Play with toy sailboats in the bathtub",
        "Origami session – make things that fly",
        "Test the effectiveness of different DIY windmills with a fan",
        "Do a wind-inspired art project - like painting with blowing ink",
        "Design your own weather vane",
        "Play a kite-simulation video game and compare it to the real thing",
        "Have a wind-themed fashion show with the windiest clothes"
      ]
    },
    "cloudy": {
      "outdoor_activities": [
        "Go for a long, contemplative walk",
        "Cloud watching and guessing their shapes",
        "Take moody cloud-filled photos",
        "Play hide and seek in a park with lots of trees",
        "Visit a local botanical garden",
        "Play a friendly game of soccer or frisbee",
        "Go rollerblading in a cloudy park",
        "Take a scenic drive to a nearby lookout point",
        "Have a relaxing outdoor yoga session",
        "Bike around your neighborhood",
        "See who can find the weirdest cloud shapes!"
      ],
      "indoor_activities": [
        "Start an indoor herb garden",
        "Read that book you'\''ve been meaning to start",
        "Do a guided meditation focused on the calming effect of clouds",
        "Bake bread and share with neighbors",
        "Try out a new board game or puzzle",
        "Host a spontaneous talent show with family or friends",
        "Learn how to make cloud-shaped pancakes",
        "Write a cloud-themed poem or short story",
        "Create cloud art using cotton balls",
        "Organize your closet - then reward yourself with a treat",
        "Have a cloud-themed trivia night"
      ]
    },
    "stormy": {
      "outdoor_activities": [
        "Watch the storm from your porch - safe distance, of course!",
        "Try capturing lightning strikes with your camera",
        "Go puddle stomping in your rain boots",
        "Collect cool-looking storm debris - leaves, sticks, etc.",
        "Go on a mini storm chase - from a safe distance",
        "Visit a coastal area to watch big waves - from a safe area",
        "Fly a kite in the wind before the storm starts",
        "Set up a safe storm-viewing station with binoculars",
        "Check for rainbows once the storm passes",
        "Storm-themed photography challenge",
        "Have a storm watch party with popcorn and storm movies!"
      ],
      "indoor_activities": [
        "Tell ghost stories while listening to the thunder",
        "Do a storm-inspired painting - lots of dark blues and grays!",
        "Watch classic disaster movies",
        "Bake something indulgent – you deserve it during a storm",
        "Create your own thunderstorm sound effects with random objects",
        "Have a stormy weather playlist jam session",
        "Start a new craft project - knitting, sewing, etc.",
        "Write a short thriller story set during a storm",
        "Host an indoor thunder Olympics with challenges like couch diving",
        "Make your own candle in case the lights go out",
        "Have a DIY storm-themed escape room at home"
      ]
    }
  }
}'

sudo apt update && apt install mongodb-org redis-server -y

MONGO_URI="mongodb://localhost:27017"
DB_NAME="weather_db"
COLLECTION_NAME="activities"

if ! command -v mongoimport &> /dev/null; then
    echo "Error: mongoimport is not installed or not in PATH"
    exit 1
fi

if echo "$JSON_DATA" | mongoimport --uri="$MONGO_URI" --db="$DB_NAME" --collection="$COLLECTION_NAME" --drop; then
    echo "Activities successfully populated in MongoDB!"
else
    echo "Error: Failed to import data into MongoDB"
    exit 1
fi

