# Typography Reference

Complete typography system using Tailwind CSS.

## Font Sizes

| Class | Size | Line Height |
|-------|------|-------------|
| `text-xs` | 0.75rem (12px) | 1rem (16px) |
| `text-sm` | 0.875rem (14px) | 1.25rem (20px) |
| `text-base` | 1rem (16px) | 1.5rem (24px) |
| `text-lg` | 1.125rem (18px) | 1.75rem (28px) |
| `text-xl` | 1.25rem (20px) | 1.75rem (28px) |
| `text-2xl` | 1.5rem (24px) | 2rem (32px) |
| `text-3xl` | 1.875rem (30px) | 2.25rem (36px) |
| `text-4xl` | 2.25rem (36px) | 2.5rem (40px) |
| `text-5xl` | 3rem (48px) | 1 |
| `text-6xl` | 3.75rem (60px) | 1 |

## Font Weights

```tsx
font-thin        // 100
font-extralight  // 200
font-light       // 300
font-normal      // 400
font-medium      // 500
font-semibold    // 600
font-bold        // 700
font-extrabold   // 800
font-black       // 900
```

## Heading Styles

```tsx
<h1 className="text-3xl md:text-4xl lg:text-5xl font-bold tracking-tight">
  Page Title
</h1>

<h2 className="text-2xl md:text-3xl font-semibold">
  Section Title
</h2>

<h3 className="text-xl md:text-2xl font-semibold">
  Subsection
</h3>

<h4 className="text-lg font-medium">
  Card Title
</h4>
```

## Body Text

```tsx
<p className="text-base leading-relaxed">
  Normal paragraph text
</p>

<p className="text-sm text-muted-foreground">
  Smaller descriptive text
</p>

<p className="text-xs text-muted-foreground">
  Very small text like captions
</p>
```

## Text Utilities

```tsx
// Alignment
text-left text-center text-right text-justify

// Transform
uppercase lowercase capitalize normal-case

// Decoration
underline line-through no-underline

// Truncate
truncate            // Single line with ellipsis
line-clamp-2        // 2 lines with ellipsis
line-clamp-3        // 3 lines with ellipsis

// Line Height
leading-none leading-tight leading-normal leading-relaxed leading-loose

// Tracking (letter spacing)
tracking-tighter tracking-tight tracking-normal tracking-wide tracking-wider

// Whitespace
whitespace-normal whitespace-nowrap whitespace-pre whitespace-pre-wrap
```

## Typography Examples

```tsx
// Article title
<h1 className="text-4xl font-bold tracking-tight mb-4">
  Article Title
</h1>

// Description
<p className="text-lg text-muted-foreground mb-8 leading-relaxed">
  Article description with good readability
</p>

// Card title with truncation
<h3 className="font-semibold text-lg truncate">
  Long task title that will be cut off
</h3>

// Small meta text
<span className="text-xs text-muted-foreground uppercase tracking-wide">
  Category
</span>
```
