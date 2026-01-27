# Shortify Frontend

Modern, responsive frontend for the Shortify URL shortening application.

## 📋 Structure

```
frontend/
├── index.html          # Main HTML file
├── redirect.html       # Redirect handling for short codes
├── dev_server.py       # Development server with SPA routing
├── nginx.conf          # Nginx configuration for production
├── css/
│   └── styles.css      # Styles and design
└── js/
    ├── api.js          # Class for API interaction
    └── app.js          # Main application
```

## 🚀 Quick Start

### Option 1: Development Server (Recommended for local development)

This server properly handles SPA routing and short code redirects:

```bash
# Navigate to frontend directory
cd frontend

# Run the development server
python dev_server.py
```

Then open: `http://localhost:8080`

### Option 2: Simple HTTP Server

If you just want a basic server:

```bash
# If Python 3 is installed
python -m http.server 8080

# Or with Python 2
python -m SimpleHTTPServer 8080
```

**Note:** Simple HTTP server won't properly handle short code redirects, so use Option 1 for full functionality.

### Option 3: Nginx (Production)

Configure nginx using the provided [nginx.conf](nginx.conf) for production deployment.

## ⚙️ API Configuration

By default, the frontend communicates with the API at `http://localhost:8000/api/v1`.

If your backend is running on a different address, edit [js/api.js](js/api.js):

```javascript
this.baseURL = 'http://your-address:port/api/v1';
```

## 🔄 How URL Shortening Works

1. **User enters a long URL** → Form validation
2. **Request sent to API** → `POST /api/v1/short_url`
3. **API returns slug** → e.g., `sTzTmo`
4. **Frontend displays result** → Shows short URL with the slug
5. **User shares short URL** → `http://localhost:8080/sTzTmo`
6. **Server returns index.html** → For any path (SPA routing)
7. **JavaScript detects slug** → Extracts from URL path
8. **Redirects to API** → Calls `GET /api/v1/sTzTmo`
9. **API redirects to original URL** → Returns 302 redirect with original URL
10. **Browser follows redirect** → User lands on original website ✅

## ✨ Features

- ✂️ **URL Shortening** - Quickly shorten long URLs
- 📋 **Copy** - Copy shortened links with one click
- 📜 **History** - Local history of the last 10 shortened links
- 📱 **Responsive Design** - Works on all devices (mobile, tablet, desktop)
- 🎨 **Modern Interface** - Beautiful and intuitive design
- 🔔 **Notifications** - Toast notifications for all actions
- 🔄 **Automatic Redirects** - Smart redirect handling for short codes
- ⚡ **Fast** - Optimized frontend and efficient routing

## 🎯 Main Components

### HTML Structure
- **Header** - Logo and title
- **Shortener Section** - Form for shortening links
- **Result Display** - Result display with copy button
- **History Section** - History of shortened URLs
- **Toast Notification** - Pop-up notifications
- **Redirect Script** - Auto-detects and handles short code redirects

### CSS
- Color variables and styles
- Responsive design (mobile-first)
- Smooth animations and transitions
- Modern gradients and shadows

### JavaScript

#### api.js
`ShortifyAPI` class for working with the API:
- `shortenURL(url)` - Shorten a URL
- `getURLInfo(shortCode)` - Get information about a link
- `getAllURLs()` - Get all links
- `deleteURL(shortCode)` - Delete a link
- `updateURL(shortCode, data)` - Update a link

#### app.js
`ShortifyApp` class for managing the application:
- Form management and validation
- Result display
- History management (localStorage)
- Toast notifications
- Copy to clipboard
- Short code redirect handling

## 📝 CORS Configuration

If the frontend and backend are on different domains, ensure CORS is enabled in the backend:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🧪 Development Tips

- **Debugging redirects**: Check the browser console (F12) for debug logs
- **Testing short codes**: Use the development server to properly test redirects
- **Clearing history**: Use browser DevTools to clear localStorage
- **API testing**: Use tools like Postman to test the API directly

## 🔧 Development

### Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Node.js and npm (for frontend development tools, optional)

### Customization
- Edit `css/styles.css` to change the design
- Edit `js/app.js` to change the application behavior
- Modify `index.html` to change the structure

## 📝 License

This project is part of the Shortify application.

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
