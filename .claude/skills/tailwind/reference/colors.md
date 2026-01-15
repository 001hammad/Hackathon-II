# Colors Reference

Tailwind color system and semantic colors.

## Semantic Colors

Use these for automatic dark mode support:

```tsx
bg-background       // Main background
bg-foreground       // Main text color
bg-card             // Card background
bg-card-foreground  // Card text
bg-primary          // Primary action color
bg-primary-foreground  // Primary text
bg-secondary        // Secondary color
bg-muted            // Muted background
bg-muted-foreground // Muted text
bg-accent           // Accent color
bg-destructive      // Destructive/error color
bg-border           // Border color
bg-input            // Input field background
```

## Text Colors

```tsx
text-foreground         // Main text
text-muted-foreground   // Subtle text
text-primary            // Primary color text
text-destructive        // Error text
```

## Border Colors

```tsx
border-border     // Standard border
border-input      // Input border
```

## Opacity Modifiers

```tsx
bg-primary/90     // 90% opacity
bg-primary/80     // 80% opacity
bg-primary/50     // 50% opacity
bg-primary/20     // 20% opacity
```

## Hover States

```tsx
hover:bg-primary/90
hover:bg-accent
hover:text-accent-foreground
```

## Complete Color Example

```tsx
<div className="bg-background text-foreground">
  <div className="bg-card border-border p-4 rounded-lg">
    <h3 className="text-card-foreground">Title</h3>
    <p className="text-muted-foreground">Description</p>
    <button className="bg-primary text-primary-foreground hover:bg-primary/90">
      Action
    </button>
  </div>
</div>
```
