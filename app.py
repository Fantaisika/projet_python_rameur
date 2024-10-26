from flask import Flask, render_template
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import json

app = Flask(__name__)

# Charger les fichiers JSON
dossier = 'C:/Users/fanti/Music/universite paris-sorbonne/python/rameur/'
dataraw = {}
noms_json = [fichier[:-5] for fichier in os.listdir(dossier) if fichier.endswith('.json')]

for fichier in os.listdir(dossier):
    if fichier.endswith(".json"):
        chemin_fichier = os.path.join(dossier, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            dataraw[fichier[:-5]] = json.load(f)

# Créer un dictionnaire pour les données nettoyées
dataclean = {
    "participant": [],
    "sexe": [],
    "calories_split_1": [],  
    "calories_split_2": [],  
    "calories_split_3": [],  
    "calories_split_4": []   
}

# Liste des noms masculins et féminins
nom_masculin = ['Maxime', 'Célestin', 'Julien', 'Eric', 'Edouard', 'Baptiste', 'Lois', 'Usama', 'Noé', 'Emilien', 'Tom', 'Ivan', 'Amaury', 'Thomas', 'Jerome', 'Corentin', 'Hervé']
nom_feminin = ['Neve', 'Jacqueline', 'Léa', 'Orlane', 'Anaë', 'Alice', 'Lison', 'Charlotte', 'Merle', 'Léonore', 'Valérie', 'Dominique', 'Nancy', 'Eloise', 'Julie']

# Extraire les données des JSON
for nfichier in noms_json:
    for participant in dataraw[nfichier]['results']['participants']:
        dataclean['participant'].append(participant.get('participant'))
        sexe = 'homme' if participant['participant'] in nom_masculin else 'femme'
        dataclean['sexe'].append(sexe)
        splits = participant['splits'][:4]
        for i in range(4):
            if i < len(splits):
                dataclean[f'calories_split_{i+1}'].append(splits[i].get('split_calories', 0))
            else:
                dataclean[f'calories_split_{i+1}'].append(0)

# Convertir en DataFrame
df = pd.DataFrame(dataclean)
df["calories_moyenne"] = df[["calories_split_1", "calories_split_2", "calories_split_3", "calories_split_4"]].mean(axis=1)

# Générer les graphiques
fig, ax = plt.subplots(1, 3, figsize=(18, 6), gridspec_kw={'width_ratios': [1.5, 1.5, 1]})

# Diagramme en courbe pour les calories par participant
ax[0].plot(df["participant"], df["calories_moyenne"], marker='o', color="skyblue")
ax[0].set_title("Calories Moyennes par Participant")
ax[0].set_xlabel("Participant")
ax[0].set_ylabel("Calories Moyennes")
ax[0].tick_params(axis='x', rotation=90)

# Diagramme en anneau (doughnut) pour les calories par sexe
df_sexe = df.groupby("sexe")["calories_moyenne"].mean()
ax[1].pie(df_sexe, labels=df_sexe.index, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.3))
ax[1].set_title("Calories Moyennes par Sexe")

# Table des données
ax[2].axis('off')
table = ax[2].table(cellText=df[["participant", "sexe", "calories_split_1", "calories_split_2", "calories_split_3", "calories_split_4"]].values, 
                    colLabels=["Participant", "Sexe", "Calories Split 1", "Calories Split 2", "Calories Split 3", "Calories Split 4"], 
                    loc="center", cellLoc="center")

bbox=[0, 0, 1.5, 1.5]
table.auto_set_font_size(False)
table.set_fontsize(6)

# Sauvegarder l'image
plt.tight_layout()
plt.savefig("static/moyenne_calories.png")
plt.close()

@app.route("/")
def calories():
    return render_template("calories.html")

if __name__ == "__main__":
    app.run(debug=True)
