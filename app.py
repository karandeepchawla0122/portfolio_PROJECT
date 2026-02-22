from flask import Flask, render_template, request

app = Flask(__name__)

def analyze_portfolio(metals, fd, stocks, mutual_funds):
    total = metals + fd + stocks + mutual_funds

    metals_pct = (metals / total) * 100 if total > 0 else 0
    fd_pct = (fd / total) * 100 if total > 0 else 0
    stocks_pct = (stocks / total) * 100 if total > 0 else 0
    mf_pct = (mutual_funds / total) * 100 if total > 0 else 0

    user_portfolio = {
        "Metals": metals_pct,
        "FD": fd_pct,
        "Stocks": stocks_pct,
        "Mutual Funds": mf_pct
    }

    suggestions = []
    

    if metals_pct > 50:
        suggestions.append("Metals are high, consider reducing them for better diversification.")
    if fd_pct > 70:
        suggestions.append("FD is dominating, consider investing in stocks or mutual funds for growth.")
    if stocks_pct < 20:
        suggestions.append("Stocks are low, consider increasing for higher potential returns.")
    if mf_pct < 20:
        suggestions.append("Mutual funds are low, consider investing for balanced growth.")

    sample_portfolios = [
        {"Metals":60, "FD":30, "Stocks":5, "MF":5},
        {"Metals":30, "FD":50, "Stocks":15, "MF":5},
        {"Metals":30, "FD":30, "Stocks":30, "MF":10},
        {"Metals":25, "FD":40, "Stocks":25, "MF":10},
        {"Metals":40, "FD":35, "Stocks":20, "MF":5}
    ]

    def find_closest_portfolio(user, samples):
        closest = None
        min_diff = float('inf')
        for sample in samples:
            diff = 0
            for asset in user:
                key = asset if asset != "Mutual Funds" else "MF"
                diff += abs(user[asset] - sample[key])
            if diff < min_diff:
                min_diff = diff
                closest = sample
        return closest

    closest_portfolio = find_closest_portfolio(user_portfolio, sample_portfolios)

    for asset in user_portfolio:
        key = asset if asset != "Mutual Funds" else "MF"
        diff = closest_portfolio[key] - user_portfolio[asset]
        if abs(diff) > 5:
            if diff > 0:
                suggestions.append(f"Increase {asset} by {round(diff,1)}%")
            else:
                suggestions.append(f"Decrease {asset} by {abs(round(diff,1))}%")

    average_total = 500000
    if total > average_total:
        suggestions.append("Your portfolio value is above average!")
    else:
        suggestions.append("Your portfolio value is below average. Try increasing investments.")

    return total, metals_pct, fd_pct, stocks_pct, mf_pct, suggestions


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    metals = float(request.form.get("metals") or 0)
    fd = float(request.form.get("fd") or 0)
    stocks = float(request.form.get("stocks") or 0)
    mf = float(request.form.get("mf") or 0)

    total, metals_pct, fd_pct, stocks_pct, mf_pct, suggestions = analyze_portfolio(
        metals, fd, stocks, mf
    )

    return render_template(
        "index.html",
        total=total,
        metals_pct=round(metals_pct, 2),
        fd_pct=round(fd_pct, 2),
        stocks_pct=round(stocks_pct, 2),
        mf_pct=round(mf_pct, 2),
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(debug=True)