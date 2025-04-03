'use client';

import { useEffect, useState, useRef } from 'react';
import { collection, addDoc } from 'firebase/firestore';
import db from '../lib/firebase';
import confetti from 'canvas-confetti';
import { motion } from 'framer-motion';
import { 
  FaInfoCircle, 
  FaUser, 
  FaEnvelope, 
  FaPhone, 
  FaCalendarAlt, 
  FaUsers, 
  FaBuilding, 
  FaMapMarkerAlt, 
  FaClock, 
  FaLightbulb, 
  FaCamera, 
  FaVideo, 
  FaMoneyCheckAlt, 
  FaFileContract 
} from 'react-icons/fa';

export default function DJContractForm() {
  const [formData, setFormData] = useState({
    clientName: '',
    email: '',
    contactPhone: '',
    eventType: '',
    guestCount: '',
    venueName: '',
    venueLocation: '',
    eventDate: '',
    startTime: '',
    endTime: '',
    paymentMethod: '',
    lighting: false,
    photography: false,
    videoVisuals: false,
    agreeToTerms: false,
    additionalHours: 0,
  });
  
  const venueLocationRef = useRef(null);
  const [isClient, setIsClient] = useState(false);
  
  const [submitted, setSubmitted] = useState(false);
  const [infoPopup, setInfoPopup] = useState(null);
  

  // Icon mappings for the main fields.
  const fieldIcons = {
    clientName: <FaUser style={{ color: '#ff6347', marginRight: '0.5rem' }} />,
    email: <FaEnvelope style={{ color: '#1e90ff', marginRight: '0.5rem' }} />,
    contactPhone: <FaPhone style={{ color: '#32cd32', marginRight: '0.5rem' }} />,
    eventType: <FaCalendarAlt style={{ color: '#ffa500', marginRight: '0.5rem' }} />,
    guestCount: <FaUsers style={{ color: '#8a2be2', marginRight: '0.5rem' }} />,
    venueName: <FaBuilding style={{ color: '#ff4500', marginRight: '0.5rem' }} />,
  };

  // Icons for time related fields.
  const timeIcons = {
    eventDate: <FaCalendarAlt style={{ color: '#ff1493', marginRight: '0.5rem' }} />,
    startTime: <FaClock style={{ color: '#20b2aa', marginRight: '0.5rem' }} />,
    endTime: <FaClock style={{ color: '#20b2aa', marginRight: '0.5rem' }} />,
  };

  // Icons for service checkboxes.
  const serviceIcons = {
    lighting: <FaLightbulb style={{ color: '#ffd700', marginRight: '0.5rem' }} />,
    photography: <FaCamera style={{ color: '#ff69b4', marginRight: '0.5rem' }} />,
    videoVisuals: <FaVideo style={{ color: '#00bfff', marginRight: '0.5rem' }} />,
  };

  // Additional icons for other fields.
  const venueLocationIcon = <FaMapMarkerAlt style={{ color: '#dc143c', marginRight: '0.5rem' }} />;
  const additionalHoursIcon = <FaClock style={{ color: '#6a5acd', marginRight: '0.5rem' }} />;
  const paymentIcon = <FaMoneyCheckAlt style={{ color: '#008000', marginRight: '0.5rem' }} />;
  const termsIcon = <FaFileContract style={{ color: '#00008b', marginRight: '0.5rem' }} />;

  useEffect(() => {
    if (typeof window !== 'undefined') {
      setIsClient(true); // This ensures the Google Places code runs only on the client
    }
  }, []);

  // Loading Google Maps API and initializing the autocomplete feature
  useEffect(() => {
    if (typeof window !== 'undefined' && !window.google) {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.NEXT_PUBLIC_GOOGLE_API_KEY}&libraries=places`;
      script.async = true;
      script.onload = () => initializeAutocomplete();
      document.head.appendChild(script);
    } else {
      initializeAutocomplete();
    }
  }, []);

  // Function to initialize Google Places Autocomplete
  const initializeAutocomplete = () => {
    if (window.google && venueLocationRef.current) {
      const autocomplete = new window.google.maps.places.Autocomplete(venueLocationRef.current, {
        types: ['geocode'],
        componentRestrictions: { country: 'us' },
      });

      autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace();
        if (place.geometry) {
          setFormData(prev => ({
            ...prev,
            venueLocation: place.formatted_address,
          }));
        }
      });
    }
  };

  const handleChange = (e) => {
    const { name, type, value, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        type === 'checkbox'
          ? checked
          : type === 'number'
          ? parseInt(value) || 0
          : value,
    }));
  };

  // Basic manual address validation: requires at least one letter, one number, and at least 5 characters.
  const validateAddress = (address) => {
    const regex = /^(?=.*[a-zA-Z])(?=.*\d).{5,}$/;
    return regex.test(address);
  };

  const validateEmail = (email) => /\S+@\S+\.\S+/.test(email);
  const validatePhone = (phone) =>
    /^[0-9]{10}$/.test(phone.replace(/\D/g, ''));

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.venueLocation) {
      return alert('Please select a venue location.');
    }

    // Validate start and end times with midnight crossover support (end must be <= 2:00 AM)
    if (formData.startTime && formData.endTime) {
      let start = new Date(`1970-01-01T${formData.startTime}:00`);
      let end = new Date(`1970-01-01T${formData.endTime}:00`);

      // If end time is not after start, assume event crosses midnight and add one day to end.
      if (end <= start) {
        end.setDate(end.getDate() + 1);
      }

      // For events that cross midnight, ensure the end time is at or before 2:00 AM.
      const twoAM = new Date(`1970-01-02T02:00:00`);
      if (end > twoAM) {
        return alert(
          'For events that cross midnight, the end time must be at or before 2:00 AM.'
        );
      }

      // Confirm that start is before end.
      if (start >= end) {
        return alert('Start time must be before end time.');
      }
    }

    if (!validateEmail(formData.email))
      return alert('Enter a valid email.');
    if (!validatePhone(formData.contactPhone))
      return alert('Enter a valid phone number.');
    if (!validateAddress(formData.venueLocation))
      return alert('Please enter a valid address.');
    if (!formData.agreeToTerms)
      return alert('Please agree to the terms.');

    try {
      await addDoc(collection(db, 'contracts'), formData);
      setSubmitted(true);
      confetti({
        particleCount: 200,
        spread: 80,
        origin: { y: 0.6 },
        zIndex: 9999,
      });
    } catch (err) {
      console.error('Error submitting contract:', err);
      alert('Something went wrong.');
    }
  };

  const BASE = 350,
    LIGHTING = 100,
    PHOTO = 150,
    VIDEO = 100,
    EXTRA_HOUR = 75;
  const calculateTotal = () => {
    let total = BASE;
    if (formData.lighting) total += LIGHTING;
    if (formData.photography) total += PHOTO;
    if (formData.videoVisuals) total += VIDEO;
    total += formData.additionalHours * EXTRA_HOUR;
    return total;
  };

  const itemizedTotal = () => (
    <ul style={{ listStyle: 'none', padding: 0, marginTop: '1rem', color: '#000' }}>
      <li>🎶 Base Package: ${BASE}</li>
      {formData.lighting && <li>💡 Lighting: ${LIGHTING}</li>}
      {formData.photography && <li>📸 Photography: ${PHOTO}</li>}
      {formData.videoVisuals && <li>📽️ Video Visuals: ${VIDEO}</li>}
      {formData.additionalHours > 0 && (
        <li>⏱️ Additional Hours: ${formData.additionalHours * EXTRA_HOUR}</li>
      )}
      <li>
        <strong>Total: ${calculateTotal()}</strong>
      </li>
    </ul>
  );

  // InfoModal component for displaying info popups with an "Ok" button.
  function InfoModal({ text, onClose }) {
    return (
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 10000,
      }}>
        <div style={{
          backgroundColor: '#fff',
          padding: '2rem',
          borderRadius: '8px',
          boxShadow: '0 2px 10px rgba(0,0,0,0.3)',
          maxWidth: '400px',
          textAlign: 'center',
        }}>
          <p style={{ marginBottom: '1.5rem', color: '#333' }}>{text}</p>
          <button onClick={onClose} style={{
            padding: '0.5rem 1rem',
            border: 'none',
            borderRadius: '4px',
            backgroundColor: '#2563eb',
            color: '#fff',
            cursor: 'pointer',
          }}>Ok</button>
        </div>
      </div>
    );
  }

  const inputStyle = {
    width: '100%',
    padding: '12px',
    marginBottom: '1rem',
    borderRadius: '8px',
    border: '1px solid #ccc',
    backgroundColor: 'rgba(255,255,255,0.85)',
    color: '#000',
    fontSize: '16px',
  };

  const labelStyle = {
    fontWeight: 'bold',
    color: '#111',
    marginBottom: '0.5rem',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between'
  };

  const linkButtonStyle = {
    display: 'inline-block',
    margin: '0.5rem',
    padding: '0.75rem 1.5rem',
    backgroundColor: '#2563eb',
    color: '#fff',
    textDecoration: 'none',
    borderRadius: '10px',
    fontWeight: 'bold'
  };

  return (
    <>
      {infoPopup && <InfoModal text={infoPopup} onClose={() => setInfoPopup(null)} />}
      <div style={{
        minHeight: '100vh',
        padding: '2rem',
        backgroundImage: "url('/dj-background.jpg')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        fontFamily: 'Helvetica Neue, Segoe UI, Roboto, sans-serif',
      }}>
        <div style={{
          maxWidth: '700px',
          margin: '0 auto',
          backgroundColor: 'rgba(255,255,255,0.9)',
          padding: '2.5rem',
          borderRadius: '20px',
          boxShadow: '0 8px 30px rgba(0,0,0,0.2)'
        }}>
          <h1 style={{ textAlign: 'center', fontSize: '2.25rem', color: '#000' }}>
            🎧 Live City DJ Contract
          </h1>

          {/* Only show the instruction text when the form is not submitted */}
          {!submitted && (
            <p style={{ textAlign: 'center', color: '#111', marginBottom: '0.5rem' }}>
              Please complete the contract form below to reserve your event date.
            </p>
          )}

          <p style={{ textAlign: 'center', color: '#111', marginBottom: '1.5rem' }}>
            📞 <a href="tel:+12036949388" style={{ color: '#0070f3' }}>(203) 694-9388</a> ·
            📧 <a href="mailto:therealdjbobbydrake@gmail.com" style={{ color: '#0070f3' }}>therealdjbobbydrake@gmail.com</a>
          </p>

          {!submitted ? (
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', width: '100%' }}>
              {['clientName', 'email', 'contactPhone', 'eventType', 'guestCount', 'venueName'].map((field) => (
                <div key={field}>
                  <label style={labelStyle}>
                    <span style={{ display: 'flex', alignItems: 'center' }}>
                      {fieldIcons[field]} 
                      {field.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}:
                    </span>
                  </label>
                  <input
                    name={field}
                    type={field.includes('guest') ? 'number' : 'text'}
                    required
                    style={inputStyle}
                    value={formData[field]}
                    onChange={handleChange}
                  />
                </div>
              ))}

            <div>
            <label style={labelStyle}>
                <span style={{ display: 'flex', alignItems: 'center' }}>
                {venueLocationIcon} Venue Location
                </span>
                  </label>
                <input
                  ref={venueLocationRef}
                  name="venueLocation"
                  type="text"
                  value={formData.venueLocation}
                  onChange={handleChange}
                  required
                  style={{ backgroundColor: 'white', width: '100%', padding: '12px', marginBottom: '1rem', borderRadius: '8px', border: '1px solid #ccc', color: 'black' }}
                />
              </div>


              {['eventDate', 'startTime', 'endTime'].map((field) => (
                <div key={field}>
                  <label style={labelStyle}>
                    <span style={{ display: 'flex', alignItems: 'center' }}>
                      {timeIcons[field]} {field.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}:
                    </span>
                  </label>
                  <input
                    name={field}
                    type={field.includes('Date') ? 'date' : 'time'}
                    required
                    style={inputStyle}
                    value={formData[field]}
                    onChange={handleChange}
                  />
                </div>
              ))}

              {[
                {
                  name: 'lighting',
                  label: 'Event Lighting (+$100)',
                  description: 'Requires 2 hour early entry to venue for setup. Includes sound activated strobing lights.',
                },
                {
                  name: 'photography',
                  label: 'Photography (+$150)',
                  description: 'Includes 50 high-quality candid shots delivered within 48 hours.',
                },
                {
                  name: 'videoVisuals',
                  label: 'Video Visuals (+$100)',
                  description: 'Slide shows, presentations, karaoke etc.',
                },
              ].map(({ name, label, description }) => (
                <div key={name}>
                  <label style={labelStyle}>
                    <span style={{ display: 'flex', alignItems: 'center' }}>
                      {serviceIcons[name]} {label}
                    </span>
                    <span onClick={() => setInfoPopup(description)} style={{ color: '#0070f3', marginLeft: 8, cursor: 'pointer' }}>
                      <FaInfoCircle />
                    </span>
                  </label>
                  <input type="checkbox" name={name} checked={formData[name]} onChange={handleChange} />
                </div>
              ))}

              {/* Redesigned compact Additional Hours Field with icon */}
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
                <label style={labelStyle}>
                  <span style={{ display: 'flex', alignItems: 'center' }}>
                    {additionalHoursIcon} Additional Hours ($75/hr):
                  </span>
                </label>
                <div style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  border: '1px solid #ccc',
                  borderRadius: '4px',
                  overflow: 'hidden',
                  width: '80px',
                  marginLeft: '0.5rem',
                }}>
                  <button
                    type="button"
                    onClick={() => setFormData(prev => ({ ...prev, additionalHours: Math.max(prev.additionalHours - 1, 0) }))}
                    style={{
                      padding: '0.2rem 0.4rem',
                      backgroundColor: 'transparent',
                      border: 'none',
                      color: '#2563eb',
                      fontSize: '1rem',
                      cursor: 'pointer'
                    }}
                  >
                    -
                  </button>
                  <span style={{
                    padding: '0 0.4rem',
                    minWidth: '20px',
                    textAlign: 'center',
                    color: '#000',
                    fontWeight: 'bold'
                  }}>
                    {formData.additionalHours}
                  </span>
                  <button
                    type="button"
                    onClick={() => setFormData(prev => ({ ...prev, additionalHours: prev.additionalHours + 1 }))}
                    style={{
                      padding: '0.2rem 0.4rem',
                      backgroundColor: 'transparent',
                      border: 'none',
                      color: '#2563eb',
                      fontSize: '1rem',
                      cursor: 'pointer'
                    }}
                  >
                    +
                  </button>
                </div>
              </div>

              <div>
                <label style={labelStyle}>
                  <span style={{ display: 'flex', alignItems: 'center' }}>
                    {paymentIcon} Payment Method:
                  </span>
                  <span onClick={() => setInfoPopup('Select your preferred payment method for booking confirmation.')} style={{ color: '#0070f3', marginLeft: 8, cursor: 'pointer' }}>
                    <FaInfoCircle />
                  </span>
                </label>
                <select name="paymentMethod" required style={inputStyle} value={formData.paymentMethod} onChange={handleChange}>
                  <option value="">Choose one</option>
                  <option value="Venmo - @Bobby-Martin-64">Venmo</option>
                  <option value="Cash App - $LiveCity">Cash App</option>
                  <option value="Cash">Cash</option>
                </select>
              </div>

              <div>
                <label style={labelStyle}>
                  <span style={{ display: 'flex', alignItems: 'center' }}>
                    {termsIcon} Terms & Conditions
                  </span>
                  <span onClick={() => setInfoPopup('Non-refundable $100 deposit required. Remaining balance due 2 weeks before event. Cancellations within 30 days require full payment.')} style={{ color: '#0070f3', marginLeft: 8, cursor: 'pointer' }}>
                    <FaInfoCircle />
                  </span>
                </label>
                <input type="checkbox" name="agreeToTerms" checked={formData.agreeToTerms} onChange={handleChange} required />
              </div>

              {itemizedTotal()}
              <button type="submit" style={{ ...inputStyle, backgroundColor: '#2563eb', color: '#fff', cursor: 'pointer' }}>
                Submit Contract
              </button>
            </form>
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              style={{ textAlign: 'center', color: '#000' }}
            >
              <h2>✅ Submitted!</h2>
              <p style={{ fontWeight: 'bold', fontSize: '1.1rem', marginBottom: '1rem' }}>
                🎉 Congratulations on successfully booking your event. Please submit your deposit or full payment to reserve your date.
              </p>
              {itemizedTotal()}
              <p>Send payment to confirm your booking:</p>
              <a href="https://venmo.com/Bobby-Martin-64" target="_blank" rel="noopener noreferrer" style={linkButtonStyle}>
                Pay with Venmo
              </a>
              <a href="https://cash.app/$LiveCity" target="_blank" rel="noopener noreferrer" style={linkButtonStyle}>
                Pay with Cash App
              </a>
            </motion.div>
          )}
        </div>
      </div>
    </>
  );
}
