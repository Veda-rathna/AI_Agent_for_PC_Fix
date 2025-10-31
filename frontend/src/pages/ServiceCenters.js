import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap } from 'react-leaflet';
import axios from 'axios';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './ServiceCenters.css';

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// Custom icons for different markers
const userIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgdmlld0JveD0iMCAwIDQwIDQwIj48Y2lyY2xlIGN4PSIyMCIgY3k9IjIwIiByPSIxNSIgZmlsbD0iIzAwN2JmZiIgc3Ryb2tlPSIjZmZmIiBzdHJva2Utd2lkdGg9IjMiLz48Y2lyY2xlIGN4PSIyMCIgY3k9IjIwIiByPSI2IiBmaWxsPSIjZmZmIi8+PC9zdmc+',
  iconSize: [40, 40],
  iconAnchor: [20, 20],
  popupAnchor: [0, -20],
});

const serviceIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzNSIgaGVpZ2h0PSI0NSIgdmlld0JveD0iMCAwIDM1IDQ1Ij48cGF0aCBmaWxsPSIjZmY0NDU2IiBkPSJNMTcuNSAwQzguNSAwIDEgNy42IDEgMTcuNWMwIDEyLjUgMTYuNSAyNy41IDE2LjUgMjcuNVMzNCAzMCAzNCAxNy41QzM0IDcuNiAyNi41IDAgMTcuNSAweiIvPjxjaXJjbGUgZmlsbD0iI2ZmZiIgY3g9IjE3LjUiIGN5PSIxNy41IiByPSI3Ii8+PHRleHQgeD0iMTcuNSIgeT0iMjIiIGZvbnQtc2l6ZT0iMTIiIGZvbnQtd2VpZ2h0PSJib2xkIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjZmY0NDU2Ij5TPC90ZXh0Pjwvc3ZnPg==',
  iconSize: [35, 45],
  iconAnchor: [17.5, 45],
  popupAnchor: [0, -45],
});

// Component to recenter map when location changes
function RecenterMap({ center }) {
  const map = useMap();
  useEffect(() => {
    if (center) {
      map.setView(center, 12);
    }
  }, [center, map]);
  return null;
}

const ServiceCenters = () => {
  const [userLocation, setUserLocation] = useState(null);
  const [serviceCenters, setServiceCenters] = useState([]);
  const [filteredCenters, setFilteredCenters] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedBrand, setSelectedBrand] = useState('all');
  const [radiusKm, setRadiusKm] = useState(30);
  const [availableBrands, setAvailableBrands] = useState([]);
  const [locationPermission, setLocationPermission] = useState('prompt');
  const [selectedCenter, setSelectedCenter] = useState(null);
  const mapRef = useRef(null);

  // Chennai default location (for fallback)
  const defaultLocation = { lat: 13.0827, lng: 80.2707 };

  useEffect(() => {
    getUserLocation();
  }, []);

  useEffect(() => {
    if (userLocation) {
      fetchServiceCenters();
    }
  }, [userLocation, radiusKm]);

  useEffect(() => {
    filterCentersByBrand();
  }, [selectedBrand, serviceCenters]);

  const getUserLocation = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser');
      setUserLocation(defaultLocation);
      return;
    }

    setLoading(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setUserLocation({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        });
        setLocationPermission('granted');
        setLoading(false);
        setError(null);
      },
      (error) => {
        console.error('Error getting location:', error);
        setLocationPermission('denied');
        
        if (error.code === error.PERMISSION_DENIED) {
          setError('Location access denied. Showing default location (Chennai). Please enable location access for accurate results.');
        } else if (error.code === error.POSITION_UNAVAILABLE) {
          setError('Location information unavailable. Using default location.');
        } else {
          setError('Unable to get your location. Using default location.');
        }
        
        setUserLocation(defaultLocation);
        setLoading(false);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
      }
    );
  };

  const fetchServiceCenters = async () => {
    if (!userLocation) return;

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/api/service-centers/nearby/', {
        latitude: userLocation.lat,
        longitude: userLocation.lng,
        radius_km: radiusKm,
      });

      if (response.data.success) {
        setServiceCenters(response.data.service_centers);
        setAvailableBrands(response.data.brands_available || []);
        setFilteredCenters(response.data.service_centers);
      } else {
        setError(response.data.error || 'Failed to fetch service centers');
      }
    } catch (err) {
      console.error('Error fetching service centers:', err);
      setError('Failed to load service centers. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const filterCentersByBrand = () => {
    if (selectedBrand === 'all') {
      setFilteredCenters(serviceCenters);
    } else {
      setFilteredCenters(
        serviceCenters.filter(center => center.brand.toLowerCase() === selectedBrand.toLowerCase())
      );
    }
  };

  const handleCenterClick = (center) => {
    setSelectedCenter(center);
    if (mapRef.current) {
      mapRef.current.setView([center.latitude, center.longitude], 15);
    }
  };

  const handleDirections = (center) => {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${center.latitude},${center.longitude}`;
    window.open(url, '_blank');
  };

  const handleCall = (phone) => {
    window.location.href = `tel:${phone}`;
  };

  const retryLocation = () => {
    getUserLocation();
  };

  if (!userLocation) {
    return (
      <div className="service-centers-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Getting your location...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="service-centers-container">
      {error && (
        <div className="error-banner">
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)} className="close-btn">×</button>
        </div>
      )}

      <div className="controls-panel">
        <div className="control-group">
          <label htmlFor="brand-filter">Filter by Brand:</label>
          <select
            id="brand-filter"
            value={selectedBrand}
            onChange={(e) => setSelectedBrand(e.target.value)}
            className="brand-select"
          >
            <option value="all">All Brands ({serviceCenters.length})</option>
            {availableBrands.sort().map((brand) => (
              <option key={brand} value={brand}>
                {brand} ({serviceCenters.filter(c => c.brand === brand).length})
              </option>
            ))}
          </select>
        </div>

        <div className="control-group">
          <label htmlFor="radius-slider">Search Radius: {radiusKm} km</label>
          <input
            id="radius-slider"
            type="range"
            min="5"
            max="100"
            step="5"
            value={radiusKm}
            onChange={(e) => setRadiusKm(Number(e.target.value))}
            className="radius-slider"
          />
        </div>

        <div className="stats">
          <div className="stat-item">
            <span className="stat-number">{filteredCenters.length}</span>
            <span className="stat-label">Centers Found</span>
          </div>
          {filteredCenters.length > 0 && (
            <div className="stat-item">
              <span className="stat-number">{filteredCenters[0].distance_km} km</span>
              <span className="stat-label">Nearest</span>
            </div>
          )}
        </div>
      </div>

      <div className="content-grid">
        <div className="map-section">
          <MapContainer
            center={[userLocation.lat, userLocation.lng]}
            zoom={12}
            className="map-container"
            ref={mapRef}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            
            <RecenterMap center={userLocation && [userLocation.lat, userLocation.lng]} />
            
            {/* User location marker */}
            {userLocation && (
              <>
                <Marker position={[userLocation.lat, userLocation.lng]} icon={userIcon}>
                  <Popup>
                    <div className="popup-content">
                      <strong>📍 Your Location</strong>
                    </div>
                  </Popup>
                </Marker>
                
                {/* Radius circle */}
                <Circle
                  center={[userLocation.lat, userLocation.lng]}
                  radius={radiusKm * 1000}
                  pathOptions={{
                    color: '#007bff',
                    fillColor: '#007bff',
                    fillOpacity: 0.1,
                    weight: 2,
                  }}
                />
              </>
            )}

            {/* Service center markers */}
            {filteredCenters.map((center, index) => (
              <Marker
                key={index}
                position={[center.latitude, center.longitude]}
                icon={serviceIcon}
                eventHandlers={{
                  click: () => setSelectedCenter(center),
                }}
              >
                <Popup>
                  <div className="popup-content">
                    <h3>{center.brand}</h3>
                    <p className="center-name">{center.name}</p>
                    <p className="center-distance">📍 {center.distance_km} km away</p>
                    <p className="center-phone">📞 {center.phone}</p>
                    <button
                      onClick={() => handleDirections(center)}
                      className="directions-btn-popup"
                    >
                      Get Directions
                    </button>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>

        <div className="list-section">
          <div className="list-header">
            <h2>Service Centers List</h2>
            {loading && <div className="loading-spinner-small"></div>}
          </div>

          <div className="centers-list">
            {filteredCenters.length === 0 ? (
              <div className="no-results">
                <p>🔍 No service centers found within {radiusKm}km</p>
                <p className="hint">Try increasing the search radius</p>
              </div>
            ) : (
              filteredCenters.map((center, index) => (
                <div
                  key={index}
                  className={`center-card ${selectedCenter === center ? 'selected' : ''}`}
                  onClick={() => handleCenterClick(center)}
                >
                  <div className="center-header">
                    <div className="brand-badge" style={{ backgroundColor: getBrandColor(center.brand) }}>
                      {center.brand}
                    </div>
                    <div className="distance-badge">
                      {center.distance_km} km
                    </div>
                  </div>
                  
                  <h3 className="center-name">{center.name}</h3>
                  
                  <div className="center-details">
                    <div className="detail-row">
                      <span className="icon">📍</span>
                      <span className="text">{center.address}</span>
                    </div>
                    <div className="detail-row">
                      <span className="icon">🏙️</span>
                      <span className="text">{center.city}</span>
                    </div>
                    <div className="detail-row">
                      <span className="icon">📞</span>
                      <span className="text">{center.phone}</span>
                    </div>
                  </div>
                  
                  <div className="center-actions">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleCall(center.phone);
                      }}
                      className="action-btn call-btn"
                    >
                      📞 Call
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDirections(center);
                      }}
                      className="action-btn directions-btn"
                    >
                      🗺️ Directions
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper function to get brand colors
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

export default ServiceCenters;
