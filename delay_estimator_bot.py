from flask import Flask, request, jsonify
import math

app = Flask(__name__)

def contextual_delay_estimator(n, fdev, a, b, c):
    """
    Estimate contextual delay based on task and environment factors.

    Parameters:
    - n: best-case time (weeks)
    - fdev: fraction of task that is R&D (0 to 1)
    - a: HPC reliability factor (0 = no HPC, 1 = average)
    - b: number of coauthors who must give feedback (excluding PI)
    - c: ambient stress factor (1 = typical, <1 = low, >1 = high)

    Returns:
    - lower: n
    - upper: n + 2 * sigma
    - mode: n + sigma
    """
    sigma1_squared = ((n / 4) ** 2) * ((2 * n * fdev) ** 2 + (1 - fdev) ** 2)
    sigma2_squared = ((n / 4) ** 2) * (4 * a ** 2 + b ** 2 + 2)
    sigma3_squared = ((c * n / 8) ** 2)

    sigma_total = math.sqrt(sigma1_squared + sigma2_squared + sigma3_squared)

    lower = round(n, 1)
    upper = round(n + 2 * sigma_total, 1)
    mode = round(n + sigma_total, 1)

    return {
        "lower": lower,
        "upper": upper,
        "mode": mode
    }

@app.route("/slack/delay", methods=["POST"])
def delay_response():
    text = request.form.get("text", "").strip()

    if text == "" or text.lower() == "help":
        return jsonify({
            "response_type": "ephemeral",
            "text": (
                "*Delay Estimator Help*\n"
                "Estimate contextual delays for research tasks using 5 parameters.\n\n"
                "*Usage:*\n"
                "`/delay-estimator best_case_weeks=2 fraction_RD=0.8 hpc_factor=1 num_coauthors=1 stress_level=1`\n\n"
                "*Parameters:*\n"
                "- `best_case_weeks`: Minimum possible time required, in weeks (e.g. 2)\n"
                "- `fraction_RD`: Fraction of task that is R&D (0 to 1)\n"
                "- `hpc_factor`: 0 = no HPC, 1 = average reliability, >1 = worse than average\n"
                "- `num_coauthors`: Number of coauthors who must weigh in (excluding PI)\n"
                "- `stress_level`: 0.5 = rested, 1 = typical, >1 = depleted\n"
            )
        })

    try:
        params = dict(pair.split('=') for pair in text.split())
        n = float(params['best_case_weeks'])
        fdev = float(params['fraction_RD'])
        a = float(params['hpc_factor'])
        b = float(params['num_coauthors'])
        c = float(params['stress_level'])

        result = contextual_delay_estimator(n, fdev, a, b, c)

        return jsonify({
            "response_type": "in_channel",
            "text": (
                f"⏲️ *Estimated Time to Completion:*\n"
                f"- Mode (most likely): {result['mode']} weeks\n"
                f"- Lower Bound: {result['lower']} weeks\n"
                f"- Upper Bound: {result['upper']} weeks"
            )
        })

    except Exception as e:
        return jsonify({
            "response_type": "ephemeral",
            "text": f"⚠️ Error: {str(e)}"
        })

if __name__ == "__main__":
    app.run()
