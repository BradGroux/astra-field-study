# Reader, figures and editorial drafts

The canonical evidence is [../evidence.json](../evidence.json). [The reader manifest](manifest.json) lists the reviewed files and draft status. These reader assets are a reviewed public derivative. The articles remain drafts for review; repository publication does not mean a final article, website deployment or social post.

- [Blog draft](blog.md) and [illustrated HTML](blog.html).
- [Study draft](study.md) and [illustrated HTML](study.html).
- [Twitter article draft](twitter-article.md).
- [LinkedIn draft](linkedin.txt): The [manifest](manifest.json) and [social preview](social.html) show the exact count, including spaces, links and trailing newline. The build enforces Brad's 4,000-character ceiling. The text file itself contains the proposed post only; this README records its draft status.
- [Interactive explorer](explorer.html) and [derived JSON](explorer-data.json).
- Six [figures and captions](figure-captions.md), in SVG and PNG.

## Local preview

From the repository root:

```sh
python3 tools/preview_reader.py
```

Open [the blog](http://127.0.0.1:8766/reader/blog.html), [the study](http://127.0.0.1:8766/reader/study.html), [social drafts](http://127.0.0.1:8766/reader/social.html), or [the explorer](http://127.0.0.1:8766/reader/explorer.html). The server includes the public evidence package so source-data and method links also work. Legacy flat article URLs redirect to the current reader paths. GitHub displays the source rather than running the HTML. Local HTTP is required for module loading; all runtime files are local, with no CDN or upload endpoint. Hosting is not configured or enabled by these files.

Use day/project filters for usage and coded observations. Repository metrics always cover the full window, with only the project filter applied. The matrix has exact keyboard-selectable cells and a fixed linear color scale. The optional 3D profile shows one project across six days with a fixed height scale, explicit project selection, and exact-value buttons. Rotation/elevation respond only to input. The flat matrix remains usable without WebGL. Zero coded contributions yields no rate; an unresolved repository is missing, not zero.

## Reproduction and licensing

Run `tools/build_evidence_reader.py` from the repository root to reproduce the JSON from the validated canonical evidence. See the [case README](../README.md) for exact commands. The article HTML and six responsive SVG figures now have reproducible standard-library builders. The figure styles include daily columns, a contribution waffle, input composition, a matrix, episode outcomes, and repository dot plots. See [the rendering guide](../../../docs/reader-design.md) for source contracts and optional PNG exports. Run from the repository root:

```sh
python3 tools/build_figures.py
python3 tools/build_articles.py
```

Markdown is the prose source; generated HTML should not be edited separately. `build_articles.py` also refreshes the social preview, captions and manifest. The reader embeds the locally served Roboto font, licensed under the [SIL Open Font License](vendor/Roboto-OFL.txt).

The viewer retains the previously reviewed Three.js 0.186.0/r186 modules under [their MIT license](vendor/LICENSE). [The release record](vendor/release.json) records the public upstream tarball and its integrity value; it is not private audit provenance. Original reader code, draft text and contributed data use the repository's MIT license. Linked third-party articles retain their own terms.

No source transcripts, private locators, source hashes, aliases-to-project mappings, machine paths, or original task/session identities are included.
