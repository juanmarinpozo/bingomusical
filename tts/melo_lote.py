import json, os, sys, traceback
shard, n = int(sys.argv[1]), int(sys.argv[2])
OUT = 'tts/out/m'; os.makedirs(OUT, exist_ok=True)
pedido = [p for i, p in enumerate(json.load(open('tts/pedido-melo.json'))) if i % n == shard]
try:
    from melo.api import TTS
    m = TTS(language='ES', device='cpu'); spk = m.hps.data.spk2id['ES']
except Exception:
    open(f'{OUT}/log-{shard}.txt', 'w').write('ERROR AL ARRANCAR MELO\n' + traceback.format_exc()[-3000:]); raise
log = []; hechos = 0
for p in pedido:
    ruta = f"{OUT}/{p['id']}.wav"
    if os.path.exists(ruta): continue
    try:
        m.tts_to_file(p['texto'], spk, ruta, speed=1.0, quiet=True); hechos += 1; print('ok', p['id'], flush=True)
    except Exception:
        log.append(p['id'] + ' ' + traceback.format_exc()[-600:])
open(f'{OUT}/log-{shard}.txt', 'w').write(f'hechos {hechos} de {len(pedido)}\n' + ('\n'.join(log) or 'sin errores'))
