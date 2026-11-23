# mskills

The one place my agent skills come from. A skill gets into Claude Code only by being added here. Updates from other people's skills get in only after I approve them.

## Two kinds of skill

- **Owned:** mine to change. Skills I wrote, and copies I changed. They never take updates from anyone.
- **Tracked:** an unchanged copy of someone else's skill. `./mskills update` fetches their new version into the repo, and committing it approves it.

`sources.json` records where each skill came from and which version I approved. A skill with no entry there is owned.

## Commands

```bash
./mskills list
```

Shows every skill by area, with its kind and source. Each area folder also has a README with a section per skill: what it is for, where it came from, and whether it can run code.

Each skill's one-sentence summary is in `sources.json`. To change one, edit it there and run `./mskills readme`. `add` takes `--summary`; without it, the summary is the first sentence of the skill's own description.

| Command | What it does |
|---|---|
| `./mskills add <source> <area>` | Fetch a skill into an area and link it. Add `--name` to rename it, or `--replace` to overwrite one that exists. |
| `./mskills remove <name>` | Delete the skill folder and its link. |
| `./mskills move <name> <area>` | Move a skill to another area. |
| `./mskills own <name>` | Mark a tracked skill as mine. Updates stop, and I can change it. |
| `./mskills update [name ...]` | Fetch new versions of tracked skills for review. |
| `./mskills link` | Link every skill into `~/.claude/skills`. |
| `./mskills readme` | Rewrite the README in each area folder. The other commands do this on their own. |
| `./mskills check` | Report anything Claude loads that did not come through mskills. |

A `<source>` is one of:

- `owner/repo/path/to/skill`, a folder in a GitHub repo. Add `@branch` to follow a branch other than the default.
- `https://github.com/owner/repo/tree/<branch>/<path>`
- `https://host/.well-known/agent-skills/<name>`, for sites that publish skills that way (uizze.sh does)
- A local folder. This adds the skill as owned.

New skills show up in new sessions. When a skill comes with scripts, `add` and `update` list them, so I know it can run code.

## Updating

```bash
./mskills update
```

For each tracked skill that changed upstream, this puts the new version in the repo and prints three commands: one to see the changes (`git diff`), one to approve them (`git commit`), one to reject them (`git restore` and `git clean`). Commit or reject before running `update` again.

If I changed a tracked skill in the repo, `update` skips it and says so. Then either run `./mskills own <name>` to keep my changes, or `./mskills update --force <name>` to drop them.

## Changing someone else's skill

1. `./mskills own <name>`
2. Change it to fit my rules: plain English, square corners, no product names in code, literal names.
3. Commit.

## Areas

| Area | What goes in it |
|---|---|
| [cloudflare/](cloudflare/README.md) | Workers, wrangler, Durable Objects and other Cloudflare work |
| [web/](web/README.md) | Next.js, React, shadcn, page speed |
| [ios/](ios/README.md) | Swift and iPhone apps |
| [design/](design/README.md) | UI design for any platform |
| [code/](code/README.md) | general engineering: debugging, tests, review, module design |
| [planning/](planning/README.md) | stress-testing plans, research, handoffs |
| [writing/](writing/README.md) | plain English, skill writing, pull requests |
| [content/](content/README.md) | reels, scripts, video, social data, images |
| [seo/](seo/README.md) | site audits, titles, internal links, comparison pages, launches |
| [marketing/](marketing/README.md) | customer research, copy, launch posts from commits |

`add` and `move` make a new area folder when one is needed. Skill names must be unique across all areas, because Claude Code sees one flat list. `add` refuses names of built-in Claude Code skills such as `code-review`, because mine would hide the built-in one.

## Rules

- Install skills only with `./mskills add`. Not with plugin installs or other skill installers. `./mskills check` catches anything that got in another way.
- Skills that belong to one project go in that project's `.claude/skills`, not here.
- Built-in Anthropic and Claude Code skills are not managed here.

## Secrets

No keys or tokens go in this repo. Skills that need them read them from somewhere else, like `~/Documents/workspace/contents/.env`, and never copy them here.

Check before each commit:

```bash
gitleaks dir . --redact
```

`.gitleaksignore` lists three findings in tracked skills that are not secrets: an example key in Cloudflare's docs, and HeyGen's public analytics key and sign-in client ID, which are in their public repo.

## Licenses

Licenses of the repos that tracked skills come from are in `licenses/`. Some skill folders also carry their own license file.

- Matt Pocock's skills: MIT
- Cloudflare skills: Apache 2.0
- HyperFrames: Apache 2.0
- shadcn: MIT
- seo-skills (Ilias Ism): MIT, stated in its README; it has no license file
- SimpleEnglish: MIT
- frontend-design and the uizze skills: license file inside the skill folder
