# Layout Patterns

Complete layout patterns using Tailwind CSS for modern web applications.

## Flexbox Layouts

### Horizontal Stack with Gap
```tsx
<div className="flex items-center gap-4">
  <span>Item 1</span>
  <span>Item 2</span>
  <span>Item 3</span>
</div>
```

### Space Between
```tsx
<div className="flex items-center justify-between">
  <span>Left</span>
  <span>Right</span>
</div>
```

### Centered Content
```tsx
<div className="flex items-center justify-center min-h-screen">
  <div>Centered content</div>
</div>
```

### Vertical Stack
```tsx
<div className="flex flex-col gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

## Grid Layouts

### Responsive Grid
```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  {items.map(item => (
    <div key={item.id} className="rounded-lg border p-4">
      {item.content}
    </div>
  ))}
</div>
```

### Auto-fit Grid
```tsx
<div className="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">
  <div>Card 1</div>
  <div>Card 2</div>
  <div>Card 3</div>
</div>
```

### Grid with Sidebar
```tsx
<div className="grid grid-cols-1 lg:grid-cols-[250px_1fr] gap-6">
  <aside className="border-r">Sidebar</aside>
  <main>Main content</main>
</div>
```

## Container Patterns

### Centered Container
```tsx
<div className="container mx-auto px-4 md:px-6 lg:px-8 max-w-7xl">
  Content with max width
</div>
```

### Full Width with Padding
```tsx
<div className="w-full px-4 md:px-6">
  Full width responsive padding
</div>
```

## Dashboard Layout
```tsx
<div className="min-h-screen flex flex-col">
  {/* Header */}
  <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur">
    <div className="container flex h-14 items-center">
      <nav className="flex items-center gap-6">
        <span className="font-bold">Logo</span>
        <a href="/">Home</a>
        <a href="/tasks">Tasks</a>
      </nav>
    </div>
  </header>

  {/* Main */}
  <div className="flex-1 flex">
    {/* Sidebar */}
    <aside className="hidden lg:block w-64 border-r">
      <nav className="p-4 space-y-2">
        <a className="block px-3 py-2 rounded-md hover:bg-accent">Dashboard</a>
        <a className="block px-3 py-2 rounded-md hover:bg-accent">Tasks</a>
        <a className="block px-3 py-2 rounded-md hover:bg-accent">Settings</a>
      </nav>
    </aside>

    {/* Content */}
    <main className="flex-1 p-6">
      <div className="max-w-5xl mx-auto">
        Content goes here
      </div>
    </main>
  </div>
</div>
```

## Card Grid
```tsx
<div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
  {tasks.map(task => (
    <div key={task.id} className="rounded-lg border bg-card p-6">
      <h3 className="font-semibold mb-2">{task.title}</h3>
      <p className="text-sm text-muted-foreground">{task.description}</p>
    </div>
  ))}
</div>
```

## Split View
```tsx
<div className="flex flex-col md:flex-row gap-6 min-h-[600px]">
  <div className="flex-1 border rounded-lg p-6">
    Left panel
  </div>
  <div className="flex-1 border rounded-lg p-6">
    Right panel
  </div>
</div>
```
