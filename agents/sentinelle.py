#!/usr/bin/env python3
"""
Ghost Vault — sentinelle.
Agent de surveillance : lit les journaux d'accès du coffre et des leurres,
repère ce qui est louche, alerte. Ne détient jamais ni clé ni donnée.
Projet de Glava Volya.
"""
import json, time, urllib.request, datetime

JOURNAL = "/var/log/labo/evenements.log"
ALERTES = "/var/log/labo/alertes.log"
LEURRES = ("lab-621", "lab-622")   # contact = alerte immédiate
MODELE  = "qwen2.5:3b"

def alerte(niveau, texte):
    ligne = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} [{niveau}] {texte}"
    print(ligne, flush=True)
    with open(ALERTES, "a") as f:
        f.write(ligne + "\n")

def avis_ia(lignes):
    consigne = ("Tu es analyste sécurité. Voici des lignes du journal d'un "
                "coffre-fort à secrets. Réponds en une ligne commençant par "
                "NORMAL ou SUSPECT, puis la raison.\n\n" + "\n".join(lignes))
    corps = json.dumps({"model": MODELE, "prompt": consigne,
                        "stream": False}).encode()
    req = urllib.request.Request("http://127.0.0.1:11434/api/generate",
                                 data=corps,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["response"].strip()

def suivre():
    with open(JOURNAL) as f:
        f.seek(0, 2)
        lot, dernier = [], time.time()
        while True:
            ligne = f.readline()
            if ligne:
                if any(l in ligne for l in LEURRES):
                    alerte("ALERTE", "Contact avec un leurre : " + ligne.strip()[:300])
                else:
                    lot.append(ligne.strip()[:500])
            else:
                time.sleep(1)
            if lot and (len(lot) >= 20 or time.time() - dernier > 60):
                try:
                    avis = avis_ia(lot)
                    if avis.upper().startswith("SUSPECT"):
                        alerte("SUSPECT", avis)
                except Exception as e:
                    alerte("PANNE", f"IA injoignable : {e}")
                lot, dernier = [], time.time()

if __name__ == "__main__":
    suivre()
