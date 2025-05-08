"""
    Projet : KingMods/webinterface
    Date Creation : 28/01/2025
    Date Revision : 08/05/2025
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : page web minimaliste pour gérer les mods
"""
from flask import Flask, render_template, request, redirect, jsonify
import configJson

app = Flask(__name__)

@app.route("/")
def home():
    new_mods_data = configJson.load_data(configJson.NEW_MODS_JSON_FILE)
    return render_template("home.html", objects=new_mods_data)

@app.route("/my_mods")
def downloaded():
    download_mods_data = configJson.load_data(configJson.DOWNLOADED_MODS_JSON_FILE)
    return render_template("my_mods.html", objects=download_mods_data)

@app.route("/add_manual_mod", methods=["GET", "POST"])
def add_mod():
    if request.method == "POST":
        name = request.form["mod_name"]
        link = request.form["mod_link"]

        download_mods_data = configJson.load_data(configJson.DOWNLOADED_MODS_JSON_FILE)
        download_mods_data.append({"title": name, "link": link, "toUpdate": 0})
        configJson.save_data(configJson.DOWNLOADED_MODS_JSON_FILE, download_mods_data)

        return redirect("/my_mods")  # ou autre route
    return render_template("add_manual_mod.html")

@app.route("/add", methods=["POST"])
def add_downloaded():
    link = request.form["link"]
    download_mods_data = configJson.load_data(configJson.DOWNLOADED_MODS_JSON_FILE)
    new_mods_data = configJson.load_data(configJson.NEW_MODS_JSON_FILE)

    # Trouver l'objet dans les nouveaux mods
    for mod in new_mods_data:
        if mod["link"] == link:
            download_mods_data.append(mod)
            new_mods_data.remove(mod)
            break

    configJson.save_data(configJson.DOWNLOADED_MODS_JSON_FILE, download_mods_data)
    configJson.save_data(configJson.NEW_MODS_JSON_FILE, new_mods_data)
    return redirect("/")

@app.route("/delete_mod", methods=["POST"])
def delete_mod():
    link = request.form["link"]
    download_mods_data = configJson.load_data(configJson.DOWNLOADED_MODS_JSON_FILE)

    for mod in download_mods_data:
        if mod["link"] == link:
            download_mods_data.remove(mod)
            break

    configJson.save_data(configJson.DOWNLOADED_MODS_JSON_FILE, download_mods_data)
    return redirect("/my_mods")

@app.route('/update_mod', methods=['POST'])
def update_mod():
    link = request.form["link"]
    download_mods_data = configJson.load_data(configJson.DOWNLOADED_MODS_JSON_FILE)

    # Recherche du lien et mise à jour du champ 'update'
    for mod in download_mods_data:
        if mod['link'] == link:
            mod['toUpdate'] = 0
            configJson.save_data(configJson.DOWNLOADED_MODS_JSON_FILE, download_mods_data)

            # return redirect(link)  # Rediriger l'utilisateur vers le lien
            return redirect("/my_mods")

    return redirect("/my_mods")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
