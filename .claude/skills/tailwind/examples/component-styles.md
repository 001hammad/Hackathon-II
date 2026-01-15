# Component Styles

Complete styling patterns for common UI components.

## Button Styles

```tsx
// Primary
<button className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors">
  Primary
</button>

// Secondary
<button className="inline-flex items-center justify-center rounded-md bg-secondary px-4 py-2 text-sm font-medium text-secondary-foreground hover:bg-secondary/80">
  Secondary
</button>

// Outline
<button className="inline-flex items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground">
  Outline
</button>

// Ghost
<button className="inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground">
  Ghost
</button>

// Destructive
<button className="inline-flex items-center justify-center rounded-md bg-destructive px-4 py-2 text-sm font-medium text-destructive-foreground hover:bg-destructive/90">
  Delete
</button>
```

## Card Styles

```tsx
<div className="rounded-lg border bg-card text-card-foreground shadow-sm">
  <div className="p-6 space-y-2">
    <h3 className="font-semibold text-lg">Card Title</h3>
    <p className="text-sm text-muted-foreground">Card description</p>
  </div>
  <div className="border-t p-6">
    Card footer
  </div>
</div>
```

## Input Styles

```tsx
<input
  type="text"
  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
  placeholder="Enter text"
/>
```

## Badge Styles

```tsx
<span className="inline-flex items-center rounded-full bg-primary px-2.5 py-0.5 text-xs font-semibold text-primary-foreground">
  Badge
</span>

<span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold">
  Outline Badge
</span>
```

## Alert Styles

```tsx
<div className="rounded-lg border bg-background p-4">
  <div className="flex gap-3">
    <AlertCircle className="h-4 w-4 text-muted-foreground" />
    <div className="space-y-1">
      <h5 className="font-medium">Alert Title</h5>
      <p className="text-sm text-muted-foreground">Alert description</p>
    </div>
  </div>
</div>
```

## Avatar Styles

```tsx
<div className="relative h-10 w-10 overflow-hidden rounded-full">
  <img src="..." alt="..." className="aspect-square h-full w-full" />
</div>

<div className="flex h-10 w-10 items-center justify-center rounded-full bg-muted">
  <span className="text-sm font-medium">JD</span>
</div>
```

## Skeleton Loaders

```tsx
<div className="space-y-2">
  <div className="h-4 w-full bg-muted animate-pulse rounded" />
  <div className="h-4 w-3/4 bg-muted animate-pulse rounded" />
  <div className="h-4 w-1/2 bg-muted animate-pulse rounded" />
</div>
```
