# Frontend Features

## Overview
The frontend has been completely redesigned with a multi-page architecture, black theme, and responsive UI.

## Pages

### 1. Home Page (`/`)
- **Hero Section**: Eye-catching introduction with animated gradient text
- **Features Grid**: Showcases 6 key features with icons
- **Floating Cards**: Interactive visual elements with hover effects
- **Call-to-Action**: Prominent button to start diagnostics

### 2. Hardware Protection (`/hardware-protection`)
- **AI Diagnostic Chat**: Full chatbot interface for PC diagnostics
- **Tips Section**: Helpful tips grid for better diagnostics
- **Real-time Communication**: Connects to Django backend API
- **Message History**: Maintains conversation context

### 3. About Us (`/about`)
- **Mission Statement**: Company vision and goals
- **Features List**: Detailed capabilities breakdown
- **Technology Overview**: AI and ML implementation details
- **Benefits Grid**: User advantages at a glance

## Design System

### Color Palette
- **Primary Black**: `#000` - Main background
- **Secondary Black**: `#0a0a0a`, `#1a1a1a` - Cards and sections
- **Accent Green**: `#00ff88` - Primary brand color
- **Accent Green Dark**: `#00cc6a` - Gradient variation
- **Border Gray**: `#333` - Borders and separators
- **Text Gray**: `#888`, `#aaa`, `#ccc` - Various text levels

### Components

#### Layout Component
- **Sidebar Navigation**: Collapsible sidebar with smooth transitions
- **Responsive Toggle**: Mobile-friendly sidebar control
- **Active State Indicators**: Visual feedback for current page
- **Footer**: Copyright information

#### Diagnostic Chat Component (Black Theme)
- **Gradient Header**: Green gradient with clear visibility
- **Message Bubbles**: Distinct styling for user vs AI messages
- **Typing Indicator**: Animated dots during AI processing
- **Custom Scrollbar**: Dark-themed scrollbar
- **Error Handling**: Styled error messages

## Features

### Responsive Design
- **Desktop**: Full sidebar, optimal layout (1024px+)
- **Tablet**: Collapsible sidebar (768px - 1024px)
- **Mobile**: Hidden sidebar by default (<768px)

### Animations
- **Fade In**: Page load animations
- **Slide Up**: Content reveal effects
- **Float**: Subtle hover animations
- **Gradient Transitions**: Smooth color changes

### Accessibility
- **High Contrast**: Black background with bright accents
- **Clear Typography**: Readable font sizes and weights
- **Focus States**: Visible focus indicators
- **Semantic HTML**: Proper heading hierarchy

## Navigation
- React Router DOM for client-side routing
- Smooth page transitions
- Active link highlighting
- Browser history support

## Technical Stack
- **React**: UI framework
- **React Router DOM**: Navigation
- **Axios**: API communication
- **CSS3**: Styling with animations
- **Flexbox & Grid**: Layout systems

## File Structure
```
frontend/src/
├── App.js                      # Main app with routing
├── App.css                     # Global app styles
├── index.js                    # Entry point
├── index.css                   # Global styles
├── components/
│   ├── Layout.js              # Main layout with sidebar
│   ├── Layout.css             # Layout styles
│   ├── DiagnosticChat.js      # Chat component
│   └── DiagnosticChat.css     # Chat styles (black theme)
└── pages/
    ├── Home.js                # Home page component
    ├── Home.css               # Home page styles
    ├── HardwareProtection.js  # Chatbot page component
    ├── HardwareProtection.css # Chatbot page styles
    ├── About.js               # About page component
    └── About.css              # About page styles
```

## Usage

### Starting the Development Server
```bash
cd frontend
npm install
npm start
```

### Building for Production
```bash
npm run build
```

### Running Tests
```bash
npm test
```

## Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance Optimizations
- Code splitting with React Router
- Lazy loading for route components (can be added)
- Optimized animations using CSS transforms
- Efficient re-renders with React hooks

## Future Enhancements
- Dark/Light theme toggle
- User preferences persistence
- Additional diagnostic tools
- Real-time hardware monitoring dashboard
- Multi-language support
