import asyncio, json, os, edge_tts
OUT = 'tts/out'; os.makedirs(OUT, exist_ok=True)
async def main():
    voces = await edge_tts.list_voices()
    es = [v for v in voces if v['Locale'].startswith('es-')]
    with open(f'{OUT}/voces.txt', 'w') as f:
        for v in es: f.write(f"{v['ShortName']}\t{v['Gender']}\t{v.get('VoiceTag',{}).get('VoicePersonalities','')}\n")
    pedido = json.load(open('tts/pedido.json'))
    sem = asyncio.Semaphore(6)
    async def una(p):
        ruta = f"{OUT}/{p['id']}.mp3"
        if os.path.exists(ruta): return
        async with sem:
            for intento in range(4):
                try:
                    await edge_tts.Communicate(p['texto'], p['voz'], rate=p.get('rate', '+0%')).save(ruta); return
                except Exception as e:
                    print('reintento', p['id'], e); await asyncio.sleep(3)
    pedidos = []
    for p in pedido:
        if p['voz'] == 'TODAS_ES_ES_MUJER':
            for v in es:
                if v['Locale'] == 'es-ES' and v['Gender'] == 'Female':
                    pedidos.append({**p, 'voz': v['ShortName'], 'id': p['id'] + '-' + v['ShortName']})
        else: pedidos.append(p)
    await asyncio.gather(*[una(p) for p in pedidos])
asyncio.run(main())
