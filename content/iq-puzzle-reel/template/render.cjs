// node render.cjs stills t1,t2,...  |  node render.cjs full
const puppeteer = require('puppeteer'); const fs = require('fs')
;(async () => {
  const mode = process.argv[2]
  const b = await puppeteer.launch({ headless: 'new', args: ['--allow-file-access-from-files'] })
  const p = await b.newPage(); await p.setViewport({ width: 1080, height: 1920 })
  await p.goto('file://' + __dirname + '/index.html', { waitUntil: 'networkidle0' })
  await p.evaluate(() => window.READY); await new Promise(r => setTimeout(r, 300))
  fs.writeFileSync('cues.json', JSON.stringify(await p.evaluate(() => window.CUES)))
  if (mode === 'stills') {
    fs.mkdirSync('stills', { recursive: true })
    for (const t of process.argv[3].split(',').map(Number)) {
      await p.evaluate((t) => window.seek(t), t)
      await p.screenshot({ path: `stills/${String(t).padStart(5, '0')}.jpg`, quality: 80, type: 'jpeg' })
    }
  } else {
    fs.rmSync('frames', { recursive: true, force: true }); fs.mkdirSync('frames')
    const dur = await p.evaluate(() => window.DUR), n = Math.round(dur * 30)
    for (let i = 0; i < n; i++) {
      await p.evaluate((t) => window.seek(t), i / 30)
      await p.screenshot({ path: `frames/${String(i).padStart(5, '0')}.jpg`, quality: 92, type: 'jpeg' })
    }
  }
  await b.close()
})()
