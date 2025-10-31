# Service Centers Feature Documentation

## Overview
The Service Centers feature allows users to find nearby authorized PC service centers based on their current location. The feature uses interactive maps and provides real-time distance calculations.

## Features

### 🗺️ Interactive Map
- **Real-time Location**: Automatically detects user's current location using browser Geolocation API
- **Visual Markers**: 
  - Blue circle with white dot: Your current location
  - Red pins: Service center locations
- **Radius Circle**: Visual representation of search radius (default 30km)
- **Interactive Popups**: Click on any marker to see service center details

### 📍 Location Features
- **Auto-detection**: Automatically requests user's location on page load
- **Fallback Location**: Uses Chennai as default if location access is denied
- **Permission Handling**: Clear UI feedback for location permission status
- **Retry Option**: Allows users to retry location access if initially denied

### 🔍 Search & Filter
- **Radius Control**: Adjustable search radius from 5km to 100km (slider)
- **Brand Filter**: Filter service centers by PC brand (Dell, HP, Lenovo, Acer, Asus)
- **Real-time Updates**: Results update automatically when filters change
- **Distance Sorting**: Centers are sorted by proximity (nearest first)

### 📋 Service Center List
- **Detailed Cards**: Each center shows:
  - Brand badge with brand-specific colors
  - Service center name
  - Complete address
  - Phone number
  - Distance from user location
- **Quick Actions**:
  - 📞 **Call**: Direct phone call link
  - 🗺️ **Directions**: Opens Google Maps with directions
- **Interactive**: Click any card to highlight it on the map

### 📊 Statistics
- **Centers Found**: Total number of centers within radius
- **Nearest Distance**: Distance to closest service center
- **Brand Availability**: List of available brands in search area

## Technical Stack

### Frontend
- **React**: Component-based UI
- **React-Leaflet**: Interactive map integration
- **Leaflet**: Open-source mapping library (no API key required)
- **Axios**: HTTP client for API calls
- **CSS3**: Modern styling with animations

### Backend
- **Django REST Framework**: RESTful API endpoint
- **CSV Data**: Service centers database
- **Haversine Formula**: Accurate distance calculations

## API Endpoint

### POST `/api/service-centers/nearby/`

**Request Body:**
```json
{
  "latitude": 13.0827,
  "longitude": 80.2707,
  "radius_km": 30,      // Optional, defaults to 30
  "brand": "Dell"       // Optional, filters by brand
}
```

**Response:**
```json
{
  "success": true,
  "user_location": {
    "latitude": 13.0827,
    "longitude": 80.2707
  },
  "radius_km": 30,
  "total_centers": 15,
  "service_centers": [
    {
      "brand": "Dell",
      "name": "TVS Electronics LTD",
      "phone": "9176614954",
      "address": "Parson Complex, 600, Anna Salai...",
      "city": "Chennai",
      "latitude": 13.0631,
      "longitude": 80.2619,
      "distance_km": 2.45
    }
  ],
  "brands_available": ["Dell", "HP", "Lenovo", "Acer", "Asus"]
}
```

## Data Structure

### Service Centers CSV
Located at: `service_centers.csv`

**Columns:**
- Brand: PC manufacturer (Dell, HP, Lenovo, Acer, Asus)
- Name: Service center name
- Phone: Contact number
- Address: Complete street address
- City: City name
- Latitude: Geographic latitude
- Longitude: Geographic longitude

## User Experience Flow

1. **Page Load**
   - System requests location permission
   - Shows loading spinner while detecting location
   - Displays permission status banner

2. **Location Detected**
   - Map centers on user location
   - Fetches nearby service centers (30km radius)
   - Displays centers on map and in list

3. **User Interaction**
   - Adjust search radius with slider
   - Filter by brand using dropdown
   - Click cards to view on map
   - Click map markers to see details
   - Call or get directions to centers

4. **Error Handling**
   - Location denied: Shows fallback location with warning
   - No centers found: Suggests increasing radius
   - API errors: Clear error messages with retry options

## Responsive Design

### Desktop (>992px)
- Side-by-side layout: Map (left) | List (right)
- Full-width controls panel
- Horizontal stats display

### Tablet (768px - 992px)
- Stacked layout: Map (top) | List (bottom)
- Map height: 400px
- Simplified controls

### Mobile (<768px)
- Reduced map height: 300px
- Single column layout
- Stacked action buttons
- Condensed navigation

## Color Scheme

### Brand Colors
- **Dell**: #007DB8 (Blue)
- **HP**: #0096D6 (Light Blue)
- **Lenovo**: #E2231A (Red)
- **Acer**: #83B81A (Green)
- **Asus**: #000000 (Black)

### UI Colors
- **Background**: #000 (Pure Black)
- **Cards**: #111 (Dark Gray)
- **Borders**: #222 (Light Gray)
- **Primary**: #007bff (Blue)
- **Success**: #28a745 (Green)
- **Warning**: #ffc107 (Yellow)
- **Danger**: #dc3545 (Red)

## Accessibility

- **Keyboard Navigation**: Full keyboard support
- **Screen Reader**: Semantic HTML structure
- **Color Contrast**: WCAG AA compliant
- **Focus Indicators**: Clear focus states
- **Alt Text**: Descriptive labels

## Performance Optimizations

1. **Lazy Loading**: Map loads only when needed
2. **Debounced Updates**: Radius changes debounced
3. **Efficient Rendering**: React memoization
4. **Optimized Icons**: SVG data URIs
5. **CSS Animations**: GPU-accelerated transforms

## Future Enhancements

### Planned Features
- [ ] Save favorite service centers
- [ ] User reviews and ratings
- [ ] Service center availability status
- [ ] Appointment booking integration
- [ ] Multi-language support
- [ ] Offline mode with cached locations
- [ ] Turn-by-turn navigation
- [ ] Service center photos
- [ ] Operating hours display
- [ ] Service specializations filter

### Data Improvements
- [ ] Add more cities across India
- [ ] Include international locations
- [ ] Real-time availability updates
- [ ] Service center verification status
- [ ] Customer satisfaction ratings

## Usage Instructions

### For Users

1. **Grant Location Permission**
   - Click "Allow" when prompted for location access
   - Or use the "Enable Location" button if denied

2. **Adjust Search Area**
   - Use the radius slider to expand/reduce search area
   - Default is 30km, max is 100km

3. **Filter by Brand**
   - Select brand from dropdown
   - Or choose "All Brands" to see everything

4. **View Details**
   - Click any service center card
   - View details in popup on map
   - See distance and contact info

5. **Take Action**
   - Click "Call" to phone the center
   - Click "Directions" for Google Maps navigation

### For Developers

1. **Add New Service Centers**
   ```csv
   Brand,Name,Phone,Address,City,Latitude,Longitude
   Dell,New Center,1234567890,123 Street,Chennai,13.08,80.27
   ```

2. **Modify Search Radius**
   ```javascript
   const [radiusKm, setRadiusKm] = useState(50); // Change default
   ```

3. **Customize Brand Colors**
   ```javascript
   const colors = {
     'NewBrand': '#FF5733',
   };
   ```

## Troubleshooting

### Common Issues

**Issue**: Location not detected
- **Solution**: Check browser location settings, enable HTTPS

**Issue**: No service centers found
- **Solution**: Increase search radius, check CSV data

**Issue**: Map not loading
- **Solution**: Check internet connection, clear browser cache

**Issue**: Wrong location shown
- **Solution**: Retry location detection, check GPS settings

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ⚠️ IE 11 (Not supported)

## Testing

### Manual Testing Checklist
- [ ] Location detection works
- [ ] Map displays correctly
- [ ] Markers appear for all centers
- [ ] Distance calculations accurate
- [ ] Brand filter works
- [ ] Radius slider updates results
- [ ] Call and directions links work
- [ ] Responsive on mobile
- [ ] Error handling displays properly
- [ ] Performance is smooth

### Test Scenarios
1. Allow location → Should show nearby centers
2. Deny location → Should show Chennai + warning
3. Change radius → Should update results
4. Filter brand → Should show only that brand
5. Click marker → Should show popup
6. Click card → Should highlight on map
7. Click call → Should open phone dialer
8. Click directions → Should open Google Maps

## Security Considerations

- ✅ HTTPS required for geolocation
- ✅ Input validation on backend
- ✅ Path traversal prevention
- ✅ Rate limiting recommended
- ✅ CORS properly configured

## Credits

- **Maps**: OpenStreetMap contributors
- **Icons**: Custom SVG icons
- **Library**: Leaflet.js (BSD 2-Clause License)
- **Framework**: React, Django

---

**Version**: 1.0.0  
**Last Updated**: October 31, 2025  
**Author**: AutoMend Development Team
