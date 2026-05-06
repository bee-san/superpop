# superpop

the absurdly juiced japanese ocr popup dictionary with SuperMemo mining sauce.

superpop is a fork of meikipop that looks at your screen, finds japanese text with ocr, pops a dictionary result under your cursor, and now lets you slam the current lookup straight into a SuperMemo Q&A import file. it is desktop yomichan energy, visual novel hover sorcery, manga panel extraction, subtitle sniping, and spaced-repetition grindset plumbing in one extremely unserious trench coat.

https://github.com/user-attachments/assets/a1834197-3059-438c-a2dc-716e8ec9078f

## why this exists

because browser-only popup dictionaries are not enough. because games do not politely expose text. because manga images refuse to become selectable. because hard-coded subtitles are smug. because sometimes you hover a word, understand it for 0.8 seconds, and then your brain throws it into the ocean.

superpop does the funny pipeline:

1. look at screen
2. ocr the japanese
3. dictionary go pop
4. click tray action
5. SuperMemo Q&A card appears in a UTF-8 text file
6. import that file into SuperMemo and pretend this was a disciplined study workflow all along

## feature smoothie

* **screen-wide japanese lookup:** websites, games, comics, videos, scans, cursed launchers, whatever. if pixels exist, superpop starts negotiating with them.
* **local and remote ocr backends:** meikiocr, Google Lens, Chrome Screen AI, owocr, and custom providers if you want to bolt on your own machine-vision contraption.
* **fast popup dictionary:** preprocessed dictionary data, deconjugation, frequency sorting, kanji side data, compact display, configurable colors, and that lovely little hover-card dopamine.
* **SuperMemo Q&A export:** tray action appends the current lookup as `Q:` / `A:` text, with HTML line breaks and UTF-8 japanese intact.
* **clipboard mining:** optionally copies the newest generated SuperMemo card so SuperMemo.com paste-import gobbles it immediately.
* **region or full screen scanning:** scan exactly the window or region you care about instead of feeding the entire desktop into the pixel furnace.
* **auto scan mode:** hover and receive knowledge pellets without repeatedly mashing the hotkey.
* **settings panel:** themes, fonts, popup behavior, ocr backend selection, kanji detail toggles, and SuperMemo export path controls.
* **pyproject installable:** run it as `superpop`, keep the old `meikipop` command around for compatibility, enjoy the fork name without losing muscle memory.

## SuperMemo support

superpop exports the current popup lookup to SuperMemo's simple Q&A text format:

```text
Q: 日本語 [にほんご]
A: <b>日本語</b> [にほんご]<br>1. Japanese language<br><small>mined by superpop for SuperMemo Q&A import</small>
```

the export file defaults to your platform data directory as `supermemo_qa.txt`:

* windows: `%LOCALAPPDATA%\superpop\supermemo_qa.txt`
* linux: `~/.local/share/superpop/supermemo_qa.txt`
* macos: `~/Library/Application Support/superpop/supermemo_qa.txt`

how to mine:

1. run `superpop`
2. hover japanese text until the popup has the entry you want
3. right-click the tray icon
4. click **Add last lookup to SuperMemo**
5. import the resulting `supermemo_qa.txt` through SuperMemo's Q&A text import, or paste the copied card into SuperMemo.com import with separators configured for your course

the settings dialog includes:

* **Q&A Export Path:** choose the text file superpop appends to
* **Copy Card to Clipboard:** copy the newest generated card after export

SuperMemo for Windows supports importing Q&A text files with `Q:` and `A:` prefixes, UTF-8 text, and HTML tags inside question or answer content. SuperMemo.com can also import pasted question-answer material through its editor import flow when you choose the right separators. that means superpop does not need a brittle local automation bridge. it produces the boring format SuperMemo already eats.

## install

### from source, because you are already here

```bash
git clone https://github.com/bee-san/superpop.git
cd superpop
pip install -e .
superpop
```

### compatibility command

```bash
meikipop
```

yes, the old command still exists. no, the branding committee was not consulted.

### dictionary setup

on first run, superpop downloads the upstream meikipop dictionary asset if you do not already have one. you can also build it yourself:

```bash
superpop build-dict
```

## how to use

1. run `superpop`
2. select a scan region if prompted
3. hover japanese text
4. read the popup
5. mine the good stuff with **Add last lookup to SuperMemo**
6. keep reading before the setup impulse convinces you to reorganize your deck tags for three hours

## configuration

right-click the tray icon and open **Settings**.

the interesting knobs:

* **OCR Provider:** swap between local speed, remote accuracy, and whatever custom backend you wired in at 2 a.m.
* **Max Lookup Length:** cap the text chunk sent into dictionary lookup
* **Auto Scan Mode:** continuously ocr the region so hover latency feels less like soup
* **Popup Content:** choose glosses, deconjugation, part of speech, frequency, kanji entries, examples, and components
* **Popup Appearance:** tune the study rectangle until it stops offending your eyes
* **SuperMemo:** set the Q&A file and clipboard behavior

config and data live under `superpop`, not `meikipop`, because this fork put on sunglasses and legally became a new thing.

## ocr backend buffet

* **meikiocr:** default local backend. fast, private, great for horizontal game text.
* **Google Lens:** remote, higher accuracy, internet required, latency tax included.
* **Chrome Screen AI:** local alternative if you have the setup in place.
* **owocr:** bridge to owocr's backend buffet.
* **custom provider:** copy the dummy provider and make your own weird ocr engine speak superpop's paragraph/word format.

owocr example:

```bash
pip install -U "owocr>=1.15"
owocr -r websocket -w websocket -of json -e glens
```

then pick the owocr provider from the tray menu.

custom provider docs still live at [docs/CUSTOM_OCR_PROVIDER.md](docs/CUSTOM_OCR_PROVIDER.md). it says meikipop in places because this fork is moving fast and the documentation intern is a hallucinated spreadsheet.

## import yomitan dictionaries

```bash
superpop import-yomitan-dict-html my_yomitan_dict.zip
superpop import-yomitan-dict-text my_yomitan_dict.zip
superpop import-yomitan-dict-text dict1.zip dict2.zip
```

html mode tries to keep formatting. text mode strips it down into lean little definition bricks.

## platform vibes

* **windows:** mainline happy path
* **linux x11:** also mainline
* **macos:** supported via community work and permission prompts
* **linux wayland:** technically possible, emotionally seasonal

macos needs screen recording, accessibility, and input monitoring permissions for the terminal or bundled app.

wayland tips:

* try the flatpak first
* make sure xwayland works
* install missing distro bits if screenshots or popups vanish
* test on a windowed xwayland app
* consider x11 when reality becomes expensive

## development

```bash
pip install -e .
python -m compileall src
```

the package is still `meikipop` internally so the fork stays small and the import graph does not get launched into the sun. the distribution and user-facing command are `superpop`.

## slop manifesto

superpop is not a lifestyle brand, except when it is. it is not a productivity methodology, except when a tray click becomes a flashcard and you feel like a cyber-scholar. it will not learn japanese for you, but it will reduce the gap between "what is that word" and "this word has been sentenced to SuperMemo prison" to a very satisfying click.

read pixels. pop definitions. mine cards. repeat until the dictionary starts looking less like a wall and more like a buffet.

## license

GPL-3.0. see [LICENSE](LICENSE). upstream meikipop by rtr46 did the hard foundation work; superpop adds the flashy fork branding and SuperMemo export plumbing.
