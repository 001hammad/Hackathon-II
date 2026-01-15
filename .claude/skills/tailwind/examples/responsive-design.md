# Responsive Design Patterns

Mobile-first responsive design patterns using Tailwind CSS breakpoints.

## Breakpoints

| Breakpoint | Min Width | Device |
|------------|-----------|--------|
| `sm:` | 640px | Phones (landscape) |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Laptops |
| `xl:` | 1280px | Desktops |
| `2xl:` | 1536px | Large desktops |

## Responsive Grid

```tsx
// 1 column mobile → 2 tablet → 3 laptop → 4 desktop
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  {items.map(item => <div key={item.id}>Card</div>)}
</div>
```

## Responsive Flex

```tsx
// Stack on mobile, row on desktop
<div className="flex flex-col md:flex-row gap-4">
  <div>Left</div>
  <div>Right</div>
</div>
```

## Responsive Typography

```tsx
<h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold">
  Scales with screen
</h1>
```

## Show/Hide

```tsx
<div className="hidden md:block">Desktop only</div>
<div className="block md:hidden">Mobile only</div>
```

## Best Practices

1. Start with mobile styles (no prefix)
2. Add larger breakpoints as needed
3. Test at 375px, 768px, 1024px, 1280px
4. Use min 44x44px touch targets on mobile
