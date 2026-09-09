# Reader, figures and editorial drafts

The canonical evidence is [../evidence.json](../evidence.json). [The reader manifest](manifest.json) lists the reviewed files and draft status. These reader assets are a reviewed public derivative. The articles remain drafts for review; repository publication does not mean a final article, website deployment or social post.

- [Blog draft](blog.md) and [illustrated HTML](blog.html).
- [Study draft](study.md) and [illustrated HTML](study.html).
- [Twitter article draft](twitter-article.md).
- [LinkedIn draft](linkedin.txt): **2,787 characters** including spaces, links and trailing newline, below Brad's 4,000-character ceiling. The text file itself contains the proposed post only; this README records its draft status.
- [Interactive explorer](explorer.html) and [derived JSON](explorer-data.json).
- Four [figure pairs and captions](figure-captions.md), in SVG and PNG.

## Local preview

From this directory:

```sh
python3 -m http.server 8766 --bind 127.0.0.1
```

Open the server address in your browser and select `explorer.html`, `blog.html` or `study.html`. GitHub displays the source rather than running the HTML. Local HTTP is required for module loading; all runtime files are local, with no CDN or upload endpoint. Hosting is not configured or enabled by these files.

Use day/project filters for usage and coded observations. Repository metrics always cover the full window, with only the project filter applied. The matrix has exact keyboard-selectable cells, fixed linear color/height scales, and an optional spatial view. Rotation/elevation respond only to input; there is no autonomous animation. The flat matrix remains usable without WebGL. Zero coded contributions yields no rate; an unresolved repository is missing, not zero.

## Reproduction and licensing

Run `tools/build_evidence_reader.py` from the repository root to reproduce the JSON from the validated canonical evidence. See the [case README](../README.md) for exact commands. Static figures are exports from the same aggregate counts; counts, scales and captions are independently inspectable. Matplotlib 3.11.1 was used for authoring figures, not as a site runtime or kit dependency.

The viewer retains the previously reviewed Three.js 0.186.0/r186 modules under [their MIT license](vendor/LICENSE). [The release record](vendor/release.json) records the public upstream tarball and its integrity value; it is not private audit provenance. Original reader code, draft text and contributed data use the repository's MIT license. Linked third-party articles retain their own terms.

No source transcripts, private locators, source hashes, aliases-to-project mappings, machine paths, or original task/session identities are included.
