from app.models.plant import Plant


DISCLAIMER_EN = (
    "HelaCare provides source-grounded traditional-health information "
    "for education. It does not diagnose conditions or prescribe treatment."
)

DISCLAIMER_SI = (
    "HelaCare ලබා දෙන්නේ මූලාශ්‍ර සහිත සාම්ප්‍රදායික සෞඛ්‍ය දැනුම "
    "අධ්‍යාපනික අරමුණින් පමණි. මෙය රෝග විනිශ්චය කිරීමක් හෝ "
    "ප්‍රතිකාර නියම කිරීමක් නොවේ."
)


SI_PLANT_DATA = {

    "H001": {
        "name": "පොල්පලා",
        "use": (
            "දේශීය වාර්තා අනුව මුත්‍රා සම්බන්ධ තත්ත්ව, "
            "ශක්ති වර්ධනය, සාම්ප්‍රදායිකව 'රුධිර පවිත්‍ර කිරීම' "
            "ලෙස හැඳින්වෙන භාවිතය සහ ශරීර වේදනාව සඳහා භාවිත කර ඇත."
        ),
        "part": "සම්පූර්ණ ශාකය",
    },

    "H002": {
        "name": "මුකුණුවැන්න",
        "use": (
            "දේශීය වාර්තා අනුව ශරීර වේදනාව සඳහා සහ "
            "ශක්ති වර්ධනය සඳහා භාවිත කර ඇත."
        ),
        "part": "සම්පූර්ණ ශාකය",
    },

    "H003": {
        "name": "සුදුලූනු",
        "use": (
            "දේශීය වාර්තා අනුව ඇදුම, බඩේ වේදනාව "
            "සහ ශරීර වේදනාව සඳහා භාවිත කර ඇත."
        ),
        "part": "බල්බය",
    },

    "H004": {
        "name": "ගොටුකොළ",
        "use": (
            "දේශීය වාර්තා අනුව සෙම් සම්බන්ධ අපහසුතා "
            "(catarrh), ඇස් සම්බන්ධ අපහසුතා සහ "
            "ශක්ති වර්ධනය සඳහා භාවිත කර ඇත."
        ),
        "part": "සම්පූර්ණ ශාකය",
    },

    "H005": {
        "name": "කොත්තමල්ලි",
        "use": (
            "දේශීය වාර්තා අනුව සෙම්ප්‍රතිශ්‍යාව, උණ, "
            "ඇදුම සහ ශරීර වේදනාව සඳහා භාවිත කර ඇත."
        ),
        "part": "බීජ",
    },

    "H006": {
        "name": "ඉරමුසු",
        "use": (
            "දේශීය වාර්තා අනුව සෙම්ප්‍රතිශ්‍යාව, උණ, "
            "සාම්ප්‍රදායිකව 'රුධිර පවිත්‍ර කිරීම' ලෙස හැඳින්වෙන "
            "භාවිතය, ශරීර වේදනාව සහ දියවැඩියාව සම්බන්ධයෙන් "
            "භාවිත කර ඇත."
        ),
        "part": "මුල් සහ සම්පූර්ණ ශාකය",
    },

    "H007": {
        "name": "කොහිල",
        "use": (
            "දේශීය වාර්තා අනුව ශක්ති වර්ධනය සඳහා "
            "භාවිත කර ඇත."
        ),
        "part": "සම්පූර්ණ ශාකය",
    },

    "H008": {
        "name": "හාතාවාරිය",
        "use": (
            "දේශීය වාර්තා අනුව මුත්‍රා සම්බන්ධ තත්ත්ව "
            "සහ මුත්‍රා ගල් සම්බන්ධයෙන් භාවිත කර ඇත."
        ),
        "part": "සම්පූර්ණ ශාකය",
    },

    "H009": {
        "name": "කොමාරිකා",
        "use": (
            "දේශීය වාර්තා අනුව පිළිස්සුම් සහ "
            "හිසකෙස් වර්ධනය සම්බන්ධයෙන් භාවිත කර ඇත."
        ),
        "part": "කොළ",
    },

    "H010": {
        "name": "රණවරා",
        "use": (
            "දේශීය වාර්තා අනුව මුත්‍රා සම්බන්ධ තත්ත්ව, "
            "මුත්‍රා ගල් සහ සාම්ප්‍රදායිකව 'රුධිර පවිත්‍ර කිරීම' "
            "ලෙස හැඳින්වෙන භාවිතය සඳහා භාවිත කර ඇත."
        ),
        "part": "මල් සහ කොළ",
    },

    "H011": {
        "name": "කතුරුමුරුංගා",
        "use": (
            "දේශීය වාර්තා අනුව තොල් පැලීම "
            "සහ මුඛයේ තුවාල සඳහා භාවිත කර ඇත."
        ),
        "part": "කොළ",
    },

    "H012": {
        "name": "කොහොඹ",
        "use": (
            "දේශීය වාර්තා අනුව සන්ධි වේදනාව, කැසීම, "
            "දියවැඩියාව සහ පණු ආසාදන සම්බන්ධයෙන් භාවිත කර ඇත."
        ),
        "part": "කොළ සහ කඳ",
    },

    "H013": {
        "name": "වෙනිවැල්ගැට",
        "use": (
            "දේශීය වාර්තා අනුව උණ, කැස්ස, වේදනාව, "
            "ඇදුම සහ ළමුන්ගේ සම සම්බන්ධ තත්ත්ව සඳහා භාවිත කර ඇත."
        ),
        "part": "කඳ",
    },

    "H014": {
        "name": "මුරුංගා",
        "use": (
            "දේශීය වාර්තා අනුව ඇදුම සහ "
            "ඉදිමීම් සඳහා භාවිත කර ඇත."
        ),
        "part": "පොත්ත",
    },

    "H015": {
        "name": "බුලත්",
        "use": (
            "දේශීය වාර්තා අනුව බඩේ වේදනාව සඳහා "
            "භාවිත කර ඇත."
        ),
        "part": "කොළ",
    },

    "H016": {
        "name": "බෙලි",
        "use": (
            "දේශීය වාර්තා අනුව ඇදුම සහ උණ සඳහා "
            "භාවිත කර ඇත."
        ),
        "part": "කොළ, මුල් සහ මල්",
    },

    "H017": {
        "name": "දෙහි",
        "use": (
            "දේශීය වාර්තා අනුව කැස්ස, සෙම්ප්‍රතිශ්‍යාව, "
            "හිසරදය සහ බඩේ වේදනාව සඳහා භාවිත කර ඇත."
        ),
        "part": "කොළ",
    },

    "H018": {
        "name": "කරපිංචා",
        "use": (
            "දේශීය වාර්තා අනුව අධි රුධිර පීඩනය "
            "සම්බන්ධයෙන් භාවිත කර ඇත."
        ),
        "part": "කොළ",
    },

    "H019": {
        "name": "කහ",
        "use": (
            "දේශීය වාර්තා අනුව තුවාල, සම සම්බන්ධ තත්ත්ව "
            "සහ ඇදීම්/ඇඹරීම් (sprains) සඳහා භාවිත කර ඇත."
        ),
        "part": "රයිසෝමය",
    },

    "H020": {
        "name": "ඉඟුරු",
        "use": (
            "දේශීය වාර්තා අනුව උණ, සෙම්ප්‍රතිශ්‍යාව, "
            "ඇදුම සහ කැස්ස සඳහා භාවිත කර ඇත."
        ),
        "part": "රයිසෝමය",
    },
}


SI_SAFETY_NOTE = (
    "මෙම සාම්ප්‍රදායික භාවිතය සඳහා සුදුසු වෛද්‍ය හෝ "
    "සුදුසුකම් ලත් ප්‍රායෝගික විශේෂඥ සමාලෝචනය තවම අවශ්‍ය වේ. "
    "HelaCare මාත්‍රා උපදෙස් ලබා නොදේ."
)


def compose_urgent_answer(
    language: str
) -> str:

    if language == "si":

        return (
            "ඔබගේ පණිවිඩයේ හදිසි වෛද්‍ය අවධානය අවශ්‍ය විය හැකි "
            "ලක්ෂණයක් හඳුනාගෙන ඇත. සාම්ප්‍රදායික ප්‍රතිකාරයක් "
            "උත්සාහ කරමින් ප්‍රමාද නොවී වහාම සුදුසු වෛද්‍ය සේවාවක් "
            "හෝ ළඟම ඇති රෝහලක් අමතන්න."
        )

    return (
        "Your message contains a possible medical red flag. "
        "Do not delay care to try a traditional remedy. "
        "Please seek urgent professional medical assessment "
        "or contact your local emergency service now."
    )


def _display_name(
    plant: Plant
) -> str:

    return (
        plant.sinhala_name
        or plant.common_name
        or plant.scientific_name
        or f"Plant #{plant.id}"
    )


def _compose_sinhala_plant(
    plant: Plant
) -> str:

    data = SI_PLANT_DATA.get(
        plant.external_id
    )

    # Fallback if the plant has no Sinhala translation yet
    if not data:

        name = _display_name(
            plant
        )

        block = (
            f"{name}\n\n"
            "සාම්ප්‍රදායික භාවිතය:\n"
            f"{plant.traditional_use}"
        )

        if plant.part_used:
            block += (
                "\n\nභාවිත වන කොටස:\n"
                f"{plant.part_used}"
            )

        block += (
            "\n\nආරක්ෂක සටහන:\n"
            f"{SI_SAFETY_NOTE}"
        )

        return block

    return (
        f"{data['name']}\n\n"
        "සාම්ප්‍රදායික භාවිත වාර්තාව:\n"
        f"{data['use']}\n\n"
        "භාවිත වන කොටස:\n"
        f"{data['part']}\n\n"
        "ආරක්ෂක සටහන:\n"
        f"{SI_SAFETY_NOTE}"
    )


def compose_grounded_answer(
    plants: list[Plant],
    language: str
) -> str:

    if not plants:

        if language == "si":

            return (
                "මෙම ප්‍රශ්නයට පිළිතුරු දීමට HelaCare හි "
                "verified knowledge base එකේ ප්‍රමාණවත් "
                "මූලාශ්‍රගත තොරතුරු හමු නොවීය. "
                "HelaCare අනුමාන කර ප්‍රතිකාරයක් නිර්මාණය නොකරයි."
            )

        return (
            "I could not find enough verified, source-grounded "
            "information in the HelaCare knowledge base for that query. "
            "I will not invent a remedy."
        )

    blocks = []

    for plant in plants:

        if language == "si":

            blocks.append(
                _compose_sinhala_plant(
                    plant
                )
            )

            continue

        name = _display_name(
            plant
        )

        block = (
            f"{name}: documented traditional use in the verified dataset — "
            f"{plant.traditional_use}"
        )

        if plant.part_used:

            block += (
                f" Part used: "
                f"{plant.part_used}."
            )

        if plant.safety_note:

            block += (
                f" Safety note: "
                f"{plant.safety_note}"
            )

        blocks.append(
            block
        )

    return "\n\n".join(
        blocks
    )