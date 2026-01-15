# Spacing Scale Reference

Tailwind's spacing scale for padding, margin, gap, and more.

## Spacing Values

| Class | Value | Pixels |
|-------|-------|--------|
| `0` | 0 | 0px |
| `px` | 1px | 1px |
| `0.5` | 0.125rem | 2px |
| `1` | 0.25rem | 4px |
| `1.5` | 0.375rem | 6px |
| `2` | 0.5rem | 8px |
| `2.5` | 0.625rem | 10px |
| `3` | 0.75rem | 12px |
| `3.5` | 0.875rem | 14px |
| `4` | 1rem | 16px |
| `5` | 1.25rem | 20px |
| `6` | 1.5rem | 24px |
| `7` | 1.75rem | 28px |
| `8` | 2rem | 32px |
| `9` | 2.25rem | 36px |
| `10` | 2.5rem | 40px |
| `11` | 2.75rem | 44px |
| `12` | 3rem | 48px |
| `14` | 3.5rem | 56px |
| `16` | 4rem | 64px |
| `20` | 5rem | 80px |
| `24` | 6rem | 96px |
| `28` | 7rem | 112px |
| `32` | 8rem | 128px |

## Common Usage

### Padding
```tsx
<div className="p-4">Padding all sides: 16px</div>
<div className="px-6 py-4">Horizontal: 24px, Vertical: 16px</div>
<div className="pt-8 pb-4">Top: 32px, Bottom: 16px</div>
```

### Margin
```tsx
<div className="m-4">Margin all sides: 16px</div>
<div className="mx-auto">Center horizontally</div>
<div className="mt-6 mb-4">Top: 24px, Bottom: 16px</div>
```

### Gap
```tsx
<div className="flex gap-4">Gap between items: 16px</div>
<div className="grid gap-6">Gap: 24px</div>
<div className="flex gap-x-4 gap-y-6">X: 16px, Y: 24px</div>
```

### Space Between
```tsx
<div className="space-y-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

## Responsive Spacing
```tsx
<div className="p-4 md:p-6 lg:p-8">
  Responsive padding
</div>
```
