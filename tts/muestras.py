import os, traceback, subprocess
OUT='tts/out'; os.makedirs(OUT, exist_ok=True); LOG=[]
T=("Korium es tu herramienta de trabajo como agente: tus contactos, tus llamadas, el test A ene ese y tus objetivos, todo en un solo lugar. "
   "Es un único archivo. Lo abres con doble clic en Chrome o en Edge, funciona sin internet y no hay que instalar nada.")
def paso(nombre, f):
    try: f(); LOG.append(nombre+' OK')
    except Exception: LOG.append(nombre+' ERROR '+traceback.format_exc()[-600:])
def gtts():
    from gtts import gTTS
    gTTS(T, lang='es', tld='es').save(f'{OUT}/m-gtts.mp3')
def melo():
    from melo.api import TTS
    m=TTS(language='ES', device='cpu'); m.tts_to_file(T, m.hps.data.spk2id['ES'], f'{OUT}/m-melo.wav', speed=1.0)
def chatter():
    import torchaudio as ta
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    m=ChatterboxMultilingualTTS.from_pretrained(device='cpu')
    w=m.generate(T, language_id='es'); ta.save(f'{OUT}/m-chatterbox.wav', w, m.sr)
    if os.path.exists('tts/ref.wav'):
        w=m.generate(T, language_id='es', audio_prompt_path='tts/ref.wav'); ta.save(f'{OUT}/m-chatterbox-ref.wav', w, m.sr)
import sys
for n in sys.argv[1:]: paso(n, globals()[n])
open(f'{OUT}/log-{"-".join(sys.argv[1:])}.txt','w').write('\n'.join(LOG))
