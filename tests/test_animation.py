import json
import logging

from chicken_dinner.models.telemetry import Telemetry

logger = logging.getLogger()
logger.setLevel("INFO")

if __name__ == "__main__":
    # Load temp
    t = json.load(open("secret.json", "r"))
    telemetry = Telemetry.from_json(t)

    telemetry.playback_animation(
        "match.html",
        zoom=True,
        labels=True,
        label_players=None,
        # highlight_teams=["shroud"],
        highlight_winner=True,
        size=4,
        use_hi_res=False,
        color_teams=True
    )
