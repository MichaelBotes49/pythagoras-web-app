from flask import Flask, render_template, request
import math
import fractions
import matplotlib.pyplot as plt

app = Flask(__name__)

def bereken_hipotenusa(a: float, b: float):
    """Bereken die hipotenusa en vereenvoudigde verhouding van die twee korter sye."""
    c_cm = math.sqrt(a**2 + b**2)
    c_mm = c_cm * 10
    c_inches = c_cm / 2.54
    verhouding = fractions.Fraction(int(a), int(b)).limit_denominator() if b != 0 else "Ongeldige verhouding"
    return format(c_cm, ".2f"), format(c_mm, ".2f"), format(c_inches, ".2f"), verhouding

def teken_driehoek(a, b, c):
    """Teken 'n driehoek en stoor dit as 'n beeld."""
    fig, ax = plt.subplots()
    ax.plot([0, a, 0], [0, 0, b], 'bo-', markersize=8)
    ax.plot([0, a], [b, 0], 'r-', linewidth=2)
    ax.text(a/2, -0.5, f'{a} cm', fontsize=12, ha='center')
    ax.text(-0.5, b/2, f'{b} cm', fontsize=12, va='center', rotation=90)
    ax.text(a/2, b/2, f'{c:.2f} cm', fontsize=12, ha='center')
    ax.set_xlim(-1, a+1)
    ax.set_ylim(-1, b+1)
    ax.set_aspect('equal')
    ax.grid(True)
    plt.title("Regte Driehoek")
    plt.savefig("static/driehoek.png")

@app.route("/", methods=["GET", "POST"])
def index():
    resultaat = None
    image_path = None
    
    if request.method == "POST":
        a = float(request.form["side_a"])
        b = float(request.form["side_b"])
        hipotenusa_cm, hipotenusa_mm, hipotenusa_inches, verhouding = bereken_hipotenusa(a, b)
        teken_driehoek(a, b, float(hipotenusa_cm))
        image_path = "static/driehoek.png"
        resultaat = {
            "cm": hipotenusa_cm,
            "mm": hipotenusa_mm,
            "inches": hipotenusa_inches,
            "verhouding": verhouding
        }

    return render_template("index.html", resultaat=resultaat, image_path=image_path)

if __name__ == "__main__":
    app.run(debug=True)
