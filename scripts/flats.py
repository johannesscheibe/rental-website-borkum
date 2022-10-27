from borkum.website.database import db_service


flats = {
    "baltrum": {
        "name": "Baltrum",
        "description": "Die Ferienwohnung Baltrum befindet sich im 1. Stock im Ferienhaus Hertha auf Borkum. Es erwarten Sie auf ca. 53 m² eine komfortabel ausgestattete Ferienwohnung mit Schlafzimmer, Wohnzimmer, Küche und Duschbad. \nDas Schlafsofa im Wohnraum bietet einer dritten Person eine Übernachtungsmöglichkeit. Beide Räume verfügen über einen Ost- bzw. Westbalkon mit Blick in die Dünen.",
        "properties": ["WiFi", "max. 3 Personen", "Nichtraucher", "Allergiker geeignet", "Parkplatz am Haus"," Balkon(ost und süd)", "Südlage", "Strandnähe"]
    },
    "borkum": {
        "name": "Borkum",
        "description": "Die Suite Borkum befindet sich im 1. Stock im Ferienhaus Hertha auf Borkum. Es erwarten Sie auf ca. 47 m² ein für 2 Personen komfortabel ausgestattetes Feriendomizil mit Schlafzimmer, Wohnzimmer, Küche und Duschbad. \nDas Schlafsofa im Wohnraum bietet einer weiteren Person eine Übernachtungsmöglichkeit. Beide Räume verfügen über einen Südbalkon mit Blick in die Dünen.",
        "properties": ["WiFi", "max. 3 Personen", "Nichtraucher", "Allergiker geeignet", "Parkplatz am Haus","2 Südbalkone mit Dünenblick", "Südlage", "Strandnähe", "Dünenblick"]
    },
    "kajo": {
        "name": "Kajo",
        "description": "Die Ferienwohnung Kajo (Greune-Stee-Weg 87) bietet ihnen sonnige und gemütliche Ferienwohnung in kurzer Entfernung zum Borkumer Südstrand und unmittelbar an den Dünen der Greune Stee mit einem herrlichen Inselwald zum Wandern. Sie blicken von den Balkonen / Terrassen oder aus den Zimmern direkt auf die Dünenlandschaft. \nVon der Haltestelle Jakob-Van-Dieken-Weg ist das Haus Hertha ca. 5-10 Gehminuten entfernt, den Südstrand erreichen sie direkt gegenüber nach 800 m Fußweg durch die Dünenlandschaft.",
        "properties": ["WiFi", "max. 6 Personen", "Nichtraucher", "Allergiker geeignet", "Parkplatz am Haus", "geräumige 74 m² Ferienwohnung", " Westbalkon", "Südlage", "Strandnähe"]
    },
    "langeoog": {
        "name": "Langeoog",
        "description": " Die Ferienwohnung Langeoog befindet sich im 2. Stock im Ferienhaus Hertha auf Borkum. Es erwarten Sie auf ca. 48 m² eine für 2 Personen komfortabel ausgestattete Ferienwohnung mit Schlafzimmer, Wohnzimmer, Küche und Duschbad. \nDas Wohnzimmer bietet einen jerrlichen Blick über die Dünen bishinzum Meer und verfügt über ein Schlafsofa für eine dritte Person.",
        "properties": ["WiFi", "max. 3 Personen", "Nichtraucher", "Allergiker geeignet", "Parkplatz am Haus", "Strandnähe", "Dünenblick"]
    },
    "memmert": {
        "name": "Memmert",
        "description": "Die Ferienwohnung Memmert befindet sich im Erdgeschoß im Ferienhaus Hertha auf Borkum. Es erwarten Sie eine für 4 bis 5 Personen komfortabel ausgestattete Ferienwohnung mit zwei Schlafzimmern, einem Wohnzimmer, sowie einer Küche und ein Duschbad. \nDas Schlafsofa im geräumigen Wohnraum bietet einer weiteren Person eine Übernachtungsmöglichkeit. Zusätzlich verfügt die Wohnung über eine eigene Terasse sowie einen kleinen Garten.",
        "properties": ["WiFi", "max. 5 Personen", "Nichtraucher", "Allergiker geeignet", "Parkplatz am Haus"," Westbalkon", "Terasse mit kleinem Garten", "Strandnähe"]
    },
    "studio-1": {
        "name": "Studio 1",
        "description": " Die Ferienwohnung Studio 1 befindet sich im 1. Stock im Ferienhaus Hertha auf Borkum. Es erwarten Sie eine für 2 Personen komfortabel ausgestattete Ferienwohnung mit Wohnzimmer, Schalfzimmer, Küche und Duschbad. \nDie Wohnung verfügt über eine große West-Dachterrasse mit eigenem Strandkorb.",
        "properties": ["WiFi", "max. 3 Personen", "Nichtraucher", "Hunde erlaubt", "Standkorb", "Parkplatz am Haus"," Westbalkon", "Südlage", "Strandnähe"]
    }, 
    "studio-2": {
        "name": "Studio 2",
        "description": "Die Ferienwohnung Studio 2 befindet sich im 1. Stock im Ferienhaus Hertha auf Borkum. Es erwarten Sie eine für 2 Personen komfortabel ausgestattete Ferienwohnung mit Wohnzimmer, Schlafzimmer, Pantryküche und Duschbad. \nDie Wohnung verfügt über eine West-Dachterrasse mit eigenem Strandkorb und Blick in die Dünen des Südstrandes.",
        "properties": ["WiFi", "max.3 Personen", "Nichtraucher", "Standkorb", "Hunde erlaubt","Parkplatz am Haus"," Westbalkon", "Südlage", "Strandnähe"]
    }
}

for _, values in flats.items():
    db_service.add_flat(name=values['name'], description=values['description'], properties=values['properties'])

