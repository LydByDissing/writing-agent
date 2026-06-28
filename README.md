# writing-agent

A Claude Code plugin that writes professional business emails in any language. It interviews you in Danish, drafts a canonical Danish email, translates it with cultural adaptation, and quality-reviews the result — all inside Claude Code.

## What it does

1. **Interview** — asks 9 structured questions in Danish to capture intent, recipient, tone, and call to action
2. **Danish draft** — writes the canonical email; you approve before anything is translated
3. **Cultural translation** — translates into your target language with formality and structure calibrated to the recipient's country
4. **Language review** — a native-speaker persona proofreads, removes LLM markers, and reports what was changed
5. **Output** — copies the final email to your clipboard and generates a `mailto:` link you can open directly in your mail client

## Install

Add the plugin to your Claude Code project:

```bash
claude mcp add writing-agent -- npx -y @lydissing/writing-agent
```

Or install globally:

```bash
claude mcp add --global writing-agent -- npx -y @lydissing/writing-agent
```

Then invoke it with:

```
/letter
```

## Requirements

- [Claude Code](https://claude.ai/code) (CLI, desktop app, or IDE extension)
- For clipboard support on Linux: `wl-copy` (Wayland) or `xclip` / `xsel` (X11)
  ```bash
  # Wayland
  sudo apt-get install wl-clipboard
  # X11
  sudo apt-get install xclip
  ```

## Usage

Run `/letter` and answer the questions. The skill handles the rest. At the end you get:

- The final email copied to your clipboard (or displayed for manual copy if clipboard tools are unavailable)
- A clickable `[Åbn i mailprogram](mailto:?subject=...&body=...)` link to open directly in your mail client

## Supported languages

Any language Claude supports. Confidence is surfaced before translation — if confidence is medium or low, you can choose to proceed, switch language, or flag for a native reviewer.

## Contributing

The code is open. Issues and pull requests welcome at <https://github.com/LydByDissing/writing-agent>.

## License

Apache 2.0 — see [LICENSE](LICENSE).
