# Typography Usage Guide

## Quick Reference

Use this guide when adding new components or updating existing styles.

## Standard Font Sizes

### Headers

```css
/* H1 - Main Page Titles */
h1 {
  font-size: 2rem;        /* 32px */
  font-weight: 700;
}

/* H2 - Section Headings */
h2 {
  font-size: 1.5rem;      /* 24px */
  font-weight: 600;
}

/* H3 - Subsection Headings */
h3 {
  font-size: 1.125rem;    /* 18px */
  font-weight: 600;
}

/* H4 - Minor Headings */
h4 {
  font-size: 1rem;        /* 16px */
  font-weight: 600;
}
```

### Body Text

```css
/* Standard Body Text */
p, body {
  font-size: 1rem;        /* 16px */
  line-height: 1.6;
}

/* Large Body Text */
.large-text {
  font-size: 1.125rem;    /* 18px */
}

/* Small Text */
.small-text {
  font-size: 0.875rem;    /* 14px */
}

/* Caption / Metadata */
.caption {
  font-size: 0.75rem;     /* 12px - minimum */
}
```

### UI Elements

```css
/* Buttons */
button, .btn {
  font-size: 0.875rem;    /* 14px */
  font-weight: 600;
}

/* Large Buttons */
.btn-large {
  font-size: 1rem;        /* 16px */
}

/* Inputs */
input, select, textarea {
  font-size: 0.875rem;    /* 14px */
}

/* Navigation Links */
.nav-link {
  font-size: 0.875rem;    /* 14px */
  font-weight: 500;
}
```

### Special Cases

```css
/* Hero Titles */
.hero-title {
  font-size: 3rem;        /* 48px */
  font-weight: 800;
}

/* Display Numbers */
.stat-number {
  font-size: 2.25rem;     /* 36px */
  font-weight: 700;
}

/* Badges */
.badge {
  font-size: 0.75rem;     /* 12px */
  font-weight: 700;
}

/* Code */
code {
  font-size: 0.875rem;    /* 14px */
  font-family: 'Consolas', monospace;
}
```

## Responsive Typography

### Tablet (768px and below)

```css
@media (max-width: 768px) {
  h1 { font-size: 1.75rem; }    /* 28px */
  h2 { font-size: 1.375rem; }   /* 22px */
  .hero-title { font-size: 2rem; } /* 32px */
}
```

### Mobile (480px and below)

```css
@media (max-width: 480px) {
  h1 { font-size: 1.5rem; }     /* 24px */
  h2 { font-size: 1.25rem; }    /* 20px */
  .hero-title { font-size: 1.75rem; } /* 28px */
}
```

## Font Family

```css
/* All elements use Open Sans */
* {
  font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, 
               'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 
               'Cantarell', 'Fira Sans', 'Droid Sans', 
               'Helvetica Neue', sans-serif;
}

/* Code/Monospace */
code, pre {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}
```

## Best Practices

### DO ✅

- Use rem units for font sizes
- Follow the established hierarchy (H1 > H2 > H3 > H4)
- Keep body text at 16px minimum on desktop
- Use 12px as absolute minimum (captions only)
- Apply proper line-height (1.4-1.7 for readability)
- Use consistent font weights (400, 500, 600, 700)

### DON'T ❌

- Don't use px units for font sizes
- Don't go below 12px for any text
- Don't skip heading levels (H1 → H3)
- Don't use too many different font sizes
- Don't use inconsistent line-heights
- Don't hardcode font-family in multiple places

## Component Examples

### Card Component

```css
.card {
  /* Card title */
  .card-title {
    font-size: 1.125rem;  /* 18px - H3 */
    font-weight: 600;
  }
  
  /* Card description */
  .card-description {
    font-size: 0.875rem;  /* 14px - Small text */
    color: #888;
  }
  
  /* Card metadata */
  .card-meta {
    font-size: 0.75rem;   /* 12px - Caption */
    color: #666;
  }
}
```

### Button Variants

```css
/* Primary Button */
.btn-primary {
  font-size: 0.875rem;    /* 14px */
  font-weight: 600;
  padding: 12px 24px;
}

/* Large Button */
.btn-large {
  font-size: 1rem;        /* 16px */
  font-weight: 600;
  padding: 16px 32px;
}

/* Small Button */
.btn-small {
  font-size: 0.75rem;     /* 12px */
  font-weight: 600;
  padding: 8px 16px;
}
```

### Form Elements

```css
/* Label */
label {
  font-size: 0.875rem;    /* 14px */
  font-weight: 600;
  color: #fff;
}

/* Input */
input, select {
  font-size: 0.875rem;    /* 14px */
  padding: 12px 15px;
}

/* Help Text */
.help-text {
  font-size: 0.75rem;     /* 12px */
  color: #888;
}
```

## Accessibility Notes

- **Minimum readable size**: 16px for body text
- **Contrast ratio**: Ensure at least 4.5:1 for normal text
- **Line height**: 1.5-1.7 for optimal readability
- **Letter spacing**: Use default or slight increase for headers
- **Text scaling**: Respect user's browser font size settings (use rem)

## Migration Checklist

When updating a component:

- [ ] Replace all `font-size: Xpx` with `font-size: Xrem`
- [ ] Check against typography guide for appropriate size
- [ ] Ensure font-family inheritance is correct
- [ ] Test on mobile and tablet breakpoints
- [ ] Verify readability and contrast
- [ ] Check that headings follow proper hierarchy

---

**Remember**: Consistency is key! Always refer to this guide when styling text elements.
