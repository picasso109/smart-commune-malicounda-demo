from functools import wraps
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

# ✅ garder le même nom pour compatibilité app.py
auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)

# =========================
# 👤 UTILISATEUR DEMO MAIRIE
# =========================
UTILISATEUR_DEMO = {
    "email": "maire@malicounda.sn",
    "mot_de_passe": "1234",
    "role": "Maire",
    "nom": "Maire de Malicounda"
}


# =========================
# 🔐 VALIDATION URL NEXT
# =========================
def is_safe_next_url(next_url):
    """
    Empêche les redirections externes dangereuses.
    """
    if not next_url:
        return False

    if next_url.startswith("http://") or next_url.startswith("https://"):
        return False

    return next_url.startswith("/")


# =========================
# 🔐 DÉCORATEUR DE PROTECTION
# =========================
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user = session.get("user")

        if not user:
            flash(
                "Veuillez vous connecter pour accéder au cockpit.",
                "warning"
            )
            return redirect(
                url_for(
                    "auth.login",
                    next=request.path
                )
            )

        return view(*args, **kwargs)

    return wrapped_view


# =========================
# 🔑 CONNEXION
# =========================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    erreur = None

    next_url = (
        request.args.get("next")
        or request.form.get("next")
    )

    # ✅ éviter boucle si next pointe login
    if next_url == url_for("auth.login"):
        next_url = None

    # ✅ si déjà connecté
    if session.get("user"):
        return redirect(
            next_url if is_safe_next_url(next_url)
            else url_for("dashboard.dashboard")
        )

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        mot_de_passe = request.form.get("password", "").strip()

        if (
            email == UTILISATEUR_DEMO["email"]
            and mot_de_passe == UTILISATEUR_DEMO["mot_de_passe"]
        ):
            session.clear()

            session["user"] = {
                "email": UTILISATEUR_DEMO["email"],
                "role": UTILISATEUR_DEMO["role"],
                "name": UTILISATEUR_DEMO["nom"]
            }

            session.permanent = True

            flash(
                f"Bienvenue {UTILISATEUR_DEMO['nom']} 👋",
                "success"
            )

            destination = (
                next_url
                if is_safe_next_url(next_url)
                else url_for("dashboard.dashboard")
            )

            return redirect(destination)

        erreur = "Email ou mot de passe incorrect."

    return render_template(
        "login.html",
        error=erreur,
        next=next_url
    )


# =========================
# 🚪 DÉCONNEXION
# =========================
@auth_bp.route("/logout")
@login_required
def logout():
    nom_utilisateur = (
        session.get("user", {})
        .get("name", "Utilisateur")
    )

    session.clear()

    flash(
        f"Déconnexion réussie. À bientôt {nom_utilisateur}.",
        "success"
    )

    return redirect(url_for("auth.login"))