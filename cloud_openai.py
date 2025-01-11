"""uses cloud version of whisper model to transcribe
a key-like project name has tob be created in de OpenAi site,
you need an OpenAI account for that"""
from openai import OpenAI
from tiutools import OpenAICloudConfig

# 08-01-2025 laatste run: $0.02

config = OpenAICloudConfig(reset_keys=False)  # the keys are safe in the macOS keychain

api_key = config.api_key
project = config.prj_id

client = OpenAI(api_key=api_key,
                project=project)

audio_file = open("data/fragment.mp3", "rb")

transcription = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file,
  language="nl"
)
print(transcription.text)


"""/Users/ncdegroot/workspace/TranscribeTools/.venv/bin/python3.12 /Users/ncdegroot/workspace/TranscribeTools/cloud_openai.py 
 Oké, we wachten op iemand anders. Ja, Margot Mertz komt. Oké. Ze is van het leger des _hels_. Aha. En iemand van 
 vluchtelingen in de knel. Dus ik kijk of ik haar contact heb. Oké. Ja, prima. Ja. We gaan beginnen. Dus toch internet? 
 Nee, nee, nee. Oké. Oké. Ik ga proberen om rustig te praten. Want we hebben hier twee gasten uit Rome. 
 Anita? Yes. Yes. From Zagreb. Oh, Zagreb. Zagreb. Yes. Oké. En Annette uit Duitsland. Echt goed, ja. De andere 
 deelnemers zijn allemaal uit Nederland. Nederland en Lidia werken hier bij het NSV. En dit zit ook bij het gesprek. 
 Wij hebben ongeveer tot half één dit gesprek met elkaar. Daarna... Twaalf uur. Twaalf uur? Ja, tot twaalf uur. 
 Twaalf uur. Daarna gaan we lekker met elkaar lunchen. Oh. Nee, we gaan op lunch starten. We starten tot half één, ja. 
 Ja, klopt. Dan moet ik straks even praten met Mathijs. We hebben nog een pauze, denk ik, hè? We hebben nog een pauze, 
 ja. Oké. Ja. We hebben nog een pauze. En ik ga denk ik de deur even dichtdoen. Ja? Dan hebben we even... Wil jij dat 
 ik doe? Ja. Maar misschien is het leuk om even van elkaar te horen wie hier allemaal zitten. Van welke organisatie 
 je bent. Wat voor werk je doet. Wie mag ik het woord geven? Zal ik beginnen? Mijn naam is Christel. Mijn naamstikker 
 staat op mijn jasje. Christel Teekman. En ik ben de, ja, hoe zeg je dat? Promovenda van Kees. Ik ga de komende jaren 
 hier bij MST onderzoek doen. En daar ben ik net mee begonnen. Echt 1 september. Je valt vandaag met je neus in de doek. 
 Dit is voor mij ook de allereerste keer. Of de tweede keer dat ik hier ben. Maar in ieder geval met deze groep mensen. 
 En ik werk hiernaast ook nog op Hogeschool FIA. Dat is een hogeschool in Zwolle. En daar woon ik ook. En ik werk 3 
 dagen hier dan. Aan de Tilburg University. En Kees en MST en jullie groep heeft zeg maar een heel mooi onderzoek 
 geschreven de laatste jaren. En daar mag ik, ja, als promovenda de komende 4 jaren mee bezighouden. Mijn achtergrond 
 is, ik ben ook een social worker. Ik heb in de vrouwenhulpverlening gewerkt. In _relaxering_ gewerkt.
"""