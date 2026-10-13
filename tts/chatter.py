import json, os, sys, traceback
import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
shard, n = int(sys.argv[1]), int(sys.argv[2])
OUT = 'tts/out/c'; os.makedirs(OUT, exist_ok=True)
pedido = [p for i, p in enumerate(json.load(open('tts/pedido-chatter.json'))) if i % n == shard]
m = ChatterboxMultilingualTTS.from_pretrained(device='cpu')
log = []
for p in pedido:
    ruta = f"{OUT}/{p['id']}.wav"
    if os.path.exists(ruta): continue
    try:
        w = m.generate(p['texto'], language_id='es', audio_prompt_path='tts/ref.wav')
        ta.save(ruta, w, m.sr); print('ok', p['id'], flush=True)
    except Exception: log.append(p['id'] + ' ' + traceback.format_exc()[-300:])
open(f'tts/out/c/log-{shard}.txt', 'w').write('\n'.join(log) or 'sin errores')
