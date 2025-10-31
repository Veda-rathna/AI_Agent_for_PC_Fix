# Quick Start Guide - Service Centers Feature

## 🚀 Running the Application

### Backend Setup
```powershell
# Navigate to backend folder
cd backend

# Start Django server (if not already running)
python manage.py runserver
```

The backend will run at: `http://localhost:8000`

### Frontend Setup
```powershell
# Open new terminal, navigate to frontend
cd frontend

# Start React development server
npm start
```

The frontend will run at: `http://localhost:3000`

## 🗺️ Accessing Service Centers

1. Open browser: `http://localhost:3000`
2. Click **"Service Centers"** in navigation
3. Allow location access when prompted
4. View nearby service centers on map and in list

## ✨ Key Features at a Glance

### 📍 Location Detection
- **Automatic**: Detects your location on page load
- **Manual**: Retry if permission denied
- **Fallback**: Chennai (if location unavailable)

### 🔍 Search Controls
- **Radius Slider**: 5km - 100km range
- **Brand Filter**: Dell, HP, Lenovo, Acer, Asus
- **Real-time**: Updates automatically

### 📱 Actions Available
- **📞 Call**: Direct phone link
- **🗺️ Directions**: Opens Google Maps
- **📍 View**: Click card to see on map

## 🎨 UI/UX Highlights

### Visual Design
- **Dark Theme**: Consistent with app branding
- **Brand Colors**: Each brand has unique color
- **Smooth Animations**: Professional transitions
- **Responsive**: Works on all devices

### Interactive Elements
- **Map Markers**: 
  - Blue circle = Your location
  - Red pins = Service centers
- **Radius Circle**: Shows search area
- **Popup Cards**: Click markers for details
- **Highlighted Selection**: Selected center glows

### User Feedback
- **Permission Status**: Green (granted) / Yellow (denied)
- **Loading States**: Spinners during data fetch
- **Error Messages**: Clear, actionable errors
- **Statistics**: Real-time center count

## 📊 Example Usage

### Scenario 1: Find Nearest Dell Service Center
1. Go to Service Centers page
2. Select "Dell" from brand filter
3. View sorted list (nearest first)
4. Click "Directions" on top result

### Scenario 2: Expand Search Area
1. No centers found in 30km?
2. Drag radius slider to 50km
3. Results update automatically
4. View more options

### Scenario 3: Contact Service Center
1. Find desired center in list
2. Click "Call" button
3. Phone dialer opens with number
4. Make direct call

## 🔧 Troubleshooting

### Location Not Working?
```
1. Check browser location permission
2. Ensure HTTPS (or localhost)
3. Click "Enable Location" to retry
4. Falls back to Chennai if unavailable
```

### No Service Centers Found?
```
1. Increase search radius
2. Remove brand filter
3. Check if backend is running
4. Verify CSV data exists
```

### Map Not Loading?
```
1. Check internet connection
2. Refresh page (Ctrl + R)
3. Clear browser cache
4. Check browser console for errors
```

## 📱 Mobile Testing

### Enable Location on Mobile
- **Chrome**: Settings → Privacy → Location
- **Safari**: Settings → Privacy → Location Services
- **Firefox**: Settings → Permissions → Location

### Test Responsiveness
```
Desktop: 1920x1080 → Side-by-side layout
Tablet:  768x1024  → Stacked layout
Mobile:  375x667   → Optimized mobile view
```

## 🎯 Navigation Structure

```
Home
  ├── Diagnosis
  ├── Hardware Protection
  ├── Service Centers ← NEW!
  └── About
```

## 📈 Performance Tips

- Maps load asynchronously
- Results cached until filter change
- Smooth 60fps animations
- Optimized for mobile networks

## 🎨 Design Consistency

Follows AutoMend design system:
- **Font**: Open Sans
- **Colors**: Black theme (#000, #111)
- **Accents**: Blue (#007bff)
- **Spacing**: Consistent padding/margins
- **Borders**: Subtle #222 outlines

## 🔐 Privacy & Security

- ✅ Location data NOT stored
- ✅ Only used for distance calculation
- ✅ No tracking or analytics
- ✅ HTTPS recommended for production

## 📝 Data Source

Service centers loaded from:
```
service_centers.csv (root directory)
```

Contains: 40+ authorized service centers across Chennai and Tamil Nadu

## 🌟 Best Practices

### For Users
1. Allow location for best experience
2. Use brand filter to narrow results
3. Check distance before calling
4. Use directions for navigation

### For Developers
1. Keep CSV data updated
2. Test on multiple devices
3. Monitor API response times
4. Validate new entries

## 📞 Support

If you encounter issues:
1. Check browser console (F12)
2. Verify both servers running
3. Review error messages
4. Check network tab for API calls

---

**Ready to test?** 
1. Start backend: `python manage.py runserver`
2. Start frontend: `npm start`
3. Visit: `http://localhost:3000/service-centers`

Enjoy your new Service Centers feature! 🎉
