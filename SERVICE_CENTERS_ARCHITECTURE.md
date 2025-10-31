# Service Centers - Component Architecture

## 🏗️ Component Hierarchy

```
App.js
└── Layout
    └── ServiceCenters (NEW PAGE)
        ├── Header Section
        │   ├── Title & Subtitle
        │   └── Location Status Banner
        │
        ├── Error Banner (conditional)
        │
        ├── Controls Panel
        │   ├── Brand Filter Dropdown
        │   ├── Radius Slider
        │   └── Statistics Display
        │
        └── Content Grid
            ├── Map Section
            │   ├── MapContainer (Leaflet)
            │   ├── TileLayer (OpenStreetMap)
            │   ├── User Marker (Blue Circle)
            │   ├── Radius Circle
            │   ├── Service Center Markers (Red Pins)
            │   └── Popups
            │
            └── List Section
                ├── List Header
                └── Centers List (Scrollable)
                    └── Center Cards
                        ├── Header (Brand + Distance)
                        ├── Name
                        ├── Details (Address, City, Phone)
                        └── Actions (Call, Directions)
```

---

## 📊 Data Flow Diagram

```
[User Opens Page]
        ↓
[Request Location Permission]
        ↓
    ┌───────┴───────┐
    ↓               ↓
[Granted]      [Denied]
    ↓               ↓
[Get GPS]   [Use Fallback: Chennai]
    ↓               ↓
    └───────┬───────┘
            ↓
    [Set userLocation State]
            ↓
    [Fetch Service Centers API]
            ↓
    ┌───────┴───────┐
    ↓               ↓
[Success]       [Error]
    ↓               ↓
[Display on    [Show Error
 Map & List]    Message]
    ↓
[User Interactions]
    ├── Change Radius → Re-fetch Data
    ├── Filter Brand → Update Filtered List
    ├── Click Card → Highlight on Map
    ├── Click Marker → Show Popup
    ├── Click Call → Open Phone Dialer
    └── Click Directions → Open Google Maps
```

---

## 🔄 State Management

### Component State Variables

```javascript
const ServiceCenters = () => {
  // Location State
  const [userLocation, setUserLocation] = useState(null);
  const [locationPermission, setLocationPermission] = useState('prompt');
  
  // Data State
  const [serviceCenters, setServiceCenters] = useState([]);
  const [filteredCenters, setFilteredCenters] = useState([]);
  const [availableBrands, setAvailableBrands] = useState([]);
  
  // UI State
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedBrand, setSelectedBrand] = useState('all');
  const [radiusKm, setRadiusKm] = useState(30);
  const [selectedCenter, setSelectedCenter] = useState(null);
  
  // Refs
  const mapRef = useRef(null);
};
```

### State Update Triggers

| State Variable | Updated By | Triggers |
|---------------|------------|----------|
| `userLocation` | getUserLocation() | → fetchServiceCenters() |
| `radiusKm` | Slider onChange | → fetchServiceCenters() |
| `selectedBrand` | Dropdown onChange | → filterCentersByBrand() |
| `serviceCenters` | API Response | → filterCentersByBrand() |
| `filteredCenters` | Filter Function | → Re-render List |
| `loading` | Async Operations | → Show/Hide Spinner |
| `error` | Error Conditions | → Show Error Banner |
| `selectedCenter` | Card/Marker Click | → Highlight UI |

---

## 🎨 Styling Architecture

### CSS Class Organization

```
ServiceCenters.css (665 lines)
├── Container & Layout
│   ├── .service-centers-container
│   ├── .content-grid
│   └── .map-section / .list-section
│
├── Header & Banners
│   ├── .service-centers-header
│   ├── .location-banner (success/warning)
│   └── .error-banner
│
├── Controls
│   ├── .controls-panel
│   ├── .brand-select
│   ├── .radius-slider
│   └── .stats
│
├── Map Components
│   ├── .map-container
│   ├── .leaflet-popup-*
│   └── .popup-content
│
├── List Components
│   ├── .centers-list
│   ├── .center-card
│   ├── .center-header
│   ├── .brand-badge
│   ├── .distance-badge
│   └── .center-actions
│
├── Utilities
│   ├── .loading-spinner
│   ├── .no-results
│   └── .action-btn
│
└── Responsive
    ├── @media (max-width: 1200px)
    ├── @media (max-width: 992px)
    ├── @media (max-width: 768px)
    └── @media (max-width: 480px)
```

---

## 🔌 API Integration

### Request Flow

```
Frontend Component
       ↓
   axios.post()
       ↓
Django URL Router
       ↓
get_nearby_service_centers(request)
       ↓
   ├── Validate Input
   ├── Read CSV File
   ├── Calculate Distances
   ├── Filter by Radius & Brand
   ├── Sort by Distance
   └── Return JSON Response
       ↓
Frontend State Update
       ↓
UI Re-render
```

### Error Handling

```
Try Block:
├── Validate coordinates → Bad Request (400)
├── Read CSV → Not Found (404)
├── Calculate distances → Internal Error (500)
└── Return response → Success (200)

Catch Block:
└── Exception → Internal Server Error (500)

Frontend:
├── Network Error → "Failed to load"
├── Permission Denied → "Location denied"
├── No Results → "No centers found"
└── Unknown Error → Generic message
```

---

## 🗺️ Map Architecture

### Leaflet Component Structure

```
<MapContainer>
  <TileLayer />              // OpenStreetMap tiles
  <RecenterMap />            // Custom component
  
  <Marker>                   // User location
    <Popup>Your Location</Popup>
  </Marker>
  
  <Circle />                 // Search radius
  
  {filteredCenters.map(center => (
    <Marker key={index}>     // Service centers
      <Popup>{center details}</Popup>
    </Marker>
  ))}
</MapContainer>
```

### Custom Icons

```javascript
// User Location Icon
const userIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml...',  // Blue circle SVG
  iconSize: [40, 40],
  iconAnchor: [20, 20]
});

// Service Center Icon
const serviceIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml...',  // Red pin SVG
  iconSize: [35, 45],
  iconAnchor: [17.5, 45]
});
```

---

## 📱 Responsive Layout Strategy

### Desktop Layout (>992px)
```
┌─────────────────────────────────────┐
│  Header + Location Banner           │
├─────────────────────────────────────┤
│  Controls: Filter | Slider | Stats  │
├──────────────────┬──────────────────┤
│                  │                  │
│   Interactive    │   Scrollable     │
│      Map         │      List        │
│                  │                  │
│  (Expandable)    │  (Fixed Width)   │
└──────────────────┴──────────────────┘
```

### Tablet Layout (768-992px)
```
┌─────────────────────────────────────┐
│  Header + Location Banner           │
├─────────────────────────────────────┤
│  Controls: Stacked                  │
├─────────────────────────────────────┤
│                                     │
│         Map (400px height)          │
│                                     │
├─────────────────────────────────────┤
│                                     │
│         Scrollable List             │
│                                     │
└─────────────────────────────────────┘
```

### Mobile Layout (<768px)
```
┌───────────────────────┐
│  Header (Compact)     │
├───────────────────────┤
│  Controls (Stacked)   │
├───────────────────────┤
│                       │
│   Map (300px)         │
│                       │
├───────────────────────┤
│                       │
│   List (Scrollable)   │
│   [Single Column]     │
│                       │
└───────────────────────┘
```

---

## 🎯 User Interaction Patterns

### Click Interactions

```
Map Marker Click:
├── Set selected center
├── Show popup with details
└── Highlight in list (scroll into view)

List Card Click:
├── Set selected center
├── Pan map to location
├── Open map popup
└── Highlight card

Call Button Click:
├── Open phone dialer
└── Pass phone number

Directions Button Click:
├── Open Google Maps
└── Pass coordinates
```

### Change Interactions

```
Radius Slider Change:
├── Update radius state
├── Re-fetch service centers
└── Update map circle

Brand Filter Change:
├── Update brand state
├── Filter centers array
└── Re-render list & map
```

---

## 🔧 Helper Functions

### Distance Calculation (Backend)
```python
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Haversine Formula Implementation
    Returns: Distance in kilometers
    """
    # Convert degrees to radians
    # Apply haversine formula
    # Return distance
```

### Brand Color Mapping (Frontend)
```javascript
const getBrandColor = (brand) => {
  const colors = {
    'Dell': '#007DB8',
    'HP': '#0096D6',
    'Lenovo': '#E2231A',
    'Acer': '#83B81A',
    'Asus': '#000000',
  };
  return colors[brand] || '#6c757d';
};
```

---

## 📦 Dependencies

### Frontend
```json
{
  "leaflet": "^1.9.x",
  "react-leaflet": "^4.2.x",
  "axios": "^1.13.1",
  "react": "^19.2.0",
  "react-dom": "^19.2.0",
  "react-router-dom": "^7.9.5"
}
```

### Backend
```python
# Django (already installed)
# csv (built-in)
# math (built-in)
```

---

## 🎨 Design Tokens

### Colors
```css
--primary: #007bff;
--background: #000;
--card-bg: #111;
--border: #222;
--text-primary: #fff;
--text-secondary: #888;
--success: #28a745;
--warning: #ffc107;
--danger: #dc3545;
```

### Typography
```css
--font-family: 'Open Sans', sans-serif;
--font-size-large: 32px;
--font-size-medium: 16px;
--font-size-small: 14px;
--font-weight-bold: 700;
--font-weight-semibold: 600;
--font-weight-regular: 400;
```

### Spacing
```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 15px;
--spacing-lg: 20px;
--spacing-xl: 30px;
```

### Borders & Radius
```css
--border-radius-sm: 6px;
--border-radius-md: 8px;
--border-radius-lg: 12px;
--border-width: 1px;
```

---

## 🚀 Performance Optimizations

### Implemented
✅ Debounced slider updates  
✅ Memoized filter functions  
✅ Lazy marker rendering  
✅ SVG data URI icons (no HTTP requests)  
✅ CSS transform animations (GPU)  
✅ Efficient re-render logic  

### Future Optimizations
- [ ] Virtual scrolling for large lists
- [ ] Map tile caching
- [ ] Service worker for offline mode
- [ ] Code splitting
- [ ] Image lazy loading

---

## 📊 Component Metrics

| Metric | Value |
|--------|-------|
| Component Size | 468 lines |
| CSS Size | 665 lines |
| State Variables | 10 |
| Event Handlers | 8 |
| API Calls | 1 |
| Custom Hooks | 3 useEffect |
| Map Markers | Dynamic (user + centers) |
| Responsive Breakpoints | 4 |

---

**This architecture ensures:**
- ✅ Maintainable code structure
- ✅ Clear separation of concerns
- ✅ Efficient state management
- ✅ Scalable component design
- ✅ Excellent user experience

**Last Updated**: October 31, 2025
