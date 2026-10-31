---
description: Images, figures with captions, zoom, and images for light and dark mode.
---

# Images

Images use standard Markdown. Paths are relative to the page, so the image works in your editor, on GitHub and on the site.

```markdown
![The Sumi mark](../../assets/sumi-mark.svg)
```

## Figures

Add `{caption="…"}` on the line after an image to turn it into a figure:

```markdown
![The Sumi mark](../../assets/sumi-mark.svg)
{caption="The Sumi mark: an ink stroke and a vermilion seal."}
```

![The Sumi mark](../../assets/sumi-mark.svg)
{caption="The Sumi mark: an ink stroke and a vermilion seal."}

## Zoom

Click an image in the content to view it full-screen; press <kbd>Esc</kbd> or click again to close. Images inside links and cards are not zoomable. To opt an image out, give it the `no-zoom` class:

```markdown
![Diagram](flow.png){.no-zoom}
```

## Light and dark variants

Append `#only-light` or `#only-dark` to an image URL to show it in one colour scheme only:

```markdown
![Architecture](arch-light.png#only-light)
![Architecture](arch-dark.png#only-dark)
```

## Size and placement

With `attr_list`, set the width or float an image:

```markdown
![Logo](logo.png){width="120"}
![Screenshot](shot.png){.left width="320"}
```

> [!NOTE]
> Images are lazy-loaded. Give large images explicit `width` and `height` attributes to avoid layout shift.
