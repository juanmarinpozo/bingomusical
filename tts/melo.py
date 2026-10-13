import json, os, sys, traceback
from melo.api import TTS
shard, n = int(sys.argv[1]), int(sys.argv[2])
OUT = 'tts/out/m'; os.makedirs(OUT, exist_ok=True)
pedido = [p for i, p in enumerate(json.load(open('tts/pedido-melo.json'))) if i % n == shard]
m = TTS(language='ES', device='cpu'); spk = m.hps.data.spk2id['ES']
log = []
for p in pedido:
    ruta = f"{OUT}/{p['id']}.wav"
    if os.path.exists(ruta): continue
    try: m.tts_to_file(p['texto'], spk, ruta, speed=1.0, quiet=True); print('ok', p['id'], flush=True)
    except Exception: log.append(p['id'] + ' ' + traceback.format_exc()[-300:])
open(f'{OUT}/log-{shard}.txt', 'w').write('\n'.join(log) or 'sin errores')
