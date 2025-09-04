from typing import Final, TypeVar

import discord

GOLD: Final[str] = 'BBA53D'
EMBED_COLOR: Final[int] = int(GOLD, 16)

CHOICES: Final[list] = [
    'Yes.',
    'No.',
    'Maybe.',
    'Unlikely.',
    'Likely.',
    'You forgot to reset encoders.',
    'Go code autonomous.',
    'Tell Ty he can solo drive for the next comp.'
]

CHARACTER_LIMIT: Final[int] = 500

ACTIVITY: Final[discord.Activity] = discord.Activity(type=discord.ActivityType.listening, name='to lifts skipping')

STARTING: Final[discord.CustomActivity] = discord.CustomActivity(name="STARTING")

FTC_LOGO: Final[str] =  "../bot/ftc.png"

AWARD_DESCRIPTIONS: Final[dict[str, str]] = {
    "inspire": "*The team that receives this award is a strong ambassador for FIRST programs and a role model FIRST team. This team is a top contender for many other judged awards and is a gracious competitor.*",
    "think": "*This judged award is given to the team that best reflects the journey the team took as they experienced their season. The content within the portfolio is the key reference for JUDGES to help identify the most deserving team. The team could share or provide additional detailed information that is helpful for the judges. *",
    "connect": "*This judged award is given to the team that connects with their local science, technology, engineering, and math community to learn and adopt new tools through effort and persistence. This team has a team plan and has identified steps to achieve their goals. A portfolio is not required for this award.*",
    "reach": "*This award celebrates a team that has introduced and recruited new people into FIRST. Through their efforts, they have sparked others to embrace the FIRST culture. A portfolio is not required for this award.*",
    "sustain": "*Sustainability and planning are essential for a FIRST team, because they ensure the program’s long-term success. This award celebrates the team that has considered their future team members and has worked to ensure that their team or program will continue to exist long after they have gone on to develop their careers.*",
    "innovate": "*The Innovate Award celebrates a team that thinks imaginatively and has the ingenuity, creativity, and inventiveness to make their designs come to life. This judged award is given to the team that has an innovative and creative ROBOT design solution to any specific COMPONENTS in the FIRST Tech Challenge game.*",
    "control": "*The Control Award celebrates a team that uses sensors and software to increase the robot’s functionality during gameplay. This award is given to the team that demonstrates innovative thinking and solutions to solve game challenges such as autonomous operation, improving mechanical systems with intelligent control, or using sensors to achieve better results.*",
    "design": "*The Design Award celebrates the team that demonstrates an understanding of industrial design principles by striking a balance between form, function, and aesthetics while meeting the needs of this season’s challenge. The design process used should result in a robot which is efficiently designed and effectively addresses the game challenge.*",
    "choice": "*During the competition, the judging panel may meet a team whose unique efforts, performance, or dynamics merit recognition, but does not fit into any of the other award categories. To recognize these unique teams, FIRST offers a Judges’ Choice Award. *"
}

SEASON_OPTIONS: Final[list[dict[str, int]]] = [
    {"Into The Deep": 2024}, {"Centerstage": 2023}, {"Power Play": 2022}, {"Freight Frenzy": 2021},
    {"Ultimate Goal": 2020}, {"Skystone": 2019}
]

REGION_OPTIONS: Final[list[dict[str, str]]] = [
    {"All": "All"}, {"International": "International"}, {"United States": "UnitedStates"}, {"Ohio": "USOH"},
    {"Australia": "AU"}, {"Brazil": "BR"}, {"Alberta": "CAAB"}, {"British Columbia": "CABC"}, {"Ontario": "CAON"},
    {"Québec": "CAQC"}, {"China": "CN"}, {"Cyprus": "CY"}, {"Germany": "DE"}, {"Egypt": "EG"}, {"Spain": "ES"},
    {"France": "FR"}, {"Great Britain": "GB"}, {"Israel": "IL"}, {"India": "IN"}, {"Jamaica": "JM"},
    {"Libya": "LY"}, {"Mexico": "MX"}, {"Netherlands": "NL"}, {"Romania": "RO"}
]

EVENT_OPTIONS: Final[list[dict[str, str]]] = [
    {"All": "All"}, {"Qualifier": "Qualifier"}, {"League Meet": "LeagueMeet"}, {"League Tournament": "LeagueTournament"},
    {"FIRST Championship": "FIRSTChampionship"}, {"Championship": "Championship"},
    {"Demo Exhibition": "DemoExhibition"}, {"Innovation Challenge": "InnovationChallenge"}, {"Kickoff": "Kickoff"},
    {"Non-Competition": "NonCompetition"}, {"Off Season": "OffSeason"}, {"Official": "Official"},
    {"Other": "Other"}, {"Practice": "PracticeDay"}, {"Premier Event": "Premier"}, {"Scrimmage": "Scrimmage"},
    {"Super Qualifier": "SuperQualifier"}, {"Volunteer Signup": "VolunteerSignup"},
    {"Workshop": "Workshop"}
]

E = TypeVar('E', None, tuple[discord.Embed, discord.ui.View])