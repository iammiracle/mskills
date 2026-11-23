// Render a scene to an mp4 (or one still) from real 3D anatomy meshes. No AI video model.
//   node render.cjs scene.resolved.json out.mp4
//   node render.cjs scene.resolved.json still.png --at 3.5      (check a moment before rendering it all)
// A scene with "page": "ipad.html" and "screen": "<another resolved scene>" first renders that
// screen recording at iPad size, then films it on a code-built iPad lying on a desk.
// STL paths in a scene are relative to the scene file (fetch_parts.py sets that up). Needs puppeteer + ffmpeg.
const http = require('http'), fs = require('fs'), path = require('path'), { spawn, execFileSync } = require('child_process')
const puppeteer = require('puppeteer')

const TYPES = { '.html': 'text/html', '.json': 'application/json', '.stl': 'application/octet-stream', '.jpg': 'image/jpeg', '.png': 'image/png' }

async function render(scenePath, outPath, stillAt = null) {
  const sceneDir = path.dirname(path.resolve(scenePath))
  const cfg = JSON.parse(fs.readFileSync(scenePath, 'utf8'))
  const FPS = cfg.fps || 30, DUR = cfg.duration || 10

  if (cfg.page === 'ipad.html') { // pass 1: the app's screen recording at iPad proportions
    const screenPath = path.resolve(sceneDir, cfg.screen)
    const screenMp4 = path.join(sceneDir, `.${path.basename(screenPath, '.json')}.screen.mp4`)
    const framesDir = `.frames-${path.basename(screenPath, '.json')}`
    if (!fs.existsSync(screenMp4) || fs.statSync(screenMp4).mtimeMs < fs.statSync(screenPath).mtimeMs) await render(screenPath, screenMp4)
    fs.rmSync(path.join(sceneDir, framesDir), { recursive: true, force: true }); fs.mkdirSync(path.join(sceneDir, framesDir))
    execFileSync('ffmpeg', ['-v', 'error', '-i', screenMp4, '-q:v', '2', path.join(sceneDir, framesDir, '%05d.jpg')])
    cfg.framesDir = framesDir
    cfg.frames = fs.readdirSync(path.join(sceneDir, framesDir)).length
  }

  const viewer = path.join(__dirname, cfg.page || 'viewer.html')
  const server = http.createServer((req, res) => {
    const u = decodeURIComponent(req.url.split('?')[0])
    if (u === '/__scene.json') { res.writeHead(200, { 'Content-Type': 'application/json' }); return res.end(JSON.stringify(cfg)) }
    const file = u === '/' + path.basename(viewer) ? viewer : path.join(sceneDir, path.normalize(u).replace(/^(\.\.[/\\])+/, ''))
    if (file !== viewer && !file.startsWith(sceneDir)) { res.writeHead(403); return res.end() }
    fs.readFile(file, (e, d) => { if (e) { res.writeHead(404); return res.end() } res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' }); res.end(d) })
  })
  await new Promise((r) => server.listen(0, '127.0.0.1', r))
  const browser = await puppeteer.launch({ headless: 'new', args: ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'] })
  try {
    const page = await browser.newPage()
    page.on('console', (m) => { if (m.type() === 'error' && !/favicon|404/.test(m.text())) console.error('page:', m.text()) })
    page.on('pageerror', (e) => console.error('page error:', e.message))
    await page.setViewport({ width: cfg.width || 1080, height: cfg.height || 1920, deviceScaleFactor: 1 })
    await page.goto(`http://127.0.0.1:${server.address().port}/${path.basename(viewer)}?scene=/__scene.json`)
    await page.waitForFunction('window.__ready === true', { timeout: 180000 })

    if (stillAt !== null) {
      await page.evaluate((t) => window.renderAt(t), stillAt)
      await page.screenshot({ path: outPath })
      console.log('still ->', outPath)
      return
    }
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', String(FPS), outPath], { stdio: ['pipe', 'inherit', 'inherit'] })
    const n = Math.round(DUR * FPS), t0 = Date.now()
    for (let i = 0; i < n; i++) {
      await page.evaluate((t) => window.renderAt(t), i / FPS)
      const buf = await page.screenshot({ type: 'jpeg', quality: 95 })
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r))
      if (i % 60 === 0) process.stdout.write(`frame ${i}/${n}\r`)
    }
    ff.stdin.end()
    await new Promise((r) => ff.on('close', r))
    console.log(`${n} frames in ${((Date.now() - t0) / 1000).toFixed(1)}s ->`, outPath)
  } finally {
    await browser.close()
    server.close()
  }
}

const [scenePath, outPath] = process.argv.slice(2)
if (!scenePath || !outPath) { console.error('usage: node render.cjs scene.resolved.json out.mp4 [--at seconds]'); process.exit(1) }
const at = process.argv.indexOf('--at')
render(scenePath, outPath, at > 0 ? parseFloat(process.argv[at + 1]) : null).catch((e) => { console.error(e); process.exit(1) })
