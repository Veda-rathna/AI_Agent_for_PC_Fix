# Conversation History - User Interface Guide

## 🎨 Visual Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  AutoMend AI - PC Diagnostic Tool                                   │
├──────────────┬──────────────────────────────────────────────────────┤
│              │                                                       │
│  [◀]         │         Welcome Screen                                │
│              │         AutoMend AI Diagnostic                        │
│  Chat        │         Describe your PC issue...                     │
│  History     │                                                       │
│              │         [My computer is running slow]                 │
│  [✚] New     │         [Blue screen error]                          │
│              │         [Screen flickering]                           │
│  ┌────────┐  │         [Computer won't turn on]                     │
│  │ Conv 1 │◄─┼─ Active conversation (highlighted)                  │
│  │ 5 msgs │  │                                                       │
│  │ 2h ago │  │                                                       │
│  └────────┘  │                                                       │
│              │                                                       │
│  ┌────────┐  │                                                       │
│  │ Conv 2 │  │                                                       │
│  │ 3 msgs │  │                                                       │
│  │ 1d ago │🗑│                                                       │
│  └────────┘  │                                                       │
│              │                                                       │
│  ┌────────┐  │                                                       │
│  │ Conv 3 │  │                                                       │
│  │ 8 msgs │  │                                                       │
│  │ 3d ago │  │                                                       │
│  └────────┘  │                                                       │
│              │                                                       │
│  [↻ Refresh] │                                                       │
│              │                                                       │
│              │  ┌─────────────────────────────────────────┐         │
│              │  │ Describe your PC issue... [↑]           │         │
│              │  └─────────────────────────────────────────┘         │
└──────────────┴──────────────────────────────────────────────────────┘
    Sidebar          Main Chat Area
  (320px wide)
```

## 🎯 Component Breakdown

### 1. Sidebar Header
```
┌─────────────────────┐
│ [◀] Chat History [✚]│
└─────────────────────┘
```
- **[◀]** = Collapse/Expand toggle
- **Chat History** = Title
- **[✚]** = New conversation button

### 2. Conversation Item
```
┌─────────────────────────┐
│ My computer is running..│ ← Title (truncated)
│ 5 messages · 2h ago     │ ← Metadata
│ Try checking your CPU...│ ← Last message preview
│                     [🗑]│ ← Delete (on hover)
└─────────────────────────┘
```

**Active State** (current conversation):
```
┌─────────────────────────┐
│█ My computer is running..│ ← Green gradient border
│█ 5 messages · 2h ago     │ ← Highlighted
│█ Try checking your CPU...│
│█                    [🗑]│
└─────────────────────────┘
```

### 3. Collapsed Sidebar
```
┌──┐
│◀│
│  │
│  │
│  │
│  │
│  │
└──┘
(50px)
```

### 4. Chat Messages
```
User Message:
                          ┌─────────────────┐
                    [U]   │ My PC is slow   │
                          └─────────────────┘

AI Response:
┌────────────────────────────────────┐
│ Let's diagnose this issue...       │  [AI]
│                                    │
│ Based on your telemetry:           │
│ • CPU usage: 85%                   │
│ • Memory: 12GB/16GB used           │
│                                    │
│ Recommendations:                   │
│ 1. Close background apps           │
│ 2. Check for malware               │
└────────────────────────────────────┘
```

## 🎨 Color Scheme

### Sidebar
- **Background**: Dark gradient (`#1a1a2e` → `#16213e`)
- **Border**: `rgba(255, 255, 255, 0.1)`
- **Text**: White
- **Accent**: Green (`#4CAF50`)

### Conversation Items
- **Default**: `rgba(255, 255, 255, 0.05)`
- **Hover**: `rgba(255, 255, 255, 0.1)`
- **Active**: Green gradient with glow

### Buttons
- **New Chat**: Green circular button
- **Toggle**: Green outlined
- **Delete**: Red on hover
- **Refresh**: Green outlined

## 📱 Responsive Design

### Desktop (> 768px)
```
Sidebar: 320px (expanded) / 50px (collapsed)
Chat: Remaining space
Messages: Max 1100px centered
```

### Tablet (768px)
```
Sidebar: 280px (expanded) / 40px (collapsed)
Chat: Remaining space
Messages: Max 800px centered
```

### Mobile (< 480px)
```
Sidebar: Overlay (full width when expanded)
Chat: Full width
Messages: Full width with padding
```

## 🎭 Animations

### Sidebar Toggle
```css
transition: width 0.3s ease
```
Smooth expand/collapse animation

### Conversation Hover
```css
transform: translateX(5px)
```
Slides right on hover

### Delete Button
```css
opacity: 0 → 1 on hover
transform: scale(1.1)
```
Fades in and enlarges

### Active Conversation
```css
box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3)
```
Glowing green border

## 🔤 Typography

### Conversation Title
- **Font Size**: 14px
- **Weight**: 500 (Medium)
- **Color**: White
- **Truncation**: Ellipsis after 50 chars

### Message Count
- **Font Size**: 11px
- **Color**: Green (#4CAF50)

### Time Stamp
- **Font Size**: 11px
- **Color**: `rgba(255, 255, 255, 0.4)`

### Last Message
- **Font Size**: 12px
- **Color**: `rgba(255, 255, 255, 0.4)`
- **Truncation**: Single line with ellipsis

## 🎯 User Interactions

### Click Behaviors
```
Conversation Item → Load conversation
New Chat Button → Start fresh conversation
Delete Button → Show confirmation dialog
Toggle Button → Expand/collapse sidebar
Refresh Button → Reload conversation list
```

### Hover States
```
Conversation → Highlight + show delete
Delete Button → Change to darker red
Toggle Button → Scale up slightly
New Chat → Rotate + scale
```

### Loading States
```
┌─────────────────┐
│   ⟳ Loading...  │ ← Spinner animation
└─────────────────┘
```

### Error States
```
┌──────────────────────────┐
│ ⚠️ Failed to load        │
│ [Retry]                  │
└──────────────────────────┘
```

### Empty State
```
┌──────────────────────────┐
│   No conversations yet   │
│ Start a new chat to begin│
└──────────────────────────┘
```

## 💡 Key Features Highlighted

### 1. Auto-Save Indicator (subtle)
No visible indicator - saves silently in background
Users don't need to think about it

### 2. Active Conversation
Clear visual feedback with:
- Green gradient background
- Glowing border
- Slightly elevated appearance

### 3. Time Formatting
Human-friendly relative times:
- "Just now"
- "5m ago" (< 1 hour)
- "2h ago" (< 24 hours)
- "3d ago" (< 7 days)
- "Jan 15" (older)

### 4. Message Preview
Shows snippet of last message:
- User messages: Plain text
- AI messages: First line only
- Truncated with ellipsis

## 🎨 Design Philosophy

### Principles Applied
1. **Minimal Distraction**: Dark theme, subtle borders
2. **Clear Hierarchy**: Size and color guide attention
3. **Responsive Feedback**: Hover states, animations
4. **Information Density**: Show enough without clutter
5. **Consistency**: Matches main chat interface

### Inspiration
- ChatGPT's conversation list
- Grok's dark theme
- Discord's sidebar design
- Slack's channel list

## ✨ Polish Details

### Shadows
- Sidebar: `2px 0 10px rgba(0, 0, 0, 0.3)`
- Active conversation: `0 2px 8px rgba(76, 175, 80, 0.3)`
- New chat button: `0 2px 5px rgba(0, 0, 0, 0.2)`

### Border Radius
- Conversation items: `8px`
- Buttons: `5px`
- Input: `24px`
- New chat: `50%` (circular)

### Transitions
- All interactive elements: `0.3s ease`
- Fast enough to feel responsive
- Slow enough to be smooth

## 🎯 Accessibility

### Current Support
- ✅ Keyboard navigation (tab through items)
- ✅ Clear focus states
- ✅ High contrast ratios
- ✅ Readable font sizes
- ✅ Descriptive titles/labels

### Future Improvements
- [ ] Screen reader announcements
- [ ] ARIA labels
- [ ] Keyboard shortcuts
- [ ] Reduced motion option

## 📊 Visual Hierarchy

```
Priority 1: Active conversation (bright + highlighted)
Priority 2: Recent conversations (visible)
Priority 3: Older conversations (slightly dimmed)
Priority 4: Metadata (smaller, grayed)
Priority 5: Delete button (hidden until hover)
```

This ensures users can quickly find what they need without being overwhelmed by information.
