import matplotlib
matplotlib.use('Agg')  # Utilizza un backend che non richiede GUI, adatto per server headless
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from flask import Flask, render_template, url_for
import os

# Configurazione Flask
app = Flask(__name__)

# Lettura dei file CSV
dati = pd.read_csv('utilizzo_social_media.csv')
lettura_vs_internet = pd.read_csv('letturaVs_internet.csv')
grafico_social_media = pd.read_csv('grafico_social_media.csv')

# Calcola alcune statistiche di base sull'utilizzo dei social media
media_utilizzo = dati['Ore_Medie_Giornaliere'].mean()

# Regressione lineare per analizzare la tendenza dell'utilizzo nel tempo
anni = dati['Anno'].values.reshape(-1, 1)
ore = dati['Ore_Medie_Giornaliere'].values.reshape(-1, 1)

modello = LinearRegression()
modello.fit(anni, ore)

pred_ore = modello.predict(anni)

# Calcolo dell'indice di dipendenza
dati['variazione_percentuale'] = dati['Ore_Medie_Giornaliere'].pct_change() * 100
media_variazione_percentuale = dati['variazione_percentuale'].mean()
dipendenza_messaggio = ""
if media_variazione_percentuale > 10:
    dipendenza_messaggio = "L'aumento dell'utilizzo suggerisce una crescita significativa nella dipendenza dai social media."
else:
    dipendenza_messaggio = "Non ci sono evidenze chiare di un aumento significativo della dipendenza dai social media."

# Funzione per generare il grafico delle ore medie di utilizzo
def genera_grafico():
    plt.figure(figsize=(10, 6))
    plt.scatter(dati['Anno'], dati['Ore_Medie_Giornaliere'], color='blue', label='Dati Reali')
    plt.plot(dati['Anno'], pred_ore, color='red', linestyle='--', label='Trend Lineare')
    plt.xlabel('Anno')
    plt.ylabel('Ore Medie di Utilizzo Giornaliere')
    plt.title('Analisi del Numero di Ore di Utilizzo dei Social Media nel Tempo')
    plt.legend()
    plt.grid(True)
    grafico_path = os.path.join('static', 'grafico.png')
    plt.savefig(grafico_path)
    plt.close()
    return 'static/grafico.png'

# Funzione per generare il grafico sull'evoluzione dei social media (numero di utenti)
def genera_grafico_evoluzione_utenti():
    plt.figure(figsize=(10, 6))
    for social in grafico_social_media['Social'].unique():
        dati_social = grafico_social_media[grafico_social_media['Social'] == social]
        plt.plot(dati_social['Anno'], dati_social['Utenti_Milioni'], marker='o', linestyle='-', label=social)
    plt.xlabel('Anno')
    plt.ylabel('Numero di Utenti (Milioni)')
    plt.title('Evoluzione delle Piattaforme Social Media nel Tempo (Numero di Utenti)')
    plt.legend()
    plt.grid(True)
    grafico_path = os.path.join('static', 'grafico_evoluzione_utenti.png')
    plt.savefig(grafico_path)
    plt.close()
    return 'static/grafico_evoluzione_utenti.png'

# Funzione per generare il grafico sull'evoluzione dei social media (ore medie giornaliere)
def genera_grafico_evoluzione_ore_medie():
    plt.figure(figsize=(10, 6))
    for social in grafico_social_media['Social'].unique():
        dati_social = grafico_social_media[grafico_social_media['Social'] == social]
        plt.plot(dati_social['Anno'], dati_social['Ore_Medio_Giornaliere'], marker='o', linestyle='-', label=social)
    plt.xlabel('Anno')
    plt.ylabel('Ore Medie di Utilizzo Giornaliere')
    plt.title('Evoluzione delle Piattaforme Social Media nel Tempo (Ore Medie di Utilizzo)')
    plt.legend()
    plt.grid(True)
    grafico_path = os.path.join('static', 'grafico_evoluzione_ore_medie.png')
    plt.savefig(grafico_path)
    plt.close()
    return 'static/grafico_evoluzione_ore_medie.png'

# Funzione per generare il grafico sul rapporto tra lettura e utilizzo di Internet
def genera_grafico_lettura_vs_internet():
    plt.figure(figsize=(10, 6))
    plt.plot(lettura_vs_internet['Anno'], lettura_vs_internet['lettura'], marker='o', linestyle='-', color='green', label='Tempo dedicato alla lettura')
    plt.plot(lettura_vs_internet['Anno'], lettura_vs_internet['internet'], marker='o', linestyle='-', color='blue', label='Tempo dedicato all utilizzo di Internet')
    plt.xlabel('Anno')
    plt.ylabel('Ore Medie per Giorno')
    plt.title('Rapporto tra Lettura e Utilizzo di Internet nel Tempo')
    plt.legend()
    grafico_path = os.path.join('static', 'grafico_lettura_vs_internet.png')
    plt.savefig(grafico_path)
    plt.close()
    return 'static/grafico_lettura_vs_internet.png'

# Rotte Flask
@app.route('/')
def index():
    grafico_path = genera_grafico()
    return render_template('index.html', media_utilizzo=media_utilizzo, media_variazione_percentuale=media_variazione_percentuale, dipendenza_messaggio=dipendenza_messaggio, grafico_path=url_for('static', filename='grafico.png'))

@app.route('/benvenuto')
def benvenuto():
    return render_template('benvenuto.html')

@app.route('/conclusione')
def conclusione():
    return render_template('conclusione.html')

@app.route('/evoluzione_utenti')
def evoluzione_utenti():
    grafico_evoluzione_utenti_path = genera_grafico_evoluzione_utenti()
    return render_template('evoluzione_utenti.html', grafico_evoluzione_utenti_path=url_for('static', filename='grafico_evoluzione_utenti.png'))

@app.route('/evoluzione_ore_medie')
def evoluzione_ore_medie():
    grafico_evoluzione_ore_medie_path = genera_grafico_evoluzione_ore_medie()
    return render_template('evoluzione_ore_medie.html', grafico_evoluzione_ore_medie_path=url_for('static', filename='grafico_evoluzione_ore_medie.png'))

@app.route('/rapporto_lettura')
def rapporto_lettura():
    grafico_lettura_vs_internet_path = genera_grafico_lettura_vs_internet()
    return render_template('rapporto_lettura.html', grafico_lettura_vs_internet_path=url_for('static', filename='grafico_lettura_vs_internet.png'))

# Avvio dell'app Flask
if __name__ == "__main__":
    from flask import url_for  # Import corretto per url_for
    app.run(debug=True)