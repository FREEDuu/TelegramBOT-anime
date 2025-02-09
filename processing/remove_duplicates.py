import json

def unisci_e_salva_url(file1, file2, file3, file_output="url_unici.json"):
    """
    Unisce gli URL da tre file JSON, rimuove i duplicati e li salva in un nuovo file.

    Args:
        file1: Percorso del primo file JSON.
        file2: Percorso del secondo file JSON.
        file3: Percorso del terzo file JSON.
        file_output: Percorso del file JSON di output (default: "url_unici.json").
    """

    try:
        url_totali = []

        # Funzione per estrarre gli URL da un file JSON
        def estrai_url(percorso_file):
            with open(percorso_file, 'r', encoding='utf-8') as f:
                dati = json.load(f)
                if "TV Series" in dati:  # Assicura che la chiave esista
                    return dati["TV Series"]
                return []  # Restituisce una lista vuota se la chiave non esiste

        # Estrai URL da ogni file
        url_totali.extend(estrai_url(file1))
        url_totali.extend(estrai_url(file2))
        url_totali.extend(estrai_url(file3))

        # Rimuovi duplicati mantenendo l'ordine
        url_unici = []
        for url in url_totali:
            if url not in url_unici:
                url_unici.append(url)

        # Crea il dizionario per il nuovo file JSON
        dati_output = {"TV Series": url_unici}
        print('url unici -->', len(url_unici))
        # Salva in un nuovo file JSON
        with open(file_output, 'w', encoding='utf-8') as outfile:
            json.dump(dati_output, outfile, indent=4, ensure_ascii=False)

        print(f"URL unici e distinti salvati in '{file_output}'")

    except FileNotFoundError:
        print("Uno o più file non trovati.")
    except json.JSONDecodeError:
        print("Errore nella decodifica JSON di uno o più file.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")

# Esempio di utilizzo:
file_json_1 = "caso.json"  # Sostituisci con i tuoi percorsi
file_json_2 = "caso1.json"
file_json_3 = "caso2.json"
file_output = "url_unici.json"

unisci_e_salva_url(file_json_1, file_json_2, file_json_3, file_output)