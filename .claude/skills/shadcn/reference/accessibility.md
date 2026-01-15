# Accessibility Reference

Accessibility guidelines, best practices, and testing strategies for shadcn/ui components.

## WCAG Compliance

All shadcn/ui components are built to meet WCAG 2.1 Level AA standards.

### Core Accessibility Features

✅ **Keyboard Navigation** - All interactive elements accessible via keyboard
✅ **Focus Management** - Proper focus indicators and tab order
✅ **Screen Reader Support** - ARIA labels and semantic HTML
✅ **Color Contrast** - Meets WCAG AA minimum contrast ratios
✅ **Reduced Motion** - Respects `prefers-reduced-motion`

## Keyboard Navigation

###Essential Keyboard Shortcuts

| Action | Key |
|--------|-----|
| Navigate forward | `Tab` |
| Navigate backward | `Shift + Tab` |
| Activate button/link | `Enter` or `Space` |
| Close dialog/modal | `Escape` |
| Open dropdown | `Enter` or `Space` |
| Navigate dropdown items | `Arrow Up/Down` |
| Select dropdown item | `Enter` |

### Custom Keyboard Handlers

```tsx
function KeyboardAccessibleComponent() {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      handleClick()
    }
  }

  return (
    <div
      role="button"
      tabIndex={0}
      onKeyDown={handleKeyDown}
      onClick={handleClick}
    >
      Accessible Element
    </div>
  )
}
```

## ARIA Attributes

### Common ARIA Patterns

```tsx
// Button with icon only
<Button aria-label="Delete task">
  <Trash2 className="h-4 w-4" />
</Button>

// Loading state
<Button disabled aria-busy="true">
  <Loader2 className="animate-spin mr-2" />
  Loading...
</Button>

// Expanded/collapsed state
<Button
  aria-expanded={isOpen}
  aria-controls="menu-id"
>
  Menu
</Button>

// Dialog
<Dialog>
  <DialogContent role="dialog" aria-labelledby="dialog-title" aria-describedby="dialog-description">
    <DialogTitle id="dialog-title">Confirm Delete</DialogTitle>
    <DialogDescription id="dialog-description">
      This action cannot be undone.
    </DialogDescription>
  </DialogContent>
</Dialog>
```

## Semantic HTML

Always use proper HTML elements:

```tsx
// ✅ Good - Semantic HTML
<button onClick={handleClick}>Click me</button>
<a href="/tasks">View Tasks</a>
<nav>...</nav>
<main>...</main>
<article>...</article>

// ❌ Bad - Non-semantic
<div onClick={handleClick}>Click me</div>
<div className="link">View Tasks</div>
```

## Form Accessibility

### Labels and Descriptions

```tsx
<FormField
  control={form.control}
  name="title"
  render={({ field }) => (
    <FormItem>
      <FormLabel htmlFor="title">Task Title</FormLabel>
      <FormControl>
        <Input
          id="title"
          aria-describedby="title-description"
          {...field}
        />
      </FormControl>
      <FormDescription id="title-description">
        Enter a descriptive title for your task
      </FormDescription>
      <FormMessage aria-live="polite" />
    </FormItem>
  )}
/>
```

### Error Messages

```tsx
// Error messages should be announced
<FormMessage
  role="alert"
  aria-live="assertive"
>
  {error.message}
</FormMessage>
```

## Focus Management

### Focus Visible Styles

```tsx
// All interactive elements should have focus styles
<Button className="focus:ring-2 focus:ring-ring focus:ring-offset-2">
  Click me
</Button>
```

### Focus Trapping in Modals

shadcn/ui Dialog components automatically trap focus:

```tsx
<Dialog>
  <DialogContent>
    {/* Focus is trapped inside this dialog */}
    <Input /> {/* First focusable element */}
    <Button>Close</Button> {/* Last focusable element */}
  </DialogContent>
</Dialog>
```

## Color Contrast

### WCAG AA Requirements

- **Normal text**: 4.5:1 minimum
- **Large text** (18px+ or 14px+ bold): 3:1 minimum
- **UI components**: 3:1 minimum

### Testing Contrast

```tsx
// Use browser DevTools or tools like:
// - WebAIM Contrast Checker
// - Stark plugin for Figma
// - axe DevTools browser extension
```

## Screen Reader Support

### Live Regions

```tsx
// Announce dynamic updates
<div role="status" aria-live="polite">
  {successMessage}
</div>

<div role="alert" aria-live="assertive">
  {errorMessage}
</div>
```

### Visually Hidden Text

```tsx
// Text for screen readers only
<span className="sr-only">Loading tasks</span>
<Loader2 className="animate-spin" aria-hidden="true" />
```

## Reduced Motion

Respect user preferences:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Testing Checklist

### Manual Testing

- [ ] Navigate entire UI with keyboard only
- [ ] Test with screen reader (NVDA, JAWS, VoiceOver)
- [ ] Check focus indicators are visible
- [ ] Verify all images have alt text
- [ ] Test color contrast with tools
- [ ] Try with browser zoom at 200%
- [ ] Test with reduced motion enabled

### Automated Testing

```bash
# Install axe-core for automated testing
npm install -D @axe-core/react

# Use in tests
import { axe } from 'jest-axe'

test('should have no accessibility violations', async () => {
  const { container } = render(<Component />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

## Common Mistakes to Avoid

❌ **Don't use `div` for buttons**
```tsx
<div onClick={handleClick}>Click</div> // Bad
<button onClick={handleClick}>Click</button> // Good
```

❌ **Don't forget alt text**
```tsx
<img src="..." /> // Bad
<img src="..." alt="Task icon" /> // Good
```

❌ **Don't skip keyboard navigation**
```tsx
<div onClick={handleClick}>Click</div> // Not keyboard accessible
<button onClick={handleClick}>Click</button> // Keyboard accessible
```

❌ **Don't use color alone for information**
```tsx
// Bad - color only
<span className="text-red-500">Error</span>

// Good - color + icon + text
<span className="text-destructive">
  <AlertCircle className="inline h-4 w-4 mr-1" />
  Error
</span>
```

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Resources](https://webaim.org/resources/)
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [WAVE Tool](https://wave.webaim.org/)
